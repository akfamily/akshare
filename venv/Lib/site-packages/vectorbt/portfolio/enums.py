# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Named tuples and enumerated types.

Defines enums and other schemas for `vectorbt.portfolio`."""

import numpy as np

from vectorbt import _typing as tp
from vectorbt.utils.docs import to_doc

__all__ = [
    'RejectedOrderError',
    'InitCashMode',
    'CallSeqType',
    'AccumulationMode',
    'ConflictMode',
    'DirectionConflictMode',
    'OppositeEntryMode',
    'StopEntryPrice',
    'StopExitPrice',
    'StopExitMode',
    'StopUpdateMode',
    'SizeType',
    'Direction',
    'OrderStatus',
    'OrderSide',
    'OrderStatusInfo',
    'TradeDirection',
    'TradeStatus',
    'TradesType',
    'ProcessOrderState',
    'ExecuteOrderState',
    'SimulationContext',
    'GroupContext',
    'RowContext',
    'SegmentContext',
    'OrderContext',
    'PostOrderContext',
    'FlexOrderContext',
    'Order',
    'NoOrder',
    'OrderResult',
    'AdjustSLContext',
    'AdjustTPContext',
    'SignalContext',
    'order_dt',
    'trade_dt',
    'log_dt'
]

__pdoc__ = {}


# ############# Errors ############# #


class RejectedOrderError(Exception):
    """Rejected order error."""
    pass


# ############# Enums ############# #


class InitCashModeT(tp.NamedTuple):
    Auto: int = 0
    AutoAlign: int = 1


InitCashMode = InitCashModeT()
"""_"""

__pdoc__['InitCashMode'] = f"""Initial cash mode.

```json
{to_doc(InitCashMode)}
```

Attributes:
    Auto: Initial cash is infinite within simulation, and then set to the total cash spent.
    AutoAlign: Initial cash is set to the total cash spent across all columns.
"""


class CallSeqTypeT(tp.NamedTuple):
    Default: int = 0
    Reversed: int = 1
    Random: int = 2
    Auto: int = 3


CallSeqType = CallSeqTypeT()
"""_"""

__pdoc__['CallSeqType'] = f"""Call sequence type.

```json
{to_doc(CallSeqType)}
```

Attributes:
    Default: Place calls from left to right.
    Reversed: Place calls from right to left.
    Random: Place calls randomly.
    Auto: Place calls dynamically based on order value.
"""


class AccumulationModeT(tp.NamedTuple):
    Disabled: int = 0
    Both: int = 1
    AddOnly: int = 2
    RemoveOnly: int = 3


AccumulationMode = AccumulationModeT()
"""_"""

__pdoc__['AccumulationMode'] = f"""Accumulation mode.

```json
{to_doc(AccumulationMode)}
```

Accumulation allows gradually increasing and decreasing positions by a size.

Attributes:
    Disabled: Disable accumulation.
    Both: Allow both adding to and removing from the position.
    AddOnly: Allow accumulation to only add to the position.
    RemoveOnly: Allow accumulation to only remove from the position.
    
!!! note
    Accumulation acts differently for exits and opposite entries: exits reduce the current position
    but won't enter the opposite one, while opposite entries reduce the position by the same amount,
    but as soon as this position is closed, they begin to increase the opposite position.

    The behavior for opposite entries can be changed by `OppositeEntryMode` and for stop orders by `StopExitMode`.
"""


class ConflictModeT(tp.NamedTuple):
    Ignore: int = 0
    Entry: int = 1
    Exit: int = 2
    Adjacent: int = 3
    Opposite: int = 4


ConflictMode = ConflictModeT()
"""_"""

__pdoc__['ConflictMode'] = f"""Conflict mode.

```json
{to_doc(ConflictMode)}
```

What should happen if both entry and exit signals occur simultaneously?

Attributes:
    Ignore: Ignore both signals.
    Entry: Execute the entry signal.
    Exit: Execute the exit signal.
    Adjacent: Execute the adjacent signal.
    
        Takes effect only when in position, otherwise ignores.
    Opposite: Execute the opposite signal.
    
        Takes effect only when in position, otherwise ignores.
"""


class DirectionConflictModeT(tp.NamedTuple):
    Ignore: int = 0
    Long: int = 1
    Short: int = 2
    Adjacent: int = 3
    Opposite: int = 4


DirectionConflictMode = DirectionConflictModeT()
"""_"""

__pdoc__['DirectionConflictMode'] = f"""Direction conflict mode.

```json
{to_doc(DirectionConflictMode)}
```

What should happen if both long and short entry signals occur simultaneously?

Attributes:
    Ignore: Ignore both entry signals.
    Long: Execute the long entry signal.
    Short: Execute the short entry signal.
    Adjacent: Execute the adjacent entry signal. 
    
        Takes effect only when in position, otherwise ignores.
    Opposite: Execute the opposite entry signal. 
    
        Takes effect only when in position, otherwise ignores.
"""


class OppositeEntryModeT(tp.NamedTuple):
    Ignore: int = 0
    Close: int = 1
    CloseReduce: int = 2
    Reverse: int = 3
    ReverseReduce: int = 4


OppositeEntryMode = OppositeEntryModeT()
"""_"""

__pdoc__['OppositeEntryMode'] = f"""Opposite entry mode.

```json
{to_doc(OppositeEntryMode)}
```

What should happen if an entry signal of opposite direction occurs before an exit signal?

Attributes:
    Ignore: Ignore the opposite entry signal.
    Close: Close the current position.
    CloseReduce: Close the current position or reduce it if accumulation is enabled.
    Reverse: Reverse the current position.
    ReverseReduce: Reverse the current position or reduce it if accumulation is enabled.
"""


class StopEntryPriceT(tp.NamedTuple):
    ValPrice: int = 0
    Price: int = 1
    FillPrice: int = 2
    Close: int = 3


StopEntryPrice = StopEntryPriceT()
"""_"""

__pdoc__['StopEntryPrice'] = f"""Stop entry price.

```json
{to_doc(StopEntryPrice)}
```

Which price to use as an initial stop price?

Attributes:
    ValPrice: Asset valuation price.
    Price: Default price.
    FillPrice: Fill price (that is, slippage is already applied).
    Close: Closing price.
