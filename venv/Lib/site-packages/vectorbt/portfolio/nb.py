# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions that are used for portfolio
modeling, such as generating and filling orders. These only accept NumPy arrays and
other Numba-compatible types.

!!! note
    vectorbt treats matrices as first-class citizens and expects input arrays to be
    2-dim, unless function has suffix `_1d` or is meant to be input to another function.
    
    All functions passed as argument should be Numba-compiled.
    
    Records should retain the order they were created in.

!!! warning
    Accumulation of roundoff error possible.
    See [here](https://en.wikipedia.org/wiki/Round-off_error#Accumulation_of_roundoff_error) for explanation.

    Rounding errors can cause trades and positions to not close properly:

    ```pycon
    >>> print('%.50f' % 0.1)  # has positive error
    0.10000000000000000555111512312578270211815834045410

    >>> # many buy transactions with positive error -> cannot close position
    >>> sum([0.1 for _ in range(1000000)]) - 100000
    1.3328826753422618e-06

    >>> print('%.50f' % 0.3)  # has negative error
    0.29999999999999998889776975374843459576368331909180

    >>> # many sell transactions with negative error -> cannot close position
    >>> 300000 - sum([0.3 for _ in range(1000000)])
    5.657668225467205e-06
    ```

    While vectorbt has implemented tolerance checks when comparing floats for equality,
    adding/subtracting small amounts large number of times may still introduce a noticable
    error that cannot be corrected post factum.

    To mitigate this issue, avoid repeating lots of micro-transactions of the same sign.
    For example, reduce by `np.inf` or `position_now` to close a long/short position.

    See `vectorbt.utils.math_` for current tolerance values.
"""

import numpy as np
from numba import njit

from vectorbt import _typing as tp
from vectorbt.base.reshape_fns import flex_select_auto_nb
from vectorbt.generic import nb as generic_nb
from vectorbt.portfolio.enums import *
from vectorbt.returns import nb as returns_nb
from vectorbt.utils.array_ import insert_argsort_nb
from vectorbt.utils.math_ import (
    is_close_nb,
    is_close_or_less_nb,
    is_less_nb,
    add_nb
)


# ############# Order processing ############# #


@njit(cache=True)
def order_not_filled_nb(status: int, status_info: int) -> OrderResult:
    """Return `OrderResult` for order that hasn't been filled."""
    return OrderResult(np.nan, np.nan, np.nan, -1, status, status_info)


@njit(cache=True)
def buy_nb(exec_state: ExecuteOrderState,
           size: float,
           price: float,
           direction: int = Direction.Both,
           fees: float = 0.,
           fixed_fees: float = 0.,
           slippage: float = 0.,
           min_size: float = 0.,
           max_size: float = np.inf,
           size_granularity: float = np.nan,
           lock_cash: bool = False,
           allow_partial: bool = True,
           percent: float = np.nan) -> tp.Tuple[ExecuteOrderState, OrderResult]:
    """Buy or/and cover."""

    # Get price adjusted with slippage
    adj_price = price * (1 + slippage)

    # Set cash limit
    if lock_cash:
        if exec_state.position >= 0:
            # cash == free_cash in a long position, unless other column(s) locked some of the cash
            cash_limit = exec_state.free_cash
        else:
            # How much free cash remains after closing out the short position?
            cover_req_cash = abs(exec_state.position) * adj_price * (1 + fees) + fixed_fees
            cover_free_cash = add_nb(exec_state.free_cash + 2 * exec_state.debt, -cover_req_cash)
            if cover_free_cash > 0:
                # Enough cash to close out the short position and open a long one
                cash_limit = exec_state.free_cash + 2 * exec_state.debt
            elif cover_free_cash < 0:
                # Not enough cash to close out the short position
                avg_entry_price = exec_state.debt / abs(exec_state.position)
                max_short_size = ((exec_state.free_cash - fixed_fees) / (adj_price * (1 + fees) - 2 * avg_entry_price))
                cash_limit = max_short_size * adj_price * (1 + fees) + fixed_fees
            else:
                # Exact amount of cash to close out the short position
                cash_limit = exec_state.cash
    else:
        cash_limit = exec_state.cash
    cash_limit = min(cash_limit, exec_state.cash)
    if not np.isnan(percent):
        # Apply percentage
        cash_limit = min(cash_limit, percent * cash_limit)

    if direction == Direction.LongOnly or direction == Direction.Both:
        if cash_limit == 0:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.NoCashLong)
        if np.isinf(size) and np.isinf(cash_limit):
            raise ValueError("Attempt to go in long direction infinitely")
    else:
        if exec_state.position == 0:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.NoOpenPosition)

    # Get optimal order size
    if direction == Direction.ShortOnly:
        adj_size = min(-exec_state.position, size)
    else:
        adj_size = size

    if adj_size == 0:
        return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.SizeZero)

    if adj_size > max_size:
        if not allow_partial:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.MaxSizeExceeded)

        adj_size = max_size

    # Adjust granularity
    if not np.isnan(size_granularity):
        adj_size = adj_size // size_granularity * size_granularity

    # Get cash required to complete this order
    req_cash = adj_size * adj_price
    req_fees = req_cash * fees + fixed_fees
    total_req_cash = req_cash + req_fees

    if is_close_or_less_nb(total_req_cash, cash_limit):
        # Sufficient amount of cash
        final_size = adj_size
        fees_paid = req_fees
        final_req_cash = total_req_cash
    else:
        # Insufficient amount of cash, size will be less than requested

        # For fees of 10% and 1$ per transaction, you can buy for 90$ (new_req_cash)
        # to spend 100$ (cash_limit) in total
        max_req_cash = add_nb(cash_limit, -fixed_fees) / (1 + fees)
        if max_req_cash <= 0:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.CantCoverFees)

        max_acq_size = max_req_cash / adj_price

        if not np.isnan(size_granularity):
            # Adjust granularity
            final_size = max_acq_size // size_granularity * size_granularity
            new_req_cash = final_size * adj_price
            fees_paid = new_req_cash * fees + fixed_fees
            final_req_cash = new_req_cash + fees_paid
        else:
            final_size = max_acq_size
            fees_paid = cash_limit - max_req_cash
            final_req_cash = cash_limit

    if is_close_nb(adj_size, 0):
        return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.SizeZero)

    # Check against minimum size
    if is_less_nb(final_size, min_size):
        return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.MinSizeNotReached)

    # Check against partial fill (np.inf doesn't count)
    if np.isfinite(size) and is_less_nb(final_size, size) and not allow_partial:
        return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.PartialFill)

    # Update current cash balance and position
    new_cash = add_nb(exec_state.cash, -final_req_cash)
    new_position = add_nb(exec_state.position, final_size)

    # Update current debt and free cash
    if exec_state.position < 0:
        if new_position < 0:
            short_size = final_size
        else:
            short_size = abs(exec_state.position)
        avg_entry_price = exec_state.debt / abs(exec_state.position)
        debt_diff = short_size * avg_entry_price
        new_debt = add_nb(exec_state.debt, -debt_diff)
        new_free_cash = add_nb(exec_state.free_cash + 2 * debt_diff, -final_req_cash)
    else:
        new_debt = exec_state.debt
        new_free_cash = add_nb(exec_state.free_cash, -final_req_cash)

    # Return filled order
    order_result = OrderResult(
        final_size,
        adj_price,
        fees_paid,
        OrderSide.Buy,
        OrderStatus.Filled,
        -1
    )
    new_exec_state = ExecuteOrderState(
        cash=new_cash,
        position=new_position,
        debt=new_debt,
        free_cash=new_free_cash
    )
    return new_exec_state, order_result


@njit(cache=True)
def sell_nb(exec_state: ExecuteOrderState,
            size: float,
            price: float,
            direction: int = Direction.Both,
            fees: float = 0.,
            fixed_fees: float = 0.,
            slippage: float = 0.,
            min_size: float = 0.,
            max_size: float = np.inf,
            size_granularity: float = np.nan,
            lock_cash: bool = False,
            allow_partial: bool = True,
            percent: float = np.nan) -> tp.Tuple[ExecuteOrderState, OrderResult]:
    """Sell or/and short sell."""

    # Get price adjusted with slippage
    adj_price = price * (1 - slippage)

    # Get optimal order size
    if direction == Direction.LongOnly:
        size_limit = min(exec_state.position, size)
    else:
        if lock_cash or (np.isinf(size) and not np.isnan(percent)):
            # Get the maximum size that can be (short) sold
            long_size = max(exec_state.position, 0)
            long_cash = long_size * adj_price * (1 - fees)
            total_free_cash = add_nb(exec_state.free_cash, long_cash)

            if total_free_cash <= 0:
                if exec_state.position <= 0:
                    # There is nothing to sell, and no free cash to short sell
                    return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.NoCashShort)

                # There is position to close, but no free cash to short sell
                max_size_limit = long_size
            else:
                # There is position to close and/or free cash to short sell
                max_short_size = add_nb(total_free_cash, -fixed_fees) / (adj_price * (1 + fees))
                max_size_limit = add_nb(long_size, max_short_size)
                if max_size_limit <= 0:
                    return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.CantCoverFees)

            if lock_cash:
                # Size has upper limit
                if np.isinf(size) and not np.isnan(percent):
                    size_limit = min(percent * max_size_limit, max_size_limit)
                    percent = np.nan
                elif not np.isnan(percent):
                    size_limit = min(percent * size, max_size_limit)
                    percent = np.nan
                else:
                    size_limit = min(size, max_size_limit)
            else:  # np.isinf(size) and not np.isnan(percent)
                # Size has no upper limit
                size_limit = max_size_limit
        else:
            size_limit = size

    if not np.isnan(percent):
        # Apply percentage
        size_limit = percent * size_limit

    if size_limit > max_size:
        if not allow_partial:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.MaxSizeExceeded)

        size_limit = max_size

    if direction == Direction.ShortOnly or direction == Direction.Both:
        if np.isinf(size_limit):
            raise ValueError("Attempt to go in short direction infinitely")
    else:
        if exec_state.position == 0:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.NoOpenPosition)

    # Adjust granularity
    if not np.isnan(size_granularity):
        size_limit = size_limit // size_granularity * size_granularity

    if is_close_nb(size_limit, 0):
        return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.SizeZero)

    # Check against minimum size
    if is_less_nb(size_limit, min_size):
        return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.MinSizeNotReached)

    # Check against partial fill
    if np.isfinite(size) and is_less_nb(size_limit, size) and not allow_partial:  # np.inf doesn't count
        return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.PartialFill)

    # Get acquired cash
    acq_cash = size_limit * adj_price

    # Update fees
    fees_paid = acq_cash * fees + fixed_fees

    # Get final cash by subtracting costs
    final_acq_cash = add_nb(acq_cash, -fees_paid)
    if final_acq_cash < 0:
        return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.CantCoverFees)

    # Update current cash balance and position
    new_cash = exec_state.cash + final_acq_cash
    new_position = add_nb(exec_state.position, -size_limit)

    # Update current debt and free cash
    if new_position < 0:
        if exec_state.position < 0:
            short_size = size_limit
        else:
            short_size = abs(new_position)
        short_value = short_size * adj_price
        new_debt = exec_state.debt + short_value
        free_cash_diff = add_nb(final_acq_cash, -2 * short_value)
        new_free_cash = add_nb(exec_state.free_cash, free_cash_diff)
    else:
        new_debt = exec_state.debt
        new_free_cash = exec_state.free_cash + final_acq_cash

    # Return filled order
    order_result = OrderResult(
        size_limit,
        adj_price,
        fees_paid,
        OrderSide.Sell,
        OrderStatus.Filled,
        -1
    )
    new_exec_state = ExecuteOrderState(
        cash=new_cash,
        position=new_position,
        debt=new_debt,
        free_cash=new_free_cash
    )
    return new_exec_state, order_result


@njit(cache=True)
def execute_order_nb(state: ProcessOrderState, order: Order) -> tp.Tuple[ExecuteOrderState, OrderResult]:
    """Execute an order given the current state.

    Args:
        state (ProcessOrderState): See `vectorbt.portfolio.enums.ProcessOrderState`.
        order (Order): See `vectorbt.portfolio.enums.Order`.

    Error is thrown if an input has value that is not expected.
    Order is ignored if its execution has no effect on current balance.
    Order is rejected if an input goes over a limit/restriction.
    """
    # numerical stability
    cash = state.cash
    if is_close_nb(cash, 0):
        cash = 0.
    position = state.position
    if is_close_nb(position, 0):
        position = 0.
    debt = state.debt
    if is_close_nb(debt, 0):
        debt = 0.
    free_cash = state.free_cash
    if is_close_nb(free_cash, 0):
        free_cash = 0.
    val_price = state.val_price
    if is_close_nb(val_price, 0):
        val_price = 0.
    value = state.value
    if is_close_nb(value, 0):
        value = 0.

    # Pre-fill execution state for convenience
    exec_state = ExecuteOrderState(
        cash=cash,
        position=position,
        debt=debt,
        free_cash=free_cash
    )

    # Ignore order
    if np.isnan(order.size):
        return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.SizeNaN)
    if np.isnan(order.price):
        return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.PriceNaN)

    # Check execution state
    if np.isnan(cash) or cash < 0:
        raise ValueError("cash cannot be NaN and must be greater than 0")
    if not np.isfinite(position):
        raise ValueError("position must be finite")
    if not np.isfinite(debt) or debt < 0:
        raise ValueError("debt must be finite and 0 or greater")
    if np.isnan(free_cash):
        raise ValueError("free_cash cannot be NaN")

    # Check order
    if not np.isfinite(order.price) or order.price <= 0:
        raise ValueError("order.price must be finite and greater than 0")
    if order.size_type < 0 or order.size_type >= len(SizeType):
        raise ValueError("order.size_type is invalid")
    if order.direction < 0 or order.direction >= len(Direction):
        raise ValueError("order.direction is invalid")
    if order.direction == Direction.LongOnly and position < 0:
        raise ValueError("position is negative but order.direction is Direction.LongOnly")
    if order.direction == Direction.ShortOnly and position > 0:
        raise ValueError("position is positive but order.direction is Direction.ShortOnly")
    if not np.isfinite(order.fees):
        raise ValueError("order.fees must be finite")
    if not np.isfinite(order.fixed_fees):
        raise ValueError("order.fixed_fees must be finite")
    if not np.isfinite(order.slippage) or order.slippage < 0:
        raise ValueError("order.slippage must be finite and 0 or greater")
    if not np.isfinite(order.min_size) or order.min_size < 0:
        raise ValueError("order.min_size must be finite and 0 or greater")
    if np.isnan(order.max_size) or order.max_size <= 0:
        raise ValueError("order.max_size must be greater than 0")
    if np.isinf(order.size_granularity) or order.size_granularity <= 0:
        raise ValueError("order.size_granularity must be either NaN or finite and greater than 0")
    if not np.isfinite(order.reject_prob) or order.reject_prob < 0 or order.reject_prob > 1:
        raise ValueError("order.reject_prob must be between 0 and 1")

    order_size = order.size
    order_size_type = order.size_type

    if order.direction == Direction.ShortOnly:
        # Positive/negative size in short direction should be treated as negative/positive
        order_size *= -1

    if order_size_type == SizeType.TargetPercent:
        # Target percentage of current value
        if np.isnan(value):
            return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.ValueNaN)
        if value <= 0:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.ValueZeroNeg)

        order_size *= value
        order_size_type = SizeType.TargetValue

    if order_size_type == SizeType.Value or order_size_type == SizeType.TargetValue:
        # Target value
        if np.isinf(val_price) or val_price <= 0:
            raise ValueError("val_price_now must be finite and greater than 0")
        if np.isnan(val_price):
            return exec_state, order_not_filled_nb(OrderStatus.Ignored, OrderStatusInfo.ValPriceNaN)

        order_size /= val_price
        if order_size_type == SizeType.Value:
            order_size_type = SizeType.Amount
        else:
            order_size_type = SizeType.TargetAmount

    if order_size_type == SizeType.TargetAmount:
        # Target amount
        order_size -= position
        order_size_type = SizeType.Amount

    if order_size_type == SizeType.Amount:
        if order.direction == Direction.ShortOnly or order.direction == Direction.Both:
            if order_size < 0 and np.isinf(order_size):
                # Infinite negative size has a special meaning: 100% to short
                order_size = -1.
                order_size_type = SizeType.Percent

    percent = np.nan
    if order_size_type == SizeType.Percent:
        # Percentage of resources
        percent = abs(order_size)
        order_size = np.sign(order_size) * np.inf
        order_size_type = SizeType.Amount

    if order_size > 0:
        new_exec_state, order_result = buy_nb(
            exec_state,
            order_size,
            order.price,
            direction=order.direction,
            fees=order.fees,
            fixed_fees=order.fixed_fees,
            slippage=order.slippage,
            min_size=order.min_size,
            max_size=order.max_size,
            size_granularity=order.size_granularity,
            lock_cash=order.lock_cash,
            allow_partial=order.allow_partial,
            percent=percent
        )
    else:
        new_exec_state, order_result = sell_nb(
            exec_state,
            -order_size,
            order.price,
            direction=order.direction,
            fees=order.fees,
            fixed_fees=order.fixed_fees,
            slippage=order.slippage,
            min_size=order.min_size,
            max_size=order.max_size,
            size_granularity=order.size_granularity,
            lock_cash=order.lock_cash,
            allow_partial=order.allow_partial,
            percent=percent
        )

    if order.reject_prob > 0:
        if np.random.uniform(0, 1) < order.reject_prob:
            return exec_state, order_not_filled_nb(OrderStatus.Rejected, OrderStatusInfo.RandomEvent)

    return new_exec_state, order_result


@njit(cache=True)
def fill_log_record_nb(record: tp.Record,
                       record_id: int,
                       i: int,
                       col: int,
                       group: int,
                       cash: float,
                       position: float,
                       debt: float,
                       free_cash: float,
                       val_price: float,
                       value: float,
                       order: Order,
                       new_cash: float,
                       new_position: float,
                       new_debt: float,
                       new_free_cash: float,
                       new_val_price: float,
                       new_value: float,
                       order_result: OrderResult,
                       order_id: int) -> None:
    """Fill a log record."""

    record['id'] = record_id
    record['group'] = group
    record['col'] = col
    record['idx'] = i
    record['cash'] = cash
    record['position'] = position
    record['debt'] = debt
    record['free_cash'] = free_cash
    record['val_price'] = val_price
    record['value'] = value
    record['req_size'] = order.size
    record['req_price'] = order.price
    record['req_size_type'] = order.size_type
    record['req_direction'] = order.direction
    record['req_fees'] = order.fees
    record['req_fixed_fees'] = order.fixed_fees
    record['req_slippage'] = order.slippage
    record['req_min_size'] = order.min_size
    record['req_max_size'] = order.max_size
    record['req_size_granularity'] = order.size_granularity
    record['req_reject_prob'] = order.reject_prob
    record['req_lock_cash'] = order.lock_cash
    record['req_allow_partial'] = order.allow_partial
    record['req_raise_reject'] = order.raise_reject
    record['req_log'] = order.log
    record['new_cash'] = new_cash
    record['new_position'] = new_position
    record['new_debt'] = new_debt
    record['new_free_cash'] = new_free_cash
    record['new_val_price'] = new_val_price
    record['new_value'] = new_value
    record['res_size'] = order_result.size
    record['res_price'] = order_result.price
    record['res_fees'] = order_result.fees
    record['res_side'] = order_result.side
    record['res_status'] = order_result.status
    record['res_status_info'] = order_result.status_info
    record['order_id'] = order_id


@njit(cache=True)
def fill_order_record_nb(record: tp.Record,
                         record_id: int,
                         i: int,
                         col: int,
                         order_result: OrderResult) -> None:
    """Fill an order record."""

    record['id'] = record_id
    record['col'] = col
    record['idx'] = i
    record['size'] = order_result.size
    record['price'] = order_result.price
    record['fees'] = order_result.fees
    record['side'] = order_result.side


@njit(cache=True)
def raise_rejected_order_nb(order_result: OrderResult) -> None:
    """Raise an `vectorbt.portfolio.enums.RejectedOrderError`."""

    if order_result.status_info == OrderStatusInfo.SizeNaN:
        raise RejectedOrderError("Size is NaN")
    if order_result.status_info == OrderStatusInfo.PriceNaN:
        raise RejectedOrderError("Price is NaN")
    if order_result.status_info == OrderStatusInfo.ValPriceNaN:
        raise RejectedOrderError("Asset valuation price is NaN")
    if order_result.status_info == OrderStatusInfo.ValueNaN:
        raise RejectedOrderError("Asset/group value is NaN")
    if order_result.status_info == OrderStatusInfo.ValueZeroNeg:
        raise RejectedOrderError("Asset/group value is zero or negative")
    if order_result.status_info == OrderStatusInfo.SizeZero:
        raise RejectedOrderError("Size is zero")
    if order_result.status_info == OrderStatusInfo.NoCashShort:
        raise RejectedOrderError("Not enough cash to short")
    if order_result.status_info == OrderStatusInfo.NoCashLong:
        raise RejectedOrderError("Not enough cash to long")
    if order_result.status_info == OrderStatusInfo.NoOpenPosition:
        raise RejectedOrderError("No open position to reduce/close")
    if order_result.status_info == OrderStatusInfo.MaxSizeExceeded:
        raise RejectedOrderError("Size is greater than maximum allowed")
    if order_result.status_info == OrderStatusInfo.RandomEvent:
        raise RejectedOrderError("Random event happened")
    if order_result.status_info == OrderStatusInfo.CantCoverFees:
        raise RejectedOrderError("Not enough cash to cover fees")
    if order_result.status_info == OrderStatusInfo.MinSizeNotReached:
        raise RejectedOrderError("Final size is less than minimum allowed")
    if order_result.status_info == OrderStatusInfo.PartialFill:
        raise RejectedOrderError("Final size is less than requested")
    raise RejectedOrderError


@njit(cache=True)
def update_value_nb(cash_before: float,
                    cash_now: float,
                    position_before: float,
                    position_now: float,
                    val_price_before: float,
                    price: float,
                    value_before: float) -> tp.Tuple[float, float]:
    """Update valuation price and value."""
    val_price_now = price
    cash_flow = cash_now - cash_before
    if position_before != 0:
        asset_value_before = position_before * val_price_before
    else:
        asset_value_before = 0.
    if position_now != 0:
        asset_value_now = position_now * val_price_now
    else:
        asset_value_now = 0.
    asset_value_diff = asset_value_now - asset_value_before
    value_now = value_before + cash_flow + asset_value_diff
    return val_price_now, value_now


