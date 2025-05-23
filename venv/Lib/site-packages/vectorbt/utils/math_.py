# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Math utilities."""

import numpy as np
from numba import njit

rel_tol = 1e-9  # 1,000,000,000 == 1,000,000,001
abs_tol = 1e-12  # 0.000000000001 == 0.000000000002


@njit(cache=True)
def is_close_nb(a: float, b: float, rel_tol: float = rel_tol, abs_tol: float = abs_tol) -> bool:
    """Tell whether two values are approximately equal."""
    if np.isnan(a) or np.isnan(b):
        return False
    if np.isinf(a) or np.isinf(b):
        return False
    if a == b:
        return True
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@njit(cache=True)
def is_close_or_less_nb(a: float, b: float, rel_tol: float = rel_tol, abs_tol: float = abs_tol) -> bool:
    """Tell whether the first value is approximately less than or equal to the second value."""
    if is_close_nb(a, b, rel_tol=rel_tol, abs_tol=abs_tol):
        return True
    return a < b


@njit(cache=True)
def is_less_nb(a: float, b: float, rel_tol: float = rel_tol, abs_tol: float = abs_tol) -> bool:
    """Tell whether the first value is approximately less than the second value."""
    if is_close_nb(a, b, rel_tol=rel_tol, abs_tol=abs_tol):
        return False
    return a < b


@njit(cache=True)
def is_addition_zero_nb(a: float, b: float, rel_tol: float = rel_tol, abs_tol: float = abs_tol) -> bool:
    """Tell whether addition of two values yields zero."""
    if np.sign(a) != np.sign(b):
        return is_close_nb(abs(a), abs(b), rel_tol=rel_tol, abs_tol=abs_tol)
    return is_close_nb(a + b, 0., rel_tol=rel_tol, abs_tol=abs_tol)


@njit(cache=True)
def add_nb(a: float, b: float, rel_tol: float = rel_tol, abs_tol: float = abs_tol) -> float:
    """Add two floats."""
    if is_addition_zero_nb(a, b, rel_tol=rel_tol, abs_tol=abs_tol):
        return 0.
    return a + b