"""


class StopExitPriceT(tp.NamedTuple):
    StopLimit: int = 0
    StopMarket: int = 1
    Price: int = 2
    Close: int = 3


StopExitPrice = StopExitPriceT()
"""_"""

__pdoc__['StopExitPrice'] = f"""Stop exit price.

```json
{to_doc(StopExitPrice)}
```

Which price to use when exiting a position upon a stop signal?

Attributes:
    StopLimit: Stop price as from a limit order.
    
        If the stop was hit before, the opening price at the next bar is used.
        User-defined slippage is not applied.
    StopMarket: Stop price as from a market order.
    
        If the stop was hit before, the opening price at the next bar is used.
        User-defined slippage is applied.
    Price: Default price.
                
        User-defined slippage is applied.
    
        !!! note
            Make sure to use `StopExitPrice.Price` only together with `StopEntryPrice.Close`.
            Otherwise, there is no proof that the price comes after the stop price.
    Close: Closing price.
    
        User-defined slippage is applied.
        
!!! note
    We can execute only one signal per asset and bar. This means the following:
    
    1) Stop signal cannot be processed at the same bar as the entry signal.
    
    2) When dealing with stop orders, we have another signal - stop signal - that may be in a conflict 
    with the signals placed by the user. To choose between both, we assume that any stop signal comes 
    before any other signal in time. Thus, make sure to always execute ordinary signals using the 
    closing price when using stop orders. Otherwise, you're looking into the future.
"""


class StopExitModeT(tp.NamedTuple):
    Close: int = 0
    CloseReduce: int = 1
    Reverse: int = 2
    ReverseReduce: int = 3


StopExitMode = StopExitModeT()
"""_"""

__pdoc__['StopExitMode'] = f"""Stop exit mode.

```json
{to_doc(StopExitMode)}
```

How to exit the current position upon a stop signal?

Attributes:
    Close: Close the current position.
    CloseReduce: Close the current position or reduce it if accumulation is enabled.
    Reverse: Reverse the current position.
    ReverseReduce: Reverse the current position or reduce it if accumulation is enabled.
            
"""


class StopUpdateModeT(tp.NamedTuple):
    Keep: int = 0
    Override: int = 1
    OverrideNaN: int = 2


StopUpdateMode = StopUpdateModeT()
"""_"""

__pdoc__['StopUpdateMode'] = f"""Stop update mode.

```json
{to_doc(StopUpdateMode)}
```

What to do with the old stop upon new acquisition? 

Attributes:
    Keep: Keep the old stop.
    Override: Override the old stop, but only if the new stop is not NaN.
    OverrideNaN: Override the old stop, even if the new stop is NaN.
"""


class SizeTypeT(tp.NamedTuple):
    Amount: int = 0
    Value: int = 1
    Percent: int = 2
    TargetAmount: int = 3
    TargetValue: int = 4
    TargetPercent: int = 5


SizeType = SizeTypeT()
"""_"""

__pdoc__['SizeType'] = f"""Size type.

```json
{to_doc(SizeType)}
```

Attributes:
    Amount: Amount of assets to trade.
    Value: Asset value to trade.
    
        Gets converted into `SizeType.Amount` using `OrderContext.val_price_now`.
    Percent: Percentage of available resources to use in either direction (not to be confused with 
        the percentage of position value!)
    
        * When buying, it's the percentage of `OrderContext.cash_now`. 
        * When selling, it's the percentage of `OrderContext.position_now`.
        * When short selling, it's the percentage of `OrderContext.free_cash_now`.
        * When selling and short selling (i.e. reversing position), it's the percentage of 
        `OrderContext.position_now` and `OrderContext.free_cash_now`.
        
        !!! note
            Takes into account fees and slippage to find the limit.
            In reality, slippage and fees are not known beforehand.
    TargetAmount: Target amount of assets to hold (= target position).
    
        Uses `OrderContext.position_now` to get the current position.
        Gets converted into `SizeType.Amount`.
    TargetValue: Target asset value. 

        Uses `OrderContext.val_price_now` to get the current asset value. 
        Gets converted into `SizeType.TargetAmount`.
    TargetPercent: Target percentage of total value. 

        Uses `OrderContext.value_now` to get the current total value.
        Gets converted into `SizeType.TargetValue`.
"""


class DirectionT(tp.NamedTuple):
    LongOnly: int = 0
    ShortOnly: int = 1
    Both: int = 2


Direction = DirectionT()
"""_"""

__pdoc__['Direction'] = f"""Position direction.

```json
{to_doc(Direction)}
```

Attributes:
    LongOnly: Only long positions.
    ShortOnly: Only short positions.
    Both: Both long and short positions.
"""


class OrderStatusT(tp.NamedTuple):
    Filled: int = 0
    Ignored: int = 1
    Rejected: int = 2


OrderStatus = OrderStatusT()
"""_"""

__pdoc__['OrderStatus'] = f"""Order status.

```json
{to_doc(OrderStatus)}
```

Attributes:
    Filled: Order has been filled.
    Ignored: Order has been ignored.
    Rejected: Order has been rejected.
"""


class OrderSideT(tp.NamedTuple):
    Buy: int = 0
    Sell: int = 1


OrderSide = OrderSideT()
"""_"""

__pdoc__['OrderSide'] = f"""Order side.

```json
{to_doc(OrderSide)}
```
"""


class OrderStatusInfoT(tp.NamedTuple):
    SizeNaN: int = 0
    PriceNaN: int = 1
    ValPriceNaN: int = 2
    ValueNaN: int = 3
    ValueZeroNeg: int = 4
    SizeZero: int = 5
    NoCashShort: int = 6
    NoCashLong: int = 7
    NoOpenPosition: int = 8
    MaxSizeExceeded: int = 9
    RandomEvent: int = 10
    CantCoverFees: int = 11
    MinSizeNotReached: int = 12
    PartialFill: int = 13


OrderStatusInfo = OrderStatusInfoT()
"""_"""

__pdoc__['OrderStatusInfo'] = f"""Order status information.

```json
{to_doc(OrderStatusInfo)}
```
"""

status_info_desc = [
    "Size is NaN",
    "Price is NaN",
    "Asset valuation price is NaN",
    "Asset/group value is NaN",
    "Asset/group value is zero or negative",
    "Size is zero",
    "Not enough cash to short",
    "Not enough cash to long",
    "No open position to reduce/close",
    "Size is greater than maximum allowed",
    "Random event happened",
    "Not enough cash to cover fees",
    "Final size is less than minimum allowed",
    "Final size is less than requested"
]
"""_"""

__pdoc__['status_info_desc'] = f"""Order status description.

