# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for scheduling jobs."""

import asyncio
import inspect
import logging
import time
from datetime import datetime, timedelta, time as dt_time

from schedule import Scheduler, Job, CancelJob

from vectorbt import _typing as tp
from vectorbt.utils import checks
from vectorbt.utils.datetime_ import tzaware_to_naive_time

logger = logging.getLogger(__name__)


class CancelledError(asyncio.CancelledError):
    """Thrown for the operation to be cancelled."""
    pass


class AsyncJob(Job):
    async def async_run(self) -> tp.Any:
        """Async `Job.run`."""
        logger.info('Running job %s', self)
        ret = self.job_func()
        if inspect.isawaitable(ret):
            ret = await ret
        self.last_run = datetime.now()
        self._schedule_next_run()
        return ret


class AsyncScheduler(Scheduler):
    async def async_run_pending(self) -> None:
        """Async `Scheduler.run_pending`."""
        runnable_jobs = (job for job in self.jobs if job.should_run)
        await asyncio.gather(*[self._async_run_job(job) for job in runnable_jobs])

    async def async_run_all(self, delay_seconds: int = 0) -> None:
        """Async `Scheduler.run_all`."""
        logger.info('Running *all* %i jobs with %is delay in-between',
                    len(self.jobs), delay_seconds)
        for job in self.jobs[:]:
            await self._async_run_job(job)
            await asyncio.sleep(delay_seconds)

    async def _async_run_job(self, job: AsyncJob) -> None:
        """Async `Scheduler.run_job`."""
        ret = await job.async_run()
        if isinstance(ret, CancelJob) or ret is CancelJob:
            self.cancel_job(job)

    def every(self, interval: int = 1) -> AsyncJob:
        """Schedule a new periodic job of type `AsyncJob`."""
        job = AsyncJob(interval, self)
        return job


