from datetime import datetime

import numpy as np
import pandas as pd
import pytest

import vectorbt as vbt
from tests.utils import isclose

qs_available = True
try:
    import quantstats as qs
except:
    qs_available = False

day_dt = np.timedelta64(86400000000000)

ts = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'b': [5, 4, 3, 2, 1],
    'c': [1, 2, 3, 2, 1]
}, index=pd.DatetimeIndex([
    datetime(2018, 1, 1),
    datetime(2018, 1, 2),
    datetime(2018, 1, 3),
    datetime(2018, 1, 4),
    datetime(2018, 1, 5)
]))
rets = ts.pct_change()

seed = 42

np.random.seed(seed)
benchmark_rets = pd.DataFrame({
    'a': rets['a'] * np.random.uniform(0.8, 1.2, rets.shape[0]),
    'b': rets['b'] * np.random.uniform(0.8, 1.2, rets.shape[0]) * 2,
    'c': rets['c'] * np.random.uniform(0.8, 1.2, rets.shape[0]) * 3
})


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []
    vbt.settings.returns.defaults = dict(
        start_value=0.,
        window=rets.shape[0],
        minp=1,
        ddof=1,
        risk_free=0.01,
        levy_alpha=2.,
        required_return=0.1,
        cutoff=0.05
    )


def teardown_module():
    vbt.settings.reset()


# ############# accessors.py ############# #