```json
{to_doc(status_info_desc)}
```
"""


class TradeDirectionT(tp.NamedTuple):
    Long: int = 0
    Short: int = 1


TradeDirection = TradeDirectionT()
"""_"""

__pdoc__['TradeDirection'] = f"""Event direction.

```json
{to_doc(TradeDirection)}
```
"""


class TradeStatusT(tp.NamedTuple):
    Open: int = 0
    Closed: int = 1


TradeStatus = TradeStatusT()
"""_"""

__pdoc__['TradeStatus'] = f"""Event status.

```json
{to_doc(TradeStatus)}
```
"""


class TradesTypeT(tp.NamedTuple):
    EntryTrades: int = 0
    ExitTrades: int = 1
    Positions: int = 2


TradesType = TradesTypeT()
"""_"""

__pdoc__['TradesType'] = f"""Trades type.

```json
{to_doc(TradesType)}
```
"""


# ############# Named tuples ############# #


class ProcessOrderState(tp.NamedTuple):
    cash: float
    position: float
    debt: float
    free_cash: float
    val_price: float
    value: float
    oidx: int
    lidx: int


__pdoc__['ProcessOrderState'] = "State before or after order processing."
__pdoc__['ProcessOrderState.cash'] = "Cash in the current column or group with cash sharing."
__pdoc__['ProcessOrderState.position'] = "Position in the current column."
__pdoc__['ProcessOrderState.debt'] = "Debt from shorting in the current column."
__pdoc__['ProcessOrderState.free_cash'] = "Free cash in the current column or group with cash sharing."
__pdoc__['ProcessOrderState.val_price'] = "Valuation price in the current column."
__pdoc__['ProcessOrderState.value'] = "Value in the current column or group with cash sharing."
__pdoc__['ProcessOrderState.oidx'] = "Index of order record."
__pdoc__['ProcessOrderState.lidx'] = "Index of log record."


class ExecuteOrderState(tp.NamedTuple):
    cash: float
    position: float
    debt: float
    free_cash: float


__pdoc__['ExecuteOrderState'] = "State after order execution."
__pdoc__['ExecuteOrderState.cash'] = "See `ProcessOrderState.cash`."
__pdoc__['ExecuteOrderState.position'] = "See `ProcessOrderState.position`."
__pdoc__['ExecuteOrderState.debt'] = "See `ProcessOrderState.debt`."
__pdoc__['ExecuteOrderState.free_cash'] = "See `ProcessOrderState.free_cash`."


class SimulationContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray


__pdoc__['SimulationContext'] = """A named tuple representing the context of a simulation.

Contains general information available to all other contexts.

Passed to `pre_sim_func_nb` and `post_sim_func_nb`."""
__pdoc__['SimulationContext.target_shape'] = """Target shape of the simulation.

A tuple with exactly two elements: the number of rows and columns.

Example:
    One day of minute data for three assets would yield a `target_shape` of `(1440, 3)`,
    where the first axis are rows (minutes) and the second axis are columns (assets).
"""
__pdoc__['SimulationContext.group_lens'] = """Number of columns in each group.

Even if columns are not grouped, `group_lens` contains ones - one column per group.

Example:
    In pairs trading, `group_lens` would be `np.array([2])`, while three independent
    columns would be represented by `group_lens` of `np.array([1, 1, 1])`.
"""
__pdoc__['SimulationContext.init_cash'] = """Initial capital per column or group with cash sharing.

If `SimulationContext.cash_sharing`, has shape `(group_lens.shape[0],)`, otherwise has shape `(target_shape[1],)`.

Example:
    Consider three columns, each having $100 of starting capital. If we built one group of two columns
    with cash sharing and one (imaginary) group with the last column, the `init_cash` would be 
    `np.array([200, 100])`. Without cash sharing, the `init_cash` would be `np.array([100, 100, 100])`.
"""
__pdoc__['SimulationContext.cash_sharing'] = "Whether cash sharing is enabled."
__pdoc__['SimulationContext.call_seq'] = """Default sequence of calls per segment.

Controls the sequence in which `order_func_nb` is executed within each segment.

Has shape `SimulationContext.target_shape` and each value must exist in the range `[0, group_len)`.

!!! note
    To use `sort_call_seq_nb`, should be generated using `CallSeqType.Default`.

    To change the call sequence dynamically, better change `SegmentContext.call_seq_now` in-place.
    
Example:
    The default call sequence for three data points and two groups with three columns each:
    
    ```python
    np.array([
        [0, 1, 2, 0, 1, 2],
        [0, 1, 2, 0, 1, 2],
        [0, 1, 2, 0, 1, 2]
    ])
    ```
"""
__pdoc__['SimulationContext.segment_mask'] = """Mask of whether a particular segment should be executed.

A segment is simply a sequence of `order_func_nb` calls under the same group and row.

If a segment is inactive, any callback function inside of it will not be executed.
You can still execute the segment's pre- and postprocessing function by enabling 
`SimulationContext.call_pre_segment` and `SimulationContext.call_post_segment` respectively.

Utilizes flexible indexing using `vectorbt.base.reshape_fns.flex_select_auto_nb` and `flex_2d`, 
so it can be passed as 

* 2-dim array, 
* 1-dim array per column (requires `flex_2d=True`), 
* 1-dim array per row (requires `flex_2d=False`), and
* a scalar. 

Broadcasts to the shape `(target_shape[0], group_lens.shape[0])`.

!!! note
    To modify the array in place, make sure to build an array of the full shape.

Example:
    Consider two groups with two columns each and the following activity mask:
    
    ```python
    np.array([[ True, False], 
              [False,  True]])
    ```
    
    The first group is only executed in the first row and the second group is only executed in the second row.
"""
__pdoc__['SimulationContext.call_pre_segment'] = """Whether to call `pre_segment_func_nb` regardless of 
`SimulationContext.segment_mask`."""
__pdoc__['SimulationContext.call_post_segment'] = """Whether to call `post_segment_func_nb` regardless of 
`SimulationContext.segment_mask`.

