# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Other metrics that are not compiled with Numba."""

import numpy as np
from scipy.stats import norm

from vectorbt import _typing as tp


def approx_exp_max_sharpe(mean_sharpe: float, var_sharpe: float, nb_trials: int) -> float:
    """Expected Maximum Sharpe Ratio."""
    return mean_sharpe + np.sqrt(var_sharpe) * \
           ((1 - np.euler_gamma) * norm.ppf(1 - 1 / nb_trials) + np.euler_gamma * norm.ppf(1 - 1 / (nb_trials * np.e)))


def deflated_sharpe_ratio(*, est_sharpe: tp.Array1d, var_sharpe: float, nb_trials: int,
                          backtest_horizon: int, skew: tp.Array1d, kurtosis: tp.Array1d) -> tp.Array1d:
    """Deflated Sharpe Ratio (DSR).

    See [Deflated Sharpe Ratio](https://gmarti.gitlab.io/qfin/2018/05/30/deflated-sharpe-ratio.html)."""
    SR0 = approx_exp_max_sharpe(0, var_sharpe, nb_trials)

    return norm.cdf(((est_sharpe - SR0) * np.sqrt(backtest_horizon - 1)) /
                    np.sqrt(1 - skew * est_sharpe + ((kurtosis - 1) / 4) * est_sharpe ** 2))