class TestAccessors:
    def test_indexing(self):
        assert rets.vbt.returns['a'].total() == rets['a'].vbt.returns.total()

    def test_benchmark_rets(self):
        ret_acc = rets.vbt.returns(benchmark_rets=benchmark_rets)
        pd.testing.assert_frame_equal(ret_acc.benchmark_rets, benchmark_rets)
        pd.testing.assert_series_equal(ret_acc['a'].benchmark_rets, benchmark_rets['a'])

    def test_freq(self):
        assert rets.vbt.returns.wrapper.freq == day_dt
        assert rets['a'].vbt.returns.wrapper.freq == day_dt
        assert rets.vbt.returns(freq='2D').wrapper.freq == day_dt * 2
        assert rets['a'].vbt.returns(freq='2D').wrapper.freq == day_dt * 2
        assert pd.Series([1, 2, 3]).vbt.returns.wrapper.freq is None
        assert pd.Series([1, 2, 3]).vbt.returns(freq='3D').wrapper.freq == day_dt * 3
        assert pd.Series([1, 2, 3]).vbt.returns(freq=np.timedelta64(4, 'D')).wrapper.freq == day_dt * 4

    def test_ann_factor(self):
        assert rets['a'].vbt.returns(year_freq='365 days').ann_factor == 365
        assert rets.vbt.returns(year_freq='365 days').ann_factor == 365
        with pytest.raises(Exception):
            assert pd.Series([1, 2, 3]).vbt.returns(freq=None).ann_factor

    def test_from_value(self):
        pd.testing.assert_series_equal(pd.Series.vbt.returns.from_value(ts['a']).obj, ts['a'].pct_change())
        pd.testing.assert_frame_equal(pd.DataFrame.vbt.returns.from_value(ts).obj, ts.pct_change())
        assert pd.Series.vbt.returns.from_value(ts['a'], year_freq='365 days').year_freq == pd.to_timedelta('365 days')
        assert pd.DataFrame.vbt.returns.from_value(ts, year_freq='365 days').year_freq == pd.to_timedelta('365 days')

    def test_daily(self):
        ret_12h = pd.DataFrame({
            'a': [0.1, 0.1, 0.1, 0.1, 0.1],
            'b': [-0.1, -0.1, -0.1, -0.1, -0.1],
            'c': [0.1, -0.1, 0.1, -0.1, 0.1]
        }, index=pd.DatetimeIndex([
            datetime(2018, 1, 1, 0),
            datetime(2018, 1, 1, 12),
            datetime(2018, 1, 2, 0),
            datetime(2018, 1, 2, 12),
            datetime(2018, 1, 3, 0)
        ]))
        pd.testing.assert_series_equal(
            ret_12h['a'].vbt.returns.daily(),
            pd.Series(
                np.array([0.21, 0.21, 0.1]),
                index=pd.DatetimeIndex([
                    '2018-01-01',
                    '2018-01-02',
                    '2018-01-03'
                ], dtype='datetime64[ns]', freq='D'),
                name=ret_12h['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            ret_12h.vbt.returns.daily(),
            pd.DataFrame(
                np.array([
                    [0.21, -0.19, -0.01],
                    [0.21, -0.19, -0.01],
                    [0.1, -0.1, 0.1]
                ]),
                index=pd.DatetimeIndex([
                    '2018-01-01',
                    '2018-01-02',
                    '2018-01-03'
                ], dtype='datetime64[ns]', freq='D'),
                columns=ret_12h.columns
            )
        )

    def test_annual(self):
        pd.testing.assert_series_equal(
            rets['a'].vbt.returns.annual(),
            pd.Series(
                np.array([4.]),
                index=pd.DatetimeIndex(['2018-01-01'], dtype='datetime64[ns]', freq='365D'),
                name=rets['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.annual(),
            pd.DataFrame(
                np.array([[4., -0.8, 0.]]),
                index=pd.DatetimeIndex(['2018-01-01'], dtype='datetime64[ns]', freq='365D'),
                columns=rets.columns
            )
        )

    def test_cumulative(self):
        pd.testing.assert_series_equal(
            rets['a'].vbt.returns.cumulative(),
            pd.Series(
                [0.0, 1.0, 2.0, 3.0, 4.0],
                index=rets.index,
                name='a'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.cumulative(),
            pd.DataFrame(
                [
                    [0.0, 0.0, 0.0],
                    [1.0, -0.19999999999999996, 1.0],
                    [2.0, -0.3999999999999999, 2.0],
                    [3.0, -0.6, 1.0],
                    [4.0, -0.8, 0.0]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_total_return(self):
        assert isclose(rets['a'].vbt.returns.total(), 4.0)
        pd.testing.assert_series_equal(
            rets.vbt.returns.total(),
            pd.Series(
                [4.0, -0.8, 0.0],
                index=rets.columns,
                name='total_return'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_total(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [1.0, -0.19999999999999996, 1.0],
                    [2.0, -0.3999999999999999, 2.0],
                    [3.0, -0.6, 1.0],
                    [4.0, -0.8, 0.0]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_annualized_return(self):
        assert isclose(rets['a'].vbt.returns.annualized(), 1.0587911840678754e+51)
        pd.testing.assert_series_equal(
            rets.vbt.returns.annualized(),
            pd.Series(
                [1.0587911840678754e+51, -1.0, 0.0],
                index=rets.columns,
                name='annualized_return'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_annualized(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [8.669103912675328e+54, -1.0, 8.669103912675328e+54],
                    [1.1213796164129035e+58, -1.0, 1.1213796164129035e+58],
                    [8.669103912675328e+54, -1.0, 2.9443342053298444e+27],
                    [1.0587911840678754e+51, -1.0, 0.0]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_annualized_volatility(self):
        assert isclose(rets['a'].vbt.returns.annualized_volatility(), 6.417884083645567)
        pd.testing.assert_series_equal(
            rets.vbt.returns.annualized_volatility(),
            pd.Series(
                [6.417884083645567, 2.5122615973129334, 13.509256086106296],
                index=rets.columns,
                name='annualized_volatility'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_annualized_volatility(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan],
                    [6.754628043053148, 0.6754628043053155, 6.754628043053148],
                    [6.62836217969305, 1.2868638306046682, 12.868638306046675],
                    [6.417884083645567, 2.5122615973129334, 13.509256086106296]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_calmar_ratio(self):
        assert isclose(rets['a'].vbt.returns.calmar_ratio(), np.nan)
        pd.testing.assert_series_equal(
            rets.vbt.returns.calmar_ratio(),
            pd.Series(
                [np.nan, -1.25, 0.0],
                index=rets.columns,
                name='calmar_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_calmar_ratio(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, -5.000000000000001, np.nan],
                    [np.nan, -2.5000000000000004, np.nan],
                    [np.nan, -1.6666666666666667, 8.833002615989533e+27],
                    [np.nan, -1.25, 0.0]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_omega_ratio(self):
        assert isclose(rets['a'].vbt.returns.omega_ratio(risk_free=0.01, required_return=0.1), np.inf)
        pd.testing.assert_series_equal(
            rets.vbt.returns.omega_ratio(risk_free=0.01, required_return=0.1),
            pd.Series(
                [np.inf, 0.0, 1.7327023435781848],
                index=rets.columns,
                name='omega_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_omega_ratio(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.inf, 0.0, np.inf],
                    [np.inf, 0.0, np.inf],
                    [np.inf, 0.0, 4.305883016460259],
                    [np.inf, 0.0, 1.7327023435781848]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_sharpe_ratio(self):
        assert isclose(rets['a'].vbt.returns.sharpe_ratio(risk_free=0.01), 29.052280196490333)
        pd.testing.assert_series_equal(
            rets.vbt.returns.sharpe_ratio(risk_free=0.01),
            pd.Series(
                [29.052280196490333, -48.06592068111974, 4.232900240313306],
                index=rets.columns,
                name='sharpe_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_sharpe_ratio(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan],
                    [39.98739801487463, -126.98700720939904, 39.98739801487463],
                    [33.101020977359426, -76.89667951041766, 10.746626111906732],
                    [29.052280196490333, -48.06592068111974, 4.232900240313306]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_deflated_sharpe_ratio(self):
        pd.testing.assert_series_equal(
            rets.vbt.returns.deflated_sharpe_ratio(risk_free=0.01),
            pd.Series([np.nan, np.nan, 0.0005355605507117676], index=rets.columns, name='deflated_sharpe_ratio')
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.deflated_sharpe_ratio(risk_free=0.03),
            pd.Series([np.nan, np.nan, 0.0003423112350834066], index=rets.columns, name='deflated_sharpe_ratio')
        )

    def test_downside_risk(self):
        assert isclose(rets['a'].vbt.returns.downside_risk(required_return=0.1), 0.0)
        pd.testing.assert_series_equal(
            rets.vbt.returns.downside_risk(required_return=0.1),
            pd.Series(
                [0.0, 8.329186468210578, 7.069987427302981],
                index=rets.columns,
                name='downside_risk'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_downside_risk(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [0.0, 5.7314919523628385, 0.0],
                    [0.0, 6.227459353540574, 0.0],
                    [0.0, 6.978571699349585, 4.779779942245908],
                    [0.0, 8.329186468210578, 7.069987427302981]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_sortino_ratio(self):
        assert isclose(rets['a'].vbt.returns.sortino_ratio(required_return=0.1), np.inf)
        pd.testing.assert_series_equal(
            rets.vbt.returns.sortino_ratio(required_return=0.1),
            pd.Series(
                [np.inf, -18.441677017667562, 3.4417788692752858],
                index=rets.columns,
                name='sortino_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_sortino_ratio(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.inf, -19.1049731745428, np.inf],
                    [np.inf, -19.04869919906529, np.inf],
                    [np.inf, -18.887182253617894, 22.06052281036573],
                    [np.inf, -18.441677017667562, 3.4417788692752858]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_information_ratio(self):
        assert isclose(rets['a'].vbt.returns.information_ratio(benchmark_rets['a']), -0.5575108215121097)
        pd.testing.assert_series_equal(
            rets.vbt.returns.information_ratio(benchmark_rets),
            pd.Series(
                [-0.5575108215121097, 1.8751745305884349, -0.3791876496995291],
                index=rets.columns,
                name='information_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_information_ratio(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan],
                    [-1.1972053570548309, 1.6499071488151926, -1.9503403469059444],
                    [-0.9036343476254122, 2.183905200180643, -0.6855076064440647],
                    [-0.5575108215121097, 1.8751745305884349, -0.3791876496995291]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_beta(self):
        assert isclose(rets['a'].vbt.returns.beta(benchmark_rets['a']), 0.7853755858374825)
        pd.testing.assert_series_equal(
            rets.vbt.returns.beta(benchmark_rets),
            pd.Series(
                [0.7853755858374825, 0.4123019930790345, 0.30840682076341036],
                index=rets.columns,
                name='beta'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_beta(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan],
                    [0.7887842027059571, 0.2049668794115673, 0.2681790192492397],
                    [0.7969484728140032, 0.34249231546013587, 0.30111751528469777],
                    [0.7853755858374825, 0.4123019930790345, 0.30840682076341036]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_alpha(self):
        assert isclose(rets['a'].vbt.returns.alpha(benchmark_rets['a'], risk_free=0.01), 41819510790.213036)
        pd.testing.assert_series_equal(
            rets.vbt.returns.alpha(benchmark_rets, risk_free=0.01),
            pd.Series(
                [41819510790.213036, -0.9999999939676926, -0.999999999999793],
                index=rets.columns,
                name='alpha'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_alpha(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan],
                    [18396133022.071487, -1.0, 558643.320341666],
                    [974350522.6315696, -0.9999999999999931, -0.9999999996015246],
                    [41819510790.213036, -0.9999999939676926, -0.999999999999793]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_tail_ratio(self):
        assert isclose(rets['a'].vbt.returns.tail_ratio(), 3.5238095238095237)
        pd.testing.assert_series_equal(
            rets.vbt.returns.tail_ratio(),
            pd.Series(
                [3.5238095238095237, 0.43684210526315786, 1.947368421052631],
                index=rets.columns,
                name='tail_ratio'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_tail_ratio(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [1.0, 1.0, 1.0],
                    [1.857142857142857, 0.818181818181818, 1.857142857142857],
                    [2.714285714285715, 0.6307692307692306, 3.8000000000000007],
                    [3.5238095238095237, 0.43684210526315786, 1.947368421052631]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_value_at_risk(self):
        assert isclose(rets['a'].vbt.returns.value_at_risk(cutoff=0.05), 0.26249999999999996)
        pd.testing.assert_series_equal(
            rets.vbt.returns.value_at_risk(cutoff=0.05),
            pd.Series(
                [0.26249999999999996, -0.47500000000000003, -0.47500000000000003],
                index=rets.columns,
                name='value_at_risk'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_value_at_risk(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [1.0, -0.19999999999999996, 1.0],
                    [0.525, -0.2475, 0.525],
                    [0.3499999999999999, -0.325, -0.24999999999999994],
                    [0.26249999999999996, -0.47500000000000003, -0.47500000000000003]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_cond_value_at_risk(self):
        assert isclose(rets['a'].vbt.returns.cond_value_at_risk(cutoff=0.05), 0.25)
        pd.testing.assert_series_equal(
            rets.vbt.returns.cond_value_at_risk(cutoff=0.05),
            pd.Series(
                [0.25, -0.5, -0.5],
                index=rets.columns,
                name='cond_value_at_risk'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_cond_value_at_risk(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [1.0, -0.19999999999999996, 1.0],
                    [0.5, -0.25, 0.5],
                    [0.33333333333333326, -0.33333333333333337, -0.33333333333333337],
                    [0.25, -0.5, -0.5]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_capture(self):
        assert isclose(rets['a'].vbt.returns.capture(benchmark_rets['a']), 0.0007435597416888084)
        pd.testing.assert_series_equal(
            rets.vbt.returns.capture(benchmark_rets),
            pd.Series(
                [0.0007435597416888084, 1.0, -0.0],
                index=rets.columns,
                name='capture'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_capture(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [1.443034545422564e-07, 1.0, 4.0670014163453153e-66],
                    [6.758314743559073e-07, 1.0, 2.2829041301869233e-75],
                    [9.623155594782632e-06, 1.0, 43620380068493.234],
                    [0.0007435597416888084, 1.0, -0.0]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_up_capture(self):
        assert isclose(rets['a'].vbt.returns.up_capture(benchmark_rets['a']), 0.0001227848643711666)
        pd.testing.assert_series_equal(
            rets.vbt.returns.up_capture(benchmark_rets),
            pd.Series(
                [0.0001227848643711666, np.nan, 1.0907657953912082e-112],
                index=rets.columns,
                name='up_capture'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_up_capture(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [2.0823486992829062e-14, np.nan, 1.6540500520554797e-131],
                    [5.555940938023189e-10, np.nan, 1.0907657953912082e-112],
                    [2.0468688202710215e-07, np.nan, 1.0907657953912082e-112],
                    [0.0001227848643711666, np.nan, 1.0907657953912082e-112]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_down_capture(self):
        assert isclose(rets['a'].vbt.returns.down_capture(benchmark_rets['a']), np.nan)
        pd.testing.assert_series_equal(
            rets.vbt.returns.down_capture(benchmark_rets),
            pd.Series(
                [np.nan, np.nan, np.nan],
                index=rets.columns,
                name='down_capture'
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_down_capture(benchmark_rets),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [np.nan, 1.0, np.nan],
                    [np.nan, 1.0, np.nan],
                    [np.nan, 1.0, 1.0],
                    [np.nan, np.nan, np.nan]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_drawdown(self):
        pd.testing.assert_series_equal(
            rets['a'].vbt.returns.drawdown(),
            pd.Series(
                np.array([0., 0., 0., 0., 0.]),
                index=rets['a'].index,
                name=rets['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.drawdown(),
            pd.DataFrame(
                np.array([
                    [0., 0., 0.],
                    [0., -0.2, 0.],
                    [0., -0.4, 0.],
                    [0., -0.6, -0.33333333],
                    [0., -0.8, -0.66666667]
                ]),
                index=pd.DatetimeIndex([
                    '2018-01-01',
                    '2018-01-02',
                    '2018-01-03',
                    '2018-01-04',
                    '2018-01-05'
                ], dtype='datetime64[ns]', freq=None),
                columns=rets.columns
            )
        )

    def test_max_drawdown(self):
        assert isclose(
            rets['a'].vbt.returns.max_drawdown(),
            rets['a'].vbt.returns.drawdowns.max_drawdown(fill_value=0.)
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.max_drawdown(),
            rets.vbt.returns.drawdowns.max_drawdown(fill_value=0.)
        )
        pd.testing.assert_frame_equal(
            rets.vbt.returns.rolling_max_drawdown(),
            pd.DataFrame(
                [
                    [np.nan, np.nan, np.nan],
                    [0.0, -0.19999999999999996, 0.0],
                    [0.0, -0.3999999999999999, 0.0],
                    [0.0, -0.6, -0.33333333333333337],
                    [0.0, -0.8, -0.6666666666666667]
                ],
                index=rets.index,
                columns=rets.columns
            )
        )

    def test_drawdowns(self):
        assert type(rets['a'].vbt.returns.drawdowns) is vbt.Drawdowns
        assert rets['a'].vbt.returns.drawdowns.wrapper.freq == rets['a'].vbt.wrapper.freq
        assert rets['a'].vbt.returns.drawdowns.wrapper.ndim == rets['a'].ndim
        assert rets.vbt.returns.drawdowns.wrapper.ndim == rets.ndim
        assert isclose(rets['a'].vbt.returns.drawdowns.max_drawdown(), rets['a'].vbt.returns.max_drawdown())
        pd.testing.assert_series_equal(
            rets.vbt.returns.drawdowns.max_drawdown(fill_value=0.),
            rets.vbt.returns.max_drawdown()
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start',
            'End',
            'Period',
            'Total Return [%]',
            'Annualized Return [%]',
            'Annualized Volatility [%]',
            'Max Drawdown [%]',
            'Max Drawdown Duration',
            'Sharpe Ratio',
            'Calmar Ratio',
            'Omega Ratio',
            'Sortino Ratio',
            'Skew',
            'Kurtosis',
            'Tail Ratio',
            'Common Sense Ratio',
            'Value at Risk'
        ], dtype='object')
        pd.testing.assert_series_equal(
            rets.vbt.returns.stats(),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'), pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'), 106.66666666666667, 3.529303946892918e+52,
                747.9800589021598, 73.33333333333333, pd.Timedelta('3 days 00:00:00'),
                -4.926913414772034, -0.625, np.inf, np.inf, 0.25687104876585726, -0.25409565813913854,
                1.9693400167084374, 1.2436594860479807e+51, -0.2291666666666667
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.stats(column='a'),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'), pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'), 400.0, 1.0587911840678753e+53, 641.7884083645566,
                np.nan, pd.NaT, 29.052280196490333, np.nan, np.inf, np.inf, 1.4693345482106241,
                2.030769230769236, 3.5238095238095237, 3.730978458143942e+51, 0.26249999999999996
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.stats(column='a', settings=dict(freq='10 days', year_freq='200 days')),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'), pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('50 days 00:00:00'), 400.0, 62400.0, 150.23130314433288, np.nan, pd.NaT,
                6.800624405721308, np.nan, np.inf, np.inf, 1.4693345482106241, 2.030769230769236,
                3.5238095238095237, 2202.3809523809523, 0.26249999999999996
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.stats(column='a', settings=dict(benchmark_rets=benchmark_rets)),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'), pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'), 400.0, 451.8597134178033, 1.0587911840678753e+53,
                641.7884083645566, np.nan, pd.NaT, 29.052280196490333, np.nan, np.inf, np.inf,
                1.4693345482106241, 2.030769230769236, 3.5238095238095237, 3.730978458143942e+51,
                0.26249999999999996, 41819510790.213036, 0.7853755858374825
            ],
                index=pd.Index([
                    'Start',
                    'End',
                    'Period',
                    'Total Return [%]',
                    'Benchmark Return [%]',
                    'Annualized Return [%]',
                    'Annualized Volatility [%]',
                    'Max Drawdown [%]',
                    'Max Drawdown Duration',
                    'Sharpe Ratio',
                    'Calmar Ratio',
                    'Omega Ratio',
                    'Sortino Ratio',
                    'Skew',
                    'Kurtosis',
                    'Tail Ratio',
                    'Common Sense Ratio',
                    'Value at Risk',
                    'Alpha',
                    'Beta'
                ], dtype='object'),
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns.stats(column='a', settings=dict(benchmark_rets=benchmark_rets)),
            rets.vbt.returns(benchmark_rets=benchmark_rets).stats(column='a'),
        )
        pd.testing.assert_series_equal(
            rets['c'].vbt.returns.stats(),
            rets.vbt.returns.stats(column='c')
        )
        pd.testing.assert_series_equal(
            rets['c'].vbt.returns.stats(),
            rets.vbt.returns.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns(freq='10d').stats(),
            rets.vbt.returns.stats(settings=dict(freq='10d'))
        )
        pd.testing.assert_series_equal(
            rets.vbt.returns(freq='d', year_freq='400d').stats(),
            rets.vbt.returns.stats(settings=dict(freq='d', year_freq='400d'))
        )
        stats_df = rets.vbt.returns.stats(agg_func=None)
        assert stats_df.shape == (3, 17)
        pd.testing.assert_index_equal(stats_df.index, rets.vbt.returns.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)

    def test_qs(self):
        if qs_available:
            pd.testing.assert_series_equal(
                rets.vbt.returns.qs.sharpe(),
                qs.stats.sharpe(rets.dropna(), periods=365, rf=0.01)
            )
            pd.testing.assert_series_equal(
                rets.vbt.returns(freq='h', year_freq='252d').qs.sharpe(),
                qs.stats.sharpe(rets.dropna(), periods=252 * 24, rf=0.01)
            )
            pd.testing.assert_series_equal(
                rets.vbt.returns(freq='h', year_freq='252d').qs.sharpe(periods=252, periods_per_year=252, rf=0),
                qs.stats.sharpe(rets.dropna())
            )
            assert rets['a'].vbt.returns(benchmark_rets=benchmark_rets['a']).qs.r_squared() == 0.6321016849785153