Allows, for example, to write user-defined arrays such as returns at the end of each segment."""
__pdoc__['SimulationContext.close'] = """Latest asset price at each time step.

Utilizes flexible indexing using `vectorbt.base.reshape_fns.flex_select_auto_nb` and `flex_2d`, 
so it can be passed as 

* 2-dim array, 
* 1-dim array per column (requires `flex_2d=True`), 
* 1-dim array per row (requires `flex_2d=False`), and
* a scalar. 

Broadcasts to the shape `SimulationContext.target_shape`.

!!! note
    To modify the array in place, make sure to build an array of the full shape.
"""
__pdoc__['SimulationContext.ffill_val_price'] = """Whether to track valuation price only if it's known.

Otherwise, unknown `SimulationContext.close` will lead to NaN in valuation price at the next timestamp."""
__pdoc__['SimulationContext.update_value'] = """Whether to update group value after each filled order.

Otherwise, stays the same for all columns in the group (the value is calculated
only once, before executing any order).

The change is marginal and mostly driven by transaction costs and slippage."""
__pdoc__['SimulationContext.fill_pos_record'] = """Whether to fill position record.

Disable this to make simulation a bit faster for simple use cases."""
__pdoc__['SimulationContext.flex_2d'] = """Whether the elements in a 1-dim array should be treated per
column rather than per row.

This flag is set automatically when using `vectorbt.portfolio.base.Portfolio.from_order_func` depending upon 
whether there is any argument that has been broadcast to 2 dimensions.

Has only effect when using flexible indexing, for example, with `vectorbt.base.reshape_fns.flex_select_auto_nb`.
"""
__pdoc__['SimulationContext.order_records'] = """Order records.

It's a 1-dimensional array with records of type `order_dt`.

The array is initialized with empty records first (they contain random data), and then 
gradually filled with order data. The number of initialized records depends upon `max_orders`, 
but usually it's `target_shape[0] * target_shape[1]`, meaning there is maximal one order record per element.
`max_orders` can be chosen lower if not every `order_func_nb` leads to a filled order, to save memory.

You can use `SimulationContext.last_oidx` to get the index of the latest filled order of each column.

Example:
    Before filling, each order record looks like this:
    
    ```python
    np.array([(-8070450532247928832, -8070450532247928832, 4, 0., 0., 0., 5764616306889786413)]
    ```
    
    After filling, it becomes like this:
    
    ```python
    np.array([(0, 0, 1, 50., 1., 0., 1)]
    ```
"""
__pdoc__['SimulationContext.log_records'] = """Log records.

Similar to `SimulationContext.order_records` but of type `log_dt` and index `SimulationContext.last_lidx`."""
__pdoc__['SimulationContext.last_cash'] = """Latest cash per column or group with cash sharing.

Has the same shape as `SimulationContext.init_cash`.

Gets updated right after `order_func_nb`.
"""
__pdoc__['SimulationContext.last_position'] = """Latest position per column.

Has shape `(target_shape[1],)`.

Gets updated right after `order_func_nb`.
"""
__pdoc__['SimulationContext.last_debt'] = """Latest debt from shorting per column.

Debt is the total value from shorting that hasn't been covered yet. Used to update `OrderContext.free_cash_now`.

Has shape `(target_shape[1],)`. 

Gets updated right after `order_func_nb`.
"""
__pdoc__['SimulationContext.last_free_cash'] = """Latest free cash per column or group with cash sharing.

Free cash never goes above the initial level, because an operation always costs money.

Has shape `(target_shape[1],)`. 

Gets updated right after `order_func_nb`.
"""
__pdoc__['SimulationContext.last_val_price'] = """Latest valuation price per column.

Has shape `(target_shape[1],)`.

Enables `SizeType.Value`, `SizeType.TargetValue`, and `SizeType.TargetPercent`.

Gets multiplied by the current position to get the value of the column (see `SimulationContext.last_value`).

Defaults to the `SimulationContext.close` before `post_segment_func_nb`.
If `SimulationContext.ffill_val_price`, gets updated only if `SimulationContext.close` is not NaN.
For example, close of `[1, 2, np.nan, np.nan, 5]` yields valuation price of `[1, 2, 2, 2, 5]`.

Also gets updated right after `pre_segment_func_nb` - you can use `pre_segment_func_nb` to
override `last_val_price` in-place, such that `order_func_nb` can use the new group value. 
You are not allowed to use `-np.inf` or `np.inf` - only finite values.
If `SimulationContext.update_value`, gets also updated right after `order_func_nb` using 
filled order price as the latest known price.

!!! note
    Since the previous `SimulationContext.close` is NaN in the first row, the first `last_val_price` is also NaN.
    
    Overriding `last_val_price` with NaN won't apply `SimulationContext.ffill_val_price`,
    so your entire group will become NaN.

Example:
    Consider 10 units in column 1 and 20 units in column 2. The previous close of them is
    $40 and $50 respectively, which is also the default valuation price in the current row,
    available as `last_val_price` in `pre_segment_func_nb`. If both columns are in the same group 
    with cash sharing, the group is valued at $1400 before any `order_func_nb` is called, and can 
    be later accessed via `OrderContext.value_now`.
"""
__pdoc__['SimulationContext.last_value'] = """Latest value per column or group with cash sharing.

Has the same shape as `SimulationContext.init_cash`.

Calculated by multiplying valuation price by the current position.
The value of each column in a group with cash sharing is summed to get the value of the entire group.

Gets updated using `SimulationContext.last_val_price` after `pre_segment_func_nb` and 
before `post_segment_func_nb`. If `SimulationContext.update_value`, gets also updated right after 
`order_func_nb` using filled order price as the latest known price (the difference will be minimal, 
only affected by costs).
"""
__pdoc__['SimulationContext.second_last_value'] = """Second-latest value per column or group with cash sharing.

Has the same shape as `SimulationContext.last_value`.

Contains the latest known value two rows before (`i - 2`) to be compared either with the latest known value 
one row before (`i - 1`) or now (`i`).

Gets updated at the end of each segment/row. 
"""
__pdoc__['SimulationContext.last_return'] = """Latest return per column or group with cash sharing.

Has the same shape as `SimulationContext.last_value`.

Calculated by comparing `SimulationContext.last_value` to `SimulationContext.second_last_value`.

