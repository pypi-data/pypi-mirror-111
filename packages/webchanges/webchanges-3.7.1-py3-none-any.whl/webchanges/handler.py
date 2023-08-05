"""Handles the running of jobs and, afterwards, of the reports."""

from __future__ import annotations

import difflib
import email.utils
import logging
import shlex
import subprocess
import tempfile
import time
import timeit
import traceback
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Type, Union

from .filters import FilterBase
from .jobs import JobBase, NotModifiedError
from .reporters import ReporterBase
from .storage import CacheStorage

# https://stackoverflow.com/questions/39740632
if TYPE_CHECKING:
    from .main import Urlwatch

logger = logging.getLogger(__name__)


class JobState(object):
    verb = ''
    old_data: Union[bytes, str] = ''
    new_data: Union[bytes, str] = ''
    history_data: Dict[str, float] = {}
    old_timestamp: Optional[float] = 0.0
    new_timestamp = 0.0
    exception: Optional[Exception] = None
    traceback: str = ''
    tries = 0
    old_etag: str = ''
    new_etag: str = ''
    error_ignored: Union[bool, str] = False
    _generated_diff: Optional[str] = ''

    def __init__(self, cache_storage: CacheStorage, job: JobBase) -> None:
        self.cache_storage = cache_storage
        self.job = job

    def __enter__(self) -> 'JobState':
        try:
            self.job.main_thread_enter()
        except Exception as ex:
            logger.info(f'Job {self.job.index_number}: Exception while creating resources for job', exc_info=True)
            self.exception = ex
            self.traceback = traceback.format_exc()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        try:
            self.job.main_thread_exit()
        except Exception:
            # We don't want exceptions from releasing resources to override job run results
            logger.warning(f'Job {self.job.index_number}: Exception while releasing resources for job', exc_info=True)

    def load(self) -> None:
        """Loads new data for the job."""
        guid = self.job.get_guid()
        self.old_data, self.old_timestamp, self.tries, self.old_etag = self.cache_storage.load(guid)
        if self.job.compared_versions and self.job.compared_versions > 1:
            self.history_data = self.cache_storage.get_history_data(guid, self.job.compared_versions)

    def save(self) -> None:
        """Saves any new data already loaded for the job."""
        if self.new_data is None and self.exception is not None:
            # If no new data has been retrieved due to an exception, reuse the old job data
            self.new_data = self.old_data
            self.new_etag = self.old_etag

        self.cache_storage.save(
            guid=self.job.get_guid(),
            data=self.new_data,
            timestamp=self.new_timestamp,
            tries=self.tries,
            etag=self.new_etag,
        )

    def process(self) -> 'JobState':
        """Processes the job: loads it and handles exceptions."""
        logger.info(f'Job {self.job.index_number}: Processing job {self.job}')

        if self.exception:
            return self

        try:
            try:
                self.load()

                self.new_timestamp = time.time()
                data, self.new_etag = self.job.retrieve(self)

                # Apply automatic filters first
                filtered_data = FilterBase.auto_process(self, data)

                # Apply any specified filters
                for filter_kind, subfilter in FilterBase.normalize_filter_list(self.job.filter):
                    filtered_data = FilterBase.process(filter_kind, subfilter, self, filtered_data)

                self.new_data = filtered_data

            except Exception as e:
                # job has a chance to format and ignore its error
                self.exception = e
                self.traceback = self.job.format_error(e, traceback.format_exc())
                self.error_ignored = self.job.ignore_error(e)
                if not (self.error_ignored or isinstance(e, NotModifiedError)):
                    self.tries += 1
                    logger.debug(
                        f'Job {self.job.index_number}: Job ended with error; incrementing cumulative tries to '
                        f'{self.tries} ({str(e).strip()})'
                    )
        except Exception as e:
            # job failed its chance to handle error
            self.exception = e
            self.traceback = traceback.format_exc()
            self.error_ignored = False
            if not isinstance(e, NotModifiedError):
                self.tries += 1
                logger.debug(
                    f'Job {self.job.index_number}: Job ended with error (internal handling failed); '
                    f'incrementing cumulative tries to {self.tries} ({str(e).strip()})'
                )

        return self

    def get_diff(self) -> Optional[str]:
        """Generates the job's diff and applies diff_filters."""
        if self._generated_diff != '':
            return self._generated_diff

        _generated_diff = self._generate_diff()
        # Apply any specified diff filters
        if isinstance(_generated_diff, str):
            for filter_kind, subfilter in FilterBase.normalize_filter_list(self.job.diff_filter):
                _generated_diff = FilterBase.process(filter_kind, subfilter, self, _generated_diff)
            self._generated_diff = str(_generated_diff)
        else:
            self._generated_diff = None

        return self._generated_diff

    def _generate_diff(self) -> Optional[Union[str, bool]]:
        """Generates the job's diff."""
        if self.job.diff_tool is not None:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmpdir = Path(tmp_dir)
                old_file_path = tmpdir.joinpath('old_file')
                new_file_path = tmpdir.joinpath('new_file')
                old_file_path.write_text(str(self.old_data))
                new_file_path.write_text(str(self.new_data))
                cmdline = shlex.split(self.job.diff_tool) + [str(old_file_path), str(new_file_path)]
                proc = subprocess.run(cmdline, capture_output=True, text=True)
                # Diff tools return 0 for "nothing changed" or 1 for "files differ", anything else is an error
                if proc.returncode == 0:
                    return False
                elif proc.returncode == 1:
                    head = f'Using external diff tool "{self.job.diff_tool}"\n'
                    head += f'Old: {email.utils.formatdate(self.old_timestamp, localtime=True)}\n'
                    head += f'New: {email.utils.formatdate(self.new_timestamp, localtime=True)}\n'
                    head += '-' * 36 + '\n'
                    return head + proc.stdout
                else:
                    raise RuntimeError(proc.stderr) from subprocess.CalledProcessError(proc.returncode, cmdline)

        timestamp_old = email.utils.formatdate(self.old_timestamp, localtime=True)
        timestamp_new = email.utils.formatdate(self.new_timestamp, localtime=True)
        if self.job.contextlines is not None:
            contextlines = self.job.contextlines
        else:
            contextlines = 0 if self.job.additions_only or self.job.deletions_only else 3
        diff = list(
            difflib.unified_diff(
                str(self.old_data).splitlines(),
                str(self.new_data).splitlines(),
                '@',
                '@',
                timestamp_old,
                timestamp_new,
                contextlines,
                lineterm='',
            )
        )
        diff[0] = diff[0].replace('\t', ' ')
        diff[1] = diff[1].replace('\t', ' ')
        if self.job.additions_only:
            if len(self.old_data) and len(self.new_data) / len(self.old_data) <= 0.25:
                diff = (
                    diff[:2]
                    + ['/**Comparison type: Additions only**']
                    + ['/**Deletions are being shown as 75% or more of the content has been deleted**']
                    + diff[2:]
                )
            else:
                head = '...' + diff[0][3:]
                diff = [line for line in diff if line.startswith('+') or line.startswith('@')]
                diff = [
                    line1
                    for line1, line2 in zip([''] + diff, diff + [''])
                    if not (line1.startswith('@') and line2.startswith('@'))
                ][1:]
                diff = diff[:-1] if diff[-1].startswith('@') else diff
                if len(diff) == 1 or len([line for line in diff if line.lstrip('+').rstrip()]) == 2:
                    self.verb = 'changed,no_report'
                    return None
                diff = [head, diff[0], '/**Comparison type: Additions only**'] + diff[1:]
        elif self.job.deletions_only:
            head = '...' + diff[1][3:]
            diff = [line for line in diff if line.startswith('-') or line.startswith('@')]
            diff = [
                line1
                for line1, line2 in zip([''] + diff, diff + [''])
                if not (line1.startswith('@') and line2.startswith('@'))
            ][1:]
            diff = diff[:-1] if diff[-1].startswith('@') else diff
            if len(diff) == 1 or len([line for line in diff if line.lstrip('-').rstrip()]) == 2:
                self.verb = 'changed,no_report'
                return None
            diff = [diff[0], head, '/**Comparison type: Deletions only**'] + diff[1:]

        return '\n'.join(diff)


