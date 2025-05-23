# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Class for scheduling data updates."""

import logging

from vectorbt import _typing as tp
from vectorbt.data.base import Data
from vectorbt.utils.config import Configured
from vectorbt.utils.schedule_ import ScheduleManager

logger = logging.getLogger(__name__)


class DataUpdater(Configured):
    """Class for scheduling data updates.

    Usage:
        * Update in the foreground:

        ```pycon
        >>> import vectorbt as vbt

        >>> class MyDataUpdater(vbt.DataUpdater):
        ...     def __init__(self, *args, **kwargs):
        ...         super().__init__(*args, **kwargs)
        ...         self.update_count = 0
        ...
        ...     def update(self, count_limit=None):
        ...         prev_index_len = len(self.data.wrapper.index)
        ...         super().update()
        ...         new_index_len = len(self.data.wrapper.index)
        ...         print(f"Data updated with {new_index_len - prev_index_len} data points")
        ...         self.update_count += 1
        ...         if count_limit is not None and self.update_count >= count_limit:
        ...             raise vbt.CancelledError

        >>> data = vbt.GBMData.download('SYMBOL', start='1 minute ago', freq='1s')
        >>> my_updater = MyDataUpdater(data)
        >>> my_updater.update_every(count_limit=10)
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points

        >>> my_updater.data.get()
        2021-05-02 16:53:51.755347+00:00    96.830482
        2021-05-02 16:53:52.755347+00:00    94.481883
        2021-05-02 16:53:53.755347+00:00    94.327835
        2021-05-02 16:53:54.755347+00:00    90.178038
        2021-05-02 16:53:55.755347+00:00    88.260168
                                              ...
        2021-05-02 16:54:57.755347+00:00    99.342590
        2021-05-02 16:54:58.755347+00:00    94.872893
        2021-05-02 16:54:59.755347+00:00    93.212823
        2021-05-02 16:55:00.755347+00:00    95.199882
        2021-05-02 16:55:01.755347+00:00    93.070532
        Freq: S, Length: 71, dtype: float64
        ```

        * Update in the background:

        ```pycon
        >>> my_updater = MyDataUpdater(my_updater.data)
        >>> my_updater.update_every(in_background=True, count_limit=10)
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points
        Data updated with 1 data points

        >>> my_updater.data.get()
        2021-05-02 16:53:51.755347+00:00    96.830482
        2021-05-02 16:53:52.755347+00:00    94.481883
        2021-05-02 16:53:53.755347+00:00    94.327835
        2021-05-02 16:53:54.755347+00:00    90.178038
        2021-05-02 16:53:55.755347+00:00    88.260168
                                              ...
        2021-05-02 16:55:07.755347+00:00    94.502885
        2021-05-02 16:55:08.755347+00:00    94.823707
        2021-05-02 16:55:09.755347+00:00    92.570025
        2021-05-02 16:55:10.755347+00:00    84.239018
        2021-05-02 16:55:11.755347+00:00    81.294486
        Freq: S, Length: 81, dtype: float64
        ```
    """

    def __init__(self, data: Data, schedule_manager: tp.Optional[ScheduleManager] = None, **kwargs) -> None:
        Configured.__init__(
            self,
            data=data,
            schedule_manager=schedule_manager,
            **kwargs
        )
        self._data = data
        if schedule_manager is None:
            schedule_manager = ScheduleManager()
        self._schedule_manager = schedule_manager

    @property
    def data(self) -> Data:
        """Data instance.

        See `vectorbt.data.base.Data`."""
        return self._data

    @property
    def schedule_manager(self) -> ScheduleManager:
        """Schedule manager instance.

        See `vectorbt.utils.schedule_.ScheduleManager`."""
        return self._schedule_manager

    def update(self, **kwargs) -> None:
        """Method that updates data.

        Override to do pre- and postprocessing.

        To stop this method from running again, raise `vectorbt.utils.schedule_.CancelledError`."""
        self._data = self.data.update(**kwargs)
        self.update_config(data=self.data)
        new_index = self.data.wrapper.index
        logger.info(f"Updated data has {len(new_index)} rows from {new_index[0]} to {new_index[-1]}")

    def update_every(self, *args, to: int = None, tags: tp.Optional[tp.Iterable[tp.Hashable]] = None,
                     in_background: bool = False, start_kwargs: dict = None, **kwargs) -> None:
        """Schedule `DataUpdater.update`.

        For `*args`, `to` and `tags`, see `vectorbt.utils.schedule_.ScheduleManager.every`.

        If `in_background` is set to True, starts in the background as an `asyncio` task.
        The task can be stopped with `vectorbt.utils.schedule_.ScheduleManager.stop`.

        `**kwargs` are passed to `DataUpdater.update`."""
        if start_kwargs is None:
            start_kwargs = {}
        self.schedule_manager.every(*args, to=to, tags=tags).do(self.update, **kwargs)
        if in_background:
            self.schedule_manager.start_in_background(**start_kwargs)
        else:
            self.schedule_manager.start(**start_kwargs)