Gets updated each time `SimulationContext.last_value` is updated.
"""
__pdoc__['SimulationContext.last_oidx'] = """Index of the latest order record of each column.

Points to `SimulationContext.order_records` and has shape `(target_shape[1],)`.

Example:
    `last_oidx` of `np.array([1, 100, -1])` means the latest filled order is `order_records[1]` for the
    first column, `order_records[100]` for the second column, and no orders have been filled yet
    for the third column.
"""
__pdoc__['SimulationContext.last_lidx'] = """Index of the latest log record of each column.

Similar to `SimulationContext.last_oidx` but for log records.
"""
__pdoc__['SimulationContext.last_pos_record'] = """Latest position record of each column.

It's a 1-dimensional array with records of type `trade_dt`.

Has shape `(target_shape[1],)`.

The array is initialized with empty records first (they contain random data)
and the field `id` is set to -1. Once the first position is entered in a column,
the `id` becomes 0 and the record materializes. Once the position is closed, the record
fixes its identifier and other data until the next position is entered. 

The fields `entry_price` and `exit_price` are average entry and exit price respectively.
The fields `pnl` and `return` contain statistics as if the position has been closed and are 
re-calculated using `SimulationContext.last_val_price` after `pre_segment_func_nb` 
(in case `SimulationContext.last_val_price` has been overridden) and before `post_segment_func_nb`.

!!! note
    In an open position record, the field `exit_price` doesn't reflect the latest valuation price,
    but keeps the average price at which the position has been reduced.

The position record is updated after successfully filling an order (after `order_func_nb` and
before `post_order_func_nb`).

Example:
    Consider a simulation that orders `order_size` for `order_price` and $1 fixed fees.
    Here's order info from `order_func_nb` and the updated position info from `post_order_func_nb`:
    
    ```plaintext
        order_size  order_price  id  col  size  entry_idx  entry_price  \\
    0          NaN            1  -1    0   1.0         13    14.000000   
    1          0.5            2   0    0   0.5          1     2.000000   
    2          1.0            3   0    0   1.5          1     2.666667   
    3          NaN            4   0    0   1.5          1     2.666667   
    4         -1.0            5   0    0   1.5          1     2.666667   
    5         -0.5            6   0    0   1.5          1     2.666667   
    6          NaN            7   0    0   1.5          1     2.666667   
    7         -0.5            8   1    0   0.5          7     8.000000   
    8         -1.0            9   1    0   1.5          7     8.666667   
    9          1.0           10   1    0   1.5          7     8.666667   
    10         0.5           11   1    0   1.5          7     8.666667   
    11         1.0           12   2    0   1.0         11    12.000000   
    12        -2.0           13   3    0   1.0         12    13.000000   
    13         2.0           14   4    0   1.0         13    14.000000   
    
        entry_fees  exit_idx  exit_price  exit_fees   pnl    return  direction  status
    0          0.5        -1         NaN        0.0 -0.50 -0.035714          0       0
    1          1.0        -1         NaN        0.0 -1.00 -1.000000          0       0
    2          2.0        -1         NaN        0.0 -1.50 -0.375000          0       0
    3          2.0        -1         NaN        0.0 -0.75 -0.187500          0       0
    4          2.0        -1    5.000000        1.0  0.50  0.125000          0       0
    5          2.0         5    5.333333        2.0  0.00  0.000000          0       1
    6          2.0         5    5.333333        2.0  0.00  0.000000          0       1
    7          1.0        -1         NaN        0.0 -1.00 -0.250000          1       0
    8          2.0        -1         NaN        0.0 -2.50 -0.192308          1       0
    9          2.0        -1   10.000000        1.0 -5.00 -0.384615          1       0
    10         2.0        10   10.333333        2.0 -6.50 -0.500000          1       1
    11         1.0        -1         NaN        0.0 -1.00 -0.083333          0       0
    12         0.5        -1         NaN        0.0 -0.50 -0.038462          1       0
    13         0.5        -1         NaN        0.0 -0.50 -0.035714          0       0
    ```
"""


class GroupContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    group: int
    group_len: int
    from_col: int
    to_col: int


__pdoc__['GroupContext'] = """A named tuple representing the context of a group.

A group is a set of nearby columns that are somehow related (for example, by sharing the same capital).
In each row, the columns under the same group are bound to the same segment.

Contains all fields from `SimulationContext` plus fields describing the current group.

Passed to `pre_group_func_nb` and `post_group_func_nb`.

Example:
    Consider a group of three columns, a group of two columns, and one more column:
    
    | group | group_len | from_col | to_col |
    | ----- | --------- | -------- | ------ |
    | 0     | 3         | 0        | 3      |
    | 1     | 2         | 3        | 5      |
    | 2     | 1         | 5        | 6      |
"""
for field in GroupContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['GroupContext.' + field] = f"See `SimulationContext.{field}`."
__pdoc__['GroupContext.group'] = """Index of the current group.

Has range `[0, group_lens.shape[0])`.
"""
__pdoc__['GroupContext.group_len'] = """Number of columns in the current group.

Scalar value. Same as `group_lens[group]`.
"""
__pdoc__['GroupContext.from_col'] = """Index of the first column in the current group.

Has range `[0, target_shape[1])`.
"""
__pdoc__['GroupContext.to_col'] = """Index of the last column in the current group plus one.

Has range `[1, target_shape[1] + 1)`. 

If columns are not grouped, equals to `from_col + 1`.

!!! warning
    In the last group, `to_col` points at a column that doesn't exist.
"""


class RowContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    i: int


__pdoc__['RowContext'] = """A named tuple representing the context of a row.

A row is a time step in which segments are executed.

Contains all fields from `SimulationContext` plus fields describing the current row.

Passed to `pre_row_func_nb` and `post_row_func_nb`.
"""
for field in RowContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['RowContext.' + field] = f"See `SimulationContext.{field}`."
__pdoc__['RowContext.i'] = """Index of the current row.

Has range `[0, target_shape[0])`.
"""


class SegmentContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    group: int
    group_len: int
    from_col: int
    to_col: int
    i: int
    call_seq_now: tp.Optional[tp.Array1d]


__pdoc__['SegmentContext'] = """A named tuple representing the context of a segment.

A segment is an intersection between groups and rows. It's an entity that defines
how and in which order elements within the same group and row are processed.