class Report(object):
    def __init__(self, urlwatch_config: Urlwatch) -> None:
        self.config: Dict[str, Any] = urlwatch_config.config_storage.config

        self.job_states: List[JobState] = []
        self.start = timeit.default_timer()

    def _result(self, verb: str, job_state: JobState) -> None:
        if job_state.exception is not None and job_state.exception is not NotModifiedError:
            logger.debug(
                f'Job {job_state.job.index_number}: Got exception while processing job {job_state.job}',
                exc_info=job_state.exception,
            )

        job_state.verb = verb
        self.job_states.append(job_state)

    def new(self, job_state: JobState) -> None:
        self._result('new', job_state)

    def changed(self, job_state: JobState) -> None:
        self._result('changed', job_state)

    def changed_no_report(self, job_state: JobState) -> None:
        self._result('changed,no_report', job_state)

    def unchanged(self, job_state: JobState) -> None:
        self._result('unchanged', job_state)

    def error(self, job_state: JobState) -> None:
        self._result('error', job_state)

    def get_filtered_job_states(self, job_states: List[JobState]) -> Iterable[JobState]:
        """Returns JobStates that have reportable changes per config['display']"""
        for job_state in job_states:
            if (
                not any(
                    job_state.verb == verb and not self.config['display'][verb]
                    for verb in ('unchanged', 'new', 'error')
                )
                and job_state.verb != 'changed,no_report'
            ):
                yield job_state

    def finish(self) -> None:
        end = timeit.default_timer()
        duration = end - self.start

        ReporterBase.submit_all(self, self.job_states, duration)

    def finish_one(self, name: str, check_enabled: Optional[bool] = True) -> None:
        end = timeit.default_timer()
        duration = end - self.start

        ReporterBase.submit_one(name, self, self.job_states, duration, check_enabled)