class ScheduleManager:
    """Class that manages `schedule.Scheduler`."""

    units: tp.ClassVar[tp.Tuple[str, ...]] = (
        "second",
        "seconds",
        "minute",
        "minutes",
        "hour",
        "hours",
        "day",
        "days",
        "week",
        "weeks"
    )

    weekdays: tp.ClassVar[tp.Tuple[str, ...]] = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )

    def __init__(self, scheduler: tp.Optional[AsyncScheduler] = None) -> None:
        if scheduler is None:
            scheduler = AsyncScheduler()
        checks.assert_instance_of(scheduler, AsyncScheduler)

        self._scheduler = scheduler
        self._async_task = None

    @property
    def scheduler(self) -> AsyncScheduler:
        """Scheduler."""
        return self._scheduler

    @property
    def async_task(self) -> tp.Optional[asyncio.Task]:
        """Current async task."""
        return self._async_task

    def every(self, *args, to: tp.Optional[int] = None,
              tags: tp.Optional[tp.Iterable[tp.Hashable]] = None) -> AsyncJob:
        """Create a new job that runs every `interval` units of time.

        `*args` can include at most four different arguments: `interval`, `unit`, `start_day`, and `at`,
        in the strict order:

        * `interval`: integer or `datetime.timedelta`
        * `unit`: `ScheduleManager.units`
        * `start_day`: `ScheduleManager.weekdays`
        * `at`: string or `datetime.time`.

        See the package `schedule` for more details.

        Usage:
            ```pycon
            >>> import datetime
            >>> import pytz
            >>> import vectorbt as vbt

            >>> def job_func(message="I'm working..."):
            ...     print(message)

            >>> my_manager = vbt.ScheduleManager()

            >>> # add jobs
            >>> my_manager.every().do(job_func, message="Hello")
            Every 1 second do job_func(message='Hello') (last run: [never], next run: 2021-03-18 19:06:47)

            >>> my_manager.every(10, 'minutes').do(job_func)
            Every 10 minutes do job_func() (last run: [never], next run: 2021-03-18 19:16:46)

            >>> my_manager.every('hour').do(job_func)
            Every 1 hour do job_func() (last run: [never], next run: 2021-03-18 20:06:46)

            >>> my_manager.every('10:30').do(job_func)
            Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)

            >>> my_manager.every('day', '10:30').do(job_func)
            Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)

            >>> my_manager.every('day', datetime.time(9, 30, tzinfo=pytz.utc)).do(job_func)
            Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)

            >>> my_manager.every('monday').do(job_func)
            Every 1 week do job_func() (last run: [never], next run: 2021-03-22 19:06:46)

            >>> my_manager.every('wednesday', '13:15').do(job_func)
            Every 1 week at 13:15:00 do job_func() (last run: [never], next run: 2021-03-24 13:15:00)

            >>> my_manager.every('minute', ':17').do(job_func)
            Every 1 minute at 00:00:17 do job_func() (last run: [never], next run: 2021-03-18 19:07:17)

            >>> my_manager.start()
            ```

            You can still use the chained approach as done by `schedule`:

            ```pycon
            >>> my_manager.every().minute.at(':17').do(job_func)
            Every 1 minute at 00:00:17 do job_func() (last run: [never], next run: 2021-03-18 19:07:17)
            ```
        """
        # Parse arguments
        interval = 1
        unit = None
        start_day = None
        at = None

        def _is_arg_interval(arg):
            return isinstance(arg, (int, timedelta))

        def _is_arg_unit(arg):
            return isinstance(arg, str) and arg in self.units

        def _is_arg_start_day(arg):
            return isinstance(arg, str) and arg in self.weekdays

        def _is_arg_at(arg):
            return (isinstance(arg, str) and ':' in arg) or isinstance(arg, dt_time)

        expected_args = ['interval', 'unit', 'start_day', 'at']
        for i, arg in enumerate(args):
            if 'interval' in expected_args and _is_arg_interval(arg):
                interval = arg
                expected_args = expected_args[expected_args.index('interval') + 1:]
                continue
            if 'unit' in expected_args and _is_arg_unit(arg):
                unit = arg
                expected_args = expected_args[expected_args.index('unit') + 1:]
                continue
            if 'start_day' in expected_args and _is_arg_start_day(arg):
                start_day = arg
                expected_args = expected_args[expected_args.index('start_day') + 1:]
                continue
            if 'at' in expected_args and _is_arg_at(arg):
                at = arg
                expected_args = expected_args[expected_args.index('at') + 1:]
                continue
            raise ValueError(f"Arg at index {i} is unexpected")

        if at is not None:
            if unit is None and start_day is None:
                unit = 'days'
        if unit is None and start_day is None:
            unit = 'seconds'

        job = self.scheduler.every(interval)
        if unit is not None:
            job = getattr(job, unit)
        if start_day is not None:
            job = getattr(job, start_day)
        if at is not None:
            if isinstance(at, dt_time):
                if job.unit == "days" or job.start_day:
                    if at.tzinfo is not None:
                        at = tzaware_to_naive_time(at, None)
                at = at.isoformat()
                if job.unit == "hours":
                    at = ':'.join(at.split(':')[1:])
                if job.unit == "minutes":
                    at = ':' + at.split(':')[2]
            job = job.at(at)
        if to is not None:
            job = job.to(to)
        if tags is not None:
            if not isinstance(tags, tuple):
                tags = (tags,)
            job = job.tag(*tags)

        return job

    def start(self, sleep: int = 1) -> None:
        """Run pending jobs in a loop."""
        logger.info("Starting schedule manager with jobs %s", str(self.scheduler.jobs))
        try:
            while True:
                self.scheduler.run_pending()
                time.sleep(sleep)
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info("Stopping schedule manager")

    async def async_start(self, sleep: int = 1) -> None:
        """Async run pending jobs in a loop."""
        logger.info("Starting schedule manager in the background with jobs %s", str(self.scheduler.jobs))
        logger.info("Jobs: %s", str(self.scheduler.jobs))
        try:
            while True:
                await self.scheduler.async_run_pending()
                await asyncio.sleep(sleep)
        except asyncio.CancelledError:
            logger.info("Stopping schedule manager")

    def done_callback(self, async_task: asyncio.Task) -> None:
        """Callback run when the async task is finished."""
        logger.info(async_task)

    def start_in_background(self, **kwargs) -> None:
        """Run `ScheduleManager.async_start` in the background."""
        async_task = asyncio.create_task(self.async_start(**kwargs))
        async_task.add_done_callback(self.done_callback)
        logger.info(async_task)
        self._async_task = async_task

    @property
    def async_task_running(self) -> bool:
        """Whether the async task is running."""
        return self.async_task is not None and not self.async_task.done()

    def stop(self) -> None:
        """Stop the async task."""
        if self.async_task_running:
            self.async_task.cancel()