Contains all fields from `SimulationContext`, `GroupContext`, and `RowContext`, plus fields 
describing the current segment.

Passed to `pre_segment_func_nb` and `post_segment_func_nb`.
"""
for field in SegmentContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['SegmentContext.' + field] = f"See `SimulationContext.{field}`."
    elif field in GroupContext._fields:
        __pdoc__['SegmentContext.' + field] = f"See `GroupContext.{field}`."
    elif field in RowContext._fields:
        __pdoc__['SegmentContext.' + field] = f"See `RowContext.{field}`."
__pdoc__['SegmentContext.call_seq_now'] = """Sequence of calls within the current segment.

Has shape `(group_len,)`. 

Each value in this sequence should indicate the position of column in the group to
call next. Processing goes always from left to right.

You can use `pre_segment_func_nb` to override `call_seq_now`.
    
Example:
    `[2, 0, 1]` would first call column 2, then 0, and finally 1.
"""


class OrderContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    group: int
    group_len: int
    from_col: int
    to_col: int
    i: int
    call_seq_now: tp.Optional[tp.Array1d]
    col: int
    call_idx: int
    cash_now: float
    position_now: float
    debt_now: float
    free_cash_now: float
    val_price_now: float
    value_now: float
    return_now: float
    pos_record_now: tp.Record


__pdoc__['OrderContext'] = """A named tuple representing the context of an order.

Contains all fields from `SegmentContext` plus fields describing the current state.

Passed to `order_func_nb`.
"""
for field in OrderContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['OrderContext.' + field] = f"See `SimulationContext.{field}`."
    elif field in GroupContext._fields:
        __pdoc__['OrderContext.' + field] = f"See `GroupContext.{field}`."
    elif field in RowContext._fields:
        __pdoc__['OrderContext.' + field] = f"See `RowContext.{field}`."
    elif field in SegmentContext._fields:
        __pdoc__['OrderContext.' + field] = f"See `SegmentContext.{field}`."
__pdoc__['OrderContext.col'] = """Current column.

Has range `[0, target_shape[1])` and is always within `[from_col, to_col)`.
"""
__pdoc__['OrderContext.call_idx'] = """Index of the current call in `SegmentContext.call_seq_now`.

Has range `[0, group_len)`.
"""
__pdoc__['OrderContext.cash_now'] = "`SimulationContext.last_cash` for the current column/group."
__pdoc__['OrderContext.position_now'] = "`SimulationContext.last_position` for the current column."
__pdoc__['OrderContext.debt_now'] = "`SimulationContext.last_debt` for the current column."
__pdoc__['OrderContext.free_cash_now'] = "`SimulationContext.last_free_cash` for the current column/group."
__pdoc__['OrderContext.val_price_now'] = "`SimulationContext.last_val_price` for the current column."
__pdoc__['OrderContext.value_now'] = "`SimulationContext.last_value` for the current column/group."
__pdoc__['OrderContext.return_now'] = "`SimulationContext.last_return` for the current column/group."
__pdoc__['OrderContext.pos_record_now'] = "`SimulationContext.last_pos_record` for the current column."


class PostOrderContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    group: int
    group_len: int
    from_col: int
    to_col: int
    i: int
    call_seq_now: tp.Optional[tp.Array1d]
    col: int
    call_idx: int
    cash_before: float
    position_before: float
    debt_before: float
    free_cash_before: float
    val_price_before: float
    value_before: float
    order_result: "OrderResult"
    cash_now: float
    position_now: float
    debt_now: float
    free_cash_now: float
    val_price_now: float
    value_now: float
    return_now: float
    pos_record_now: tp.Record


__pdoc__['PostOrderContext'] = """A named tuple representing the context after an order has been processed.

Contains all fields from `OrderContext` plus fields describing the order result and the previous state.

Passed to `post_order_func_nb`.
"""
for field in PostOrderContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['PostOrderContext.' + field] = f"See `SimulationContext.{field}`."
    elif field in GroupContext._fields:
        __pdoc__['PostOrderContext.' + field] = f"See `GroupContext.{field}`."
    elif field in RowContext._fields:
        __pdoc__['PostOrderContext.' + field] = f"See `RowContext.{field}`."
    elif field in SegmentContext._fields:
        __pdoc__['PostOrderContext.' + field] = f"See `SegmentContext.{field}`."
    elif field in OrderContext._fields:
        __pdoc__['PostOrderContext.' + field] = f"See `OrderContext.{field}`."
__pdoc__['PostOrderContext.cash_before'] = "`OrderContext.cash_now` before execution."
__pdoc__['PostOrderContext.position_before'] = "`OrderContext.position_now` before execution."
__pdoc__['PostOrderContext.debt_before'] = "`OrderContext.debt_now` before execution."
__pdoc__['PostOrderContext.free_cash_before'] = "`OrderContext.free_cash_now` before execution."
__pdoc__['PostOrderContext.val_price_before'] = "`OrderContext.val_price_now` before execution."
__pdoc__['PostOrderContext.value_before'] = "`OrderContext.value_now` before execution."
__pdoc__['PostOrderContext.order_result'] = """Order result of type `OrderResult`.

Can be used to check whether the order has been filled, ignored, or rejected.
"""
__pdoc__['PostOrderContext.cash_now'] = "`OrderContext.cash_now` after execution."
__pdoc__['PostOrderContext.position_now'] = "`OrderContext.position_now` after execution."
__pdoc__['PostOrderContext.debt_now'] = "`OrderContext.debt_now` after execution."
__pdoc__['PostOrderContext.free_cash_now'] = "`OrderContext.free_cash_now` after execution."
__pdoc__['PostOrderContext.val_price_now'] = """`OrderContext.val_price_now` after execution.

If `SimulationContext.update_value`, gets replaced with the fill price, 
as it becomes the most recently known price. Otherwise, stays the same.
"""
__pdoc__['PostOrderContext.value_now'] = """`OrderContext.value_now` after execution.

