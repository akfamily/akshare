# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with log records.

Order records capture information on simulation logs. Logs are populated when
simulating a portfolio and can be accessed as `vectorbt.portfolio.base.Portfolio.logs`.

```pycon
>>> import pandas as pd
>>> import numpy as np
>>> from datetime import datetime, timedelta
>>> import vectorbt as vbt

>>> np.random.seed(42)
>>> price = pd.DataFrame({
...     'a': np.random.uniform(1, 2, size=100),
...     'b': np.random.uniform(1, 2, size=100)
... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
>>> size = pd.DataFrame({
...     'a': np.random.uniform(-100, 100, size=100),
...     'b': np.random.uniform(-100, 100, size=100),
... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
>>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d', log=True)
>>> logs = pf.logs

>>> logs.filled.count()
a    88
b    99
Name: count, dtype: int64

>>> logs.ignored.count()
a    0
b    0
Name: count, dtype: int64

>>> logs.rejected.count()
a    12
b     1
Name: count, dtype: int64
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Logs.metrics`.

```pycon
>>> logs['a'].stats()
Start                             2020-01-01 00:00:00
End                               2020-04-09 00:00:00
Period                              100 days 00:00:00
Total Records                                     100
Status Counts: None                                 0
Status Counts: Filled                              88
Status Counts: Ignored                              0
Status Counts: Rejected                            12
Status Info Counts: None                           88
Status Info Counts: NoCashLong                     12
Name: a, dtype: object
```

`Logs.stats` also supports (re-)grouping:

```pycon
>>> logs.stats(group_by=True)
Start                             2020-01-01 00:00:00
End                               2020-04-09 00:00:00
Period                              100 days 00:00:00
Total Records                                     200
Status Counts: None                                 0
Status Counts: Filled                             187
Status Counts: Ignored                              0
Status Counts: Rejected                            13
Status Info Counts: None                          187
Status Info Counts: NoCashLong                     13
Name: group, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Logs.subplots`.

This class does not have any subplots.
"""

import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base.reshape_fns import to_dict
from vectorbt.portfolio.enums import (
    log_dt,
    SizeType,
    Direction,
    OrderSide,
    OrderStatus,
    OrderStatusInfo
)
from vectorbt.records.base import Records
from vectorbt.records.decorators import attach_fields, override_field_config
from vectorbt.utils.config import merge_dicts, Config

__pdoc__ = {}

logs_field_config = Config(
    dict(
        dtype=log_dt,
        settings=dict(
            id=dict(
                title='Log Id'
            ),
            group=dict(
                title='Group'
            ),
            cash=dict(
                title='Cash'
            ),
            position=dict(
                title='Position'
            ),
            debt=dict(
                title='Debt'
            ),
            free_cash=dict(
                title='Free Cash'
            ),
            val_price=dict(
                title='Val Price'
            ),
            value=dict(
                title='Value'
            ),
            req_size=dict(
                title='Request Size'
            ),
            req_price=dict(
                title='Request Price'
            ),
            req_size_type=dict(
                title='Request Size Type',
                mapping=SizeType
            ),
            req_direction=dict(
                title='Request Direction',
                mapping=Direction
            ),
            req_fees=dict(
                title='Request Fees'
            ),
            req_fixed_fees=dict(
                title='Request Fixed Fees'
            ),
            req_slippage=dict(
                title='Request Slippage'
            ),
            req_min_size=dict(
                title='Request Min Size'
            ),
            req_max_size=dict(
                title='Request Max Size'
            ),
            req_size_granularity=dict(
                title='Request Size Granularity'
            ),
            req_reject_prob=dict(
                title='Request Rejection Prob'
            ),
            req_lock_cash=dict(
                title='Request Lock Cash'
            ),
            req_allow_partial=dict(
                title='Request Allow Partial'
            ),
            req_raise_reject=dict(
                title='Request Raise Rejection'
            ),
            req_log=dict(
                title='Request Log'
            ),
            new_cash=dict(
                title='New Cash'
            ),
            new_position=dict(
                title='New Position'
            ),
            new_debt=dict(
                title='New Debt'
            ),
            new_free_cash=dict(
                title='New Free Cash'
            ),
            new_val_price=dict(
                title='New Val Price'
            ),
            new_value=dict(
                title='New Value'
            ),
            res_size=dict(
                title='Result Size'
            ),
            res_price=dict(
                title='Result Price'
            ),
            res_fees=dict(
                title='Result Fees'
            ),
            res_side=dict(
                title='Result Side',
                mapping=OrderSide
            ),
            res_status=dict(
                title='Result Status',
                mapping=OrderStatus
            ),
            res_status_info=dict(
                title='Result Status Info',
                mapping=OrderStatusInfo
            ),
            order_id=dict(
                title='Order Id'
            )
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['logs_field_config'] = f"""Field config for `Logs`.

```json
{logs_field_config.to_doc()}
```
"""

logs_attach_field_config = Config(
    dict(
        res_side=dict(
            attach_filters=True
        ),
        res_status=dict(
            attach_filters=True
        ),
        res_status_info=dict(
            attach_filters=True
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['logs_attach_field_config'] = f"""Config of fields to be attached to `Logs`.

```json
{logs_attach_field_config.to_doc()}
```
"""

LogsT = tp.TypeVar("LogsT", bound="Logs")


@attach_fields(logs_attach_field_config)
@override_field_config(logs_field_config)
class Logs(Records):
    """Extends `Records` for working with log records."""

    @property
    def field_config(self) -> Config:
        return self._field_config

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Logs.stats`.

        Merges `vectorbt.records.base.Records.stats_defaults` and
        `logs.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        logs_stats_cfg = settings['logs']['stats']

        return merge_dicts(
            Records.stats_defaults.__get__(self),
            logs_stats_cfg
        )

    _metrics: tp.ClassVar[Config] = Config(
        dict(
            start=dict(
                title='Start',
                calc_func=lambda self: self.wrapper.index[0],
                agg_func=None,
                tags='wrapper'
            ),
            end=dict(
                title='End',
                calc_func=lambda self: self.wrapper.index[-1],
                agg_func=None,
                tags='wrapper'
            ),
            period=dict(
                title='Period',
                calc_func=lambda self: len(self.wrapper.index),
                apply_to_timedelta=True,
                agg_func=None,
                tags='wrapper'
            ),
            total_records=dict(
                title='Total Records',
                calc_func='count',
                tags='records'
            ),
            res_status_counts=dict(
                title='Status Counts',
                calc_func='res_status.value_counts',
                incl_all_keys=True,
                post_calc_func=lambda self, out, settings: to_dict(out, orient='index_series'),
                tags=['logs', 'res_status', 'value_counts']
            ),
            res_status_info_counts=dict(
                title='Status Info Counts',
                calc_func='res_status_info.value_counts',
                post_calc_func=lambda self, out, settings: to_dict(out, orient='index_series'),
                tags=['logs', 'res_status_info', 'value_counts']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Logs.plots`.

        Merges `vectorbt.records.base.Records.plots_defaults` and
        `logs.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        logs_plots_cfg = settings['logs']['plots']

        return merge_dicts(
            Records.plots_defaults.__get__(self),
            logs_plots_cfg
        )

    @property
    def subplots(self) -> Config:
        return self._subplots


Logs.override_field_config_doc(__pdoc__)
Logs.override_metrics_doc(__pdoc__)
Logs.override_subplots_doc(__pdoc__)