@njit(cache=True)
def process_order_nb(i: int,
                     col: int,
                     group: int,
                     state: ProcessOrderState,
                     update_value: bool,
                     order: Order,
                     order_records: tp.RecordArray,
                     log_records: tp.RecordArray) -> tp.Tuple[OrderResult, ProcessOrderState]:
    """Process an order by executing it, saving relevant information to the logs, and returning a new state."""

    # Execute the order
    exec_state, order_result = execute_order_nb(state, order)

    # Raise if order rejected
    is_rejected = order_result.status == OrderStatus.Rejected
    if is_rejected and order.raise_reject:
        raise_rejected_order_nb(order_result)

    # Update valuation price and value
    is_filled = order_result.status == OrderStatus.Filled
    if is_filled and update_value:
        new_val_price, new_value = update_value_nb(
            state.cash,
            exec_state.cash,
            state.position,
            exec_state.position,
            state.val_price,
            order_result.price,
            state.value
        )
    else:
        new_val_price = state.val_price
        new_value = state.value

    new_oidx = state.oidx
    if is_filled:
        # Fill order record
        if state.oidx > len(order_records) - 1:
            raise IndexError("order_records index out of range. Set a higher max_orders.")
        fill_order_record_nb(
            order_records[state.oidx],
            state.oidx,
            i,
            col,
            order_result
        )
        new_oidx += 1

    new_lidx = state.lidx
    if order.log:
        # Fill log record
        if state.lidx > len(log_records) - 1:
            raise IndexError("log_records index out of range. Set a higher max_logs.")
        fill_log_record_nb(
            log_records[state.lidx],
            state.lidx,
            i,
            col,
            group,
            state.cash,
            state.position,
            state.debt,
            state.free_cash,
            state.val_price,
            state.value,
            order,
            exec_state.cash,
            exec_state.position,
            exec_state.debt,
            exec_state.free_cash,
            new_val_price,
            new_value,
            order_result,
            state.oidx if is_filled else -1
        )
        new_lidx += 1

    # Create new state
    new_state = ProcessOrderState(
        cash=exec_state.cash,
        position=exec_state.position,
        debt=exec_state.debt,
        free_cash=exec_state.free_cash,
        val_price=new_val_price,
        value=new_value,
        oidx=new_oidx,
        lidx=new_lidx
    )

    return order_result, new_state


@njit(cache=True)
def order_nb(size: float = np.nan,
             price: float = np.inf,
             size_type: int = SizeType.Amount,
             direction: int = Direction.Both,
             fees: float = 0.,
             fixed_fees: float = 0.,
             slippage: float = 0.,
             min_size: float = 0.,
             max_size: float = np.inf,
             size_granularity: float = np.nan,
             reject_prob: float = 0.,
             lock_cash: bool = False,
             allow_partial: bool = True,
             raise_reject: bool = False,
             log: bool = False) -> Order:
    """Create an order.

    See `vectorbt.portfolio.enums.Order` for details on arguments."""

    return Order(
        size=float(size),
        price=float(price),
        size_type=int(size_type),
        direction=int(direction),
        fees=float(fees),
        fixed_fees=float(fixed_fees),
        slippage=float(slippage),
        min_size=float(min_size),
        max_size=float(max_size),
        size_granularity=float(size_granularity),
        reject_prob=float(reject_prob),
        lock_cash=bool(lock_cash),
        allow_partial=bool(allow_partial),
        raise_reject=bool(raise_reject),
        log=bool(log)
    )


@njit(cache=True)
def close_position_nb(price: float = np.inf,
                      fees: float = 0.,
                      fixed_fees: float = 0.,
                      slippage: float = 0.,
                      min_size: float = 0.,
                      max_size: float = np.inf,
                      size_granularity: float = np.nan,
                      reject_prob: float = 0.,
                      lock_cash: bool = False,
                      allow_partial: bool = True,
                      raise_reject: bool = False,
                      log: bool = False) -> Order:
    """Close the current position."""

    return order_nb(
        size=0.,
        price=price,
        size_type=SizeType.TargetAmount,
        direction=Direction.Both,
        fees=fees,
        fixed_fees=fixed_fees,
        slippage=slippage,
        min_size=min_size,
        max_size=max_size,
        size_granularity=size_granularity,
        reject_prob=reject_prob,
        lock_cash=lock_cash,
        allow_partial=allow_partial,
        raise_reject=raise_reject,
        log=log
    )


@njit(cache=True)
def order_nothing_nb() -> Order:
    """Convenience function to order nothing."""
    return NoOrder


# ############# Checks ############# #


@njit(cache=True)
def check_group_lens_nb(group_lens: tp.Array1d, n_cols: int) -> None:
    """Check `group_lens`."""
    if np.sum(group_lens) != n_cols:
        raise ValueError("group_lens has incorrect total number of columns")


@njit(cache=True)
def check_group_init_cash_nb(group_lens: tp.Array1d, n_cols: int, init_cash: tp.Array1d, cash_sharing: bool) -> None:
    """Check `init_cash`."""
    if cash_sharing:
        if len(init_cash) != len(group_lens):
            raise ValueError("If cash sharing is enabled, init_cash must match the number of groups")
    else:
        if len(init_cash) != n_cols:
            raise ValueError("If cash sharing is disabled, init_cash must match the number of columns")


@njit(cache=True)
def is_grouped_nb(group_lens: tp.Array1d) -> bool:
    """Check if columm,ns are grouped, that is, more than one column per group."""
    return np.any(group_lens > 1)


# ############# Call sequence ############# #


@njit(cache=True)
def shuffle_call_seq_nb(call_seq: tp.Array2d, group_lens: tp.Array1d) -> None:
    """Shuffle the call sequence array."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        for i in range(call_seq.shape[0]):
            np.random.shuffle(call_seq[i, from_col:to_col])
        from_col = to_col


@njit(cache=True)
def build_call_seq_nb(target_shape: tp.Shape,
                      group_lens: tp.Array1d,
                      call_seq_type: int = CallSeqType.Default) -> tp.Array2d:
    """Build a new call sequence array."""
    if call_seq_type == CallSeqType.Reversed:
        out = np.full(target_shape[1], 1, dtype=np.int64)
        out[np.cumsum(group_lens)[1:] - group_lens[1:] - 1] -= group_lens[1:]
        out = np.cumsum(out[::-1])[::-1] - 1
        out = out * np.ones((target_shape[0], 1), dtype=np.int64)
        return out
    out = np.full(target_shape[1], 1, dtype=np.int64)
    out[np.cumsum(group_lens)[:-1]] -= group_lens[:-1]
    out = np.cumsum(out) - 1
    out = out * np.ones((target_shape[0], 1), dtype=np.int64)
    if call_seq_type == CallSeqType.Random:
        shuffle_call_seq_nb(out, group_lens)
    return out


def require_call_seq(call_seq: tp.Array2d) -> tp.Array2d:
    """Force the call sequence array to pass our requirements."""
    return np.require(call_seq, dtype=np.int64, requirements=['A', 'O', 'W', 'F'])


def build_call_seq(target_shape: tp.Shape,
                   group_lens: tp.Array1d,
                   call_seq_type: int = CallSeqType.Default) -> tp.Array2d:
    """Not compiled but faster version of `build_call_seq_nb`."""
    call_seq = np.full(target_shape[1], 1, dtype=np.int64)
    if call_seq_type == CallSeqType.Reversed:
        call_seq[np.cumsum(group_lens)[1:] - group_lens[1:] - 1] -= group_lens[1:]
        call_seq = np.cumsum(call_seq[::-1])[::-1] - 1
    else:
        call_seq[np.cumsum(group_lens[:-1])] -= group_lens[:-1]
        call_seq = np.cumsum(call_seq) - 1
    call_seq = np.broadcast_to(call_seq, target_shape)
    if call_seq_type == CallSeqType.Random:
        call_seq = require_call_seq(call_seq)
        shuffle_call_seq_nb(call_seq, group_lens)
    return require_call_seq(call_seq)


# ############# Helper functions ############# #

@njit(cache=True)
def get_col_elem_nb(ctx: tp.Union[RowContext, SegmentContext, FlexOrderContext], col: int,
                    a: tp.ArrayLike) -> tp.Scalar:
    """Get the current element using flexible indexing given the context and the column."""
    return flex_select_auto_nb(a, ctx.i, col, ctx.flex_2d)


@njit(cache=True)
def get_elem_nb(ctx: tp.Union[OrderContext, PostOrderContext, SignalContext],
                a: tp.ArrayLike) -> tp.Scalar:
    """Get the current element using flexible indexing given just the context."""
    return flex_select_auto_nb(a, ctx.i, ctx.col, ctx.flex_2d)


@njit(cache=True)
def get_group_value_nb(from_col: int,
                       to_col: int,
                       cash_now: float,
                       last_position: tp.Array1d,
                       last_val_price: tp.Array1d) -> float:
    """Get group value."""
    group_value = cash_now
    group_len = to_col - from_col
    for k in range(group_len):
        col = from_col + k
        if last_position[col] != 0:
            group_value += last_position[col] * last_val_price[col]
    return group_value


@njit(cache=True)
def get_group_value_ctx_nb(seg_ctx: SegmentContext) -> float:
    """Get group value from context.

    Accepts `vectorbt.portfolio.enums.SegmentContext`.

    Best called once from `pre_segment_func_nb`.
    To set the valuation price, change `last_val_price` of the context in-place.

    !!! note
        Cash sharing must be enabled."""
    if not seg_ctx.cash_sharing:
        raise ValueError("Cash sharing must be enabled")
    return get_group_value_nb(
        seg_ctx.from_col,
        seg_ctx.to_col,
        seg_ctx.last_cash[seg_ctx.group],
        seg_ctx.last_position,
        seg_ctx.last_val_price
    )


@njit(cache=True)
def approx_order_value_nb(size: float,
                          size_type: int,
                          direction: int,
                          cash_now: float,
                          position_now: float,
                          free_cash_now: float,
                          val_price_now: float,
                          value_now: float) -> float:
    """Approximate value of an order."""
    if direction == Direction.ShortOnly:
        size *= -1
    asset_value_now = position_now * val_price_now
    if size_type == SizeType.Amount:
        return size * val_price_now
    if size_type == SizeType.Value:
        return size
    if size_type == SizeType.Percent:
        if size >= 0:
            return size * cash_now
        else:
            if direction == Direction.LongOnly:
                return size * asset_value_now
            return size * (2 * max(asset_value_now, 0) + max(free_cash_now, 0))
    if size_type == SizeType.TargetAmount:
        return size * val_price_now - asset_value_now
    if size_type == SizeType.TargetValue:
        return size - asset_value_now
    if size_type == SizeType.TargetPercent:
        return size * value_now - asset_value_now
    return np.nan


@njit(cache=True)
def sort_call_seq_out_nb(ctx: SegmentContext,
                         size: tp.ArrayLike,
                         size_type: tp.ArrayLike,
                         direction: tp.ArrayLike,
                         order_value_out: tp.Array1d,
                         call_seq_out: tp.Array1d,
                         ctx_select: bool = True) -> None:
    """Sort call sequence `call_seq_out` based on the value of each potential order.

    Accepts `vectorbt.portfolio.enums.SegmentContext` and other arguments, sorts `call_seq_out` in place,
    and returns nothing.

    Arrays `size`, `size_type`, and `direction` utilize flexible indexing.
    If `ctx_select` is True, selects the elements of each `size`, `size_type`, and `direction`
    using `get_col_elem_nb` assuming that each array can broadcast to `target_shape`.
    Otherwise, selects using `vectorbt.base.reshape_fns.flex_select_auto_nb` assuming that each array
    can broadcast to `group_len`.

    The lengths of `order_value_out` and `call_seq_out` should match the number of columns in the group.
    Array `order_value_out` should be empty and will contain sorted order values after execution.
    Array `call_seq_out` should be filled with integers ranging from 0 to the number of columns in the group
    (in this exact order).

    Best called once from `pre_segment_func_nb`.

    !!! note
        Cash sharing must be enabled and `call_seq_out` should follow `CallSeqType.Default`.

        Should be used in flexible simulation functions."""
    if not ctx.cash_sharing:
        raise ValueError("Cash sharing must be enabled")
    size_arr = np.asarray(size)
    size_type_arr = np.asarray(size_type)
    direction_arr = np.asarray(direction)

    group_value_now = get_group_value_ctx_nb(ctx)
    group_len = ctx.to_col - ctx.from_col
    for k in range(group_len):
        if call_seq_out[k] != k:
            raise ValueError("call_seq_out should follow CallSeqType.Default")
        col = ctx.from_col + k
        if ctx_select:
            _size = get_col_elem_nb(ctx, col, size_arr)
            _size_type = get_col_elem_nb(ctx, col, size_type_arr)
            _direction = get_col_elem_nb(ctx, col, direction_arr)
        else:
            _size = flex_select_auto_nb(size_arr, k, 0, False)
            _size_type = flex_select_auto_nb(size_type_arr, k, 0, False)
            _direction = flex_select_auto_nb(direction_arr, k, 0, False)
        if ctx.cash_sharing:
            cash_now = ctx.last_cash[ctx.group]
            free_cash_now = ctx.last_free_cash[ctx.group]
        else:
            cash_now = ctx.last_cash[col]
            free_cash_now = ctx.last_free_cash[col]
        order_value_out[k] = approx_order_value_nb(
            _size,
            _size_type,
            _direction,
            cash_now,
            ctx.last_position[col],
            free_cash_now,
            ctx.last_val_price[col],
            group_value_now
        )
    # Sort by order value
    insert_argsort_nb(order_value_out, call_seq_out)


@njit(cache=True)
def sort_call_seq_nb(ctx: SegmentContext,
                     size: tp.ArrayLike,
                     size_type: tp.ArrayLike,
                     direction: tp.ArrayLike,
                     order_value_out: tp.Array1d,
                     ctx_select: bool = True) -> None:
    """Sort call sequence attached to `vectorbt.portfolio.enums.SegmentContext`.

    See `sort_call_seq_out_nb`.

    !!! note
        Can only be used in non-flexible simulation functions."""
    if ctx.call_seq_now is None:
        raise ValueError("Call sequence array is None. Use sort_call_seq_out_nb to sort a custom array.")
    sort_call_seq_out_nb(
        ctx,
        size,
        size_type,
        direction,
        order_value_out,
        ctx.call_seq_now,
        ctx_select=ctx_select
    )


@njit(cache=True)
def replace_inf_price_nb(prev_close: float, close: float, order: Order) -> Order:
    """Replace infinity price in an order."""
    order_price = order.price
    if order_price > 0:
        order_price = close  # upper bound is close
    else:
        order_price = prev_close  # lower bound is prev close
    return order_nb(
        size=order.size,
        price=order_price,
        size_type=order.size_type,
        direction=order.direction,
        fees=order.fees,
        fixed_fees=order.fixed_fees,
        slippage=order.slippage,
        min_size=order.min_size,
        max_size=order.max_size,
        size_granularity=order.size_granularity,
        reject_prob=order.reject_prob,
        lock_cash=order.lock_cash,
        allow_partial=order.allow_partial,
        raise_reject=order.raise_reject,
        log=order.log
    )


@njit(cache=True)
def try_order_nb(ctx: OrderContext, order: Order) -> tp.Tuple[ExecuteOrderState, OrderResult]:
    """Execute an order without persistence."""
    state = ProcessOrderState(
        cash=ctx.cash_now,
        position=ctx.position_now,
        debt=ctx.debt_now,
        free_cash=ctx.free_cash_now,
        val_price=ctx.val_price_now,
        value=ctx.value_now,
        oidx=-1,
        lidx=-1
    )
    if np.isinf(order.price):
        if ctx.i > 0:
            prev_close = flex_select_auto_nb(ctx.close, ctx.i - 1, ctx.col, ctx.flex_2d)
        else:
            prev_close = np.nan
        close = flex_select_auto_nb(ctx.close, ctx.i, ctx.col, ctx.flex_2d)
        order = replace_inf_price_nb(prev_close, close, order)
    return execute_order_nb(state, order)


@njit(cache=True)
def init_records_nb(target_shape: tp.Shape,
                    max_orders: tp.Optional[int] = None,
                    max_logs: int = 0) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Initialize order and log records."""
    if max_orders is None:
        _max_orders = target_shape[0] * target_shape[1]
    else:
        _max_orders = max_orders
    order_records = np.empty(_max_orders, dtype=order_dt)
    if max_logs == 0:
        max_logs = 1
    log_records = np.empty(max_logs, dtype=log_dt)
    return order_records, log_records


@njit(cache=True)
def update_open_pos_stats_nb(record: tp.Record, position_now: float, price: float) -> None:
    """Update statistics of an open position record using custom price."""
    if record['id'] >= 0 and record['status'] == TradeStatus.Open:
        if np.isnan(record['exit_price']):
            exit_price = price
        else:
            exit_size_sum = record['size'] - abs(position_now)
            exit_gross_sum = exit_size_sum * record['exit_price']
            exit_gross_sum += abs(position_now) * price
            exit_price = exit_gross_sum / record['size']
        pnl, ret = get_trade_stats_nb(
            record['size'],
            record['entry_price'],
            record['entry_fees'],
            exit_price,
            record['exit_fees'],
            record['direction']
        )
        record['pnl'] = pnl
        record['return'] = ret


@njit(cache=True)
def update_pos_record_nb(record: tp.Record,
                         i: int,
                         col: int,
                         position_before: float,
                         position_now: float,
                         order_result: OrderResult) -> None:
    """Update position record after filling an order."""
    if order_result.status == OrderStatus.Filled:
        if position_before == 0 and position_now != 0:
            # New position opened
            record['id'] += 1
            record['col'] = col
            record['size'] = order_result.size
            record['entry_idx'] = i
            record['entry_price'] = order_result.price
            record['entry_fees'] = order_result.fees
            record['exit_idx'] = -1
            record['exit_price'] = np.nan
            record['exit_fees'] = 0.
            if order_result.side == OrderSide.Buy:
                record['direction'] = TradeDirection.Long
            else:
                record['direction'] = TradeDirection.Short
            record['status'] = TradeStatus.Open
            record['parent_id'] = record['id']
        elif position_before != 0 and position_now == 0:
            # Position closed
            record['exit_idx'] = i
            if np.isnan(record['exit_price']):
                exit_price = order_result.price
            else:
                exit_size_sum = record['size'] - abs(position_before)
                exit_gross_sum = exit_size_sum * record['exit_price']
                exit_gross_sum += abs(position_before) * order_result.price
                exit_price = exit_gross_sum / record['size']
            record['exit_price'] = exit_price
            record['exit_fees'] += order_result.fees
            pnl, ret = get_trade_stats_nb(
                record['size'],
                record['entry_price'],
                record['entry_fees'],
                record['exit_price'],
                record['exit_fees'],
                record['direction']
            )
            record['pnl'] = pnl
            record['return'] = ret
            record['status'] = TradeStatus.Closed
        elif np.sign(position_before) != np.sign(position_now):
            # Position reversed
            record['id'] += 1
            record['size'] = abs(position_now)
            record['entry_idx'] = i
            record['entry_price'] = order_result.price
            new_pos_fraction = abs(position_now) / abs(position_now - position_before)
            record['entry_fees'] = new_pos_fraction * order_result.fees
            record['exit_idx'] = -1
            record['exit_price'] = np.nan
            record['exit_fees'] = 0.
            if order_result.side == OrderSide.Buy:
                record['direction'] = TradeDirection.Long
            else:
                record['direction'] = TradeDirection.Short
            record['status'] = TradeStatus.Open
            record['parent_id'] = record['id']
        else:
            # Position changed
            if abs(position_before) <= abs(position_now):
                # Position increased
                entry_gross_sum = record['size'] * record['entry_price']
                entry_gross_sum += order_result.size * order_result.price
                entry_price = entry_gross_sum / (record['size'] + order_result.size)
                record['entry_price'] = entry_price
                record['entry_fees'] += order_result.fees
                record['size'] += order_result.size
            else:
                # Position decreased
                if np.isnan(record['exit_price']):
                    exit_price = order_result.price
                else:
                    exit_size_sum = record['size'] - abs(position_before)
                    exit_gross_sum = exit_size_sum * record['exit_price']
                    exit_gross_sum += order_result.size * order_result.price
                    exit_price = exit_gross_sum / (exit_size_sum + order_result.size)
                record['exit_price'] = exit_price
                record['exit_fees'] += order_result.fees

        # Update open position stats
        update_open_pos_stats_nb(
            record,
            position_now,
            order_result.price
        )


# ############# Simulation ############# #