If `SimulationContext.update_value`, gets updated with the new cash and value of the column. Otherwise, stays the same.
"""
__pdoc__['PostOrderContext.return_now'] = "`OrderContext.return_now` after execution."
__pdoc__['PostOrderContext.pos_record_now'] = "`OrderContext.pos_record_now` after execution."


class FlexOrderContext(tp.NamedTuple):
    target_shape: tp.Shape
    group_lens: tp.Array1d
    init_cash: tp.Array1d
    cash_sharing: bool
    call_seq: tp.Optional[tp.Array2d]
    segment_mask: tp.ArrayLike
    call_pre_segment: bool
    call_post_segment: bool
    close: tp.ArrayLike
    ffill_val_price: bool
    update_value: bool
    fill_pos_record: bool
    flex_2d: bool
    order_records: tp.RecordArray
    log_records: tp.RecordArray
    last_cash: tp.Array1d
    last_position: tp.Array1d
    last_debt: tp.Array1d
    last_free_cash: tp.Array1d
    last_val_price: tp.Array1d
    last_value: tp.Array1d
    second_last_value: tp.Array1d
    last_return: tp.Array1d
    last_oidx: tp.Array1d
    last_lidx: tp.Array1d
    last_pos_record: tp.RecordArray
    group: int
    group_len: int
    from_col: int
    to_col: int
    i: int
    call_seq_now: None
    call_idx: int


__pdoc__['FlexOrderContext'] = """A named tuple representing the context of a flexible order.

Contains all fields from `SegmentContext` plus the current call index.

Passed to `flex_order_func_nb`.
"""
for field in FlexOrderContext._fields:
    if field in SimulationContext._fields:
        __pdoc__['FlexOrderContext.' + field] = f"See `SimulationContext.{field}`."
    elif field in GroupContext._fields:
        __pdoc__['FlexOrderContext.' + field] = f"See `GroupContext.{field}`."
    elif field in RowContext._fields:
        __pdoc__['FlexOrderContext.' + field] = f"See `RowContext.{field}`."
    elif field in SegmentContext._fields:
        __pdoc__['FlexOrderContext.' + field] = f"See `SegmentContext.{field}`."
__pdoc__['FlexOrderContext.call_idx'] = "Index of the current call."


class Order(tp.NamedTuple):
    size: float = np.inf
    price: float = np.inf
    size_type: int = SizeType.Amount
    direction: int = Direction.Both
    fees: float = 0.0
    fixed_fees: float = 0.0
    slippage: float = 0.0
    min_size: float = 0.0
    max_size: float = np.inf
    size_granularity: float = np.nan
    reject_prob: float = 0.0
    lock_cash: bool = False
    allow_partial: bool = True
    raise_reject: bool = False
    log: bool = False


__pdoc__['Order'] = """A named tuple representing an order.

!!! note
    Currently, Numba has issues with using defaults when filling named tuples. 
    Use `vectorbt.portfolio.nb.order_nb` to create an order."""
__pdoc__['Order.size'] = """Size in units.

Behavior depends upon `Order.size_type` and `Order.direction`.

For any fixed size:

* Set to any number to buy/sell some fixed amount or value.
    Longs are limited by the current cash balance, while shorts are only limited if `Order.lock_cash`.
* Set to `np.inf` to buy for all cash, or `-np.inf` to sell for all free cash.
    If `Order.direction` is not `Direction.Both`, `-np.inf` will close the position.
* Set to `np.nan` or 0 to skip.

For any target size:

* Set to any number to buy/sell an amount relative to the current position or value.
* Set to 0 to close the current position.
* Set to `np.nan` to skip.
"""
__pdoc__['Order.price'] = """Price per unit. 

Final price will depend upon slippage.

* If `-np.inf`, replaced by the current open (if available) or the previous close (≈ the current open in crypto).
* If `np.inf`, replaced by the current close.

!!! note
    Make sure to use timestamps that come between (and ideally not including) the current open and close."""
__pdoc__['Order.size_type'] = "See `SizeType`."
__pdoc__['Order.direction'] = "See `Direction`."
__pdoc__['Order.fees'] = """Fees in percentage of the order value.

Negative trading fees like -0.05 means earning 0.05% per trade instead of paying a fee.

!!! note
    0.01 = 1%."""
__pdoc__['Order.fixed_fees'] = """Fixed amount of fees to pay for this order.

Similar to `Order.fees`, can be negative."""
__pdoc__['Order.fixed_fees'] = "Fixed amount of fees to pay for this order."
__pdoc__['Order.slippage'] = """Slippage in percentage of `Order.price`. 

Slippage is a penalty applied on the price.

!!! note
    0.01 = 1%."""
__pdoc__['Order.min_size'] = """Minimum size in both directions. 

Lower than that will be rejected."""
__pdoc__['Order.max_size'] = """Maximum size in both directions. 

Higher than that will be partly filled."""
__pdoc__['Order.size_granularity'] = """Granularity of the size.

For example, granularity of 1.0 makes the quantity to behave like an integer. 
Placing an order of 12.5 shares (in any direction) will order exactly 12.0 shares.

!!! note
    The filled size remains a floating number."""
__pdoc__['Order.reject_prob'] = """Probability of rejecting this order to simulate a random rejection event.

Not everything goes smoothly in real life. Use random rejections to test your order management for robustness."""
__pdoc__['Order.lock_cash'] = """Whether to lock cash when shorting. 

If enabled, prevents `free_cash` from turning negative when buying or short selling.
A negative `free_cash` means one column used collateral of another column, which is generally undesired."""
__pdoc__['Order.allow_partial'] = """Whether to allow partial fill.

Otherwise, the order gets rejected.

Does not apply when `Order.size` is `np.inf`."""
__pdoc__['Order.raise_reject'] = """Whether to raise exception if order has been rejected.

Terminates the simulation."""
__pdoc__['Order.log'] = """Whether to log this order by filling a log record. 

Remember to increase `max_logs`."""

NoOrder = Order(
    size=np.nan,
    price=np.nan,
    size_type=-1,
    direction=-1,
    fees=np.nan,
    fixed_fees=np.nan,
    slippage=np.nan,
    min_size=np.nan,
    max_size=np.nan,
    size_granularity=np.nan,
    reject_prob=np.nan,
    lock_cash=False,
    allow_partial=False,
    raise_reject=False,
    log=False
)
"""_"""

__pdoc__['NoOrder'] = "Order that should not be processed."


class OrderResult(tp.NamedTuple):
    size: float
    price: float
    fees: float
    side: int
    status: int
    status_info: int


__pdoc__['OrderResult'] = "A named tuple representing an order result."
__pdoc__['OrderResult.size'] = "Filled size."
__pdoc__['OrderResult.price'] = "Filled price per unit, adjusted with slippage."
__pdoc__['OrderResult.fees'] = "Total fees paid for this order."
__pdoc__['OrderResult.side'] = "See `OrderSide`."
__pdoc__['OrderResult.status'] = "See `OrderStatus`."
__pdoc__['OrderResult.status_info'] = "See `OrderStatusInfo`."


class AdjustSLContext(tp.NamedTuple):
    i: int
    col: int
    position_now: float
    val_price_now: float
    init_i: int
    init_price: float
    curr_i: int
    curr_price: float
    curr_stop: float
    curr_trail: bool


__pdoc__['AdjustSLContext'] = "A named tuple representing the context for adjusting (trailing) stop loss."
__pdoc__['AdjustSLContext.i'] = """Index of the current row.

Has range `[0, target_shape[0])`."""
__pdoc__['AdjustSLContext.col'] = """Current column.

Has range `[0, target_shape[1])` and is always within `[from_col, to_col)`."""
__pdoc__['AdjustSLContext.position_now'] = "Latest position."
__pdoc__['AdjustSLContext.val_price_now'] = "Latest valuation price."
__pdoc__['AdjustSLContext.init_i'] = """Index of the row of the initial stop.

Doesn't change."""
__pdoc__['AdjustSLContext.init_price'] = """Price of the initial stop.

Doesn't change."""
__pdoc__['AdjustSLContext.curr_i'] = """Index of the row of the updated stop.

Gets updated once the price is updated."""
__pdoc__['AdjustSLContext.curr_price'] = """Current stop price.

Gets updated in trailing SL once a higher price is discovered."""
__pdoc__['AdjustSLContext.curr_stop'] = """Current stop value.

Can be updated by adjustment function."""
__pdoc__['AdjustSLContext.curr_trail'] = """Current trailing flag.

Can be updated by adjustment function."""


class AdjustTPContext(tp.NamedTuple):
    i: int
    col: int
    position_now: float
    val_price_now: float
    init_i: int
    init_price: float
    curr_stop: float


__pdoc__['AdjustTPContext'] = "A named tuple representing the context for adjusting take profit."
__pdoc__['AdjustTPContext.i'] = "See `AdjustSLContext.i`."
__pdoc__['AdjustTPContext.col'] = "See `AdjustSLContext.col`."
__pdoc__['AdjustTPContext.position_now'] = "See `AdjustSLContext.position_now`."
__pdoc__['AdjustTPContext.val_price_now'] = "See `AdjustSLContext.val_price_now`."
__pdoc__['AdjustTPContext.init_i'] = "See `AdjustSLContext.init_i`."
__pdoc__['AdjustTPContext.init_price'] = "See `AdjustSLContext.curr_price`."
__pdoc__['AdjustTPContext.curr_stop'] = "See `AdjustSLContext.curr_stop`."


class SignalContext(tp.NamedTuple):
    i: int
    col: int
    position_now: float
    val_price_now: float
    flex_2d: bool


__pdoc__['AdjustSLContext'] = "A named tuple representing the context for generation of signals."
__pdoc__['AdjustSLContext.i'] = """Index of the current row.

Has range `[0, target_shape[0])`."""
__pdoc__['AdjustSLContext.col'] = """Current column.

Has range `[0, target_shape[1])` and is always within `[from_col, to_col)`."""
__pdoc__['AdjustSLContext.position_now'] = "Latest position."
__pdoc__['AdjustSLContext.val_price_now'] = "Latest valuation price."
__pdoc__['AdjustSLContext.flex_2d'] = "See `vectorbt.base.reshape_fns.flex_select_auto_nb`."

# ############# Records ############# #

order_dt = np.dtype([
    ('id', np.int64),
    ('col', np.int64),
    ('idx', np.int64),
    ('size', np.float64),
    ('price', np.float64),
    ('fees', np.float64),
    ('side', np.int64),
], align=True)
"""_"""

__pdoc__['order_dt'] = f"""`np.dtype` of order records.

```json
{to_doc(order_dt)}
```
"""

_trade_fields = [
    ('id', np.int64),
    ('col', np.int64),
    ('size', np.float64),
    ('entry_idx', np.int64),
    ('entry_price', np.float64),
    ('entry_fees', np.float64),
    ('exit_idx', np.int64),
    ('exit_price', np.float64),
    ('exit_fees', np.float64),
    ('pnl', np.float64),
    ('return', np.float64),
    ('direction', np.int64),
    ('status', np.int64),
    ('parent_id', np.int64)
]

trade_dt = np.dtype(_trade_fields, align=True)
"""_"""

__pdoc__['trade_dt'] = f"""`np.dtype` of trade records.

```json
{to_doc(trade_dt)}
```
"""

_log_fields = [
    ('id', np.int64),
    ('group', np.int64),
    ('col', np.int64),
    ('idx', np.int64),
    ('cash', np.float64),
    ('position', np.float64),
    ('debt', np.float64),
    ('free_cash', np.float64),
    ('val_price', np.float64),
    ('value', np.float64),
    ('req_size', np.float64),
    ('req_price', np.float64),
    ('req_size_type', np.int64),
    ('req_direction', np.int64),
    ('req_fees', np.float64),
    ('req_fixed_fees', np.float64),
    ('req_slippage', np.float64),
    ('req_min_size', np.float64),
    ('req_max_size', np.float64),
    ('req_size_granularity', np.float64),
    ('req_reject_prob', np.float64),
    ('req_lock_cash', np.bool_),
    ('req_allow_partial', np.bool_),
    ('req_raise_reject', np.bool_),
    ('req_log', np.bool_),
    ('new_cash', np.float64),
    ('new_position', np.float64),
    ('new_debt', np.float64),
    ('new_free_cash', np.float64),
    ('new_val_price', np.float64),
    ('new_value', np.float64),
    ('res_size', np.float64),
    ('res_price', np.float64),
    ('res_fees', np.float64),
    ('res_side', np.int64),
    ('res_status', np.int64),
    ('res_status_info', np.int64),
    ('order_id', np.int64)
]

log_dt = np.dtype(_log_fields, align=True)
"""_"""

__pdoc__['log_dt'] = f"""`np.dtype` of log records.

```json
{to_doc(log_dt)}
```
"""