@njit(cache=True)
def simulate_from_orders_nb(target_shape: tp.Shape,
                            group_lens: tp.Array1d,
                            init_cash: tp.Array1d,
                            call_seq: tp.Array2d,
                            size: tp.ArrayLike = np.asarray(np.inf),
                            price: tp.ArrayLike = np.asarray(np.inf),
                            size_type: tp.ArrayLike = np.asarray(SizeType.Amount),
                            direction: tp.ArrayLike = np.asarray(Direction.Both),
                            fees: tp.ArrayLike = np.asarray(0.),
                            fixed_fees: tp.ArrayLike = np.asarray(0.),
                            slippage: tp.ArrayLike = np.asarray(0.),
                            min_size: tp.ArrayLike = np.asarray(0.),
                            max_size: tp.ArrayLike = np.asarray(np.inf),
                            size_granularity: tp.ArrayLike = np.asarray(np.nan),
                            reject_prob: tp.ArrayLike = np.asarray(0.),
                            lock_cash: tp.ArrayLike = np.asarray(False),
                            allow_partial: tp.ArrayLike = np.asarray(True),
                            raise_reject: tp.ArrayLike = np.asarray(False),
                            log: tp.ArrayLike = np.asarray(False),
                            val_price: tp.ArrayLike = np.asarray(np.inf),
                            close: tp.ArrayLike = np.asarray(np.nan),
                            auto_call_seq: bool = False,
                            ffill_val_price: bool = True,
                            update_value: bool = False,
                            max_orders: tp.Optional[int] = None,
                            max_logs: int = 0,
                            flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Creates on order out of each element.

    Iterates in the column-major order.
    Utilizes flexible broadcasting.

    !!! note
        Should be only grouped if cash sharing is enabled.

        If `auto_call_seq` is True, make sure that `call_seq` follows `CallSeqType.Default`.

        Single value should be passed as a 0-dim array (for example, by using `np.asarray(value)`).

    Usage:
        * Buy and hold using all cash and closing price (default):

        ```pycon
        >>> import numpy as np
        >>> from vectorbt.records.nb import col_map_nb
        >>> from vectorbt.portfolio.nb import simulate_from_orders_nb, asset_flow_nb
        >>> from vectorbt.portfolio.enums import Direction

        >>> close = np.array([1, 2, 3, 4, 5])[:, None]
        >>> order_records, _ = simulate_from_orders_nb(
        ...     target_shape=close.shape,
        ...     close=close,
        ...     group_lens=np.array([1]),
        ...     init_cash=np.array([100]),
        ...     call_seq=np.full(close.shape, 0)
        ... )
        >>> col_map = col_map_nb(order_records['col'], close.shape[1])
        >>> asset_flow = asset_flow_nb(close.shape, order_records, col_map, Direction.Both)
        >>> asset_flow
        array([[100.],
               [  0.],
               [  0.],
               [  0.],
               [  0.]])
        ```
    """
    check_group_lens_nb(group_lens, target_shape[1])
    cash_sharing = is_grouped_nb(group_lens)
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    order_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    temp_order_value = np.empty(target_shape[1], dtype=np.float64)
    oidx = 0
    lidx = 0

    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        cash_now = init_cash[group]
        free_cash_now = init_cash[group]

        for i in range(target_shape[0]):
            for k in range(group_len):
                col = from_col + k

                # Resolve order price
                _price = flex_select_auto_nb(price, i, col, flex_2d)
                if np.isinf(_price):
                    if _price > 0:
                        _price = flex_select_auto_nb(close, i, col, flex_2d)  # upper bound is close
                    elif i > 0:
                        _price = flex_select_auto_nb(close, i - 1, col, flex_2d)  # lower bound is prev close
                    else:
                        _price = np.nan  # first timestamp has no prev close
                order_price[col] = _price

                # Resolve valuation price
                _val_price = flex_select_auto_nb(val_price, i, col, flex_2d)
                if np.isinf(_val_price):
                    if _val_price > 0:
                        _val_price = _price  # upper bound is order price
                    elif i > 0:
                        _val_price = flex_select_auto_nb(close, i - 1, col, flex_2d)  # lower bound is prev close
                    else:
                        _val_price = np.nan  # first timestamp has no prev close
                if not np.isnan(_val_price) or not ffill_val_price:
                    last_val_price[col] = _val_price

            # Calculate group value and rearrange if cash sharing is enabled
            if cash_sharing:
                # Same as get_group_value_ctx_nb but with flexible indexing
                value_now = cash_now
                for k in range(group_len):
                    col = from_col + k

                    if last_position[col] != 0:
                        value_now += last_position[col] * last_val_price[col]

                # Dynamically sort by order value -> selling comes first to release funds early
                if auto_call_seq:
                    # Same as sort_by_order_value_ctx_nb but with flexible indexing
                    for k in range(group_len):
                        col = from_col + k
                        temp_order_value[k] = approx_order_value_nb(
                            flex_select_auto_nb(size, i, col, flex_2d),
                            flex_select_auto_nb(size_type, i, col, flex_2d),
                            flex_select_auto_nb(direction, i, col, flex_2d),
                            cash_now,
                            last_position[col],
                            free_cash_now,
                            last_val_price[col],
                            value_now
                        )

                    # Sort by order value
                    insert_argsort_nb(temp_order_value[:group_len], call_seq[i, from_col:to_col])

            for k in range(group_len):
                col = from_col + k
                if cash_sharing:
                    col_i = call_seq[i, col]
                    if col_i >= group_len:
                        raise ValueError("Call index exceeds bounds of the group")
                    col = from_col + col_i

                # Get current values per column
                position_now = last_position[col]
                debt_now = last_debt[col]
                val_price_now = last_val_price[col]
                if not cash_sharing:
                    value_now = cash_now
                    if position_now != 0:
                        value_now += position_now * val_price_now

                # Generate the next order
                order = order_nb(
                    size=flex_select_auto_nb(size, i, col, flex_2d),
                    price=order_price[col],
                    size_type=flex_select_auto_nb(size_type, i, col, flex_2d),
                    direction=flex_select_auto_nb(direction, i, col, flex_2d),
                    fees=flex_select_auto_nb(fees, i, col, flex_2d),
                    fixed_fees=flex_select_auto_nb(fixed_fees, i, col, flex_2d),
                    slippage=flex_select_auto_nb(slippage, i, col, flex_2d),
                    min_size=flex_select_auto_nb(min_size, i, col, flex_2d),
                    max_size=flex_select_auto_nb(max_size, i, col, flex_2d),
                    size_granularity=flex_select_auto_nb(size_granularity, i, col, flex_2d),
                    reject_prob=flex_select_auto_nb(reject_prob, i, col, flex_2d),
                    lock_cash=flex_select_auto_nb(lock_cash, i, col, flex_2d),
                    allow_partial=flex_select_auto_nb(allow_partial, i, col, flex_2d),
                    raise_reject=flex_select_auto_nb(raise_reject, i, col, flex_2d),
                    log=flex_select_auto_nb(log, i, col, flex_2d)
                )

                # Process the order
                state = ProcessOrderState(
                    cash=cash_now,
                    position=position_now,
                    debt=debt_now,
                    free_cash=free_cash_now,
                    val_price=val_price_now,
                    value=value_now,
                    oidx=oidx,
                    lidx=lidx
                )

                order_result, new_state = process_order_nb(
                    i, col, group,
                    state,
                    update_value,
                    order,
                    order_records,
                    log_records
                )

                # Update state
                cash_now = new_state.cash
                position_now = new_state.position
                debt_now = new_state.debt
                free_cash_now = new_state.free_cash
                val_price_now = new_state.val_price
                value_now = new_state.value
                oidx = new_state.oidx
                lidx = new_state.lidx

                # Now becomes last
                last_position[col] = position_now
                last_debt[col] = debt_now
                if not np.isnan(val_price_now) or not ffill_val_price:
                    last_val_price[col] = val_price_now

        from_col = to_col

    return order_records[:oidx], log_records[:lidx]


@njit(cache=True)
def generate_stop_signal_nb(position_now: float,
                            upon_stop_exit: int,
                            accumulate: int) -> tp.Tuple[bool, bool, bool, bool, int]:
    """Generate stop signal and change accumulation if needed."""
    is_long_entry = False
    is_long_exit = False
    is_short_entry = False
    is_short_exit = False
    if position_now > 0:
        if upon_stop_exit == StopExitMode.Close:
            is_long_exit = True
            accumulate = AccumulationMode.Disabled
        elif upon_stop_exit == StopExitMode.CloseReduce:
            is_long_exit = True
        elif upon_stop_exit == StopExitMode.Reverse:
            is_short_entry = True
            accumulate = AccumulationMode.Disabled
        else:
            is_short_entry = True
    elif position_now < 0:
        if upon_stop_exit == StopExitMode.Close:
            is_short_exit = True
            accumulate = AccumulationMode.Disabled
        elif upon_stop_exit == StopExitMode.CloseReduce:
            is_short_exit = True
        elif upon_stop_exit == StopExitMode.Reverse:
            is_long_entry = True
            accumulate = AccumulationMode.Disabled
        else:
            is_long_entry = True
    return is_long_entry, is_long_exit, is_short_entry, is_short_exit, accumulate


@njit(cache=True)
def resolve_stop_price_and_slippage_nb(stop_price: float,
                                       price: float,
                                       close: float,
                                       slippage: float,
                                       stop_exit_price: int) -> tp.Tuple[float, float]:
    """Resolve price and slippage of a stop order."""
    if stop_exit_price == StopExitPrice.StopMarket:
        return stop_price, slippage
    elif stop_exit_price == StopExitPrice.StopLimit:
        return stop_price, 0.
    elif stop_exit_price == StopExitPrice.Close:
        return close, slippage
    return price, slippage


@njit(cache=True)
def resolve_signal_conflict_nb(position_now: float,
                               is_entry: bool,
                               is_exit: bool,
                               direction: int,
                               conflict_mode: int) -> tp.Tuple[bool, bool]:
    """Resolve any conflict between an entry and an exit."""
    if is_entry and is_exit:
        # Conflict
        if conflict_mode == ConflictMode.Entry:
            # Ignore exit signal
            is_exit = False
        elif conflict_mode == ConflictMode.Exit:
            # Ignore entry signal
            is_entry = False
        elif conflict_mode == ConflictMode.Adjacent:
            # Take the signal adjacent to the position we are in
            if position_now == 0:
                # Cannot decide -> ignore
                is_entry = False
                is_exit = False
            else:
                if direction == Direction.Both:
                    if position_now > 0:
                        is_exit = False
                    elif position_now < 0:
                        is_entry = False
                else:
                    is_exit = False
        elif conflict_mode == ConflictMode.Opposite:
            # Take the signal opposite to the position we are in
            if position_now == 0:
                # Cannot decide -> ignore
                is_entry = False
                is_exit = False
            else:
                if direction == Direction.Both:
                    if position_now > 0:
                        is_entry = False
                    elif position_now < 0:
                        is_exit = False
                else:
                    is_entry = False
        else:
            is_entry = False
            is_exit = False
    return is_entry, is_exit


@njit(cache=True)
def resolve_dir_conflict_nb(position_now: float,
                            is_long_entry: bool,
                            is_short_entry: bool,
                            upon_dir_conflict: int) -> tp.Tuple[bool, bool]:
    """Resolve any direction conflict between a long entry and a short entry."""
    if is_long_entry and is_short_entry:
        if upon_dir_conflict == DirectionConflictMode.Long:
            is_short_entry = False
        elif upon_dir_conflict == DirectionConflictMode.Short:
            is_long_entry = False
        elif upon_dir_conflict == DirectionConflictMode.Adjacent:
            if position_now > 0:
                is_short_entry = False
            elif position_now < 0:
                is_long_entry = False
            else:
                is_long_entry = False
                is_short_entry = False
        elif upon_dir_conflict == DirectionConflictMode.Opposite:
            if position_now > 0:
                is_long_entry = False
            elif position_now < 0:
                is_short_entry = False
            else:
                is_long_entry = False
                is_short_entry = False
        else:
            is_long_entry = False
            is_short_entry = False
    return is_long_entry, is_short_entry


@njit(cache=True)
def resolve_opposite_entry_nb(position_now: float,
                              is_long_entry: bool,
                              is_long_exit: bool,
                              is_short_entry: bool,
                              is_short_exit: bool,
                              upon_opposite_entry: int,
                              accumulate: int) -> tp.Tuple[bool, bool, bool, bool, int]:
    """Resolve opposite entry."""
    if position_now > 0 and is_short_entry:
        if upon_opposite_entry == OppositeEntryMode.Ignore:
            is_short_entry = False
        elif upon_opposite_entry == OppositeEntryMode.Close:
            is_short_entry = False
            is_long_exit = True
            accumulate = AccumulationMode.Disabled
        elif upon_opposite_entry == OppositeEntryMode.CloseReduce:
            is_short_entry = False
            is_long_exit = True
        elif upon_opposite_entry == OppositeEntryMode.Reverse:
            accumulate = AccumulationMode.Disabled
    if position_now < 0 and is_long_entry:
        if upon_opposite_entry == OppositeEntryMode.Ignore:
            is_long_entry = False
        elif upon_opposite_entry == OppositeEntryMode.Close:
            is_long_entry = False
            is_short_exit = True
            accumulate = AccumulationMode.Disabled
        elif upon_opposite_entry == OppositeEntryMode.CloseReduce:
            is_long_entry = False
            is_short_exit = True
        elif upon_opposite_entry == OppositeEntryMode.Reverse:
            accumulate = AccumulationMode.Disabled
    return is_long_entry, is_long_exit, is_short_entry, is_short_exit, accumulate


@njit(cache=True)
def signals_to_size_nb(position_now: float,
                       is_long_entry: bool,
                       is_long_exit: bool,
                       is_short_entry: bool,
                       is_short_exit: bool,
                       size: float,
                       size_type: int,
                       accumulate: int,
                       val_price_now: float) -> tp.Tuple[float, int, int]:
    """Translate direction-aware signals into size, size type, and direction."""
    if size_type != SizeType.Amount and size_type != SizeType.Value and size_type != SizeType.Percent:
        raise ValueError("Only SizeType.Amount, SizeType.Value, and SizeType.Percent are supported")
    order_size = 0.
    direction = Direction.Both
    abs_position_now = abs(position_now)
    if is_less_nb(size, 0):
        raise ValueError("Negative size is not allowed. You must express direction using signals.")

    if position_now > 0:
        # We're in a long position
        if is_short_entry:
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.RemoveOnly:
                # Decrease the position
                order_size = -size
            else:
                # Reverse the position
                order_size = -abs_position_now
                if not np.isnan(size):
                    if size_type == SizeType.Percent:
                        raise ValueError(
                            "SizeType.Percent does not support position reversal using signals")
                    if size_type == SizeType.Value:
                        order_size -= size / val_price_now
                    else:
                        order_size -= size
                size_type = SizeType.Amount
        elif is_long_exit:
            direction = Direction.LongOnly
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.RemoveOnly:
                # Decrease the position
                order_size = -size
            else:
                # Close the position
                order_size = -abs_position_now
                size_type = SizeType.Amount
        elif is_long_entry:
            direction = Direction.LongOnly
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.AddOnly:
                # Increase the position
                order_size = size
    elif position_now < 0:
        # We're in a short position
        if is_long_entry:
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.RemoveOnly:
                # Decrease the position
                order_size = size
            else:
                # Reverse the position
                order_size = abs_position_now
                if not np.isnan(size):
                    if size_type == SizeType.Percent:
                        raise ValueError("SizeType.Percent does not support position reversal using signals")
                    if size_type == SizeType.Value:
                        order_size += size / val_price_now
                    else:
                        order_size += size
                size_type = SizeType.Amount
        elif is_short_exit:
            direction = Direction.ShortOnly
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.RemoveOnly:
                # Decrease the position
                order_size = size
            else:
                # Close the position
                order_size = abs_position_now
                size_type = SizeType.Amount
        elif is_short_entry:
            direction = Direction.ShortOnly
            if accumulate == AccumulationMode.Both or accumulate == AccumulationMode.AddOnly:
                # Increase the position
                order_size = -size
    else:
        if is_long_entry:
            # Open long position
            order_size = size
        elif is_short_entry:
            # Open short position
            order_size = -size

    return order_size, size_type, direction


@njit(cache=True)
def should_update_stop_nb(stop: float, upon_stop_update: int) -> bool:
    """Whether to update stop."""
    if upon_stop_update == StopUpdateMode.Override or upon_stop_update == StopUpdateMode.OverrideNaN:
        if not np.isnan(stop) or upon_stop_update == StopUpdateMode.OverrideNaN:
            return True
    return False


@njit(cache=True)
def get_stop_price_nb(position_now: float,
                      stop_price: float,
                      stop: float,
                      open: float,
                      low: float,
                      high: float,
                      hit_below: bool) -> float:
    """Get stop price.

    If hit before open, returns open."""
    if stop < 0:
        raise ValueError("Stop value must be 0 or greater")
    if (position_now > 0 and hit_below) or (position_now < 0 and not hit_below):
        stop_price = stop_price * (1 - stop)
        if open <= stop_price:
            return open
        if low <= stop_price <= high:
            return stop_price
        return np.nan
    if (position_now < 0 and hit_below) or (position_now > 0 and not hit_below):
        stop_price = stop_price * (1 + stop)
        if stop_price <= open:
            return open
        if low <= stop_price <= high:
            return stop_price
        return np.nan
    return np.nan


@njit
def no_signal_func_nb(c: SignalContext, *args) -> tp.Tuple[bool, bool, bool, bool]:
    """Placeholder signal function that returns no signal."""
    return False, False, False, False


@njit
def no_adjust_sl_func_nb(c: AdjustSLContext, *args) -> tp.Tuple[float, bool]:
    """Placeholder function that returns the initial stop-loss value and trailing flag."""
    return c.curr_stop, c.curr_trail


@njit
def no_adjust_tp_func_nb(c: AdjustTPContext, *args) -> float:
    """Placeholder function that returns the initial take-profit value."""
    return c.curr_stop


SignalFuncT = tp.Callable[[SignalContext, tp.VarArg()], tp.Tuple[bool, bool, bool, bool]]
AdjustSLFuncT = tp.Callable[[AdjustSLContext, tp.VarArg()], tp.Tuple[float, bool]]
AdjustTPFuncT = tp.Callable[[AdjustTPContext, tp.VarArg()], float]


@njit
def simulate_from_signal_func_nb(target_shape: tp.Shape,
                                 group_lens: tp.Array1d,
                                 init_cash: tp.Array1d,
                                 call_seq: tp.Array2d,
                                 signal_func_nb: SignalFuncT = no_signal_func_nb,
                                 signal_args: tp.ArgsLike = (),
                                 size: tp.ArrayLike = np.asarray(np.inf),
                                 price: tp.ArrayLike = np.asarray(np.inf),
                                 size_type: tp.ArrayLike = np.asarray(SizeType.Amount),
                                 fees: tp.ArrayLike = np.asarray(0.),
                                 fixed_fees: tp.ArrayLike = np.asarray(0.),
                                 slippage: tp.ArrayLike = np.asarray(0.),
                                 min_size: tp.ArrayLike = np.asarray(0.),
                                 max_size: tp.ArrayLike = np.asarray(np.inf),
                                 size_granularity: tp.ArrayLike = np.asarray(np.nan),
                                 reject_prob: tp.ArrayLike = np.asarray(0.),
                                 lock_cash: tp.ArrayLike = np.asarray(False),
                                 allow_partial: tp.ArrayLike = np.asarray(True),
                                 raise_reject: tp.ArrayLike = np.asarray(False),
                                 log: tp.ArrayLike = np.asarray(False),
                                 accumulate: tp.ArrayLike = np.asarray(AccumulationMode.Disabled),
                                 upon_long_conflict: tp.ArrayLike = np.asarray(ConflictMode.Ignore),
                                 upon_short_conflict: tp.ArrayLike = np.asarray(ConflictMode.Ignore),
                                 upon_dir_conflict: tp.ArrayLike = np.asarray(DirectionConflictMode.Ignore),
                                 upon_opposite_entry: tp.ArrayLike = np.asarray(OppositeEntryMode.ReverseReduce),
                                 val_price: tp.ArrayLike = np.asarray(np.inf),
                                 open: tp.ArrayLike = np.asarray(np.nan),
                                 high: tp.ArrayLike = np.asarray(np.nan),
                                 low: tp.ArrayLike = np.asarray(np.nan),
                                 close: tp.ArrayLike = np.asarray(np.nan),
                                 sl_stop: tp.ArrayLike = np.asarray(np.nan),
                                 sl_trail: tp.ArrayLike = np.asarray(False),
                                 tp_stop: tp.ArrayLike = np.asarray(np.nan),
                                 stop_entry_price: tp.ArrayLike = np.asarray(StopEntryPrice.Close),
                                 stop_exit_price: tp.ArrayLike = np.asarray(StopExitPrice.StopLimit),
                                 upon_stop_exit: tp.ArrayLike = np.asarray(StopExitMode.Close),
                                 upon_stop_update: tp.ArrayLike = np.asarray(StopUpdateMode.Override),
                                 adjust_sl_func_nb: AdjustSLFuncT = no_adjust_sl_func_nb,
                                 adjust_sl_args: tp.Args = (),
                                 adjust_tp_func_nb: AdjustTPFuncT = no_adjust_tp_func_nb,
                                 adjust_tp_args: tp.Args = (),
                                 use_stops: bool = True,
                                 auto_call_seq: bool = False,
                                 ffill_val_price: bool = True,
                                 update_value: bool = False,
                                 max_orders: tp.Optional[int] = None,
                                 max_logs: int = 0,
                                 flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Creates an order out of each element by resolving entry and exit signals returned by `signal_func_nb`.

    Iterates in the column-major order. Utilizes flexible broadcasting.

    Signals are processed using the following pipeline:

    1) If there is a stop signal, convert it to direction-aware signals and proceed to 7)
    2) Get direction-aware signals using `signal_func_nb`
    3) Resolve any entry and exit conflict of each direction using `resolve_signal_conflict_nb`
    4) Resolve any direction conflict using `resolve_dir_conflict_nb`
    5) Resolve an opposite entry signal scenario using `resolve_opposite_entry_nb`
    7) Convert the final signals into size, size type, and direction using `signals_to_size_nb`

    !!! note
        Should be only grouped if cash sharing is enabled.

        If `auto_call_seq` is True, make sure that `call_seq` follows `CallSeqType.Default`.

        Single value should be passed as a 0-dim array (for example, by using `np.asarray(value)`).

    Usage:
        * Buy and hold using all cash and closing price (default):

        ```pycon
        >>> import numpy as np
        >>> from vectorbt.records.nb import col_map_nb
        >>> from vectorbt.portfolio import nb
        >>> from vectorbt.portfolio.enums import Direction

        >>> close = np.array([1, 2, 3, 4, 5])[:, None]
        >>> order_records, _ = nb.simulate_from_signal_func_nb(
        ...     target_shape=close.shape,
        ...     close=close,
        ...     group_lens=np.array([1]),
        ...     init_cash=np.array([100]),
        ...     call_seq=np.full(close.shape, 0),
        ...     signal_func_nb=nb.dir_enex_signal_func_nb,
        ...     signal_args=(np.asarray(True), np.asarray(False), np.asarray(Direction.LongOnly))
        ... )
        >>> col_map = col_map_nb(order_records['col'], close.shape[1])
        >>> asset_flow = nb.asset_flow_nb(close.shape, order_records, col_map, Direction.Both)
        >>> asset_flow
        array([[100.],
               [  0.],
               [  0.],
               [  0.],
               [  0.]])
        ```
    """
    check_group_lens_nb(group_lens, target_shape[1])
    cash_sharing = is_grouped_nb(group_lens)
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    if use_stops:
        sl_init_i = np.full(target_shape[1], -1, dtype=np.int64)
        sl_init_price = np.full(target_shape[1], np.nan, dtype=np.float64)
        sl_curr_i = np.full(target_shape[1], -1, dtype=np.int64)
        sl_curr_price = np.full(target_shape[1], np.nan, dtype=np.float64)
        sl_curr_stop = np.full(target_shape[1], np.nan, dtype=np.float64)
        sl_curr_trail = np.full(target_shape[1], False, dtype=np.bool_)
        tp_init_i = np.full(target_shape[1], -1, dtype=np.int64)
        tp_init_price = np.full(target_shape[1], np.nan, dtype=np.float64)
        tp_curr_stop = np.full(target_shape[1], np.nan, dtype=np.float64)
    else:
        sl_init_i = np.empty(0, dtype=np.int64)
        sl_init_price = np.empty(0, dtype=np.float64)
        sl_curr_i = np.empty(0, dtype=np.int64)
        sl_curr_price = np.empty(0, dtype=np.float64)
        sl_curr_stop = np.empty(0, dtype=np.float64)
        sl_curr_trail = np.empty(0, dtype=np.bool_)
        tp_init_i = np.empty(0, dtype=np.int64)
        tp_init_price = np.empty(0, dtype=np.float64)
        tp_curr_stop = np.empty(0, dtype=np.float64)
    price_arr = np.full(target_shape[1], np.nan, dtype=np.float64)
    size_arr = np.empty(target_shape[1], dtype=np.float64)
    size_type_arr = np.empty(target_shape[1], dtype=np.float64)
    slippage_arr = np.empty(target_shape[1], dtype=np.float64)
    direction_arr = np.empty(target_shape[1], dtype=np.int64)
    temp_order_value = np.empty(target_shape[1], dtype=np.float64)
    oidx = 0
    lidx = 0

    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        cash_now = init_cash[group]
        free_cash_now = init_cash[group]

        for i in range(target_shape[0]):
            for k in range(group_len):
                col = from_col + k

                # Resolve order price
                _price = flex_select_auto_nb(price, i, col, flex_2d)
                if np.isinf(_price):
                    if _price > 0:
                        _price = flex_select_auto_nb(close, i, col, flex_2d)  # upper bound is close
                    else:
                        _open = flex_select_auto_nb(open, i, col, flex_2d)
                        if not np.isnan(_open):
                            _price = _open  # lower bound is open
                        elif i > 0:
                            _price = flex_select_auto_nb(close, i - 1, col, flex_2d)  # lower bound is prev close
                        else:
                            _price = np.nan  # first timestamp has no prev close

                # Resolve valuation price
                _val_price = flex_select_auto_nb(val_price, i, col, flex_2d)
                if np.isinf(_val_price):
                    if _val_price > 0:
                        _val_price = _price  # upper bound is order price
                    elif i > 0:
                        _val_price = flex_select_auto_nb(close, i - 1, col, flex_2d)  # lower bound is prev close
                    else:
                        _val_price = np.nan  # first timestamp has no prev close
                if not np.isnan(_val_price) or not ffill_val_price:
                    last_val_price[col] = _val_price
                price_arr[col] = _price

            # Get size and value of each order
            for k in range(group_len):
                col = from_col + k  # order doesn't matter

                position_now = last_position[col]
                _price = price_arr[col]
                _slippage = flex_select_auto_nb(slippage, i, col, flex_2d)
                stop_price = np.nan
                if use_stops:
                    # Adjust stops
                    adjust_sl_ctx = AdjustSLContext(
                        i=i,
                        col=col,
                        position_now=last_position[col],
                        val_price_now=last_val_price[col],
                        init_i=sl_init_i[col],
                        init_price=sl_init_price[col],
                        curr_i=sl_curr_i[col],
                        curr_price=sl_curr_price[col],
                        curr_stop=sl_curr_stop[col],
                        curr_trail=sl_curr_trail[col]
                    )
                    sl_curr_stop[col], sl_curr_trail[col] = adjust_sl_func_nb(adjust_sl_ctx, *adjust_sl_args)
                    adjust_tp_ctx = AdjustTPContext(
                        i=i,
                        col=col,
                        position_now=last_position[col],
                        val_price_now=last_val_price[col],
                        init_i=tp_init_i[col],
                        init_price=tp_init_price[col],
                        curr_stop=tp_curr_stop[col]
                    )
                    tp_curr_stop[col] = adjust_tp_func_nb(adjust_tp_ctx, *adjust_tp_args)

                    if not np.isnan(sl_curr_stop[col]) or not np.isnan(tp_curr_stop[col]):
                        # Resolve current bar
                        _open = flex_select_auto_nb(open, i, col, flex_2d)
                        _high = flex_select_auto_nb(high, i, col, flex_2d)
                        _low = flex_select_auto_nb(low, i, col, flex_2d)
                        _close = flex_select_auto_nb(close, i, col, flex_2d)
                        if np.isnan(_open):
                            _open = _close
                        if np.isnan(_low):
                            _low = min(_open, _close)
                        if np.isnan(_high):
                            _high = max(_open, _close)

                        # Get stop price
                        if not np.isnan(sl_curr_stop[col]):
                            stop_price = get_stop_price_nb(
                                position_now,
                                sl_curr_price[col],
                                sl_curr_stop[col],
                                _open, _low, _high,
                                True
                            )
                        if np.isnan(stop_price) and not np.isnan(tp_curr_stop[col]):
                            stop_price = get_stop_price_nb(
                                position_now,
                                tp_init_price[col],
                                tp_curr_stop[col],
                                _open, _low, _high,
                                False
                            )

                        if not np.isnan(sl_curr_stop[col]) and sl_curr_trail[col]:
                            # Update trailing stop
                            if position_now > 0:
                                if _high > sl_curr_price[col]:
                                    sl_curr_i[col] = i
                                    sl_curr_price[col] = _high
                            elif position_now < 0:
                                if _low < sl_curr_price[col]:
                                    sl_curr_i[col] = i
                                    sl_curr_price[col] = _low

                # Get signals
                _accumulate = flex_select_auto_nb(accumulate, i, col, flex_2d)
                if use_stops and not np.isnan(stop_price):
                    # Stop signal comes first
                    _upon_stop_exit = flex_select_auto_nb(upon_stop_exit, i, col, flex_2d)
                    is_long_entry, is_long_exit, is_short_entry, is_short_exit, _accumulate = \
                        generate_stop_signal_nb(position_now, _upon_stop_exit, _accumulate)

                    _close = flex_select_auto_nb(close, i, col, flex_2d)
                    _stop_exit_price = flex_select_auto_nb(stop_exit_price, i, col, flex_2d)
                    _price, _slippage = resolve_stop_price_and_slippage_nb(
                        stop_price,
                        _price,
                        _close,
                        _slippage,
                        _stop_exit_price
                    )
                else:
                    # User-defined signal comes first
                    signal_ctx = SignalContext(
                        i=i,
                        col=col,
                        position_now=position_now,
                        val_price_now=last_val_price[col],
                        flex_2d=flex_2d
                    )
                    is_long_entry, is_long_exit, is_short_entry, is_short_exit = \
                        signal_func_nb(signal_ctx, *signal_args)

                    # Resolve signal conflicts
                    if is_long_entry or is_short_entry:
                        _upon_long_conflict = flex_select_auto_nb(upon_long_conflict, i, col, flex_2d)
                        is_long_entry, is_long_exit = resolve_signal_conflict_nb(
                            position_now,
                            is_long_entry,
                            is_long_exit,
                            Direction.LongOnly,
                            _upon_long_conflict
                        )
                        _upon_short_conflict = flex_select_auto_nb(upon_short_conflict, i, col, flex_2d)
                        is_short_entry, is_short_exit = resolve_signal_conflict_nb(
                            position_now,
                            is_short_entry,
                            is_short_exit,
                            Direction.ShortOnly,
                            _upon_short_conflict
                        )

                        # Resolve direction conflicts
                        _upon_dir_conflict = flex_select_auto_nb(upon_dir_conflict, i, col, flex_2d)
                        is_long_entry, is_short_entry = resolve_dir_conflict_nb(
                            position_now,
                            is_long_entry,
                            is_short_entry,
                            _upon_dir_conflict
                        )

                        # Resolve opposite entry
                        _upon_opposite_entry = flex_select_auto_nb(upon_opposite_entry, i, col, flex_2d)
                        is_long_entry, is_long_exit, is_short_entry, is_short_exit, _accumulate = \
                            resolve_opposite_entry_nb(
                                position_now,
                                is_long_entry,
                                is_long_exit,
                                is_short_entry,
                                is_short_exit,
                                _upon_opposite_entry,
                                _accumulate
                            )

                # Convert both signals to size (direction-aware), size type, and direction
                _size, _size_type, _direction = signals_to_size_nb(
                    last_position[col],
                    is_long_entry,
                    is_long_exit,
                    is_short_entry,
                    is_short_exit,
                    flex_select_auto_nb(size, i, col, flex_2d),
                    flex_select_auto_nb(size_type, i, col, flex_2d),
                    _accumulate,
                    last_val_price[col]
                )

                # Save all info
                price_arr[col] = _price
                slippage_arr[col] = _slippage
                size_arr[col] = _size
                size_type_arr[col] = _size_type
                direction_arr[col] = _direction

                if cash_sharing:
                    if _size == 0:
                        temp_order_value[k] = 0.
                    else:
                        # Approximate order value
                        if _size_type == SizeType.Amount:
                            temp_order_value[k] = _size * last_val_price[col]
                        elif _size_type == SizeType.Value:
                            temp_order_value[k] = _size
                        else:  # SizeType.Percent
                            if _size >= 0:
                                temp_order_value[k] = _size * cash_now
                            else:
                                asset_value_now = last_position[col] * last_val_price[col]
                                if _direction == Direction.LongOnly:
                                    temp_order_value[k] = _size * asset_value_now
                                else:
                                    max_exposure = (2 * max(asset_value_now, 0) + max(free_cash_now, 0))
                                    temp_order_value[k] = _size * max_exposure

            if cash_sharing:
                # Dynamically sort by order value -> selling comes first to release funds early
                if auto_call_seq:
                    insert_argsort_nb(temp_order_value[:group_len], call_seq[i, from_col:to_col])

                # Same as get_group_value_ctx_nb but with flexible indexing
                value_now = cash_now
                for k in range(group_len):
                    col = from_col + k
                    if last_position[col] != 0:
                        value_now += last_position[col] * last_val_price[col]

            for k in range(group_len):
                col = from_col + k
                if cash_sharing:
                    col_i = call_seq[i, col]
                    if col_i >= group_len:
                        raise ValueError("Call index exceeds bounds of the group")
                    col = from_col + col_i

                # Get current values per column
                position_now = last_position[col]
                debt_now = last_debt[col]
                val_price_now = last_val_price[col]
                if not cash_sharing:
                    value_now = cash_now
                    if position_now != 0:
                        value_now += position_now * val_price_now

                # Generate the next order
                _price = price_arr[col]
                _size = size_arr[col]  # already takes into account direction
                _size_type = size_type_arr[col]
                _direction = direction_arr[col]
                _slippage = slippage_arr[col]
                if _size != 0:
                    if _size > 0:  # long order
                        if _direction == Direction.ShortOnly:
                            _size *= -1  # must reverse for process_order_nb
                    else:  # short order
                        if _direction == Direction.ShortOnly:
                            _size *= -1
                    order = order_nb(
                        size=_size,
                        price=_price,
                        size_type=_size_type,
                        direction=_direction,
                        fees=flex_select_auto_nb(fees, i, col, flex_2d),
                        fixed_fees=flex_select_auto_nb(fixed_fees, i, col, flex_2d),
                        slippage=_slippage,
                        min_size=flex_select_auto_nb(min_size, i, col, flex_2d),
                        max_size=flex_select_auto_nb(max_size, i, col, flex_2d),
                        size_granularity=flex_select_auto_nb(size_granularity, i, col, flex_2d),
                        reject_prob=flex_select_auto_nb(reject_prob, i, col, flex_2d),
                        lock_cash=flex_select_auto_nb(lock_cash, i, col, flex_2d),
                        allow_partial=flex_select_auto_nb(allow_partial, i, col, flex_2d),
                        raise_reject=flex_select_auto_nb(raise_reject, i, col, flex_2d),
                        log=flex_select_auto_nb(log, i, col, flex_2d)
                    )

                    # Process the order
                    state = ProcessOrderState(
                        cash=cash_now,
                        position=position_now,
                        debt=debt_now,
                        free_cash=free_cash_now,
                        val_price=val_price_now,
                        value=value_now,
                        oidx=oidx,
                        lidx=lidx
                    )

                    order_result, new_state = process_order_nb(
                        i, col, group,
                        state,
                        update_value,
                        order,
                        order_records,
                        log_records
                    )

                    # Update state
                    cash_now = new_state.cash
                    position_now = new_state.position
                    debt_now = new_state.debt
                    free_cash_now = new_state.free_cash
                    val_price_now = new_state.val_price
                    value_now = new_state.value
                    oidx = new_state.oidx
                    lidx = new_state.lidx

                    if use_stops:
                        # Update stop price
                        if order_result.status == OrderStatus.Filled:
                            if position_now == 0:
                                # Position closed -> clear stops
                                sl_curr_i[col] = sl_init_i[col] = -1
                                sl_curr_price[col] = sl_init_price[col] = np.nan
                                sl_curr_stop[col] = np.nan
                                sl_curr_trail[col] = False
                                tp_init_i[col] = -1
                                tp_init_price[col] = np.nan
                                tp_curr_stop[col] = np.nan
                            else:
                                _stop_entry_price = flex_select_auto_nb(stop_entry_price, i, col, flex_2d)
                                if _stop_entry_price == StopEntryPrice.ValPrice:
                                    new_init_price = val_price_now
                                elif _stop_entry_price == StopEntryPrice.Price:
                                    new_init_price = order.price
                                elif _stop_entry_price == StopEntryPrice.FillPrice:
                                    new_init_price = order_result.price
                                else:
                                    new_init_price = flex_select_auto_nb(close, i, col, flex_2d)
                                _upon_stop_update = flex_select_auto_nb(upon_stop_update, i, col, flex_2d)
                                _sl_stop = flex_select_auto_nb(sl_stop, i, col, flex_2d)
                                _sl_trail = flex_select_auto_nb(sl_trail, i, col, flex_2d)
                                _tp_stop = flex_select_auto_nb(tp_stop, i, col, flex_2d)

                                if state.position == 0 or np.sign(position_now) != np.sign(state.position):
                                    # Position opened/reversed -> set stops
                                    sl_curr_i[col] = sl_init_i[col] = i
                                    sl_curr_price[col] = sl_init_price[col] = new_init_price
                                    sl_curr_stop[col] = _sl_stop
                                    sl_curr_trail[col] = _sl_trail
                                    tp_init_i[col] = i
                                    tp_init_price[col] = new_init_price
                                    tp_curr_stop[col] = _tp_stop
                                elif abs(position_now) > abs(state.position):
                                    # Position increased -> keep/override stops
                                    if should_update_stop_nb(_sl_stop, _upon_stop_update):
                                        sl_curr_i[col] = sl_init_i[col] = i
                                        sl_curr_price[col] = sl_init_price[col] = new_init_price
                                        sl_curr_stop[col] = _sl_stop
                                        sl_curr_trail[col] = _sl_trail
                                    if should_update_stop_nb(_tp_stop, _upon_stop_update):
                                        tp_init_i[col] = i
                                        tp_init_price[col] = new_init_price
                                        tp_curr_stop[col] = _tp_stop

                # Now becomes last
                last_position[col] = position_now
                last_debt[col] = debt_now
                if not np.isnan(val_price_now) or not ffill_val_price:
                    last_val_price[col] = val_price_now

        from_col = to_col

    return order_records[:oidx], log_records[:lidx]


@njit
def dir_enex_signal_func_nb(c: SignalContext,
                            entries: tp.ArrayLike,
                            exits: tp.ArrayLike,
                            direction: tp.ArrayLike) -> tp.Tuple[bool, bool, bool, bool]:
    """Resolve direction-aware signals out of entries, exits, and direction."""
    is_entry = flex_select_auto_nb(entries, c.i, c.col, c.flex_2d)
    is_exit = flex_select_auto_nb(exits, c.i, c.col, c.flex_2d)
    _direction = flex_select_auto_nb(direction, c.i, c.col, c.flex_2d)
    if _direction == Direction.LongOnly:
        return is_entry, is_exit, False, False
    if _direction == Direction.ShortOnly:
        return False, False, is_entry, is_exit
    return is_entry, False, is_exit, False


@njit
def ls_enex_signal_func_nb(c: SignalContext,
                           long_entries: tp.ArrayLike,
                           long_exits: tp.ArrayLike,
                           short_entries: tp.ArrayLike,
                           short_exits: tp.ArrayLike) -> tp.Tuple[bool, bool, bool, bool]:
    """Get an element of direction-aware signals."""
    is_long_entry = flex_select_auto_nb(long_entries, c.i, c.col, c.flex_2d)
    is_long_exit = flex_select_auto_nb(long_exits, c.i, c.col, c.flex_2d)
    is_short_entry = flex_select_auto_nb(short_entries, c.i, c.col, c.flex_2d)
    is_short_exit = flex_select_auto_nb(short_exits, c.i, c.col, c.flex_2d)
    return is_long_entry, is_long_exit, is_short_entry, is_short_exit


@njit
def no_pre_func_nb(c: tp.NamedTuple, *args) -> tp.Args:
    """Placeholder preprocessing function that forwards received arguments down the stack."""
    return args


@njit
def no_order_func_nb(c: OrderContext, *args) -> Order:
    """Placeholder order function that returns no order."""
    return NoOrder


@njit
def no_post_func_nb(c: tp.NamedTuple, *args) -> None:
    """Placeholder postprocessing function that returns nothing."""
    return None


PreSimFuncT = tp.Callable[[SimulationContext, tp.VarArg()], tp.Args]
PostSimFuncT = tp.Callable[[SimulationContext, tp.VarArg()], None]
PreGroupFuncT = tp.Callable[[GroupContext, tp.VarArg()], tp.Args]
PostGroupFuncT = tp.Callable[[GroupContext, tp.VarArg()], None]
PreRowFuncT = tp.Callable[[RowContext, tp.VarArg()], tp.Args]
PostRowFuncT = tp.Callable[[RowContext, tp.VarArg()], None]
PreSegmentFuncT = tp.Callable[[SegmentContext, tp.VarArg()], tp.Args]
PostSegmentFuncT = tp.Callable[[SegmentContext, tp.VarArg()], None]
OrderFuncT = tp.Callable[[OrderContext, tp.VarArg()], Order]
PostOrderFuncT = tp.Callable[[PostOrderContext, OrderResult, tp.VarArg()], None]


@njit
def simulate_nb(target_shape: tp.Shape,
                group_lens: tp.Array1d,
                init_cash: tp.Array1d,
                cash_sharing: bool,
                call_seq: tp.Array2d,
                segment_mask: tp.ArrayLike = np.asarray(True),
                call_pre_segment: bool = False,
                call_post_segment: bool = False,
                pre_sim_func_nb: PreSimFuncT = no_pre_func_nb,
                pre_sim_args: tp.Args = (),
                post_sim_func_nb: PostSimFuncT = no_post_func_nb,
                post_sim_args: tp.Args = (),
                pre_group_func_nb: PreGroupFuncT = no_pre_func_nb,
                pre_group_args: tp.Args = (),
                post_group_func_nb: PostGroupFuncT = no_post_func_nb,
                post_group_args: tp.Args = (),
                pre_segment_func_nb: PreSegmentFuncT = no_pre_func_nb,
                pre_segment_args: tp.Args = (),
                post_segment_func_nb: PostSegmentFuncT = no_post_func_nb,
                post_segment_args: tp.Args = (),
                order_func_nb: OrderFuncT = no_order_func_nb,
                order_args: tp.Args = (),
                post_order_func_nb: PostOrderFuncT = no_post_func_nb,
                post_order_args: tp.Args = (),
                close: tp.ArrayLike = np.asarray(np.nan),
                ffill_val_price: bool = True,
                update_value: bool = False,
                fill_pos_record: bool = True,
                max_orders: tp.Optional[int] = None,
                max_logs: int = 0,
                flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Fill order and log records by iterating over a shape and calling a range of user-defined functions.

    Starting with initial cash `init_cash`, iterates over each group and column in `target_shape`,
    and for each data point, generates an order using `order_func_nb`. Tries then to fulfill that
    order. Upon success, updates the current state including the cash balance and the position.

    Returns order records of layout `vectorbt.portfolio.enums.order_dt` and log records of layout
    `vectorbt.portfolio.enums.log_dt`.

    As opposed to `simulate_row_wise_nb`, order processing happens in column-major order.
    Column-major order means processing the entire column/group with all rows before moving to the next one.
    See [Row- and column-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order).

    Args:
        target_shape (tuple): See `vectorbt.portfolio.enums.SimulationContext.target_shape`.
        group_lens (array_like of int): See `vectorbt.portfolio.enums.SimulationContext.group_lens`.
        init_cash (array_like of float): See `vectorbt.portfolio.enums.SimulationContext.init_cash`.
        cash_sharing (bool): See `vectorbt.portfolio.enums.SimulationContext.cash_sharing`.
        call_seq (array_like of int): See `vectorbt.portfolio.enums.SimulationContext.call_seq`.
        segment_mask (array_like of bool): See `vectorbt.portfolio.enums.SimulationContext.segment_mask`.
        call_pre_segment (bool): See `vectorbt.portfolio.enums.SimulationContext.call_pre_segment`.
        call_post_segment (bool): See `vectorbt.portfolio.enums.SimulationContext.call_post_segment`.
        pre_sim_func_nb (callable): Function called before simulation.

            Can be used for creation of global arrays and setting the seed.

            Should accept `vectorbt.portfolio.enums.SimulationContext` and `*pre_sim_args`.
            Should return a tuple of any content, which is then passed to `pre_group_func_nb` and
            `post_group_func_nb`.
        pre_sim_args (tuple): Packed arguments passed to `pre_sim_func_nb`.
        post_sim_func_nb (callable): Function called after simulation.

            Should accept `vectorbt.portfolio.enums.SimulationContext` and `*post_sim_args`.
            Should return nothing.
        post_sim_args (tuple): Packed arguments passed to `post_sim_func_nb`.
        pre_group_func_nb (callable): Function called before each group.

            Should accept `vectorbt.portfolio.enums.GroupContext`, unpacked tuple from `pre_sim_func_nb`,
            and `*pre_group_args`. Should return a tuple of any content, which is then passed to
            `pre_segment_func_nb` and `post_segment_func_nb`.
        pre_group_args (tuple): Packed arguments passed to `pre_group_func_nb`.
        post_group_func_nb (callable): Function called after each group.

            Should accept `vectorbt.portfolio.enums.GroupContext`, unpacked tuple from `pre_sim_func_nb`,
            and `*post_group_args`. Should return nothing.
        post_group_args (tuple): Packed arguments passed to `post_group_func_nb`.
        pre_segment_func_nb (callable): Function called before each segment.

            Called if `segment_mask` or `call_pre_segment` is True.

            Should accept `vectorbt.portfolio.enums.SegmentContext`, unpacked tuple from `pre_group_func_nb`,
            and `*pre_segment_args`. Should return a tuple of any content, which is then passed to
            `order_func_nb` and `post_order_func_nb`.

            This is the right place to change call sequence and set the valuation price.
            Group re-valuation and update of the open position stats happens right after this function,
            regardless of whether it has been called.

            !!! note
                To change the call sequence of a segment, access
                `vectorbt.portfolio.enums.SegmentContext.call_seq_now` and change it in-place.
                Make sure to not generate any new arrays as it may negatively impact performance.
                Assigning `SegmentContext.call_seq_now` as any other context (named tuple) value
                is not supported. See `vectorbt.portfolio.enums.SegmentContext.call_seq_now`.

            !!! note
                You can override elements of `last_val_price` to manipulate group valuation.
                See `vectorbt.portfolio.enums.SimulationContext.last_val_price`.
        pre_segment_args (tuple): Packed arguments passed to `pre_segment_func_nb`.
        post_segment_func_nb (callable): Function called after each segment.

            Called if `segment_mask` or `call_post_segment` is True.

            The last group re-valuation and update of the open position stats happens right before this function,
            regardless of whether it has been called.

            Should accept `vectorbt.portfolio.enums.SegmentContext`, unpacked tuple from `pre_group_func_nb`,
            and `*post_segment_args`. Should return nothing.
        post_segment_args (tuple): Packed arguments passed to `post_segment_func_nb`.
        order_func_nb (callable): Order generation function.

            Used for either generating an order or skipping.

            Should accept `vectorbt.portfolio.enums.OrderContext`, unpacked tuple from `pre_segment_func_nb`,
            and `*order_args`. Should return `vectorbt.portfolio.enums.Order`.

            !!! note
                If the returned order has been rejected, there is no way of issuing a new order.
                You should make sure that the order passes, for example, by using `try_order_nb`.

                To have a greater freedom in order management, use `flex_simulate_nb`.
        order_args (tuple): Arguments passed to `order_func_nb`.
        post_order_func_nb (callable): Callback that is called after the order has been processed.

            Used for checking the order status and doing some post-processing.

            Should accept `vectorbt.portfolio.enums.PostOrderContext`, unpacked tuple from
            `pre_segment_func_nb`, and `*post_order_args`. Should return nothing.
        post_order_args (tuple): Arguments passed to `post_order_func_nb`.
        close (array_like of float): See `vectorbt.portfolio.enums.SimulationContext.close`.
        ffill_val_price (bool): See `vectorbt.portfolio.enums.SimulationContext.ffill_val_price`.
        update_value (bool): See `vectorbt.portfolio.enums.SimulationContext.update_value`.
        fill_pos_record (bool): See `vectorbt.portfolio.enums.SimulationContext.fill_pos_record`.
        max_orders (int): Size of the order records array.
        max_logs (int): Size of the log records array.
        flex_2d (bool): See `vectorbt.portfolio.enums.SimulationContext.flex_2d`.

    !!! note
        Remember that indexing of 2-dim arrays in vectorbt follows that of pandas: `a[i, col]`.

    !!! warning
        You can only safely access data of columns that are to the left of the current group and
        rows that are to the top of the current row within the same group. Other data points have
        not been processed yet and thus empty. Accessing them will not trigger any errors or warnings,
        but provide you with arbitrary data (see [np.empty](https://numpy.org/doc/stable/reference/generated/numpy.empty.html)).

    Call hierarchy:
        Like most things in the vectorbt universe, simulation is also done by iterating over a (imaginary) frame.
        This frame consists of two dimensions: time (rows) and assets/features (columns).
        Each element of this frame is a potential order, which gets generated by calling an order function.

        The question is: how do we move across this frame to simulate trading? There are two movement patterns:
        column-major (as done by `simulate_nb`) and row-major order (as done by `simulate_row_wise_nb`).
        In each of these patterns, we are always moving from top to bottom (time axis) and from left to right
        (asset/feature axis); the only difference between them is across which axis we are moving faster:
        do we want to process each column first (thus assuming that columns are independent) or each row?
        Choosing between them is mostly a matter of preference, but it also makes different data being
        available when generating an order.

        The frame is further divided into "blocks": columns, groups, rows, segments, and elements.
        For example, columns can be grouped into groups that may or may not share the same capital.
        Regardless of capital sharing, each collection of elements within a group and a time step is called
        a segment, which simply defines a single context (such as shared capital) for one or multiple orders.
        Each segment can also define a custom sequence (a so-called call sequence) in which orders are executed.

        You can imagine each of these blocks as a rectangle drawn over different parts of the frame,
        and having its own context and pre/post-processing function. The pre-processing function is a
        simple callback that is called before entering the block, and can be provided by the user to, for example,
        prepare arrays or do some custom calculations. It must return a tuple (can be empty) that is then unpacked and
        passed as arguments to the pre- and postprocessing function coming next in the call hierarchy.
        The postprocessing function can be used, for example, to write user-defined arrays such as returns.

        Let's demonstrate a frame with one group of two columns and one group of one column, and the
        following call sequence:

        ```plaintext
        array([[0, 1, 0],
               [1, 0, 0]])
        ```

        ![](/assets/images/simulate_nb.gif)

        And here is the context information available at each step:

        ![](/assets/images/context_info.png)

    Usage:
        * Create a group of three assets together sharing 100$ and simulate an equal-weighted portfolio
        that rebalances every second tick, all without leaving Numba:

        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from collections import namedtuple
        >>> from numba import njit
        >>> from vectorbt.generic.plotting import Scatter
        >>> from vectorbt.records.nb import col_map_nb
        >>> from vectorbt.portfolio.enums import SizeType, Direction
        >>> from vectorbt.portfolio.nb import (
        ...     get_col_elem_nb,
        ...     get_elem_nb,
        ...     order_nb,
        ...     simulate_nb,
        ...     simulate_row_wise_nb,
        ...     build_call_seq,
        ...     sort_call_seq_nb,
        ...     asset_flow_nb,
        ...     assets_nb,
        ...     asset_value_nb
        ... )

        >>> @njit
        ... def pre_sim_func_nb(c):
        ...     print('before simulation')
        ...     # Create a temporary array and pass it down the stack
        ...     order_value_out = np.empty(c.target_shape[1], dtype=np.float64)
        ...     return (order_value_out,)

        >>> @njit
        ... def pre_group_func_nb(c, order_value_out):
        ...     print('\\tbefore group', c.group)
        ...     # Forward down the stack (you can omit pre_group_func_nb entirely)
        ...     return (order_value_out,)

        >>> @njit
        ... def pre_segment_func_nb(c, order_value_out, size, price, size_type, direction):
        ...     print('\\t\\tbefore segment', c.i)
        ...     for col in range(c.from_col, c.to_col):
        ...         # Here we use order price for group valuation
        ...         c.last_val_price[col] = get_col_elem_nb(c, col, price)
        ...
        ...     # Reorder call sequence of this segment such that selling orders come first and buying last
        ...     # Rearranges c.call_seq_now based on order value (size, size_type, direction, and val_price)
        ...     # Utilizes flexible indexing using get_col_elem_nb (as we did above)
        ...     sort_call_seq_nb(c, size, size_type, direction, order_value_out[c.from_col:c.to_col])
        ...     # Forward nothing
        ...     return ()

        >>> @njit
        ... def order_func_nb(c, size, price, size_type, direction, fees, fixed_fees, slippage):
        ...     print('\\t\\t\\tcreating order', c.call_idx, 'at column', c.col)
        ...     # Create and return an order
        ...     return order_nb(
        ...         size=get_elem_nb(c, size),
        ...         price=get_elem_nb(c, price),
        ...         size_type=get_elem_nb(c, size_type),
        ...         direction=get_elem_nb(c, direction),
        ...         fees=get_elem_nb(c, fees),
        ...         fixed_fees=get_elem_nb(c, fixed_fees),
        ...         slippage=get_elem_nb(c, slippage)
        ...     )

        >>> @njit
        ... def post_order_func_nb(c):
        ...     print('\\t\\t\\t\\torder status:', c.order_result.status)
        ...     return None

        >>> @njit
        ... def post_segment_func_nb(c, order_value_out):
        ...     print('\\t\\tafter segment', c.i)
        ...     return None

        >>> @njit
        ... def post_group_func_nb(c, order_value_out):
        ...     print('\\tafter group', c.group)
        ...     return None

        >>> @njit
        ... def post_sim_func_nb(c):
        ...     print('after simulation')
        ...     return None

        >>> target_shape = (5, 3)
        >>> np.random.seed(42)
        >>> group_lens = np.array([3])  # one group of three columns
        >>> init_cash = np.array([100.])  # one capital per group
        >>> cash_sharing = True
        >>> call_seq = build_call_seq(target_shape, group_lens)  # will be overridden
        >>> segment_mask = np.array([True, False, True, False, True])[:, None]
        >>> segment_mask = np.copy(np.broadcast_to(segment_mask, target_shape))
        >>> size = np.asarray(1 / target_shape[1])  # scalars must become 0-dim arrays
        >>> price = close = np.random.uniform(1, 10, size=target_shape)
        >>> size_type = np.asarray(SizeType.TargetPercent)
        >>> direction = np.asarray(Direction.LongOnly)
        >>> fees = np.asarray(0.001)
        >>> fixed_fees = np.asarray(1.)
        >>> slippage = np.asarray(0.001)

        >>> order_records, log_records = simulate_nb(
        ...     target_shape,
        ...     group_lens,
        ...     init_cash,
        ...     cash_sharing,
        ...     call_seq,
        ...     segment_mask=segment_mask,
        ...     pre_sim_func_nb=pre_sim_func_nb,
        ...     post_sim_func_nb=post_sim_func_nb,
        ...     pre_group_func_nb=pre_group_func_nb,
        ...     post_group_func_nb=post_group_func_nb,
        ...     pre_segment_func_nb=pre_segment_func_nb,
        ...     pre_segment_args=(size, price, size_type, direction),
        ...     post_segment_func_nb=post_segment_func_nb,
        ...     order_func_nb=order_func_nb,
        ...     order_args=(size, price, size_type, direction, fees, fixed_fees, slippage),
        ...     post_order_func_nb=post_order_func_nb
        ... )
        before simulation
            before group 0
                before segment 0
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 1
                        order status: 0
                    creating order 2 at column 2
                        order status: 0
                after segment 0
                before segment 2
                    creating order 0 at column 1
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 0
                        order status: 0
                after segment 2
                before segment 4
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 1
                        order status: 0
                after segment 4
            after group 0
        after simulation

        >>> pd.DataFrame.from_records(order_records)
           id  col  idx       size     price      fees  side
        0   0    0    0   7.626262  4.375232  1.033367     0
        1   1    1    0   3.488053  9.565985  1.033367     0
        2   2    2    0   3.972040  7.595533  1.030170     0
        3   3    1    2   0.920352  8.786790  1.008087     1
        4   4    2    2   0.448747  6.403625  1.002874     1
        5   5    0    2   5.210115  1.524275  1.007942     0
        6   6    0    4   7.899568  8.483492  1.067016     1
        7   7    2    4  12.378281  2.639061  1.032667     0
        8   8    1    4  10.713236  2.913963  1.031218     0

        >>> call_seq
        array([[0, 1, 2],
               [0, 1, 2],
               [1, 2, 0],
               [0, 1, 2],
               [0, 2, 1]])

        >>> col_map = col_map_nb(order_records['col'], target_shape[1])
        >>> asset_flow = asset_flow_nb(target_shape, order_records, col_map, Direction.Both)
        >>> assets = assets_nb(asset_flow)
        >>> asset_value = asset_value_nb(close, assets)
        >>> Scatter(data=asset_value).fig.show()
        ```

        ![](/assets/images/simulate_nb.svg)

        Note that the last order in a group with cash sharing is always disadvantaged
        as it has a bit less funds than the previous orders due to costs, which are not
        included when valuating the group.
    """
    check_group_lens_nb(group_lens, target_shape[1])
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_cash = init_cash.copy()
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_free_cash = init_cash.copy()
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    last_value = init_cash.copy()
    second_last_value = init_cash.copy()
    temp_value = init_cash.copy()
    last_return = np.full_like(last_value, np.nan)
    last_pos_record = np.empty(target_shape[1], dtype=trade_dt)
    last_pos_record['id'][:] = -1
    last_oidx = np.full(target_shape[1], -1, dtype=np.int64)
    last_lidx = np.full(target_shape[1], -1, dtype=np.int64)
    oidx = 0
    lidx = 0

    # Call function before the simulation
    pre_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=call_seq,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    pre_sim_out = pre_sim_func_nb(pre_sim_ctx, *pre_sim_args)

    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col

        # Call function before the group
        pre_group_ctx = GroupContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            group=group,
            group_len=group_len,
            from_col=from_col,
            to_col=to_col
        )
        pre_group_out = pre_group_func_nb(pre_group_ctx, *pre_sim_out, *pre_group_args)

        for i in range(target_shape[0]):
            call_seq_now = call_seq[i, from_col:to_col]

            # Is this segment active?
            if call_pre_segment or segment_mask[i, group]:
                # Call function before the segment
                pre_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=call_seq_now
                )
                pre_segment_out = pre_segment_func_nb(pre_seg_ctx, *pre_group_out, *pre_segment_args)

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Update value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Is this segment active?
            if segment_mask[i, group]:

                for k in range(group_len):
                    col_i = call_seq_now[k]
                    if col_i >= group_len:
                        raise ValueError("Call index exceeds bounds of the group")
                    col = from_col + col_i

                    # Get current values
                    position_now = last_position[col]
                    debt_now = last_debt[col]
                    val_price_now = last_val_price[col]
                    pos_record_now = last_pos_record[col]
                    if cash_sharing:
                        cash_now = last_cash[group]
                        free_cash_now = last_free_cash[group]
                        value_now = last_value[group]
                        return_now = last_return[group]
                    else:
                        cash_now = last_cash[col]
                        free_cash_now = last_free_cash[col]
                        value_now = last_value[col]
                        return_now = last_return[col]

                    # Generate the next order
                    order_ctx = OrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=call_seq,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=call_seq_now,
                        col=col,
                        call_idx=k,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    order = order_func_nb(order_ctx, *pre_segment_out, *order_args)
                    if np.isinf(order.price):
                        if i > 0:
                            _prev_close = flex_select_auto_nb(close, i - 1, col, flex_2d)
                        else:
                            _prev_close = np.nan
                        _close = flex_select_auto_nb(close, i, col, flex_2d)
                        order = replace_inf_price_nb(_prev_close, _close, order)

                    # Process the order
                    state = ProcessOrderState(
                        cash=cash_now,
                        position=position_now,
                        debt=debt_now,
                        free_cash=free_cash_now,
                        val_price=val_price_now,
                        value=value_now,
                        oidx=oidx,
                        lidx=lidx
                    )

                    order_result, new_state = process_order_nb(
                        i, col, group,
                        state,
                        update_value,
                        order,
                        order_records,
                        log_records
                    )

                    # Update state
                    cash_now = new_state.cash
                    position_now = new_state.position
                    debt_now = new_state.debt
                    free_cash_now = new_state.free_cash
                    val_price_now = new_state.val_price
                    value_now = new_state.value
                    if cash_sharing:
                        return_now = returns_nb.get_return_nb(second_last_value[group], value_now)
                    else:
                        return_now = returns_nb.get_return_nb(second_last_value[col], value_now)
                    oidx = new_state.oidx
                    lidx = new_state.lidx

                    # Now becomes last
                    last_position[col] = position_now
                    last_debt[col] = debt_now
                    if not np.isnan(val_price_now) or not ffill_val_price:
                        last_val_price[col] = val_price_now
                    if cash_sharing:
                        last_cash[group] = cash_now
                        last_free_cash[group] = free_cash_now
                        last_value[group] = value_now
                        last_return[group] = return_now
                    else:
                        last_cash[col] = cash_now
                        last_free_cash[col] = free_cash_now
                        last_value[col] = value_now
                        last_return[col] = return_now
                    if state.oidx != new_state.oidx:
                        last_oidx[col] = state.oidx
                    if state.lidx != new_state.lidx:
                        last_lidx[col] = state.lidx

                    # Update position record
                    if fill_pos_record:
                        update_pos_record_nb(
                            pos_record_now,
                            i, col,
                            state.position, position_now,
                            order_result
                        )

                    # Post-order callback
                    post_order_ctx = PostOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=call_seq,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=call_seq_now,
                        col=col,
                        call_idx=k,
                        cash_before=state.cash,
                        position_before=state.position,
                        debt_before=state.debt,
                        free_cash_before=state.free_cash,
                        val_price_before=state.val_price,
                        value_before=state.value,
                        order_result=order_result,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    post_order_func_nb(post_order_ctx, *pre_segment_out, *post_order_args)

            # NOTE: Regardless of segment_mask, we still need to update stats to be accessed by future rows
            # Update valuation price
            for col in range(from_col, to_col):
                _close = flex_select_auto_nb(close, i, col, flex_2d)
                if not np.isnan(_close) or not ffill_val_price:
                    last_val_price[col] = _close

            # Update previous value, current value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                second_last_value[group] = temp_value[group]
                temp_value[group] = last_value[group]
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    second_last_value[col] = temp_value[col]
                    temp_value[col] = last_value[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Is this segment active?
            if call_post_segment or segment_mask[i, group]:
                # Call function before the segment
                post_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=call_seq_now
                )
                post_segment_func_nb(post_seg_ctx, *pre_group_out, *post_segment_args)

        # Call function after the group
        post_group_ctx = GroupContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            group=group,
            group_len=group_len,
            from_col=from_col,
            to_col=to_col
        )
        post_group_func_nb(post_group_ctx, *pre_sim_out, *post_group_args)

        from_col = to_col

    # Call function after the simulation
    post_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=call_seq,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    post_sim_func_nb(post_sim_ctx, *post_sim_args)

    return order_records[:oidx], log_records[:lidx]


@njit
def simulate_row_wise_nb(target_shape: tp.Shape,
                         group_lens: tp.Array1d,
                         init_cash: tp.Array1d,
                         cash_sharing: bool,
                         call_seq: tp.Array2d,
                         segment_mask: tp.ArrayLike = np.asarray(True),
                         call_pre_segment: bool = False,
                         call_post_segment: bool = False,
                         pre_sim_func_nb: PreSimFuncT = no_pre_func_nb,
                         pre_sim_args: tp.Args = (),
                         post_sim_func_nb: PostSimFuncT = no_post_func_nb,
                         post_sim_args: tp.Args = (),
                         pre_row_func_nb: PreRowFuncT = no_pre_func_nb,
                         pre_row_args: tp.Args = (),
                         post_row_func_nb: PostRowFuncT = no_post_func_nb,
                         post_row_args: tp.Args = (),
                         pre_segment_func_nb: PreSegmentFuncT = no_pre_func_nb,
                         pre_segment_args: tp.Args = (),
                         post_segment_func_nb: PostSegmentFuncT = no_post_func_nb,
                         post_segment_args: tp.Args = (),
                         order_func_nb: OrderFuncT = no_order_func_nb,
                         order_args: tp.Args = (),
                         post_order_func_nb: PostOrderFuncT = no_post_func_nb,
                         post_order_args: tp.Args = (),
                         close: tp.ArrayLike = np.asarray(np.nan),
                         ffill_val_price: bool = True,
                         update_value: bool = False,
                         fill_pos_record: bool = True,
                         max_orders: tp.Optional[int] = None,
                         max_logs: int = 0,
                         flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Same as `simulate_nb`, but iterates in row-major order.

    Row-major order means processing the entire row with all groups/columns before moving to the next one.

    The main difference is that instead of `pre_group_func_nb` it now exposes `pre_row_func_nb`,
    which is executed per entire row. It should accept `vectorbt.portfolio.enums.RowContext`.

    !!! note
        Function `pre_row_func_nb` is only called if there is at least on active segment in
        the row. Functions `pre_segment_func_nb` and `order_func_nb` are only called if their
        segment is active. If the main task of `pre_row_func_nb` is to activate/deactivate segments,
        all segments should be activated by default to allow `pre_row_func_nb` to be called.

    !!! warning
        You can only safely access data points that are to the left of the current group and
        rows that are to the top of the current row.

    Call hierarchy:
        Let's illustrate the same example as in `simulate_nb` but adapted for this function:

        ![](/assets/images/simulate_row_wise_nb.gif)

    Usage:
        * Running the same example as in `simulate_nb` but adapted for this function:

        ```pycon
        >>> @njit
        ... def pre_row_func_nb(c, order_value_out):
        ...     print('\\tbefore row', c.i)
        ...     # Forward down the stack
        ...     return (order_value_out,)

        >>> @njit
        ... def post_row_func_nb(c, order_value_out):
        ...     print('\\tafter row', c.i)
        ...     return None

        >>> call_seq = build_call_seq(target_shape, group_lens)
        >>> order_records, log_records = simulate_row_wise_nb(
        ...     target_shape,
        ...     group_lens,
        ...     init_cash,
        ...     cash_sharing,
        ...     call_seq,
        ...     segment_mask=segment_mask,
        ...     pre_sim_func_nb=pre_sim_func_nb,
        ...     post_sim_func_nb=post_sim_func_nb,
        ...     pre_row_func_nb=pre_row_func_nb,
        ...     post_row_func_nb=post_row_func_nb,
        ...     pre_segment_func_nb=pre_segment_func_nb,
        ...     pre_segment_args=(size, price, size_type, direction),
        ...     post_segment_func_nb=post_segment_func_nb,
        ...     order_func_nb=order_func_nb,
        ...     order_args=(size, price, size_type, direction, fees, fixed_fees, slippage),
        ...     post_order_func_nb=post_order_func_nb
        ... )
        before simulation
            before row 0
                before segment 0
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 1
                        order status: 0
                    creating order 2 at column 2
                        order status: 0
                after segment 0
            after row 0
            before row 1
            after row 1
            before row 2
                before segment 2
                    creating order 0 at column 1
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 0
                        order status: 0
                after segment 2
            after row 2
            before row 3
            after row 3
            before row 4
                before segment 4
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 1
                        order status: 0
                after segment 4
            after row 4
        after simulation
        ```
    """
    check_group_lens_nb(group_lens, target_shape[1])
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_cash = init_cash.copy()
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_free_cash = init_cash.copy()
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    last_value = init_cash.copy()
    second_last_value = init_cash.copy()
    temp_value = init_cash.copy()
    last_return = np.full_like(last_value, np.nan)
    last_pos_record = np.empty(target_shape[1], dtype=trade_dt)
    last_pos_record['id'][:] = -1
    last_oidx = np.full(target_shape[1], -1, dtype=np.int64)
    last_lidx = np.full(target_shape[1], -1, dtype=np.int64)
    oidx = 0
    lidx = 0

    # Call function before the simulation
    pre_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=call_seq,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    pre_sim_out = pre_sim_func_nb(pre_sim_ctx, *pre_sim_args)

    for i in range(target_shape[0]):

        # Call function before the row
        pre_row_ctx = RowContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            i=i
        )
        pre_row_out = pre_row_func_nb(pre_row_ctx, *pre_sim_out, *pre_row_args)

        from_col = 0
        for group in range(len(group_lens)):
            to_col = from_col + group_lens[group]
            group_len = to_col - from_col
            call_seq_now = call_seq[i, from_col:to_col]

            # Is this segment active?
            if call_pre_segment or segment_mask[i, group]:
                # Call function before the segment
                pre_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=call_seq_now
                )
                pre_segment_out = pre_segment_func_nb(pre_seg_ctx, *pre_row_out, *pre_segment_args)

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Update value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Is this segment active?
            if segment_mask[i, group]:

                for k in range(group_len):
                    col_i = call_seq_now[k]
                    if col_i >= group_len:
                        raise ValueError("Call index exceeds bounds of the group")
                    col = from_col + col_i

                    # Get current values
                    position_now = last_position[col]
                    debt_now = last_debt[col]
                    val_price_now = last_val_price[col]
                    pos_record_now = last_pos_record[col]
                    if cash_sharing:
                        cash_now = last_cash[group]
                        free_cash_now = last_free_cash[group]
                        value_now = last_value[group]
                        return_now = last_return[group]
                    else:
                        cash_now = last_cash[col]
                        free_cash_now = last_free_cash[col]
                        value_now = last_value[col]
                        return_now = last_return[col]

                    # Generate the next order
                    order_ctx = OrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=call_seq,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=call_seq_now,
                        col=col,
                        call_idx=k,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    order = order_func_nb(order_ctx, *pre_segment_out, *order_args)
                    if np.isinf(order.price):
                        if i > 0:
                            _prev_close = flex_select_auto_nb(close, i - 1, col, flex_2d)
                        else:
                            _prev_close = np.nan
                        _close = flex_select_auto_nb(close, i, col, flex_2d)
                        order = replace_inf_price_nb(_prev_close, _close, order)

                    # Process the order
                    state = ProcessOrderState(
                        cash=cash_now,
                        position=position_now,
                        debt=debt_now,
                        free_cash=free_cash_now,
                        val_price=val_price_now,
                        value=value_now,
                        oidx=oidx,
                        lidx=lidx
                    )

                    order_result, new_state = process_order_nb(
                        i, col, group,
                        state,
                        update_value,
                        order,
                        order_records,
                        log_records
                    )

                    # Update state
                    cash_now = new_state.cash
                    position_now = new_state.position
                    debt_now = new_state.debt
                    free_cash_now = new_state.free_cash
                    val_price_now = new_state.val_price
                    value_now = new_state.value
                    if cash_sharing:
                        return_now = returns_nb.get_return_nb(second_last_value[group], value_now)
                    else:
                        return_now = returns_nb.get_return_nb(second_last_value[col], value_now)
                    oidx = new_state.oidx
                    lidx = new_state.lidx

                    # Now becomes last
                    last_position[col] = position_now
                    last_debt[col] = debt_now
                    if not np.isnan(val_price_now) or not ffill_val_price:
                        last_val_price[col] = val_price_now
                    if cash_sharing:
                        last_cash[group] = cash_now
                        last_free_cash[group] = free_cash_now
                        last_value[group] = value_now
                        last_return[group] = return_now
                    else:
                        last_cash[col] = cash_now
                        last_free_cash[col] = free_cash_now
                        last_value[col] = value_now
                        last_return[col] = return_now
                    if state.oidx != new_state.oidx:
                        last_oidx[col] = state.oidx
                    if state.lidx != new_state.lidx:
                        last_lidx[col] = state.lidx

                    # Update position record
                    if fill_pos_record:
                        update_pos_record_nb(
                            pos_record_now,
                            i, col,
                            state.position, position_now,
                            order_result
                        )

                    # Post-order callback
                    post_order_ctx = PostOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=call_seq,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=call_seq_now,
                        col=col,
                        call_idx=k,
                        cash_before=state.cash,
                        position_before=state.position,
                        debt_before=state.debt,
                        free_cash_before=state.free_cash,
                        val_price_before=state.val_price,
                        value_before=state.value,
                        order_result=order_result,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    post_order_func_nb(post_order_ctx, *pre_segment_out, *post_order_args)

            # NOTE: Regardless of segment_mask, we still need to update stats to be accessed by future rows
            # Update valuation price
            for col in range(from_col, to_col):
                _close = flex_select_auto_nb(close, i, col, flex_2d)
                if not np.isnan(_close) or not ffill_val_price:
                    last_val_price[col] = _close

            # Update previous value, current value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                second_last_value[group] = temp_value[group]
                temp_value[group] = last_value[group]
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    second_last_value[col] = temp_value[col]
                    temp_value[col] = last_value[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Is this segment active?
            if call_post_segment or segment_mask[i, group]:
                # Call function after the segment
                post_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=call_seq_now
                )
                post_segment_func_nb(post_seg_ctx, *pre_row_out, *post_segment_args)

            from_col = to_col

        # Call function after the row
        post_row_ctx = RowContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            i=i
        )
        post_row_func_nb(post_row_ctx, *pre_sim_out, *post_row_args)

    # Call function after the simulation
    post_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=call_seq,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    post_sim_func_nb(post_sim_ctx, *post_sim_args)

    return order_records[:oidx], log_records[:lidx]


@njit
def no_flex_order_func_nb(c: FlexOrderContext, *args) -> tp.Tuple[int, Order]:
    """Placeholder flexible order function that returns break column and no order."""
    return -1, NoOrder


FlexOrderFuncT = tp.Callable[[FlexOrderContext, tp.VarArg()], tp.Tuple[int, Order]]


@njit
def flex_simulate_nb(target_shape: tp.Shape,
                     group_lens: tp.Array1d,
                     init_cash: tp.Array1d,
                     cash_sharing: bool,
                     segment_mask: tp.ArrayLike = np.asarray(True),
                     call_pre_segment: bool = False,
                     call_post_segment: bool = False,
                     pre_sim_func_nb: PreSimFuncT = no_pre_func_nb,
                     pre_sim_args: tp.Args = (),
                     post_sim_func_nb: PostSimFuncT = no_post_func_nb,
                     post_sim_args: tp.Args = (),
                     pre_group_func_nb: PreGroupFuncT = no_pre_func_nb,
                     pre_group_args: tp.Args = (),
                     post_group_func_nb: PostGroupFuncT = no_post_func_nb,
                     post_group_args: tp.Args = (),
                     pre_segment_func_nb: PreSegmentFuncT = no_pre_func_nb,
                     pre_segment_args: tp.Args = (),
                     post_segment_func_nb: PostSegmentFuncT = no_post_func_nb,
                     post_segment_args: tp.Args = (),
                     flex_order_func_nb: FlexOrderFuncT = no_flex_order_func_nb,
                     flex_order_args: tp.Args = (),
                     post_order_func_nb: PostOrderFuncT = no_post_func_nb,
                     post_order_args: tp.Args = (),
                     close: tp.ArrayLike = np.asarray(np.nan),
                     ffill_val_price: bool = True,
                     update_value: bool = False,
                     fill_pos_record: bool = True,
                     max_orders: tp.Optional[int] = None,
                     max_logs: int = 0,
                     flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Same as `simulate_nb`, but with no predefined call sequence.

    In contrast to `order_func_nb` in`simulate_nb`, `post_order_func_nb` is a segment-level order function
    that returns a column along with the order, and gets repeatedly called until some condition is met.
    This allows multiple orders to be issued within a single element and in an arbitrary order.

    The order function should accept `vectorbt.portfolio.enums.FlexOrderContext`, unpacked tuple from
    `pre_segment_func_nb`, and `*flex_order_args`. Should return column and `vectorbt.portfolio.enums.Order`.
    To break out of the loop, return column of -1.

    !!! note
        Since one element can now accommodate multiple orders, you may run into "order_records index out of range"
        exception. In this case, you should increase `max_orders`. This cannot be done automatically and
        dynamically to avoid performance degradation.

    Usage:
        * The same example as in `simulate_nb`:

        ```pycon
        >>> import numpy as np
        >>> from numba import njit
        >>> from vectorbt.portfolio.enums import SizeType, Direction
        >>> from vectorbt.portfolio.nb import (
        ...     get_col_elem_nb,
        ...     order_nb,
        ...     order_nothing_nb,
        ...     flex_simulate_nb,
        ...     flex_simulate_row_wise_nb,
        ...     sort_call_seq_out_nb
        ... )

        >>> @njit
        ... def pre_sim_func_nb(c):
        ...     print('before simulation')
        ...     return ()

        >>> @njit
        ... def pre_group_func_nb(c):
        ...     print('\\tbefore group', c.group)
        ...     # Create temporary arrays and pass them down the stack
        ...     order_value_out = np.empty(c.group_len, dtype=np.float64)
        ...     call_seq_out = np.empty(c.group_len, dtype=np.int64)
        ...     # Forward down the stack
        ...     return (order_value_out, call_seq_out)

        >>> @njit
        ... def pre_segment_func_nb(c, order_value_out, call_seq_out, size, price, size_type, direction):
        ...     print('\\t\\tbefore segment', c.i)
        ...     for col in range(c.from_col, c.to_col):
        ...         # Here we use order price for group valuation
        ...         c.last_val_price[col] = get_col_elem_nb(c, col, price)
        ...
        ...     # Same as for simulate_nb, but since we don't have a predefined c.call_seq_now anymore,
        ...     # we need to store our new call sequence somewhere else
        ...     call_seq_out[:] = np.arange(c.group_len)
        ...     sort_call_seq_out_nb(c, size, size_type, direction, order_value_out, call_seq_out)
        ...
        ...     # Forward the sorted call sequence
        ...     return (call_seq_out,)

        >>> @njit
        ... def flex_order_func_nb(c, call_seq_out, size, price, size_type, direction, fees, fixed_fees, slippage):
        ...     if c.call_idx < c.group_len:
        ...         col = c.from_col + call_seq_out[c.call_idx]
        ...         print('\\t\\t\\tcreating order', c.call_idx, 'at column', col)
        ...         # # Create and return an order
        ...         return col, order_nb(
        ...             size=get_col_elem_nb(c, col, size),
        ...             price=get_col_elem_nb(c, col, price),
        ...             size_type=get_col_elem_nb(c, col, size_type),
        ...             direction=get_col_elem_nb(c, col, direction),
        ...             fees=get_col_elem_nb(c, col, fees),
        ...             fixed_fees=get_col_elem_nb(c, col, fixed_fees),
        ...             slippage=get_col_elem_nb(c, col, slippage)
        ...         )
        ...     # All columns already processed -> break the loop
        ...     print('\\t\\t\\tbreaking out of the loop')
        ...     return -1, order_nothing_nb()

        >>> @njit
        ... def post_order_func_nb(c, call_seq_out):
        ...     print('\\t\\t\\t\\torder status:', c.order_result.status)
        ...     return None

        >>> @njit
        ... def post_segment_func_nb(c, order_value_out, call_seq_out):
        ...     print('\\t\\tafter segment', c.i)
        ...     return None

        >>> @njit
        ... def post_group_func_nb(c):
        ...     print('\\tafter group', c.group)
        ...     return None

        >>> @njit
        ... def post_sim_func_nb(c):
        ...     print('after simulation')
        ...     return None

        >>> target_shape = (5, 3)
        >>> np.random.seed(42)
        >>> group_lens = np.array([3])  # one group of three columns
        >>> init_cash = np.array([100.])  # one capital per group
        >>> cash_sharing = True
        >>> call_seq = build_call_seq(target_shape, group_lens)  # will be overridden
        >>> segment_mask = np.array([True, False, True, False, True])[:, None]
        >>> segment_mask = np.copy(np.broadcast_to(segment_mask, target_shape))
        >>> size = np.asarray(1 / target_shape[1])  # scalars must become 0-dim arrays
        >>> price = close = np.random.uniform(1, 10, size=target_shape)
        >>> size_type = np.asarray(SizeType.TargetPercent)
        >>> direction = np.asarray(Direction.LongOnly)
        >>> fees = np.asarray(0.001)
        >>> fixed_fees = np.asarray(1.)
        >>> slippage = np.asarray(0.001)

        >>> order_records, log_records = flex_simulate_nb(
        ...     target_shape,
        ...     group_lens,
        ...     init_cash,
        ...     cash_sharing,
        ...     segment_mask=segment_mask,
        ...     pre_sim_func_nb=pre_sim_func_nb,
        ...     post_sim_func_nb=post_sim_func_nb,
        ...     pre_group_func_nb=pre_group_func_nb,
        ...     post_group_func_nb=post_group_func_nb,
        ...     pre_segment_func_nb=pre_segment_func_nb,
        ...     pre_segment_args=(size, price, size_type, direction),
        ...     post_segment_func_nb=post_segment_func_nb,
        ...     flex_order_func_nb=flex_order_func_nb,
        ...     flex_order_args=(size, price, size_type, direction, fees, fixed_fees, slippage),
        ...     post_order_func_nb=post_order_func_nb
        ... )
        before simulation
            before group 0
                before segment 0
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 1
                        order status: 0
                    creating order 2 at column 2
                        order status: 0
                    breaking out of the loop
                after segment 0
                before segment 2
                    creating order 0 at column 1
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 0
                        order status: 0
                    breaking out of the loop
                after segment 2
                before segment 4
                    creating order 0 at column 0
                        order status: 0
                    creating order 1 at column 2
                        order status: 0
                    creating order 2 at column 1
                        order status: 0
                    breaking out of the loop
                after segment 4
            after group 0
        after simulation
        ```
    """

    check_group_lens_nb(group_lens, target_shape[1])
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_cash = init_cash.copy()
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_free_cash = init_cash.copy()
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    last_value = init_cash.copy()
    second_last_value = init_cash.copy()
    temp_value = init_cash.copy()
    last_return = np.full_like(last_value, np.nan)
    last_pos_record = np.empty(target_shape[1], dtype=trade_dt)
    last_pos_record['id'][:] = -1
    last_oidx = np.full(target_shape[1], -1, dtype=np.int64)
    last_lidx = np.full(target_shape[1], -1, dtype=np.int64)
    oidx = 0
    lidx = 0

    # Call function before the simulation
    pre_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=None,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    pre_sim_out = pre_sim_func_nb(pre_sim_ctx, *pre_sim_args)

    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col

        # Call function before the group
        pre_group_ctx = GroupContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=None,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            group=group,
            group_len=group_len,
            from_col=from_col,
            to_col=to_col
        )
        pre_group_out = pre_group_func_nb(pre_group_ctx, *pre_sim_out, *pre_group_args)

        for i in range(target_shape[0]):
            # Is this segment active?
            if call_pre_segment or segment_mask[i, group]:
                # Call function before the segment
                pre_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=None,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=None
                )
                pre_segment_out = pre_segment_func_nb(pre_seg_ctx, *pre_group_out, *pre_segment_args)

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Update value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Is this segment active?
            if segment_mask[i, group]:

                call_idx = -1
                while True:
                    call_idx += 1

                    # Generate the next order
                    flex_order_ctx = FlexOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=None,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=None,
                        call_idx=call_idx
                    )
                    col, order = flex_order_func_nb(flex_order_ctx, *pre_segment_out, *flex_order_args)

                    if col == -1:
                        break
                    if col < from_col or col >= to_col:
                        raise ValueError("Column exceeds bounds of the group")

                    # Get current values
                    position_now = last_position[col]
                    debt_now = last_debt[col]
                    val_price_now = last_val_price[col]
                    pos_record_now = last_pos_record[col]
                    if cash_sharing:
                        cash_now = last_cash[group]
                        free_cash_now = last_free_cash[group]
                        value_now = last_value[group]
                        return_now = last_return[group]
                    else:
                        cash_now = last_cash[col]
                        free_cash_now = last_free_cash[col]
                        value_now = last_value[col]
                        return_now = last_return[col]

                    if np.isinf(order.price):
                        if i > 0:
                            _prev_close = flex_select_auto_nb(close, i - 1, col, flex_2d)
                        else:
                            _prev_close = np.nan
                        _close = flex_select_auto_nb(close, i, col, flex_2d)
                        order = replace_inf_price_nb(_prev_close, _close, order)

                    # Process the order
                    state = ProcessOrderState(
                        cash=cash_now,
                        position=position_now,
                        debt=debt_now,
                        free_cash=free_cash_now,
                        val_price=val_price_now,
                        value=value_now,
                        oidx=oidx,
                        lidx=lidx
                    )

                    order_result, new_state = process_order_nb(
                        i, col, group,
                        state,
                        update_value,
                        order,
                        order_records,
                        log_records
                    )

                    # Update state
                    cash_now = new_state.cash
                    position_now = new_state.position
                    debt_now = new_state.debt
                    free_cash_now = new_state.free_cash
                    val_price_now = new_state.val_price
                    value_now = new_state.value
                    if cash_sharing:
                        return_now = returns_nb.get_return_nb(second_last_value[group], value_now)
                    else:
                        return_now = returns_nb.get_return_nb(second_last_value[col], value_now)
                    oidx = new_state.oidx
                    lidx = new_state.lidx

                    # Now becomes last
                    last_position[col] = position_now
                    last_debt[col] = debt_now
                    if not np.isnan(val_price_now) or not ffill_val_price:
                        last_val_price[col] = val_price_now
                    if cash_sharing:
                        last_cash[group] = cash_now
                        last_free_cash[group] = free_cash_now
                        last_value[group] = value_now
                        last_return[group] = return_now
                    else:
                        last_cash[col] = cash_now
                        last_free_cash[col] = free_cash_now
                        last_value[col] = value_now
                        last_return[col] = return_now
                    if state.oidx != new_state.oidx:
                        last_oidx[col] = state.oidx
                    if state.lidx != new_state.lidx:
                        last_lidx[col] = state.lidx

                    # Update position record
                    if fill_pos_record:
                        update_pos_record_nb(
                            pos_record_now,
                            i, col,
                            state.position, position_now,
                            order_result
                        )

                    # Post-order callback
                    post_order_ctx = PostOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=None,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=None,
                        col=col,
                        call_idx=call_idx,
                        cash_before=state.cash,
                        position_before=state.position,
                        debt_before=state.debt,
                        free_cash_before=state.free_cash,
                        val_price_before=state.val_price,
                        value_before=state.value,
                        order_result=order_result,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    post_order_func_nb(post_order_ctx, *pre_segment_out, *post_order_args)

            # NOTE: Regardless of segment_mask, we still need to update stats to be accessed by future rows
            # Update valuation price
            for col in range(from_col, to_col):
                _close = flex_select_auto_nb(close, i, col, flex_2d)
                if not np.isnan(_close) or not ffill_val_price:
                    last_val_price[col] = _close

            # Update previous value, current value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                second_last_value[group] = temp_value[group]
                temp_value[group] = last_value[group]
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    second_last_value[col] = temp_value[col]
                    temp_value[col] = last_value[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Is this segment active?
            if call_post_segment or segment_mask[i, group]:
                # Call function before the segment
                post_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=None,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=None
                )
                post_segment_func_nb(post_seg_ctx, *pre_group_out, *post_segment_args)

        # Call function after the group
        post_group_ctx = GroupContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=None,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            group=group,
            group_len=group_len,
            from_col=from_col,
            to_col=to_col
        )
        post_group_func_nb(post_group_ctx, *pre_sim_out, *post_group_args)

        from_col = to_col

    # Call function after the simulation
    post_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=None,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    post_sim_func_nb(post_sim_ctx, *post_sim_args)

    return order_records[:oidx], log_records[:lidx]


@njit
def flex_simulate_row_wise_nb(target_shape: tp.Shape,
                              group_lens: tp.Array1d,
                              init_cash: tp.Array1d,
                              cash_sharing: bool,
                              segment_mask: tp.ArrayLike = np.asarray(True),
                              call_pre_segment: bool = False,
                              call_post_segment: bool = False,
                              pre_sim_func_nb: PreSimFuncT = no_pre_func_nb,
                              pre_sim_args: tp.Args = (),
                              post_sim_func_nb: PostSimFuncT = no_post_func_nb,
                              post_sim_args: tp.Args = (),
                              pre_row_func_nb: PreRowFuncT = no_pre_func_nb,
                              pre_row_args: tp.Args = (),
                              post_row_func_nb: PostRowFuncT = no_post_func_nb,
                              post_row_args: tp.Args = (),
                              pre_segment_func_nb: PreSegmentFuncT = no_pre_func_nb,
                              pre_segment_args: tp.Args = (),
                              post_segment_func_nb: PostSegmentFuncT = no_post_func_nb,
                              post_segment_args: tp.Args = (),
                              flex_order_func_nb: FlexOrderFuncT = no_flex_order_func_nb,
                              flex_order_args: tp.Args = (),
                              post_order_func_nb: PostOrderFuncT = no_post_func_nb,
                              post_order_args: tp.Args = (),
                              close: tp.ArrayLike = np.asarray(np.nan),
                              ffill_val_price: bool = True,
                              update_value: bool = False,
                              fill_pos_record: bool = True,
                              max_orders: tp.Optional[int] = None,
                              max_logs: int = 0,
                              flex_2d: bool = True) -> tp.Tuple[tp.RecordArray, tp.RecordArray]:
    """Same as `flex_simulate_nb`, but iterates using row-major order, with the rows
    changing fastest, and the columns/groups changing slowest."""

    check_group_lens_nb(group_lens, target_shape[1])
    check_group_init_cash_nb(group_lens, target_shape[1], init_cash, cash_sharing)

    order_records, log_records = init_records_nb(target_shape, max_orders, max_logs)
    init_cash = init_cash.astype(np.float64)
    last_cash = init_cash.copy()
    last_position = np.full(target_shape[1], 0., dtype=np.float64)
    last_debt = np.full(target_shape[1], 0., dtype=np.float64)
    last_free_cash = init_cash.copy()
    last_val_price = np.full(target_shape[1], np.nan, dtype=np.float64)
    last_value = init_cash.copy()
    second_last_value = init_cash.copy()
    temp_value = init_cash.copy()
    last_return = np.full_like(last_value, np.nan)
    last_pos_record = np.empty(target_shape[1], dtype=trade_dt)
    last_pos_record['id'][:] = -1
    last_oidx = np.full(target_shape[1], -1, dtype=np.int64)
    last_lidx = np.full(target_shape[1], -1, dtype=np.int64)
    oidx = 0
    lidx = 0

    # Call function before the simulation
    pre_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=None,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    pre_sim_out = pre_sim_func_nb(pre_sim_ctx, *pre_sim_args)

    for i in range(target_shape[0]):

        # Call function before the row
        pre_row_ctx = RowContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=None,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            i=i
        )
        pre_row_out = pre_row_func_nb(pre_row_ctx, *pre_sim_out, *pre_row_args)

        from_col = 0
        for group in range(len(group_lens)):
            to_col = from_col + group_lens[group]
            group_len = to_col - from_col

            # Is this segment active?
            if call_pre_segment or segment_mask[i, group]:
                # Call function before the segment
                pre_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=None,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=None
                )
                pre_segment_out = pre_segment_func_nb(pre_seg_ctx, *pre_row_out, *pre_segment_args)

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Update value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Is this segment active?
            if segment_mask[i, group]:

                call_idx = -1
                while True:
                    call_idx += 1

                    # Generate the next order
                    flex_order_ctx = FlexOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=None,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=None,
                        call_idx=call_idx
                    )
                    col, order = flex_order_func_nb(flex_order_ctx, *pre_segment_out, *flex_order_args)

                    if col == -1:
                        break
                    if col < from_col or col >= to_col:
                        raise ValueError("Column exceeds bounds of the group")

                    # Get current values
                    position_now = last_position[col]
                    debt_now = last_debt[col]
                    val_price_now = last_val_price[col]
                    pos_record_now = last_pos_record[col]
                    if cash_sharing:
                        cash_now = last_cash[group]
                        free_cash_now = last_free_cash[group]
                        value_now = last_value[group]
                        return_now = last_return[group]
                    else:
                        cash_now = last_cash[col]
                        free_cash_now = last_free_cash[col]
                        value_now = last_value[col]
                        return_now = last_return[col]

                    if np.isinf(order.price):
                        if i > 0:
                            _prev_close = flex_select_auto_nb(close, i - 1, col, flex_2d)
                        else:
                            _prev_close = np.nan
                        _close = flex_select_auto_nb(close, i, col, flex_2d)
                        order = replace_inf_price_nb(_prev_close, _close, order)

                    # Process the order
                    state = ProcessOrderState(
                        cash=cash_now,
                        position=position_now,
                        debt=debt_now,
                        free_cash=free_cash_now,
                        val_price=val_price_now,
                        value=value_now,
                        oidx=oidx,
                        lidx=lidx
                    )

                    order_result, new_state = process_order_nb(
                        i, col, group,
                        state,
                        update_value,
                        order,
                        order_records,
                        log_records
                    )

                    # Update state
                    cash_now = new_state.cash
                    position_now = new_state.position
                    debt_now = new_state.debt
                    free_cash_now = new_state.free_cash
                    val_price_now = new_state.val_price
                    value_now = new_state.value
                    if cash_sharing:
                        return_now = returns_nb.get_return_nb(second_last_value[group], value_now)
                    else:
                        return_now = returns_nb.get_return_nb(second_last_value[col], value_now)
                    oidx = new_state.oidx
                    lidx = new_state.lidx

                    # Now becomes last
                    last_position[col] = position_now
                    last_debt[col] = debt_now
                    if not np.isnan(val_price_now) or not ffill_val_price:
                        last_val_price[col] = val_price_now
                    if cash_sharing:
                        last_cash[group] = cash_now
                        last_free_cash[group] = free_cash_now
                        last_value[group] = value_now
                        last_return[group] = return_now
                    else:
                        last_cash[col] = cash_now
                        last_free_cash[col] = free_cash_now
                        last_value[col] = value_now
                        last_return[col] = return_now
                    if state.oidx != new_state.oidx:
                        last_oidx[col] = state.oidx
                    if state.lidx != new_state.lidx:
                        last_lidx[col] = state.lidx

                    # Update position record
                    if fill_pos_record:
                        update_pos_record_nb(
                            pos_record_now,
                            i, col,
                            state.position, position_now,
                            order_result
                        )

                    # Post-order callback
                    post_order_ctx = PostOrderContext(
                        target_shape=target_shape,
                        group_lens=group_lens,
                        init_cash=init_cash,
                        cash_sharing=cash_sharing,
                        call_seq=None,
                        segment_mask=segment_mask,
                        call_pre_segment=call_pre_segment,
                        call_post_segment=call_post_segment,
                        close=close,
                        ffill_val_price=ffill_val_price,
                        update_value=update_value,
                        fill_pos_record=fill_pos_record,
                        flex_2d=flex_2d,
                        order_records=order_records,
                        log_records=log_records,
                        last_cash=last_cash,
                        last_position=last_position,
                        last_debt=last_debt,
                        last_free_cash=last_free_cash,
                        last_val_price=last_val_price,
                        last_value=last_value,
                        second_last_value=second_last_value,
                        last_return=last_return,
                        last_oidx=last_oidx,
                        last_lidx=last_lidx,
                        last_pos_record=last_pos_record,
                        group=group,
                        group_len=group_len,
                        from_col=from_col,
                        to_col=to_col,
                        i=i,
                        call_seq_now=None,
                        col=col,
                        call_idx=call_idx,
                        cash_before=state.cash,
                        position_before=state.position,
                        debt_before=state.debt,
                        free_cash_before=state.free_cash,
                        val_price_before=state.val_price,
                        value_before=state.value,
                        order_result=order_result,
                        cash_now=cash_now,
                        position_now=position_now,
                        debt_now=debt_now,
                        free_cash_now=free_cash_now,
                        val_price_now=val_price_now,
                        value_now=value_now,
                        return_now=return_now,
                        pos_record_now=pos_record_now
                    )
                    post_order_func_nb(post_order_ctx, *pre_segment_out, *post_order_args)

            # NOTE: Regardless of segment_mask, we still need to update stats to be accessed by future rows
            # Update valuation price
            for col in range(from_col, to_col):
                _close = flex_select_auto_nb(close, i, col, flex_2d)
                if not np.isnan(_close) or not ffill_val_price:
                    last_val_price[col] = _close

            # Update previous value, current value and return
            if cash_sharing:
                last_value[group] = get_group_value_nb(
                    from_col,
                    to_col,
                    last_cash[group],
                    last_position,
                    last_val_price
                )
                second_last_value[group] = temp_value[group]
                temp_value[group] = last_value[group]
                last_return[group] = returns_nb.get_return_nb(second_last_value[group], last_value[group])
            else:
                for col in range(from_col, to_col):
                    if last_position[col] == 0:
                        last_value[col] = last_cash[col]
                    else:
                        last_value[col] = last_cash[col] + last_position[col] * last_val_price[col]
                    second_last_value[col] = temp_value[col]
                    temp_value[col] = last_value[col]
                    last_return[col] = returns_nb.get_return_nb(second_last_value[col], last_value[col])

            # Update open position stats
            if fill_pos_record:
                for col in range(from_col, to_col):
                    update_open_pos_stats_nb(
                        last_pos_record[col],
                        last_position[col],
                        last_val_price[col]
                    )

            # Is this segment active?
            if call_post_segment or segment_mask[i, group]:
                # Call function after the segment
                post_seg_ctx = SegmentContext(
                    target_shape=target_shape,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=None,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    close=close,
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    flex_2d=flex_2d,
                    order_records=order_records,
                    log_records=log_records,
                    last_cash=last_cash,
                    last_position=last_position,
                    last_debt=last_debt,
                    last_free_cash=last_free_cash,
                    last_val_price=last_val_price,
                    last_value=last_value,
                    second_last_value=second_last_value,
                    last_return=last_return,
                    last_oidx=last_oidx,
                    last_lidx=last_lidx,
                    last_pos_record=last_pos_record,
                    group=group,
                    group_len=group_len,
                    from_col=from_col,
                    to_col=to_col,
                    i=i,
                    call_seq_now=None
                )
                post_segment_func_nb(post_seg_ctx, *pre_row_out, *post_segment_args)

            from_col = to_col

        # Call function after the row
        post_row_ctx = RowContext(
            target_shape=target_shape,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=None,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            close=close,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            flex_2d=flex_2d,
            order_records=order_records,
            log_records=log_records,
            last_cash=last_cash,
            last_position=last_position,
            last_debt=last_debt,
            last_free_cash=last_free_cash,
            last_val_price=last_val_price,
            last_value=last_value,
            second_last_value=second_last_value,
            last_return=last_return,
            last_oidx=last_oidx,
            last_lidx=last_lidx,
            last_pos_record=last_pos_record,
            i=i
        )
        post_row_func_nb(post_row_ctx, *pre_sim_out, *post_row_args)

    # Call function after the simulation
    post_sim_ctx = SimulationContext(
        target_shape=target_shape,
        group_lens=group_lens,
        init_cash=init_cash,
        cash_sharing=cash_sharing,
        call_seq=None,
        segment_mask=segment_mask,
        call_pre_segment=call_pre_segment,
        call_post_segment=call_post_segment,
        close=close,
        ffill_val_price=ffill_val_price,
        update_value=update_value,
        fill_pos_record=fill_pos_record,
        flex_2d=flex_2d,
        order_records=order_records,
        log_records=log_records,
        last_cash=last_cash,
        last_position=last_position,
        last_debt=last_debt,
        last_free_cash=last_free_cash,
        last_val_price=last_val_price,
        last_value=last_value,
        second_last_value=second_last_value,
        last_return=last_return,
        last_oidx=last_oidx,
        last_lidx=last_lidx,
        last_pos_record=last_pos_record
    )
    post_sim_func_nb(post_sim_ctx, *post_sim_args)

    return order_records[:oidx], log_records[:lidx]


# ############# Trade records ############# #

size_zero_neg_err = "Found order with size 0 or less"
price_zero_neg_err = "Found order with price 0 or less"


@njit(cache=True)
def get_trade_stats_nb(size: float,
                       entry_price: float,
                       entry_fees: float,
                       exit_price: float,
                       exit_fees: float,
                       direction: int) -> tp.Tuple[float, float]:
    """Get trade statistics."""
    entry_val = size * entry_price
    exit_val = size * exit_price
    val_diff = add_nb(exit_val, -entry_val)
    if val_diff != 0 and direction == TradeDirection.Short:
        val_diff *= -1
    pnl = val_diff - entry_fees - exit_fees
    ret = pnl / entry_val
    return pnl, ret


@njit(cache=True)
def fill_trade_record_nb(record: tp.Record,
                         id_: int,
                         col: int,
                         size: float,
                         entry_idx: int,
                         entry_price: float,
                         entry_fees: float,
                         exit_idx: int,
                         exit_price: float,
                         exit_fees: float,
                         direction: int,
                         status: int,
                         parent_id: int) -> None:
    """Fill a trade record."""
    # Calculate PnL and return
    pnl, ret = get_trade_stats_nb(
        size,
        entry_price,
        entry_fees,
        exit_price,
        exit_fees,
        direction
    )

    # Save trade
    record['id'] = id_
    record['col'] = col
    record['size'] = size
    record['entry_idx'] = entry_idx
    record['entry_price'] = entry_price
    record['entry_fees'] = entry_fees
    record['exit_idx'] = exit_idx
    record['exit_price'] = exit_price
    record['exit_fees'] = exit_fees
    record['pnl'] = pnl
    record['return'] = ret
    record['direction'] = direction
    record['status'] = status
    record['parent_id'] = parent_id


@njit(cache=True)
def fill_entry_trades_in_position_nb(order_records: tp.RecordArray,
                                     col_map: tp.ColMap,
                                     col: int,
                                     first_c: int,
                                     last_c: int,
                                     first_entry_size: float,
                                     first_entry_fees: float,
                                     exit_idx: int,
                                     exit_size_sum: float,
                                     exit_gross_sum: float,
                                     exit_fees_sum: float,
                                     direction: int,
                                     status: int,
                                     parent_id: int,
                                     trade_records: tp.RecordArray,
                                     tidx: int) -> int:
    """Fill entry trades located within a single position."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens

    # Iterate over orders located within a single position
    for c in range(first_c, last_c + 1):
        oidx = col_idxs[col_start_idxs[col] + c]
        record = order_records[oidx]
        order_side = record['side']

        # Ignore exit orders
        if (direction == TradeDirection.Long and order_side == OrderSide.Sell) \
                or (direction == TradeDirection.Short and order_side == OrderSide.Buy):
            continue

        if c == first_c:
            entry_size = first_entry_size
            entry_fees = first_entry_fees
        else:
            entry_size = record['size']
            entry_fees = record['fees']

        # Take a size-weighted average of exit price
        exit_price = exit_gross_sum / exit_size_sum

        # Take a fraction of exit fees
        size_fraction = entry_size / exit_size_sum
        exit_fees = size_fraction * exit_fees_sum

        # Fill the record
        fill_trade_record_nb(
            trade_records[tidx],
            tidx,
            col,
            entry_size,
            record['idx'],
            record['price'],
            entry_fees,
            exit_idx,
            exit_price,
            exit_fees,
            direction,
            status,
            parent_id
        )
        tidx += 1

    return tidx


@njit(cache=True)
def get_entry_trades_nb(order_records: tp.RecordArray, close: tp.Array2d, col_map: tp.ColMap) -> tp.RecordArray:
    """Fill entry trade records by aggregating order records.

    Entry trade records are buy orders in a long position and sell orders in a short position.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from numba import njit
        >>> from vectorbt.records.nb import col_map_nb
        >>> from vectorbt.portfolio.nb import simulate_from_orders_nb, get_entry_trades_nb

        >>> close = order_price = np.array([
        ...     [1, 6],
        ...     [2, 5],
        ...     [3, 4],
        ...     [4, 3],
        ...     [5, 2],
        ...     [6, 1]
        ... ])
        >>> size = np.asarray([
        ...     [1, -1],
        ...     [0.1, -0.1],
        ...     [-1, 1],
        ...     [-0.1, 0.1],
        ...     [1, -1],
        ...     [-2, 2]
        ... ])
        >>> target_shape = close.shape
        >>> group_lens = np.full(target_shape[1], 1)
        >>> init_cash = np.full(target_shape[1], 100)
        >>> call_seq = np.full(target_shape, 0)

        >>> order_records, log_records = simulate_from_orders_nb(
        ...     target_shape,
        ...     group_lens,
        ...     init_cash,
        ...     call_seq,
        ...     size=size,
        ...     price=close,
        ...     fees=np.asarray(0.01),
        ...     slippage=np.asarray(0.01)
        ... )

        >>> col_map = col_map_nb(order_records['col'], target_shape[1])
        >>> entry_trade_records = get_entry_trades_nb(order_records, close, col_map)
        >>> pd.DataFrame.from_records(entry_trade_records)
           id  col  size  entry_idx  entry_price  entry_fees  exit_idx  exit_price  \\
        0   0    0   1.0          0         1.01     0.01010         3    3.060000
        1   1    0   0.1          1         2.02     0.00202         3    3.060000
        2   2    0   1.0          4         5.05     0.05050         5    5.940000
        3   3    0   1.0          5         5.94     0.05940         5    6.000000
        4   4    1   1.0          0         5.94     0.05940         3    3.948182
        5   5    1   0.1          1         4.95     0.00495         3    3.948182
        6   6    1   1.0          4         1.98     0.01980         5    1.010000
        7   7    1   1.0          5         1.01     0.01010         5    1.000000

           exit_fees       pnl    return  direction  status  parent_id
        0   0.030600  2.009300  1.989406          0       1          0
        1   0.003060  0.098920  0.489703          0       1          0
        2   0.059400  0.780100  0.154475          0       1          1
        3   0.000000 -0.119400 -0.020101          1       0          2
        4   0.039482  1.892936  0.318676          1       1          3
        5   0.003948  0.091284  0.184411          1       1          3
        6   0.010100  0.940100  0.474798          1       1          4
        7   0.000000 -0.020100 -0.019901          0       0          5
        ```
    """
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    records = np.empty(len(order_records), dtype=trade_dt)
    tidx = 0
    parent_id = -1

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        last_id = -1
        in_position = False

        for c in range(col_len):
            oidx = col_idxs[col_start_idxs[col] + c]
            record = order_records[oidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            order_idx = record['idx']
            order_size = record['size']
            order_price = record['price']
            order_fees = record['fees']
            order_side = record['side']

            if order_size <= 0.:
                raise ValueError(size_zero_neg_err)
            if order_price <= 0.:
                raise ValueError(price_zero_neg_err)

            if not in_position:
                # New position opened
                first_c = c
                in_position = True
                parent_id += 1
                if order_side == OrderSide.Buy:
                    direction = TradeDirection.Long
                else:
                    direction = TradeDirection.Short
                entry_size_sum = 0.
                entry_gross_sum = 0.
                entry_fees_sum = 0.
                exit_size_sum = 0.
                exit_gross_sum = 0.
                exit_fees_sum = 0.
                first_entry_size = order_size
                first_entry_fees = order_fees

            if (direction == TradeDirection.Long and order_side == OrderSide.Buy) \
                    or (direction == TradeDirection.Short and order_side == OrderSide.Sell):
                # Position increased
                entry_size_sum += order_size
                entry_gross_sum += order_size * order_price
                entry_fees_sum += order_fees

            elif (direction == TradeDirection.Long and order_side == OrderSide.Sell) \
                    or (direction == TradeDirection.Short and order_side == OrderSide.Buy):
                if is_close_nb(exit_size_sum + order_size, entry_size_sum):
                    # Position closed
                    last_c = c
                    in_position = False
                    exit_size_sum = entry_size_sum
                    exit_gross_sum += order_size * order_price
                    exit_fees_sum += order_fees

                    # Fill trade records
                    tidx = fill_entry_trades_in_position_nb(
                        order_records,
                        col_map,
                        col,
                        first_c,
                        last_c,
                        first_entry_size,
                        first_entry_fees,
                        order_idx,
                        exit_size_sum,
                        exit_gross_sum,
                        exit_fees_sum,
                        direction,
                        TradeStatus.Closed,
                        parent_id,
                        records,
                        tidx
                    )
                elif is_less_nb(exit_size_sum + order_size, entry_size_sum):
                    # Position decreased
                    exit_size_sum += order_size
                    exit_gross_sum += order_size * order_price
                    exit_fees_sum += order_fees
                else:
                    # Position closed
                    last_c = c
                    remaining_size = add_nb(entry_size_sum, -exit_size_sum)
                    exit_size_sum = entry_size_sum
                    exit_gross_sum += remaining_size * order_price
                    exit_fees_sum += remaining_size / order_size * order_fees

                    # Fill trade records
                    tidx = fill_entry_trades_in_position_nb(
                        order_records,
                        col_map,
                        col,
                        first_c,
                        last_c,
                        first_entry_size,
                        first_entry_fees,
                        order_idx,
                        exit_size_sum,
                        exit_gross_sum,
                        exit_fees_sum,
                        direction,
                        TradeStatus.Closed,
                        parent_id,
                        records,
                        tidx
                    )

                    # New position opened
                    first_c = c
                    parent_id += 1
                    if order_side == OrderSide.Buy:
                        direction = TradeDirection.Long
                    else:
                        direction = TradeDirection.Short
                    entry_size_sum = add_nb(order_size, -remaining_size)
                    entry_gross_sum = entry_size_sum * order_price
                    entry_fees_sum = entry_size_sum / order_size * order_fees
                    first_entry_size = entry_size_sum
                    first_entry_fees = entry_fees_sum
                    exit_size_sum = 0.
                    exit_gross_sum = 0.
                    exit_fees_sum = 0.

        if in_position and is_less_nb(exit_size_sum, entry_size_sum):
            # Position hasn't been closed
            last_c = col_len - 1
            remaining_size = add_nb(entry_size_sum, -exit_size_sum)
            exit_size_sum = entry_size_sum
            exit_gross_sum += remaining_size * close[close.shape[0] - 1, col]

            # Fill trade records
            tidx = fill_entry_trades_in_position_nb(
                order_records,
                col_map,
                col,
                first_c,
                last_c,
                first_entry_size,
                first_entry_fees,
                close.shape[0] - 1,
                exit_size_sum,
                exit_gross_sum,
                exit_fees_sum,
                direction,
                TradeStatus.Open,
                parent_id,
                records,
                tidx
            )

    return records[:tidx]


@njit(cache=True)
def get_exit_trades_nb(order_records: tp.RecordArray, close: tp.Array2d, col_map: tp.ColMap) -> tp.RecordArray:
    """Fill exit trade records by aggregating order records.

    Exit trade records are sell orders in a long position and buy orders in a short position.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from numba import njit
        >>> from vectorbt.records.nb import col_map_nb
        >>> from vectorbt.portfolio.nb import simulate_from_orders_nb, get_exit_trades_nb

        >>> close = order_price = np.array([
        ...     [1, 6],
        ...     [2, 5],
        ...     [3, 4],
        ...     [4, 3],
        ...     [5, 2],
        ...     [6, 1]
        ... ])
        >>> size = np.asarray([
        ...     [1, -1],
        ...     [0.1, -0.1],
        ...     [-1, 1],
        ...     [-0.1, 0.1],
        ...     [1, -1],
        ...     [-2, 2]
        ... ])
        >>> target_shape = close.shape
        >>> group_lens = np.full(target_shape[1], 1)
        >>> init_cash = np.full(target_shape[1], 100)
        >>> call_seq = np.full(target_shape, 0)

        >>> order_records, log_records = simulate_from_orders_nb(
        ...     target_shape,
        ...     group_lens,
        ...     init_cash,
        ...     call_seq,
        ...     size=size,
        ...     price=close,
        ...     fees=np.asarray(0.01),
        ...     slippage=np.asarray(0.01)
        ... )

        >>> col_map = col_map_nb(order_records['col'], target_shape[1])
        >>> exit_trade_records = get_exit_trades_nb(order_records, close, col_map)
        >>> pd.DataFrame.from_records(exit_trade_records)
           id  col  size  entry_idx  entry_price  entry_fees  exit_idx  exit_price  \\
        0   0    0   1.0          0     1.101818    0.011018         2        2.97
        1   1    0   0.1          0     1.101818    0.001102         3        3.96
        2   2    0   1.0          4     5.050000    0.050500         5        5.94
        3   3    0   1.0          5     5.940000    0.059400         5        6.00
        4   4    1   1.0          0     5.850000    0.058500         2        4.04
        5   5    1   0.1          0     5.850000    0.005850         3        3.03
        6   6    1   1.0          4     1.980000    0.019800         5        1.01
        7   7    1   1.0          5     1.010000    0.010100         5        1.00

           exit_fees       pnl    return  direction  status  parent_id
        0    0.02970  1.827464  1.658589          0       1          0
        1    0.00396  0.280756  2.548119          0       1          0
        2    0.05940  0.780100  0.154475          0       1          1
        3    0.00000 -0.119400 -0.020101          1       0          2
        4    0.04040  1.711100  0.292496          1       1          3
        5    0.00303  0.273120  0.466872          1       1          3
        6    0.01010  0.940100  0.474798          1       1          4
        7    0.00000 -0.020100 -0.019901          0       0          5
        ```
    """
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    records = np.empty(len(order_records), dtype=trade_dt)
    tidx = 0
    parent_id = -1

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        last_id = -1
        in_position = False

        for c in range(col_len):
            oidx = col_idxs[col_start_idxs[col] + c]
            record = order_records[oidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            i = record['idx']
            order_size = record['size']
            order_price = record['price']
            order_fees = record['fees']
            order_side = record['side']

            if order_size <= 0.:
                raise ValueError(size_zero_neg_err)
            if order_price <= 0.:
                raise ValueError(price_zero_neg_err)

            if not in_position:
                # Trade opened
                in_position = True
                entry_idx = i
                if order_side == OrderSide.Buy:
                    direction = TradeDirection.Long
                else:
                    direction = TradeDirection.Short
                parent_id += 1
                entry_size_sum = 0.
                entry_gross_sum = 0.
                entry_fees_sum = 0.

            if (direction == TradeDirection.Long and order_side == OrderSide.Buy) \
                    or (direction == TradeDirection.Short and order_side == OrderSide.Sell):
                # Position increased
                entry_size_sum += order_size
                entry_gross_sum += order_size * order_price
                entry_fees_sum += order_fees

            elif (direction == TradeDirection.Long and order_side == OrderSide.Sell) \
                    or (direction == TradeDirection.Short and order_side == OrderSide.Buy):
                if is_close_or_less_nb(order_size, entry_size_sum):
                    # Trade closed
                    if is_close_nb(order_size, entry_size_sum):
                        exit_size = entry_size_sum
                    else:
                        exit_size = order_size
                    exit_price = order_price
                    exit_fees = order_fees
                    exit_idx = i

                    # Take a size-weighted average of entry price
                    entry_price = entry_gross_sum / entry_size_sum

                    # Take a fraction of entry fees
                    size_fraction = exit_size / entry_size_sum
                    entry_fees = size_fraction * entry_fees_sum

                    fill_trade_record_nb(
                        records[tidx],
                        tidx,
                        col,
                        exit_size,
                        entry_idx,
                        entry_price,
                        entry_fees,
                        exit_idx,
                        exit_price,
                        exit_fees,
                        direction,
                        TradeStatus.Closed,
                        parent_id
                    )
                    tidx += 1

                    if is_close_nb(order_size, entry_size_sum):
                        # Position closed
                        entry_idx = -1
                        direction = -1
                        in_position = False
                    else:
                        # Position decreased, previous orders have now less impact
                        size_fraction = (entry_size_sum - order_size) / entry_size_sum
                        entry_size_sum *= size_fraction
                        entry_gross_sum *= size_fraction
                        entry_fees_sum *= size_fraction
                else:
                    # Trade reversed
                    # Close current trade
                    cl_exit_size = entry_size_sum
                    cl_exit_price = order_price
                    cl_exit_fees = cl_exit_size / order_size * order_fees
                    cl_exit_idx = i

                    # Take a size-weighted average of entry price
                    entry_price = entry_gross_sum / entry_size_sum

                    # Take a fraction of entry fees
                    size_fraction = cl_exit_size / entry_size_sum
                    entry_fees = size_fraction * entry_fees_sum

                    fill_trade_record_nb(
                        records[tidx],
                        tidx,
                        col,
                        cl_exit_size,
                        entry_idx,
                        entry_price,
                        entry_fees,
                        cl_exit_idx,
                        cl_exit_price,
                        cl_exit_fees,
                        direction,
                        TradeStatus.Closed,
                        parent_id
                    )
                    tidx += 1

                    # Open a new trade
                    entry_size_sum = order_size - cl_exit_size
                    entry_gross_sum = entry_size_sum * order_price
                    entry_fees_sum = order_fees - cl_exit_fees
                    entry_idx = i
                    if direction == TradeDirection.Long:
                        direction = TradeDirection.Short
                    else:
                        direction = TradeDirection.Long
                    parent_id += 1

        if in_position and is_less_nb(-entry_size_sum, 0):
            # Trade hasn't been closed
            exit_size = entry_size_sum
            exit_price = close[close.shape[0] - 1, col]
            exit_fees = 0.
            exit_idx = close.shape[0] - 1

            # Take a size-weighted average of entry price
            entry_price = entry_gross_sum / entry_size_sum

            # Take a fraction of entry fees
            size_fraction = exit_size / entry_size_sum
            entry_fees = size_fraction * entry_fees_sum

            fill_trade_record_nb(
                records[tidx],
                tidx,
                col,
                exit_size,
                entry_idx,
                entry_price,
                entry_fees,
                exit_idx,
                exit_price,
                exit_fees,
                direction,
                TradeStatus.Open,
                parent_id
            )
            tidx += 1

    return records[:tidx]


@njit(cache=True)
def trade_winning_streak_nb(records: tp.RecordArray) -> tp.Array1d:
    """Return the current winning streak of each trade."""
    out = np.full(len(records), 0, dtype=np.int64)
    curr_rank = 0
    for i in range(len(records)):
        if records[i]['pnl'] > 0:
            curr_rank += 1
        else:
            curr_rank = 0
        out[i] = curr_rank
    return out


@njit(cache=True)
def trade_losing_streak_nb(records: tp.RecordArray) -> tp.Array1d:
    """Return the current losing streak of each trade."""
    out = np.full(len(records), 0, dtype=np.int64)
    curr_rank = 0
    for i in range(len(records)):
        if records[i]['pnl'] < 0:
            curr_rank += 1
        else:
            curr_rank = 0
        out[i] = curr_rank
    return out


# ############# Position records ############# #

@njit(cache=True)
def fill_position_record_nb(record: tp.Record, id_: int, trade_records: tp.RecordArray) -> None:
    """Fill a position record by aggregating trade records."""
    # Aggregate trades
    col = trade_records['col'][0]
    size = np.sum(trade_records['size'])
    entry_idx = trade_records['entry_idx'][0]
    entry_price = np.sum(trade_records['size'] * trade_records['entry_price']) / size
    entry_fees = np.sum(trade_records['entry_fees'])
    exit_idx = trade_records['exit_idx'][-1]
    exit_price = np.sum(trade_records['size'] * trade_records['exit_price']) / size
    exit_fees = np.sum(trade_records['exit_fees'])
    direction = trade_records['direction'][-1]
    status = trade_records['status'][-1]
    pnl, ret = get_trade_stats_nb(
        size,
        entry_price,
        entry_fees,
        exit_price,
        exit_fees,
        direction
    )

    # Save position
    record['id'] = id_
    record['col'] = col
    record['size'] = size
    record['entry_idx'] = entry_idx
    record['entry_price'] = entry_price
    record['entry_fees'] = entry_fees
    record['exit_idx'] = exit_idx
    record['exit_price'] = exit_price
    record['exit_fees'] = exit_fees
    record['pnl'] = pnl
    record['return'] = ret
    record['direction'] = direction
    record['status'] = status
    record['parent_id'] = id_


@njit(cache=True)
def copy_trade_record_nb(record: tp.Record, trade_record: tp.Record) -> None:
    """Copy a trade record."""
    record['id'] = trade_record['id']
    record['col'] = trade_record['col']
    record['size'] = trade_record['size']
    record['entry_idx'] = trade_record['entry_idx']
    record['entry_price'] = trade_record['entry_price']
    record['entry_fees'] = trade_record['entry_fees']
    record['exit_idx'] = trade_record['exit_idx']
    record['exit_price'] = trade_record['exit_price']
    record['exit_fees'] = trade_record['exit_fees']
    record['pnl'] = trade_record['pnl']
    record['return'] = trade_record['return']
    record['direction'] = trade_record['direction']
    record['status'] = trade_record['status']
    record['parent_id'] = trade_record['parent_id']


@njit(cache=True)
def get_positions_nb(trade_records: tp.RecordArray, col_map: tp.ColMap) -> tp.RecordArray:
    """Fill position records by aggregating trade records.

    Trades can be entry trades, exit trades, and even positions themselves - all will produce the same results.

    Usage:
        * Building upon the example in `get_exit_trades_nb`:

        ```pycon
        >>> from vectorbt.portfolio.nb import get_positions_nb

        >>> col_map = col_map_nb(exit_trade_records['col'], target_shape[1])
        >>> position_records = get_positions_nb(exit_trade_records, col_map)
        >>> pd.DataFrame.from_records(position_records)
           id  col  size  entry_idx  entry_price  entry_fees  exit_idx  exit_price  \\
        0   0    0   1.1          0     1.101818     0.01212         3    3.060000
        1   1    0   1.0          4     5.050000     0.05050         5    5.940000
        2   2    0   1.0          5     5.940000     0.05940         5    6.000000
        3   3    1   1.1          0     5.850000     0.06435         3    3.948182
        4   4    1   1.0          4     1.980000     0.01980         5    1.010000
        5   5    1   1.0          5     1.010000     0.01010         5    1.000000

           exit_fees      pnl    return  direction  status  parent_id
        0    0.03366  2.10822  1.739455          0       1          0
        1    0.05940  0.78010  0.154475          0       1          1
        2    0.00000 -0.11940 -0.020101          1       0          2
        3    0.04343  1.98422  0.308348          1       1          3
        4    0.01010  0.94010  0.474798          1       1          4
        5    0.00000 -0.02010 -0.019901          0       0          5
        ```
    """
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    records = np.empty(len(trade_records), dtype=trade_dt)
    pidx = 0
    from_tidx = -1

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        last_id = -1
        last_position_id = -1

        for c in range(col_len):
            tidx = col_idxs[col_start_idxs[col] + c]
            record = trade_records[tidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            parent_id = record['parent_id']

            if parent_id != last_position_id:
                if last_position_id != -1:
                    if tidx - from_tidx > 1:
                        fill_position_record_nb(records[pidx], pidx, trade_records[from_tidx:tidx])
                    else:
                        # Speed up
                        copy_trade_record_nb(records[pidx], trade_records[from_tidx])
                        records[pidx]['id'] = pidx
                        records[pidx]['parent_id'] = pidx
                    pidx += 1
                from_tidx = tidx
                last_position_id = parent_id

        if tidx - from_tidx > 0:
            fill_position_record_nb(records[pidx], pidx, trade_records[from_tidx:tidx + 1])
        else:
            # Speed up
            copy_trade_record_nb(records[pidx], trade_records[from_tidx])
            records[pidx]['id'] = pidx
            records[pidx]['parent_id'] = pidx
        pidx += 1

    return records[:pidx]


# ############# Assets ############# #


@njit(cache=True)
def get_long_size_nb(position_before: float, position_now: float) -> float:
    """Get long size."""
    if position_before <= 0 and position_now <= 0:
        return 0.
    if position_before >= 0 and position_now < 0:
        return -position_before
    if position_before < 0 and position_now >= 0:
        return position_now
    return add_nb(position_now, -position_before)


@njit(cache=True)
def get_short_size_nb(position_before: float, position_now: float) -> float:
    """Get short size."""
    if position_before >= 0 and position_now >= 0:
        return 0.
    if position_before >= 0 and position_now < 0:
        return -position_now
    if position_before < 0 and position_now >= 0:
        return position_before
    return add_nb(position_before, -position_now)


@njit(cache=True)
def asset_flow_nb(target_shape: tp.Shape,
                  order_records: tp.RecordArray,
                  col_map: tp.ColMap,
                  direction: int) -> tp.Array2d:
    """Get asset flow series per column.

    Returns the total transacted amount of assets at each time step."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full(target_shape, 0., dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        last_id = -1
        position_now = 0.

        for c in range(col_len):
            oidx = col_idxs[col_start_idxs[col] + c]
            record = order_records[oidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            i = record['idx']
            side = record['side']
            size = record['size']

            if side == OrderSide.Sell:
                size *= -1
            new_position_now = add_nb(position_now, size)
            if direction == Direction.LongOnly:
                asset_flow = get_long_size_nb(position_now, new_position_now)
            elif direction == Direction.ShortOnly:
                asset_flow = get_short_size_nb(position_now, new_position_now)
            else:
                asset_flow = size
            out[i, col] = add_nb(out[i, col], asset_flow)
            position_now = new_position_now
    return out


@njit(cache=True)
def assets_nb(asset_flow: tp.Array2d) -> tp.Array2d:
    """Get asset series per column.

    Returns the current position at each time step."""
    out = np.empty_like(asset_flow)
    for col in range(asset_flow.shape[1]):
        position_now = 0.
        for i in range(asset_flow.shape[0]):
            flow_value = asset_flow[i, col]
            position_now = add_nb(position_now, flow_value)
            out[i, col] = position_now
    return out


@njit(cache=True)
def i_group_any_reduce_nb(i: int, group: int, a: tp.Array1d) -> bool:
    """Boolean "any" reducer for grouped columns."""
    return np.any(a)


@njit
def position_mask_grouped_nb(position_mask: tp.Array2d, group_lens: tp.Array1d) -> tp.Array2d:
    """Get whether in position for each row and group."""
    return generic_nb.squeeze_grouped_nb(position_mask, group_lens, i_group_any_reduce_nb).astype(np.bool_)


@njit(cache=True)
def group_mean_reduce_nb(group: int, a: tp.Array1d) -> float:
    """Mean reducer for grouped columns."""
    return np.mean(a)


@njit
def position_coverage_grouped_nb(position_mask: tp.Array2d, group_lens: tp.Array1d) -> tp.Array2d:
    """Get coverage of position for each row and group."""
    return generic_nb.reduce_grouped_nb(position_mask, group_lens, group_mean_reduce_nb)


# ############# Cash ############# #


@njit(cache=True)
def get_free_cash_diff_nb(position_before: float,
                          position_now: float,
                          debt_now: float,
                          price: float,
                          fees: float) -> tp.Tuple[float, float]:
    """Get updated debt and free cash flow."""
    size = add_nb(position_now, -position_before)
    final_cash = -size * price - fees
    if is_close_nb(size, 0):
        new_debt = debt_now
        free_cash_diff = 0.
    elif size > 0:
        if position_before < 0:
            if position_now < 0:
                short_size = abs(size)
            else:
                short_size = abs(position_before)
            avg_entry_price = debt_now / abs(position_before)
            debt_diff = short_size * avg_entry_price
            new_debt = add_nb(debt_now, -debt_diff)
            free_cash_diff = add_nb(2 * debt_diff, final_cash)
        else:
            new_debt = debt_now
            free_cash_diff = final_cash
    else:
        if position_now < 0:
            if position_before < 0:
                short_size = abs(size)
            else:
                short_size = abs(position_now)
            short_value = short_size * price
            new_debt = debt_now + short_value
            free_cash_diff = add_nb(final_cash, -2 * short_value)
        else:
            new_debt = debt_now
            free_cash_diff = final_cash
    return new_debt, free_cash_diff


@njit(cache=True)
def cash_flow_nb(target_shape: tp.Shape,
                 order_records: tp.RecordArray,
                 col_map: tp.ColMap,
                 free: bool) -> tp.Array2d:
    """Get (free) cash flow series per column."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full(target_shape, 0., dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        last_id = -1
        position_now = 0.
        debt_now = 0.

        for c in range(col_len):
            oidx = col_idxs[col_start_idxs[col] + c]
            record = order_records[oidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            i = record['idx']
            side = record['side']
            size = record['size']
            price = record['price']
            fees = record['fees']

            if side == OrderSide.Sell:
                size *= -1
            new_position_now = add_nb(position_now, size)
            if free:
                debt_now, cash_flow = get_free_cash_diff_nb(
                    position_now,
                    new_position_now,
                    debt_now,
                    price,
                    fees
                )
            else:
                cash_flow = -size * price - fees
            out[i, col] = add_nb(out[i, col], cash_flow)
            position_now = new_position_now
    return out


@njit(cache=True)
def sum_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d) -> tp.Array2d:
    """Squeeze each group of columns into a single column using sum operation."""
    check_group_lens_nb(group_lens, a.shape[1])

    out = np.empty((a.shape[0], len(group_lens)), dtype=np.float64)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        out[:, group] = np.sum(a[:, from_col:to_col], axis=1)
        from_col = to_col
    return out


@njit(cache=True)
def cash_flow_grouped_nb(cash_flow: tp.Array2d, group_lens: tp.Array1d) -> tp.Array2d:
    """Get cash flow series per group."""
    return sum_grouped_nb(cash_flow, group_lens)


@njit(cache=True)
def init_cash_grouped_nb(init_cash: tp.Array1d, group_lens: tp.Array1d, cash_sharing: bool) -> tp.Array1d:
    """Get initial cash per group."""
    if cash_sharing:
        return init_cash
    out = np.empty(group_lens.shape, dtype=np.float64)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        cash_sum = 0.
        for col in range(from_col, to_col):
            cash_sum += init_cash[col]
        out[group] = cash_sum
        from_col = to_col
    return out


@njit(cache=True)
def init_cash_nb(init_cash: tp.Array1d, group_lens: tp.Array1d, cash_sharing: bool) -> tp.Array1d:
    """Get initial cash per column."""
    if not cash_sharing:
        return init_cash
    group_lens_cs = np.cumsum(group_lens)
    out = np.full(group_lens_cs[-1], np.nan, dtype=np.float64)
    out[group_lens_cs - group_lens] = init_cash
    out = generic_nb.ffill_1d_nb(out)
    return out


@njit(cache=True)
def cash_nb(cash_flow: tp.Array2d, init_cash: tp.Array1d) -> tp.Array2d:
    """Get cash series per column."""
    out = np.empty_like(cash_flow)
    for col in range(cash_flow.shape[1]):
        for i in range(cash_flow.shape[0]):
            cash_now = init_cash[col] if i == 0 else out[i - 1, col]
            out[i, col] = add_nb(cash_now, cash_flow[i, col])
    return out


@njit(cache=True)
def cash_in_sim_order_nb(cash_flow: tp.Array2d,
                         group_lens: tp.Array1d,
                         init_cash_grouped: tp.Array1d,
                         call_seq: tp.Array2d) -> tp.Array2d:
    """Get cash series in simulation order."""
    check_group_lens_nb(group_lens, cash_flow.shape[1])

    out = np.empty_like(cash_flow)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        cash_now = init_cash_grouped[group]
        for i in range(cash_flow.shape[0]):
            for k in range(group_len):
                col = from_col + call_seq[i, from_col + k]
                cash_now = add_nb(cash_now, cash_flow[i, col])
                out[i, col] = cash_now
        from_col = to_col
    return out


@njit(cache=True)
def cash_grouped_nb(target_shape: tp.Shape,
                    cash_flow_grouped: tp.Array2d,
                    group_lens: tp.Array1d,
                    init_cash_grouped: tp.Array1d) -> tp.Array2d:
    """Get cash series per group."""
    check_group_lens_nb(group_lens, target_shape[1])

    out = np.empty_like(cash_flow_grouped)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        cash_now = init_cash_grouped[group]
        for i in range(cash_flow_grouped.shape[0]):
            flow_value = cash_flow_grouped[i, group]
            cash_now = add_nb(cash_now, flow_value)
            out[i, group] = cash_now
        from_col = to_col
    return out


# ############# Performance ############# #


@njit(cache=True)
def asset_value_nb(close: tp.Array2d, assets: tp.Array2d) -> tp.Array2d:
    """Get asset value series per column."""
    return close * assets


@njit(cache=True)
def asset_value_grouped_nb(asset_value: tp.Array2d, group_lens: tp.Array1d) -> tp.Array2d:
    """Get asset value series per group."""
    return sum_grouped_nb(asset_value, group_lens)


@njit(cache=True)
def value_in_sim_order_nb(cash: tp.Array2d,
                          asset_value: tp.Array2d,
                          group_lens: tp.Array1d,
                          call_seq: tp.Array2d) -> tp.Array2d:
    """Get portfolio value series in simulation order."""
    check_group_lens_nb(group_lens, cash.shape[1])

    out = np.empty_like(cash)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        asset_value_now = 0.
        # Without correctly treating NaN values, after one NaN all will be NaN
        since_last_nan = group_len
        for j in range(cash.shape[0] * group_len):
            i = j // group_len
            col = from_col + call_seq[i, from_col + j % group_len]
            if j >= group_len:
                last_j = j - group_len
                last_i = last_j // group_len
                last_col = from_col + call_seq[last_i, from_col + last_j % group_len]
                if not np.isnan(asset_value[last_i, last_col]):
                    asset_value_now -= asset_value[last_i, last_col]
            if np.isnan(asset_value[i, col]):
                since_last_nan = 0
            else:
                asset_value_now += asset_value[i, col]
            if since_last_nan < group_len:
                out[i, col] = np.nan
            else:
                out[i, col] = cash[i, col] + asset_value_now
            since_last_nan += 1

        from_col = to_col
    return out


@njit(cache=True)
def value_nb(cash: tp.Array2d, asset_value: tp.Array2d) -> tp.Array2d:
    """Get portfolio value series per column/group."""
    return cash + asset_value


@njit(cache=True)
def total_profit_nb(target_shape: tp.Shape,
                    close: tp.Array2d,
                    order_records: tp.RecordArray,
                    col_map: tp.ColMap) -> tp.Array1d:
    """Get total profit per column.

    A much faster version than the one based on `value_nb`."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    assets = np.full(target_shape[1], 0., dtype=np.float64)
    cash = np.full(target_shape[1], 0., dtype=np.float64)
    zero_mask = np.full(target_shape[1], False, dtype=np.bool_)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            zero_mask[col] = True
            continue
        last_id = -1

        for c in range(col_len):
            oidx = col_idxs[col_start_idxs[col] + c]
            record = order_records[oidx]

            if record['id'] < last_id:
                raise ValueError("id must come in ascending order per column")
            last_id = record['id']

            # Fill assets
            if record['side'] == OrderSide.Buy:
                order_size = record['size']
                assets[col] = add_nb(assets[col], order_size)
            else:
                order_size = record['size']
                assets[col] = add_nb(assets[col], -order_size)

            # Fill cash balance
            if record['side'] == OrderSide.Buy:
                order_cash = record['size'] * record['price'] + record['fees']
                cash[col] = add_nb(cash[col], -order_cash)
            else:
                order_cash = record['size'] * record['price'] - record['fees']
                cash[col] = add_nb(cash[col], order_cash)

    total_profit = cash + assets * close[-1, :]
    total_profit[zero_mask] = 0.
    return total_profit


@njit(cache=True)
def total_profit_grouped_nb(total_profit: tp.Array1d, group_lens: tp.Array1d) -> tp.Array1d:
    """Get total profit per group."""
    check_group_lens_nb(group_lens, total_profit.shape[0])

    out = np.empty(len(group_lens), dtype=np.float64)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        out[group] = np.sum(total_profit[from_col:to_col])
        from_col = to_col
    return out


@njit(cache=True)
def final_value_nb(total_profit: tp.Array1d, init_cash: tp.Array1d) -> tp.Array1d:
    """Get total profit per column/group."""
    return total_profit + init_cash


@njit(cache=True)
def total_return_nb(total_profit: tp.Array1d, init_cash: tp.Array1d) -> tp.Array1d:
    """Get total return per column/group."""
    return total_profit / init_cash


@njit(cache=True)
def returns_in_sim_order_nb(value_iso: tp.Array2d,
                            group_lens: tp.Array1d,
                            init_cash_grouped: tp.Array1d,
                            call_seq: tp.Array2d) -> tp.Array2d:
    """Get portfolio return series in simulation order."""
    check_group_lens_nb(group_lens, value_iso.shape[1])

    out = np.empty_like(value_iso)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        input_value = init_cash_grouped[group]
        for j in range(value_iso.shape[0] * group_len):
            i = j // group_len
            col = from_col + call_seq[i, from_col + j % group_len]
            output_value = value_iso[i, col]
            out[i, col] = returns_nb.get_return_nb(input_value, output_value)
            input_value = output_value
        from_col = to_col
    return out


@njit(cache=True)
def asset_returns_nb(cash_flow: tp.Array2d, asset_value: tp.Array2d) -> tp.Array2d:
    """Get asset return series per column/group."""
    out = np.empty_like(cash_flow)
    for col in range(cash_flow.shape[1]):
        for i in range(cash_flow.shape[0]):
            input_value = 0. if i == 0 else asset_value[i - 1, col]
            output_value = asset_value[i, col] + cash_flow[i, col]
            out[i, col] = returns_nb.get_return_nb(input_value, output_value)
    return out


@njit(cache=True)
def benchmark_value_nb(close: tp.Array2d, init_cash: tp.Array1d) -> tp.Array2d:
    """Get market value per column."""
    return close / close[0] * init_cash


@njit(cache=True)
def benchmark_value_grouped_nb(close: tp.Array2d, group_lens: tp.Array1d, init_cash_grouped: tp.Array1d) -> tp.Array2d:
    """Get market value per group."""
    check_group_lens_nb(group_lens, close.shape[1])

    out = np.empty((close.shape[0], len(group_lens)), dtype=np.float64)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        col_init_cash = init_cash_grouped[group] / group_len
        close_norm = close[:, from_col:to_col] / close[0, from_col:to_col]
        out[:, group] = col_init_cash * np.sum(close_norm, axis=1)
        from_col = to_col
    return out


@njit(cache=True)
def total_benchmark_return_nb(benchmark_value: tp.Array2d) -> tp.Array1d:
    """Get total market return per column/group."""
    out = np.empty(benchmark_value.shape[1], dtype=np.float64)
    for col in range(benchmark_value.shape[1]):
        out[col] = returns_nb.get_return_nb(benchmark_value[0, col], benchmark_value[-1, col])
    return out


@njit(cache=True)
def gross_exposure_nb(asset_value: tp.Array2d, cash: tp.Array2d) -> tp.Array2d:
    """Get gross exposure per column/group."""
    out = np.empty(asset_value.shape, dtype=np.float64)
    for col in range(out.shape[1]):
        for i in range(out.shape[0]):
            denom = add_nb(asset_value[i, col], cash[i, col])
            if denom == 0:
                out[i, col] = 0.
            else:
                out[i, col] = asset_value[i, col] / denom
    return out
