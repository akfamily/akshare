# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""A factory for building new indicators with ease.

The indicator factory class `IndicatorFactory` offers a convenient way to create technical
indicators of any complexity. By providing it with information such as calculation functions and
the names of your inputs, parameters, and outputs, it will create a stand-alone indicator class
capable of running the indicator for an arbitrary combination of your inputs and parameters. It also
creates methods for signal generation and supports common pandas and parameter indexing operations.

Each indicator is basically a pipeline that:

* Accepts a list of input arrays (for example, OHLCV data)
* Accepts a list of parameter arrays (for example, window size)
* Accepts other relevant arguments and keyword arguments
* For each parameter combination, performs calculation on the input arrays
* Concatenates results into new output arrays (for example, rolling average)

This pipeline can be well standardized, which is done by `run_pipeline`.

`IndicatorFactory` simplifies the usage of `run_pipeline` by generating and pre-configuring
a new Python class with various class methods for running the indicator.

Each generated class includes the following features:

* Accepts input arrays of any compatible shape thanks to broadcasting
* Accepts output arrays written in-place instead of returning
* Accepts arbitrary parameter grids
* Supports caching and other optimizations out of the box
* Supports pandas and parameter indexing
* Offers helper methods for all inputs, outputs, and properties

Consider the following price DataFrame composed of two columns, one per asset:

```pycon
>>> import vectorbt as vbt
>>> import numpy as np
>>> import pandas as pd
>>> from numba import njit
>>> from datetime import datetime

>>> price = pd.DataFrame({
...     'a': [1, 2, 3, 4, 5],
...     'b': [5, 4, 3, 2, 1]
... }, index=pd.Index([
...     datetime(2020, 1, 1),
...     datetime(2020, 1, 2),
...     datetime(2020, 1, 3),
...     datetime(2020, 1, 4),
...     datetime(2020, 1, 5),
... ])).astype(float)
>>> price
            a    b
2020-01-01  1.0  5.0
2020-01-02  2.0  4.0
2020-01-03  3.0  3.0
2020-01-04  4.0  2.0
2020-01-05  5.0  1.0
```

For each column in the DataFrame, let's calculate a simple moving average and get its
crossover with price. In particular, we want to test two different window sizes: 2 and 3.

## Naive approach

A naive way of doing this:

```pycon
>>> ma_df = pd.DataFrame.vbt.concat(
...     price.rolling(window=2).mean(),
...     price.rolling(window=3).mean(),
...     keys=pd.Index([2, 3], name='ma_window'))
>>> ma_df
ma_window          2         3
              a    b    a    b
2020-01-01  NaN  NaN  NaN  NaN
2020-01-02  1.5  4.5  NaN  NaN
2020-01-03  2.5  3.5  2.0  4.0
2020-01-04  3.5  2.5  3.0  3.0
2020-01-05  4.5  1.5  4.0  2.0

>>> above_signals = (price.vbt.tile(2).vbt > ma_df)
>>> above_signals = above_signals.vbt.signals.first(after_false=True)
>>> above_signals
ma_window              2             3
                a      b      a      b
2020-01-01  False  False  False  False
2020-01-02   True  False  False  False
2020-01-03  False  False   True  False
2020-01-04  False  False  False  False
2020-01-05  False  False  False  False

>>> below_signals = (price.vbt.tile(2).vbt < ma_df)
>>> below_signals = below_signals.vbt.signals.first(after_false=True)
>>> below_signals
ma_window              2             3
                a      b      a      b
2020-01-01  False  False  False  False
2020-01-02  False   True  False  False
2020-01-03  False  False  False   True
2020-01-04  False  False  False  False
2020-01-05  False  False  False  False
```

Now the same using `IndicatorFactory`:

```pycon
>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window'],
...     output_names=['ma'],
... ).from_apply_func(vbt.nb.rolling_mean_nb)

>>> myind = MyInd.run(price, [2, 3])
>>> above_signals = myind.price_crossed_above(myind.ma)
>>> below_signals = myind.price_crossed_below(myind.ma)
```

The `IndicatorFactory` class is used to construct indicator classes from UDFs. First, we provide
all the necessary information (indicator config) to build the facade of the indicator, such as the names
of inputs, parameters, and outputs, and the actual calculation function. The factory then generates a
self-contained indicator class capable of running arbitrary configurations of inputs and parameters.
To run any configuration, we can either use the `run` method (as we did above) or the `run_combs` method.

## run and run_combs methods

The main method to run an indicator is `run`, which accepts arguments based on the config
provided to the `IndicatorFactory` (see the example above). These arguments include input arrays,
in-place output arrays, parameters, and arguments for `run_pipeline`.

The `run_combs` method takes the same inputs as the method above, but computes all combinations
of passed parameters based on a combinatorial function and returns multiple instances that
can be compared with each other. For example, this is useful to generate crossover signals
of multiple moving averages:

```pycon
>>> myind1, myind2 = MyInd.run_combs(price, [2, 3, 4])

>>> myind1.ma
myind_1_window                  2         3
                 a    b    a    b    a    b
2020-01-01     NaN  NaN  NaN  NaN  NaN  NaN
2020-01-02     1.5  4.5  1.5  4.5  NaN  NaN
2020-01-03     2.5  3.5  2.5  3.5  2.0  4.0
2020-01-04     3.5  2.5  3.5  2.5  3.0  3.0
2020-01-05     4.5  1.5  4.5  1.5  4.0  2.0

>>> myind2.ma
myind_2_window        3                   4
                 a    b    a    b    a    b
2020-01-01     NaN  NaN  NaN  NaN  NaN  NaN
2020-01-02     NaN  NaN  NaN  NaN  NaN  NaN
2020-01-03     2.0  4.0  NaN  NaN  NaN  NaN
2020-01-04     3.0  3.0  2.5  3.5  2.5  3.5
2020-01-05     4.0  2.0  3.5  2.5  3.5  2.5

>>> myind1.ma_crossed_above(myind2.ma)
myind_1_window                          2             3
myind_2_window            3             4             4
                   a      b      a      b      a      b
2020-01-01     False  False  False  False  False  False
2020-01-02     False  False  False  False  False  False
2020-01-03      True  False  False  False  False  False
2020-01-04     False  False   True  False   True  False
2020-01-05     False  False  False  False  False  False
```

Its main advantage is that it doesn't need to re-compute each combination thanks to smart caching.

To get details on what arguments are accepted by any of the class methods, use `help`:

```pycon
>>> help(MyInd.run)
Help on method run:

run(price, window, short_name='custom', hide_params=None, hide_default=True, **kwargs) method of builtins.type instance
    Run `Indicator` indicator.

    * Inputs: `price`
    * Parameters: `window`
    * Outputs: `ma`

    Pass a list of parameter names as `hide_params` to hide their column levels.
    Set `hide_default` to False to show the column levels of the parameters with a default value.

    Other keyword arguments are passed to `vectorbt.indicators.factory.run_pipeline`.
```

## Parameters

`IndicatorFactory` allows definition of arbitrary parameter grids.

Parameters are variables that can hold one or more values. A single value can be passed as a
scalar, an array, or any other object. Multiple values are passed as a list or an array
(if the flag `is_array_like` is set to False for that parameter). If there are multiple parameters
and each is having multiple values, their values will broadcast to a single shape:

```plaintext
       p1         p2            result
0       0          1          [(0, 1)]
1  [0, 1]        [2]  [(0, 2), (1, 2)]
2  [0, 1]     [2, 3]  [(0, 2), (1, 3)]
3  [0, 1]  [2, 3, 4]             error
```

To illustrate the usage of parameters in indicators, let's build a basic indicator that returns 1
if the rolling mean is within upper and lower bounds, and -1 if it's outside:

```pycon
>>> @njit
... def apply_func_nb(price, window, lower, upper):
...     output = np.full(price.shape, np.nan, dtype=np.float64)
...     for col in range(price.shape[1]):
...         for i in range(window, price.shape[0]):
...             mean = np.mean(price[i - window:i, col])
...             output[i, col] = lower < mean < upper
...     return output

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window', 'lower', 'upper'],
...     output_names=['output']
... ).from_apply_func(apply_func_nb)
```

By default, when `per_column` is set to False, each parameter is applied to the entire input.

One parameter combination:

```pycon
>>> MyInd.run(
...     price,
...     window=2,
...     lower=3,
...     upper=5
... ).output
custom_window         2
custom_lower          3
custom_upper          5
                 a    b
2020-01-01     NaN  NaN
2020-01-02     NaN  NaN
2020-01-03     0.0  1.0
2020-01-04     0.0  1.0
2020-01-05     1.0  0.0
```

Multiple parameter combinations:

```pycon
>>> MyInd.run(
...     price,
...     window=[2, 3],
...     lower=3,
...     upper=5
... ).output
custom_window         2         3
custom_lower          3         3
custom_upper          5         5
                 a    b    a    b
2020-01-01     NaN  NaN  NaN  NaN
2020-01-02     NaN  NaN  NaN  NaN
2020-01-03     0.0  1.0  NaN  NaN
2020-01-04     0.0  1.0  0.0  1.0
2020-01-05     1.0  0.0  0.0  0.0
```

Product of parameter combinations:

```pycon
>>> MyInd.run(
...     price,
...     window=[2, 3],
...     lower=[3, 4],
...     upper=5,
...     param_product=True
... ).output
custom_window                   2                   3
custom_lower          3         4         3         4
custom_upper          5         5         5         5
                 a    b    a    b    a    b    a    b
2020-01-01     NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
2020-01-02     NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
2020-01-03     0.0  1.0  0.0  1.0  NaN  NaN  NaN  NaN
2020-01-04     0.0  1.0  0.0  0.0  0.0  1.0  0.0  0.0
2020-01-05     1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
```

Multiple parameter combinations, one per column:

```pycon
>>> MyInd.run(
...     price,
...     window=[2, 3],
...     lower=[3, 4],
...     upper=5,
...     per_column=True
... ).output
custom_window    2    3
custom_lower     3    4
custom_upper     5    5
                 a    b
2020-01-01     NaN  NaN
2020-01-02     NaN  NaN
2020-01-03     0.0  NaN
2020-01-04     0.0  0.0
2020-01-05     1.0  0.0
```

Parameter defaults can be passed directly to the `IndicatorFactory.from_custom_func` and
`IndicatorFactory.from_apply_func`, and overridden in the run method:

```pycon
>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window', 'lower', 'upper'],
...     output_names=['output']
... ).from_apply_func(apply_func_nb, window=2, lower=3, upper=4)

>>> MyInd.run(price, upper=5).output
custom_window         2
custom_lower          3
custom_upper          5
                 a    b
2020-01-01     NaN  NaN
2020-01-02     NaN  NaN
2020-01-03     0.0  1.0
2020-01-04     0.0  1.0
2020-01-05     1.0  0.0
```

Some parameters are meant to be defined per row, column, or element of the input.
By default, if we pass the parameter value as an array, the indicator will treat this array
as a list of multiple values - one per input. To make the indicator view this array as a single
value, set the flag `is_array_like` to True in `param_settings`. Also, to automatically broadcast
the passed scalar/array to the input shape, set `bc_to_input` to True, 0 (index axis), or 1 (column axis).

In our example, the parameter `window` can broadcast per column, and both parameters
`lower` and `upper` can broadcast per element:

```pycon
>>> @njit
... def apply_func_nb(price, window, lower, upper):
...     output = np.full(price.shape, np.nan, dtype=np.float64)
...     for col in range(price.shape[1]):
...         for i in range(window[col], price.shape[0]):
...             mean = np.mean(price[i - window[col]:i, col])
...             output[i, col] = lower[i, col] < mean < upper[i, col]
...     return output

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window', 'lower', 'upper'],
...     output_names=['output']
... ).from_apply_func(
...     apply_func_nb,
...     param_settings=dict(
...         window=dict(is_array_like=True, bc_to_input=1, per_column=True),
...         lower=dict(is_array_like=True, bc_to_input=True),
...         upper=dict(is_array_like=True, bc_to_input=True)
...     )
... )

>>> MyInd.run(
...     price,
...     window=[np.array([2, 3]), np.array([3, 4])],
...     lower=np.array([1, 2]),
...     upper=np.array([3, 4]),
... ).output
custom_window       2       3               4
custom_lower  array_0 array_0 array_1 array_1
custom_upper  array_0 array_0 array_1 array_1
                    a       b       a       b
2020-01-01        NaN     NaN     NaN     NaN
2020-01-02        NaN     NaN     NaN     NaN
2020-01-03        1.0     NaN     NaN     NaN
2020-01-04        1.0     0.0     1.0     NaN
2020-01-05        0.0     1.0     0.0     1.0
```

Broadcasting a huge number of parameters to the input shape can consume lots of memory,
especially when the array materializes. Luckily, vectorbt implements flexible broadcasting,
which preserves the original dimensions of the parameter. This requires two changes:
setting `keep_raw` to True in `broadcast_kwargs` and passing `flex_2d` to the apply function.

There are two configs in `vectorbt.indicators.configs` exactly for this purpose: one for column-wise
broadcasting and one for element-wise broadcasting:

```pycon
>>> from vectorbt.base.reshape_fns import flex_select_auto_nb
>>> from vectorbt.indicators.configs import flex_col_param_config, flex_elem_param_config

>>> @njit
... def apply_func_nb(price, window, lower, upper, flex_2d):
...     output = np.full(price.shape, np.nan, dtype=np.float64)
...     for col in range(price.shape[1]):
...         _window = flex_select_auto_nb(window, 0, col, flex_2d)
...         for i in range(_window, price.shape[0]):
...             _lower = flex_select_auto_nb(lower, i, col, flex_2d)
...             _upper = flex_select_auto_nb(upper, i, col, flex_2d)
...             mean = np.mean(price[i - _window:i, col])
...             output[i, col] = _lower < mean < _upper
...     return output

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window', 'lower', 'upper'],
...     output_names=['output']
... ).from_apply_func(
...     apply_func_nb,
...     param_settings=dict(
...         window=flex_col_param_config,
...         lower=flex_elem_param_config,
...         upper=flex_elem_param_config
...     ),
...     pass_flex_2d=True
... )
```

Both bound parameters can now be passed as a scalar (value per whole input), a 1-dimensional
array (value per row or column, depending upon whether input is a Series or a DataFrame),
a 2-dimensional array (value per element), or a list of any of those. This allows for the
highest parameter flexibility at the lowest memory cost.

For example, let's build a grid of two parameter combinations, each being one window size per column
and both bounds per element:

```pycon
>>> MyInd.run(
...     price,
...     window=[np.array([2, 3]), np.array([3, 4])],
...     lower=price.values - 3,
...     upper=price.values + 3,
... ).output
custom_window       2       3               4
custom_lower  array_0 array_0 array_1 array_1
custom_upper  array_0 array_0 array_1 array_1
                    a       b       a       b
2020-01-01        NaN     NaN     NaN     NaN
2020-01-02        NaN     NaN     NaN     NaN
2020-01-03        1.0     NaN     NaN     NaN
2020-01-04        1.0     1.0     1.0     NaN
2020-01-05        1.0     1.0     1.0     1.0
```

Indicators can also be parameterless. See `vectorbt.indicators.basic.OBV`.

## Inputs

`IndicatorFactory` supports passing none, one, or multiple inputs. If multiple inputs are passed,
it tries to broadcast them into a single shape.

Remember that in vectorbt each column means a separate backtest instance. That's why in order to use
multiple pieces of information, such as open, high, low, close, and volume, we need to provide
them as separate pandas objects rather than a single DataFrame.

Let's create a parameterless indicator that measures the position of the close price within each bar:

```pycon
>>> @njit
... def apply_func_nb(high, low, close):
...     return (close - low) / (high - low)

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['high', 'low', 'close'],
...     output_names=['output']
... ).from_apply_func(apply_func_nb)

>>> MyInd.run(price + 1, price - 1, price).output
              a    b
2020-01-01  0.5  0.5
2020-01-02  0.5  0.5
2020-01-03  0.5  0.5
2020-01-04  0.5  0.5
2020-01-05  0.5  0.5
```

To demonstrate broadcasting, let's pass high as a DataFrame, low as a Series, and close as a scalar:

```pycon
>>> df = pd.DataFrame(np.random.uniform(1, 2, size=(5, 2)))
>>> sr = pd.Series(np.random.uniform(0, 1, size=5))
>>> MyInd.run(df, sr, 1).output
          0         1
0  0.960680  0.666820
1  0.400646  0.528456
2  0.093467  0.134777
3  0.037210  0.102411
4  0.529012  0.652602
```

By default, if a Series was passed, it's automatically expanded into a 2-dimensional array.
To keep it as 1-dimensional, set `to_2d` to False.

Similar to parameters, we can also define defaults for inputs. In addition to using scalars
and arrays as default values, we can reference other inputs:

```pycon
>>> @njit
... def apply_func_nb(ts1, ts2, ts3):
...     return ts1 + ts2 + ts3

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['ts1', 'ts2', 'ts3'],
...     output_names=['output']
... ).from_apply_func(apply_func_nb, ts2='ts1', ts3='ts1')

>>> MyInd.run(price).output
               a     b
2020-01-01   3.0  15.0
2020-01-02   6.0  12.0
2020-01-03   9.0   9.0
2020-01-04  12.0   6.0
2020-01-05  15.0   3.0

>>> MyInd.run(price, ts2=price * 2).output
               a     b
2020-01-01   4.0  20.0
2020-01-02   8.0  16.0
2020-01-03  12.0  12.0
2020-01-04  16.0   8.0
2020-01-05  20.0   4.0
```

What if an indicator doesn't take any input arrays? In that case, we can force the user to
at least provide the input shape. Let's define a generator that emulates random returns and
generates synthetic price:

```pycon
>>> @njit
... def apply_func_nb(input_shape, start, mu, sigma):
...     rand_returns = np.random.normal(mu, sigma, input_shape)
...     return start * vbt.nb.nancumprod_nb(rand_returns + 1)

>>> MyInd = vbt.IndicatorFactory(
...     param_names=['start', 'mu', 'sigma'],
...     output_names=['output']
... ).from_apply_func(
...     apply_func_nb,
...     require_input_shape=True,
...     seed=42
... )

>>> MyInd.run(price.shape, 100, 0, 0.01).output
custom_start                     100
custom_mu                          0
custom_sigma        0.01        0.01
0             100.496714   99.861736
1             101.147620  101.382660
2             100.910779  101.145285
3             102.504375  101.921510
4             102.023143  102.474495
```

We can also supply pandas meta such as `input_index` and `input_columns` to the run method:

```pycon
>>> MyInd.run(
...     price.shape, 100, 0, 0.01,
...     input_index=price.index, input_columns=price.columns
... ).output
custom_start                     100
custom_mu                          0
custom_sigma        0.01        0.01
                       a           b
2020-01-01    100.496714   99.861736
2020-01-02    101.147620  101.382660
2020-01-03    100.910779  101.145285
2020-01-04    102.504375  101.921510
2020-01-05    102.023143  102.474495
```

One can even build input-less indicator that decides on the output shape dynamically:

```pycon
>>> from vectorbt.base.combine_fns import apply_and_concat_one

>>> def apply_func(i, ps, input_shape):
...      out = np.full(input_shape, 0)
...      out[:ps[i]] = 1
...      return out

>>> def custom_func(ps):
...     input_shape = (np.max(ps),)
...     return apply_and_concat_one(len(ps), apply_func, ps, input_shape)

>>> MyInd = vbt.IndicatorFactory(
...     param_names=['p'],
...     output_names=['output']
... ).from_custom_func(custom_func)

>>> MyInd.run([1, 2, 3, 4, 5]).output
custom_p  1  2  3  4  5
0         1  1  1  1  1
1         0  1  1  1  1
2         0  0  1  1  1
3         0  0  0  1  1
4         0  0  0  0  1
```

## Outputs

There are two types of outputs: regular and in-place outputs:

* Regular outputs are one or more arrays returned by the function. Each should have an exact
same shape and match the number of columns in the input multiplied by the number of parameter values.
* In-place outputs are not returned but modified in-place. They broadcast together with inputs
and are passed to the calculation function as a list, one per parameter.

Two regular outputs:

```pycon
>>> @njit
... def apply_func_nb(price):
...     return price - 1, price + 1

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     output_names=['out1', 'out2']
... ).from_apply_func(apply_func_nb)

>>> myind = MyInd.run(price)
>>> pd.testing.assert_frame_equal(myind.out1, myind.price - 1)
>>> pd.testing.assert_frame_equal(myind.out2, myind.price + 1)
```

One regular output and one in-place output:

```pycon
>>> @njit
... def apply_func_nb(price, in_out2):
...     in_out2[:] = price + 1
...     return price - 1

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     output_names=['out1'],
...     in_output_names=['in_out2']
... ).from_apply_func(apply_func_nb)

>>> myind = MyInd.run(price)
>>> pd.testing.assert_frame_equal(myind.out1, myind.price - 1)
>>> pd.testing.assert_frame_equal(myind.in_out2, myind.price + 1)
```

Two in-place outputs:

```pycon
>>> @njit
... def apply_func_nb(price, in_out1, in_out2):
...     in_out1[:] = price - 1
...     in_out2[:] = price + 1

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     in_output_names=['in_out1', 'in_out2']
... ).from_apply_func(apply_func_nb)

>>> myind = MyInd.run(price)
>>> pd.testing.assert_frame_equal(myind.in_out1, myind.price - 1)
>>> pd.testing.assert_frame_equal(myind.in_out2, myind.price + 1)
```

By default, in-place outputs are created as empty arrays with uninitialized values.
This allows creation of optional outputs that, if not written, do not occupy much memory.
Since not all outputs are meant to be of data type `float`, we can pass `dtype` in the `in_output_settings`.

```pycon
>>> @njit
... def apply_func_nb(price, in_out):
...     in_out[:] = price > np.mean(price)

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     in_output_names=['in_out']
... ).from_apply_func(
...     apply_func_nb,
...     in_output_settings=dict(in_out=dict(dtype=bool))
... )

>>> MyInd.run(price).in_out
                a      b
2020-01-01  False   True
2020-01-02  False   True
2020-01-03  False  False
2020-01-04   True  False
2020-01-05   True  False
```

Another advantage of in-place outputs is that we can provide their initial state:

```pycon
>>> @njit
... def apply_func_nb(price, in_out1, in_out2):
...     in_out1[:] = in_out1 + price
...     in_out2[:] = in_out2 + price

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     in_output_names=['in_out1', 'in_out2']
... ).from_apply_func(
...     apply_func_nb,
...     in_out1=100,
...     in_out2='price'
... )

>>> myind = MyInd.run(price)
>>> myind.in_out1
              a    b
2020-01-01  101  105
2020-01-02  102  104
2020-01-03  103  103
2020-01-04  104  102
2020-01-05  105  101
>>> myind.in_out2
               a     b
2020-01-01   2.0  10.0
2020-01-02   4.0   8.0
2020-01-03   6.0   6.0
2020-01-04   8.0   4.0
2020-01-05  10.0   2.0
```

## Without Numba

It's also possible to supply a function that is not Numba-compiled. This is handy when working with
third-party libraries (see the implementation of `IndicatorFactory.from_talib`). Additionally,
we can set `keep_pd` to True to pass all inputs as pandas objects instead of raw NumPy arrays.

!!! note
    Already broadcasted pandas meta will be provided; that is, each input array will have the
    same index and columns.

Let's demonstrate this by wrapping a basic composed [pandas_ta](https://github.com/twopirllc/pandas-ta) strategy:

```pycon
>>> import pandas_ta

>>> def apply_func(open, high, low, close, volume, ema_len, linreg_len):
...     df = pd.DataFrame(dict(open=open, high=high, low=low, close=close, volume=volume))
...     df.ta.strategy(pandas_ta.Strategy("MyStrategy", [
...         dict(kind='ema', length=ema_len),
...         dict(kind='linreg', close='EMA_' + str(ema_len), length=linreg_len)
...     ]))
...     return tuple([df.iloc[:, i] for i in range(5, len(df.columns))])

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['open', 'high', 'low', 'close', 'volume'],
...     param_names=['ema_len', 'linreg_len'],
...     output_names=['ema', 'ema_linreg']
... ).from_apply_func(
...     apply_func,
...     keep_pd=True,
...     to_2d=False
... )

>>> my_ind = MyInd.run(
...     ohlcv['Open'],
...     ohlcv['High'],
...     ohlcv['Low'],
...     ohlcv['Close'],
...     ohlcv['Volume'],
...     ema_len=5,
...     linreg_len=[8, 9, 10]
... )

>>> my_ind.ema_linreg
custom_ema_len                                            5
custom_linreg_len            8             9             10
date
2021-02-02                  NaN           NaN           NaN
2021-02-03                  NaN           NaN           NaN
2021-02-04                  NaN           NaN           NaN
2021-02-05                  NaN           NaN           NaN
2021-02-06                  NaN           NaN           NaN
...                         ...           ...           ...
2021-02-25         52309.302811  52602.005326  52899.576568
2021-02-26         50797.264793  51224.188381  51590.825690
2021-02-28         49217.904905  49589.546052  50066.206828
2021-03-01         48316.305403  48553.540713  48911.701664
2021-03-02         47984.395969  47956.885953  48150.929668
```

In the example above, only one Series per open, high, low, close, and volume can be passed.
To enable the indicator to process two-dimensional data, set `to_2d` to True and create a loop
over each column in the `apply_func`.

!!! hint
    Writing a native Numba-compiled code may provide a performance that is magnitudes higher
    than that offered by libraries that work on pandas.

## Raw outputs and caching

`IndicatorFactory` re-uses calculation artifacts whenever possible. Since it was originally designed
for hyperparameter optimization and there are times when parameter values gets repeated,
prevention of processing the same parameter over and over again is inevitable for good performance.
For instance, when the `run_combs` method is being used and `run_unique` is set to True, it first calculates
the raw outputs of all unique parameter combinations and then uses them to build outputs for
the whole parameter grid.

Let's first take a look at a typical raw output by setting `return_raw` to True:

```pycon
>>> raw = vbt.MA.run(price, 2, [False, True], return_raw=True)
>>> raw
([array([[       nan,        nan,        nan,        nan],
         [1.5       , 4.5       , 1.66666667, 4.33333333],
         [2.5       , 3.5       , 2.55555556, 3.44444444],
         [3.5       , 2.5       , 3.51851852, 2.48148148],
         [4.5       , 1.5       , 4.50617284, 1.49382716]])],
 [(2, False), (2, True)],
 2,
 [])
```

It consists of a list of the returned output arrays, a list of the zipped parameter combinations,
the number of input columns, and other objects returned along with output arrays but not listed
in `output_names`. The next time we decide to run the indicator on a subset of the parameters above,
we can simply pass this tuple as the `use_raw` argument. This won't call the calculation function and
will throw an error if some of the requested parameter combinations cannot be found in `raw`.

```pycon
>>> vbt.MA.run(price, 2, True, use_raw=raw).ma
ma_window                    2
ma_ewm                    True
                   a         b
2020-01-01       NaN       NaN
2020-01-02  1.666667  4.333333
2020-01-03  2.555556  3.444444
2020-01-04  3.518519  2.481481
2020-01-05  4.506173  1.493827
```

Here is how the performance compares when repeatedly running the same parameter combination
with and without `run_unique`:

```pycon
>>> a = np.random.uniform(size=(1000,))

>>> %timeit vbt.MA.run(a, np.full(1000, 2), run_unique=False)
73.4 ms ± 4.76 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit vbt.MA.run(a, np.full(1000, 2), run_unique=True)
8.99 ms ± 114 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

!!! note
    `run_unique` is disabled by default.

Enable `run_unique` if input arrays have few columns and there are tons of repeated parameter combinations.
Disable `run_unique` if input arrays are very wide, if two identical parameter combinations can lead to
different results, or when requesting raw output, cache, or additional outputs outside of `output_names`.

Another performance enhancement can be introduced by caching, which has to be implemented by the user.
The class method `IndicatorFactory.from_apply_func` has an argument `cache_func`, which is called
prior to the main calculation.

Consider the following scenario: we want to compute the relative distance between two expensive
rolling windows. We have already decided on the value for the first window, and want to test
thousands of values for the second window. Without caching, and even with `run_unique` enabled,
the first rolling window will be re-calculated over and over again and waste our resources:

```pycon
>>> @njit
... def roll_mean_expensive_nb(price, w):
...     for i in range(100):
...         out = vbt.nb.rolling_mean_nb(price, w)
...     return out

>>> @njit
... def apply_func_nb(price, w1, w2):
...     roll_mean1 = roll_mean_expensive_nb(price, w1)
...     roll_mean2 = roll_mean_expensive_nb(price, w2)
...     return (roll_mean2 - roll_mean1) / roll_mean1

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['w1', 'w2'],
...     output_names=['output'],
... ).from_apply_func(apply_func_nb)

>>> MyInd.run(price, 2, 3).output
custom_w1                    2
custom_w2                    3
                   a         b
2020-01-01       NaN       NaN
2020-01-02       NaN       NaN
2020-01-03 -0.200000  0.142857
2020-01-04 -0.142857  0.200000
2020-01-05 -0.111111  0.333333

>>> %timeit MyInd.run(price, 2, np.arange(2, 1000))
264 ms ± 3.22 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

To avoid this, let's cache all unique rolling windows:

```pycon
>>> @njit
... def cache_func_nb(price, ws1, ws2):
...     cache_dict = dict()
...     ws = ws1.copy()
...     ws.extend(ws2)
...     for i in range(len(ws)):
...         h = hash((ws[i]))
...         if h not in cache_dict:
...             cache_dict[h] = roll_mean_expensive_nb(price, ws[i])
...     return cache_dict

>>> @njit
... def apply_func_nb(price, w1, w2, cache_dict):
...     return (cache_dict[hash(w2)] - cache_dict[hash(w1)]) / cache_dict[hash(w1)]

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['w1', 'w2'],
...     output_names=['output'],
... ).from_apply_func(apply_func_nb, cache_func=cache_func_nb)

>>> MyInd.run(price, 2, 3).output
custom_w1                    2
custom_w2                    3
                   a         b
2020-01-01       NaN       NaN
2020-01-02       NaN       NaN
2020-01-03 -0.200000  0.142857
2020-01-04 -0.142857  0.200000
2020-01-05 -0.111111  0.333333

>>> %timeit MyInd.run(price, 2, np.arange(2, 1000))
145 ms ± 4.55 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

We have cut down the processing time almost in half.

Similar to raw outputs, we can force `IndicatorFactory` to return the cache, so it can be used
in other calculations or even indicators. The clear advantage of this approach is that we don't
rely on some fixed set of parameter combinations any more, but on the values of each parameter,
which gives us more granularity in managing performance.

```pycon
>>> cache = MyInd.run(price, 2, np.arange(2, 1000), return_cache=True)

>>> %timeit MyInd.run(price, np.arange(2, 1000), np.arange(2, 1000), use_cache=cache)
30.1 ms ± 2 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

## Custom properties and methods

Use `custom_output_props` argument when constructing an indicator to define lazy outputs -
outputs that are processed only when explicitly called. They will become cached properties
and, in contrast to regular outputs, they can have an arbitrary shape. For example, let's
attach a property that will calculate the distance between the moving average and the price.

```pycon
>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     param_names=['window'],
...     output_names=['ma'],
...     custom_output_props=dict(distance=lambda self: (self.price - self.ma) / self.ma)
... ).from_apply_func(vbt.nb.rolling_mean_nb)

>>> MyInd.run(price, [2, 3]).distance
custom_window                   2                   3
                      a         b         a         b
2020-01-01          NaN       NaN       NaN       NaN
2020-01-02     0.333333 -0.111111       NaN       NaN
2020-01-03     0.200000 -0.142857  0.500000 -0.250000
2020-01-04     0.142857 -0.200000  0.333333 -0.333333
2020-01-05     0.111111 -0.333333  0.250000 -0.500000
```

Another way of defining own properties and methods is subclassing:

```pycon
>>> class MyIndExtended(MyInd):
...     def plot(self, column=None, **kwargs):
...         self_col = self.select_one(column=column, group_by=False)
...         return self.ma.vbt.plot(**kwargs)

>>> MyIndExtended.run(price, [2, 3])[(2, 'a')].plot()
```

![](/assets/images/MyInd_plot.svg)

## Helper properties and methods

For all in `input_names`, `in_output_names`, `output_names`, and `custom_output_props`,
`IndicatorFactory` will create a bunch of comparison and combination methods, such as for generating signals.
What kind of methods are created can be regulated using `dtype` in the `attr_settings` dictionary.

```pycon
>>> from collections import namedtuple

>>> MyEnum = namedtuple('MyEnum', ['one', 'two'])(0, 1)

>>> def apply_func_nb(price):
...     out_float = np.empty(price.shape, dtype=np.float64)
...     out_bool = np.empty(price.shape, dtype=np.bool_)
...     out_enum = np.empty(price.shape, dtype=np.int64)
...     return out_float, out_bool, out_enum

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     output_names=['out_float', 'out_bool', 'out_enum'],
...     attr_settings=dict(
...         out_float=dict(dtype=np.float64),
...         out_bool=dict(dtype=np.bool_),
...         out_enum=dict(dtype=MyEnum)
... )).from_apply_func(apply_func_nb)

>>> myind = MyInd.run(price)
>>> dir(myind)
[
    ...
    'out_bool',
    'out_bool_and',
    'out_bool_or',
    'out_bool_stats',
    'out_bool_xor',
    'out_enum',
    'out_enum_readable',
    'out_enum_stats',
    'out_float',
    'out_float_above',
    'out_float_below',
    'out_float_equal',
    'out_float_stats',
    ...
    'price',
    'price_above',
    'price_below',
    'price_equal',
    'price_stats',
    ...
]
```

Each of these methods and properties are created for sheer convenience: to easily combine
boolean arrays using logical rules and to compare numeric arrays. All operations are done
strictly using NumPy. Another advantage is utilization of vectorbt's own broadcasting, such
that one can combine inputs and outputs with an arbitrary array-like object, given their
shapes can broadcast together.

We can also do comparison with multiple objects at once by passing them as a tuple/list:

```pycon
>>> myind.price_above([1.5, 2.5])
custom_price_above           1.5           2.5
                        a      b      a      b
2020-01-01          False   True  False   True
2020-01-02           True   True  False   True
2020-01-03           True   True   True   True
2020-01-04           True   True   True  False
2020-01-05           True  False   True  False
```

## Indexing

`IndicatorFactory` attaches pandas indexing to the indicator class thanks to
`vectorbt.base.array_wrapper.ArrayWrapper`. Supported are `iloc`, `loc`,
`*param_name*_loc`, `xs`, and `__getitem__`.

This makes possible accessing rows and columns by labels, integer positions, and parameters.

```pycon
>>> ma = vbt.MA.run(price, [2, 3])

>>> ma[(2, 'b')]
<vectorbt.indicators.basic.MA at 0x7fe4d10ddcc0>

>>> ma[(2, 'b')].ma
2020-01-01    NaN
2020-01-02    4.5
2020-01-03    3.5
2020-01-04    2.5
2020-01-05    1.5
Name: (2, b), dtype: float64

>>> ma.window_loc[2].ma
              a    b
2020-01-01  NaN  NaN
2020-01-02  1.5  4.5
2020-01-03  2.5  3.5
2020-01-04  3.5  2.5
2020-01-05  4.5  1.5
```

## TA-Lib

Indicator factory also provides a class method `IndicatorFactory.from_talib`
that can be used to wrap any function from TA-Lib. It automatically fills all the
necessary information, such as input, parameter and output names.

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats`.

We can attach metrics to any new indicator class:

```pycon
>>> @njit
... def apply_func_nb(price):
...     return price ** 2, price ** 3

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     output_names=['out1', 'out2'],
...     metrics=dict(
...         sum_diff=dict(
...             calc_func=lambda self: self.out2.sum() - self.out1.sum()
...         )
...     )
... ).from_apply_func(
...     apply_func_nb
... )

>>> myind = MyInd.run(price)
>>> myind.stats(column='a')
sum_diff    170.0
Name: a, dtype: float64
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots`.

Similarly to stats, we can attach subplots to any new indicator class:

```pycon
>>> @njit
... def apply_func_nb(price):
...     return price ** 2, price ** 3

>>> def plot_outputs(out1, out2, column=None, fig=None):
...     fig = out1[column].rename('out1').vbt.plot(fig=fig)
...     fig = out2[column].rename('out2').vbt.plot(fig=fig)

>>> MyInd = vbt.IndicatorFactory(
...     input_names=['price'],
...     output_names=['out1', 'out2'],
...     subplots=dict(
...         plot_outputs=dict(
...             plot_func=plot_outputs,
...             resolve_out1=True,
...             resolve_out2=True
...         )
...     )
... ).from_apply_func(
...     apply_func_nb
... )

>>> myind = MyInd.run(price)
>>> myind.plots(column='a')
```

![](/assets/images/IndicatorFactory_plots.svg)
"""

import inspect
import itertools
import warnings
from collections import Counter
from collections import OrderedDict
from datetime import datetime, timedelta
from types import ModuleType

import numpy as np
import pandas as pd
from numba import njit
from numba.typed import List

from vectorbt import _typing as tp
from vectorbt.base import index_fns, reshape_fns, combine_fns
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.base.indexing import build_param_indexer
from vectorbt.generic import nb as generic_nb
from vectorbt.generic.accessors import BaseAccessor
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, resolve_dict, Config, Default
from vectorbt.utils.decorators import classproperty, cached_property
from vectorbt.utils.docs import to_doc
from vectorbt.utils.enum_ import map_enum_fields
from vectorbt.utils.mapping import to_mapping, apply_mapping
from vectorbt.utils.params import to_typed_list, broadcast_params, create_param_product
from vectorbt.utils.random_ import set_seed

try:
    from ta.utils import IndicatorMixin as IndicatorMixinT
except ImportError:
    IndicatorMixinT = tp.Any


def params_to_list(params: tp.Params, is_tuple: bool, is_array_like: bool) -> list:
    """Cast parameters to a list."""
    check_against = [list, List]
    if not is_tuple:
        check_against.append(tuple)
    if not is_array_like:
        check_against.append(np.ndarray)
    if isinstance(params, tuple(check_against)):
        new_params = list(params)
    else:
        new_params = [params]
    return new_params


def prepare_params(param_list: tp.Sequence[tp.Params],
                   param_settings: tp.KwargsLikeSequence = None,
                   input_shape: tp.Optional[tp.Shape] = None,
                   to_2d: bool = False) -> tp.List[tp.List]:
    """Prepare parameters."""
    new_param_list = []
    for i, params in enumerate(param_list):
        _param_settings = resolve_dict(param_settings, i=i)
        is_tuple = _param_settings.get('is_tuple', False)
        dtype = _param_settings.get('dtype', None)
        if checks.is_mapping_like(dtype):
            if checks.is_namedtuple(dtype):
                params = map_enum_fields(params, dtype)
            else:
                params = apply_mapping(params, dtype)
        is_array_like = _param_settings.get('is_array_like', False)
        bc_to_input = _param_settings.get('bc_to_input', False)
        broadcast_kwargs = _param_settings.get('broadcast_kwargs', dict(require_kwargs=dict(requirements='W')))

        new_params = params_to_list(params, is_tuple, is_array_like)
        if bc_to_input is not False:
            # Broadcast to input or its axis
            if is_tuple:
                raise ValueError("Cannot broadcast to input if tuple")
            if input_shape is None:
                raise ValueError("Cannot broadcast to input if input shape is unknown. Pass input_shape.")
            if bc_to_input is True:
                to_shape = input_shape
            else:
                checks.assert_in(bc_to_input, (0, 1))
                # Note that input_shape can be 1D
                if bc_to_input == 0:
                    to_shape = (input_shape[0],)
                else:
                    to_shape = (input_shape[1],) if len(input_shape) > 1 else (1,)
            _new_params = reshape_fns.broadcast(
                *new_params,
                to_shape=to_shape,
                **broadcast_kwargs
            )
            if len(new_params) == 1:
                _new_params = [_new_params]
            else:
                _new_params = list(_new_params)
            if to_2d and bc_to_input is True:
                # If inputs are meant to reshape to 2D, do the same to parameters
                # But only to those that fully resemble inputs (= not raw)
                __new_params = _new_params.copy()
                for j, param in enumerate(__new_params):
                    keep_raw = broadcast_kwargs.get('keep_raw', False)
                    if keep_raw is False or (isinstance(keep_raw, (tuple, list)) and not keep_raw[j]):
                        __new_params[j] = reshape_fns.to_2d(param)
                new_params = __new_params
            else:
                new_params = _new_params
        new_param_list.append(new_params)
    return new_param_list


def build_columns(param_list: tp.Sequence[tp.Sequence[tp.Param]],
                  input_columns: tp.IndexLike,
                  level_names: tp.Optional[tp.Sequence[str]] = None,
                  hide_levels: tp.Optional[tp.Sequence[int]] = None,
                  param_settings: tp.KwargsLikeSequence = None,
                  per_column: bool = False,
                  ignore_default: bool = False,
                  **kwargs) -> tp.Tuple[tp.List[tp.Index], tp.Index]:
    """For each parameter in `param_list`, create a new column level with parameter values
    and stack it on top of `input_columns`.

    Returns a list of parameter indexes and new columns."""
    if level_names is not None:
        checks.assert_len_equal(param_list, level_names)
    if hide_levels is None:
        hide_levels = []
    input_columns = index_fns.to_any_index(input_columns)

    param_indexes = []
    shown_param_indexes = []
    for i in range(len(param_list)):
        params = param_list[i]
        level_name = None
        if level_names is not None:
            level_name = level_names[i]
        if per_column:
            param_index = index_fns.index_from_values(params, name=level_name)
        else:
            _param_settings = resolve_dict(param_settings, i=i)
            _per_column = _param_settings.get('per_column', False)
            if _per_column:
                param_index = None
                for param in params:
                    bc_param = np.broadcast_to(param, (len(input_columns),))
                    _param_index = index_fns.index_from_values(bc_param, name=level_name)
                    if param_index is None:
                        param_index = _param_index
                    else:
                        param_index = param_index.append(_param_index)
                if len(param_index) == 1 and len(input_columns) > 1:
                    # When using flexible column-wise parameters
                    param_index = index_fns.repeat_index(
                        param_index,
                        len(input_columns),
                        ignore_default=ignore_default
                    )
            else:
                param_index = index_fns.index_from_values(param_list[i], name=level_name)
                param_index = index_fns.repeat_index(
                    param_index,
                    len(input_columns),
                    ignore_default=ignore_default
                )
        param_indexes.append(param_index)
        if i not in hide_levels:
            shown_param_indexes.append(param_index)
    if len(shown_param_indexes) > 0:
        if not per_column:
            n_param_values = len(param_list[0]) if len(param_list) > 0 else 1
            input_columns = index_fns.tile_index(
                input_columns,
                n_param_values,
                ignore_default=ignore_default
            )
        stacked_columns = index_fns.stack_indexes([*shown_param_indexes, input_columns], **kwargs)
        return param_indexes, stacked_columns
    return param_indexes, input_columns


CacheOutputT = tp.Any
RawOutputT = tp.Tuple[tp.List[tp.Array2d], tp.List[tp.Tuple[tp.Param, ...]], int, tp.List[tp.Any]]
InputListT = tp.List[tp.Array2d]
InputMapperT = tp.Optional[tp.Array1d]
InOutputListT = tp.List[tp.Array2d]
OutputListT = tp.List[tp.Array2d]
ParamListT = tp.List[tp.List[tp.Param]]
MapperListT = tp.List[tp.Index]
OtherListT = tp.List[tp.Any]
PipelineOutputT = tp.Tuple[
    ArrayWrapper,
    InputListT,
    InputMapperT,
    InOutputListT,
    OutputListT,
    ParamListT,
    MapperListT,
    OtherListT
]


def run_pipeline(
        num_ret_outputs: int,
        custom_func: tp.Callable,
        *args,
        require_input_shape: bool = False,
        input_shape: tp.Optional[tp.RelaxedShape] = None,
        input_index: tp.Optional[tp.IndexLike] = None,
        input_columns: tp.Optional[tp.IndexLike] = None,
        input_list: tp.Optional[tp.Sequence[tp.ArrayLike]] = None,
        in_output_list: tp.Optional[tp.Sequence[tp.ArrayLike]] = None,
        in_output_settings: tp.KwargsLikeSequence = None,
        broadcast_kwargs: tp.KwargsLike = None,
        param_list: tp.Optional[tp.Sequence[tp.Param]] = None,
        param_product: bool = False,
        param_settings: tp.KwargsLikeSequence = None,
        run_unique: bool = False,
        silence_warnings: bool = False,
        per_column: bool = False,
        pass_col: bool = False,
        keep_pd: bool = False,
        to_2d: bool = True,
        as_lists: bool = False,
        pass_input_shape: bool = False,
        pass_flex_2d: bool = False,
        level_names: tp.Optional[tp.Sequence[str]] = None,
        hide_levels: tp.Optional[tp.Sequence[int]] = None,
        stacking_kwargs: tp.KwargsLike = None,
        return_raw: bool = False,
        use_raw: tp.Optional[RawOutputT] = None,
        wrapper_kwargs: tp.KwargsLike = None,
        seed: tp.Optional[int] = None,
        **kwargs) -> tp.Union[CacheOutputT, RawOutputT, PipelineOutputT]:
    """A pipeline for running an indicator, used by `IndicatorFactory`.

    Args:
        num_ret_outputs (int): The number of output arrays returned by `custom_func`.
        custom_func (callable): A custom calculation function.

            See `IndicatorFactory.from_custom_func`.
        *args: Arguments passed to the `custom_func`.
        require_input_shape (bool): Whether to input shape is required.

            Will set `pass_input_shape` to True and raise an error if `input_shape` is None.
        input_shape (tuple): Shape to broadcast each input to.

            Can be passed to `custom_func`. See `pass_input_shape`.
        input_index (index_like): Sets index of each input.

            Can be used to label index if no inputs passed.
        input_columns (index_like): Sets columns of each input.

            Can be used to label columns if no inputs passed.
        input_list (list of array_like): A list of input arrays.
        in_output_list (list of array_like): A list of in-place output arrays.
            
            If an array should be generated, pass None.
        in_output_settings (dict or list of dict): Settings corresponding to each in-place output.

            Following keys are accepted:

            * `dtype`: Create this array using this data type and `np.empty`. Default is None.
        broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`
            to broadcast inputs.
        param_list (list of any): A list of parameters.

            Each element is either an array-like object or a single value of any type.
        param_product (bool): Whether to build a Cartesian product out of all parameters.
        param_settings (dict or list of dict): Settings corresponding to each parameter.

            Following keys are accepted:

            * `dtype`: If data type is an enumerated type or other mapping, and a string as parameter
                value was passed, will convert it first.
            * `is_tuple`: If tuple was passed, it will be considered as a single value.
                To treat it as multiple values, pack it into a list.
            * `is_array_like`: If array-like object was passed, it will be considered as a single value.
                To treat it as multiple values, pack it into a list.
            * `bc_to_input`: Whether to broadcast parameter to input size. You can also broadcast
                parameter to an axis by passing an integer.
            * `broadcast_kwargs`: Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            * `per_column`: Whether each parameter value can be split per column such that it can
                be better reflected in a multi-index. Does not affect broadcasting.
        run_unique (bool): Whether to run only on unique parameter combinations.

            Disable if two identical parameter combinations can lead to different results
            (e.g., due to randomness) or if inputs are large and `custom_func` is fast.

            !!! note
                Cache, raw output, and output objects outside of `num_ret_outputs` will be returned
                for unique parameter combinations only.
        silence_warnings (bool): Whether to hide warnings such as coming from `run_unique`.
        per_column (bool): Whether to split the DataFrame into Series, one per column, and run `custom_func`
            on each Series.

            Each list of parameter values will broadcast to the number of columns and
            each parameter value will be applied per Series rather than per DataFrame.
            Input shape must be known beforehand.
        pass_col (bool): Whether to pass column index as keyword argument if `per_column` is set to True.
        keep_pd (bool): Whether to keep inputs as pandas objects, otherwise convert to NumPy arrays.
        to_2d (bool): Whether to reshape inputs to 2-dim arrays, otherwise keep as-is.
        as_lists (bool): Whether to pass inputs and parameters to `custom_func` as lists.

            If `custom_func` is Numba-compiled, passes tuples.
        pass_input_shape (bool): Whether to pass `input_shape` to `custom_func` as keyword argument.
        pass_flex_2d (bool): Whether to pass `flex_2d` to `custom_func` as keyword argument.
        level_names (list of str): A list of column level names corresponding to each parameter.

            Should have the same length as `param_list`.
        hide_levels (list of int): A list of indices of parameter levels to hide.
        stacking_kwargs (dict): Keyword arguments passed to `vectorbt.base.index_fns.repeat_index`,
            `vectorbt.base.index_fns.tile_index`, and `vectorbt.base.index_fns.stack_indexes`
            when stacking parameter and input column levels.
        return_raw (bool): Whether to return raw output without post-processing and hashed parameter tuples.
        use_raw (bool): Takes the raw results and uses them instead of running `custom_func`.
        wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
        seed (int): Set seed to make output deterministic.
        **kwargs: Keyword arguments passed to the `custom_func`.

            Some common arguments include `return_cache` to return cache and `use_cache` to use cache.
            Those are only applicable to `custom_func` that supports it (`custom_func` created using
            `IndicatorFactory.from_apply_func` are supported by default).
            
    Returns:
        Array wrapper, list of inputs (`np.ndarray`), input mapper (`np.ndarray`), list of outputs
        (`np.ndarray`), list of parameter arrays (`np.ndarray`), list of parameter mappers (`np.ndarray`),
        list of outputs that are outside of `num_ret_outputs`.

    Explanation:
        Here is a subset of tasks that the function `run_pipeline` does:

        * Takes one or multiple array objects in `input_list` and broadcasts them.

        ```pycon
        >>> sr = pd.Series([1, 2], index=['x', 'y'])
        >>> df = pd.DataFrame([[3, 4], [5, 6]], index=['x', 'y'], columns=['a', 'b'])
        >>> input_list = vbt.base.reshape_fns.broadcast(sr, df)
        >>> input_list[0]
           a  b
        x  1  1
        y  2  2
        >>> input_list[1]
           a  b
        x  3  4
        y  5  6
        ```

        * Takes one or multiple parameters in `param_list`, converts them to NumPy arrays and
            broadcasts them.

        ```pycon
        >>> p1, p2, p3 = 1, [2, 3, 4], [False]
        >>> param_list = vbt.base.reshape_fns.broadcast(p1, p2, p3)
        >>> param_list[0]
        array([1, 1, 1])
        >>> param_list[1]
        array([2, 3, 4])
        >>> param_list[2]
        array([False, False, False])
        ```

        * Performs calculation using `custom_func` to build output arrays (`output_list`) and
            other objects (`other_list`, optionally).

        ```pycon
        >>> def custom_func(ts1, ts2, p1, p2, p3, *args, **kwargs):
        ...     return np.hstack((
        ...         ts1 + ts2 + p1[0] * p2[0],
        ...         ts1 + ts2 + p1[1] * p2[1],
        ...         ts1 + ts2 + p1[2] * p2[2],
        ...     ))

        >>> output = custom_func(*input_list, *param_list)
        >>> output
        array([[ 6,  7,  7,  8,  8,  9],
               [ 9, 10, 10, 11, 11, 12]])
        ```

        * Creates new column hierarchy based on parameters and level names.

        ```pycon
        >>> p1_columns = pd.Index(param_list[0], name='p1')
        >>> p2_columns = pd.Index(param_list[1], name='p2')
        >>> p3_columns = pd.Index(param_list[2], name='p3')
        >>> p_columns = vbt.base.index_fns.stack_indexes([p1_columns, p2_columns, p3_columns])
        >>> new_columns = vbt.base.index_fns.combine_indexes([p_columns, input_list[0].columns])

        >>> output_df = pd.DataFrame(output, columns=new_columns)
        >>> output_df
        p1                                         1
        p2             2             3             4
        p3  False  False  False  False  False  False
                a      b      a      b      a      b
        0       6      7      7      8      8      9
        1       9     10     10     11     11     12
        ```

        * Broadcasts objects in `input_list` to match the shape of objects in `output_list` through tiling.
            This is done to be able to compare them and generate signals, since we cannot compare NumPy
            arrays that have totally different shapes, such as (2, 2) and (2, 6).

        ```pycon
        >>> new_input_list = [
        ...     input_list[0].vbt.tile(len(param_list[0]), keys=p_columns),
        ...     input_list[1].vbt.tile(len(param_list[0]), keys=p_columns)
        ... ]
        >>> new_input_list[0]
        p1                                         1
        p2             2             3             4
        p3  False  False  False  False  False  False
                a      b      a      b      a      b
        0       1      1      1      1      1      1
        1       2      2      2      2      2      2
        ```

        * Builds parameter mappers that will link parameters from `param_list` to columns in
            `input_list` and `output_list`. This is done to enable column indexing using parameter values.
    """
    if require_input_shape:
        checks.assert_not_none(input_shape)
        pass_input_shape = True
    if input_index is not None:
        input_index = index_fns.to_any_index(input_index)
    if input_columns is not None:
        input_columns = index_fns.to_any_index(input_columns)
    if input_list is None:
        input_list = []
    else:
        input_list = list(input_list)
    if in_output_list is None:
        in_output_list = []
    else:
        in_output_list = list(in_output_list)
    if in_output_settings is None:
        in_output_settings = {}
    checks.assert_dict_sequence_valid(in_output_settings, ['dtype'])
    if broadcast_kwargs is None:
        broadcast_kwargs = {}
    if param_list is None:
        param_list = []
    else:
        param_list = list(param_list)
    if param_settings is None:
        param_settings = {}
    checks.assert_dict_sequence_valid(param_settings, [
        'dtype',
        'is_tuple',
        'is_array_like',
        'bc_to_input',
        'broadcast_kwargs',
        'per_column'
    ])
    if hide_levels is None:
        hide_levels = []
    if stacking_kwargs is None:
        stacking_kwargs = {}
    if wrapper_kwargs is None:
        wrapper_kwargs = {}
    if keep_pd and checks.is_numba_func(custom_func):
        raise ValueError("Cannot pass pandas objects to a Numba-compiled custom_func. Set keep_pd to False.")

    in_output_idxs = [i for i, x in enumerate(in_output_list) if x is not None]
    if len(in_output_idxs) > 0:
        # In-place outputs should broadcast together with inputs
        input_list += [in_output_list[i] for i in in_output_idxs]
    if len(input_list) > 0:
        # Broadcast inputs
        # If input_shape is provided, will broadcast all inputs to this shape
        broadcast_kwargs = merge_dicts(dict(
            to_shape=input_shape,
            index_from=input_index,
            columns_from=input_columns,
            require_kwargs=dict(requirements='W')
        ), broadcast_kwargs)
        bc_input_list, input_shape, input_index, input_columns = reshape_fns.broadcast(
            *input_list,
            return_meta=True,
            **broadcast_kwargs
        )
        if input_index is None:
            input_index = pd.RangeIndex(start=0, step=1, stop=input_shape[0])
        if input_columns is None:
            input_columns = pd.RangeIndex(start=0, step=1, stop=input_shape[1] if len(input_shape) > 1 else 1)
        if len(input_list) == 1:
            bc_input_list = (bc_input_list,)
        input_list = list(map(np.asarray, bc_input_list))
    if len(in_output_idxs) > 0:
        # Separate inputs and in-place outputs
        in_output_list = input_list[-len(in_output_idxs):]
        input_list = input_list[:-len(in_output_idxs)]

    # Reshape input shape
    if input_shape is not None and not isinstance(input_shape, tuple):
        input_shape = (input_shape,)
    # Keep original input_shape for per_column=True
    orig_input_shape = input_shape
    orig_input_shape_2d = input_shape
    if input_shape is not None:
        orig_input_shape_2d = input_shape if len(input_shape) > 1 else (input_shape[0], 1)
    if per_column:
        # input_shape is now the size of one column
        if input_shape is None:
            raise ValueError("input_shape is required when per_column=True")
        input_shape = (input_shape[0],)
    input_shape_ready = input_shape
    input_shape_2d = input_shape
    if input_shape is not None:
        input_shape_2d = input_shape if len(input_shape) > 1 else (input_shape[0], 1)
    if to_2d:
        if input_shape is not None:
            input_shape_ready = input_shape_2d  # ready for custom_func

    # Prepare parameters
    # NOTE: input_shape instead of input_shape_ready since parameters should
    # broadcast by the same rules as inputs
    param_list = prepare_params(param_list, param_settings, input_shape=input_shape, to_2d=to_2d)
    if len(param_list) > 1:
        if level_names is not None:
            # Check level names
            checks.assert_len_equal(param_list, level_names)
            # Columns should be free of the specified level names
            if input_columns is not None:
                for level_name in level_names:
                    if level_name is not None:
                        checks.assert_level_not_exists(input_columns, level_name)
        if param_product:
            # Make Cartesian product out of all params
            param_list = create_param_product(param_list)
    if len(param_list) > 0:
        # Broadcast such that each array has the same length
        if per_column:
            # The number of parameters should match the number of columns before split
            param_list = broadcast_params(param_list, to_n=orig_input_shape_2d[1])
        else:
            param_list = broadcast_params(param_list)
    n_param_values = len(param_list[0]) if len(param_list) > 0 else 1
    use_run_unique = False
    param_list_unique = param_list
    if not per_column and run_unique:
        try:
            # Try to get all unique parameter combinations
            param_tuples = list(zip(*param_list))
            unique_param_tuples = list(OrderedDict.fromkeys(param_tuples).keys())
            if len(unique_param_tuples) < len(param_tuples):
                param_list_unique = list(map(list, zip(*unique_param_tuples)))
                use_run_unique = True
        except:
            pass
    if checks.is_numba_func(custom_func):
        # Numba can't stand untyped lists
        param_list_ready = [to_typed_list(params) for params in param_list_unique]
    else:
        param_list_ready = param_list_unique
    n_unique_param_values = len(param_list_unique[0]) if len(param_list_unique) > 0 else 1

    # Prepare inputs
    if per_column:
        # Split each input into Series/1-dim arrays, one per column
        input_list_ready = []
        for input in input_list:
            input_2d = reshape_fns.to_2d(input)
            col_inputs = []
            for i in range(input_2d.shape[1]):
                if to_2d:
                    col_input = input_2d[:, [i]]
                else:
                    col_input = input_2d[:, i]
                if keep_pd:
                    # Keep as pandas object
                    col_input = ArrayWrapper(input_index, input_columns[[i]], col_input.ndim).wrap(col_input)
                col_inputs.append(col_input)
            input_list_ready.append(col_inputs)
    else:
        input_list_ready = []
        for input in input_list:
            new_input = input
            if to_2d:
                new_input = reshape_fns.to_2d(input)
            if keep_pd:
                # Keep as pandas object
                new_input = ArrayWrapper(input_index, input_columns, new_input.ndim).wrap(new_input)
            input_list_ready.append(new_input)

    # Prepare in-place outputs
    in_output_list_ready = []
    j = 0
    for i in range(len(in_output_list)):
        if input_shape_2d is None:
            raise ValueError("input_shape is required when using in-place outputs")
        if i in in_output_idxs:
            # This in-place output has been already broadcast with inputs
            in_output_wide = np.require(in_output_list[j], requirements='W')
            if not per_column:
                # One per parameter combination
                in_output_wide = reshape_fns.tile(in_output_wide, n_unique_param_values, axis=1)
            j += 1
        else:
            # This in-place output hasn't been provided, so create empty
            _in_output_settings = in_output_settings if isinstance(in_output_settings, dict) else in_output_settings[i]
            dtype = _in_output_settings.get('dtype', None)
            in_output_shape = (input_shape_2d[0], input_shape_2d[1] * n_unique_param_values)
            in_output_wide = np.empty(in_output_shape, dtype=dtype)
        in_output_list[i] = in_output_wide
        in_outputs = []
        # Split each in-place output into chunks, each of input shape, and append to a list
        for i in range(n_unique_param_values):
            in_output = in_output_wide[:, i * input_shape_2d[1]: (i + 1) * input_shape_2d[1]]
            if len(input_shape_ready) == 1:
                in_output = in_output[:, 0]
            if keep_pd:
                if per_column:
                    in_output = ArrayWrapper(input_index, input_columns[[i]], in_output.ndim).wrap(in_output)
                else:
                    in_output = ArrayWrapper(input_index, input_columns, in_output.ndim).wrap(in_output)
            in_outputs.append(in_output)
        in_output_list_ready.append(in_outputs)
    if checks.is_numba_func(custom_func):
        # Numba can't stand untyped lists
        in_output_list_ready = [to_typed_list(in_outputs) for in_outputs in in_output_list_ready]

    def _use_raw(_raw):
        # Use raw results of previous run to build outputs
        _output_list, _param_map, _n_input_cols, _other_list = _raw
        idxs = np.array([_param_map.index(param_tuple) for param_tuple in zip(*param_list)])
        _output_list = [
            np.hstack([o[:, idx * _n_input_cols:(idx + 1) * _n_input_cols] for idx in idxs])
            for o in _output_list
        ]
        return _output_list, _param_map, _n_input_cols, _other_list

    # Get raw results
    if use_raw is not None:
        # Use raw results of previous run to build outputs
        output_list, param_map, n_input_cols, other_list = _use_raw(use_raw)
    else:
        # Prepare other arguments
        func_args = args
        func_kwargs = {}
        if pass_input_shape:
            func_kwargs['input_shape'] = input_shape_ready
        if pass_flex_2d:
            if input_shape is None:
                raise ValueError("Cannot determine flex_2d without inputs")
            func_kwargs['flex_2d'] = len(input_shape) == 2
        func_kwargs = merge_dicts(func_kwargs, kwargs)

        # Set seed
        if seed is not None:
            set_seed(seed)

        def _call_custom_func(_input_list_ready, _in_output_list_ready, _param_list_ready, *_func_args, **_func_kwargs):
            # Run the function
            if as_lists:
                if checks.is_numba_func(custom_func):
                    return custom_func(
                        tuple(_input_list_ready),
                        tuple(_in_output_list_ready),
                        tuple(_param_list_ready),
                        *_func_args, **_func_kwargs
                    )
                return custom_func(
                    _input_list_ready,
                    _in_output_list_ready,
                    _param_list_ready,
                    *_func_args, **_func_kwargs
                )
            return custom_func(
                *_input_list_ready,
                *_in_output_list_ready,
                *_param_list_ready,
                *_func_args, **_func_kwargs
            )

        if per_column:
            output = []
            for col in range(orig_input_shape_2d[1]):
                # Select the column of each input and in-place output, and the respective parameter combination
                _input_list_ready = []
                for _inputs in input_list_ready:
                    # Each input array is now one column wide
                    _input_list_ready.append(_inputs[col])

                _in_output_list_ready = []
                for _in_outputs in in_output_list_ready:
                    # Each in-output array is now one column wide
                    if isinstance(_in_outputs, List):
                        __in_outputs = List()
                    else:
                        __in_outputs = []
                    __in_outputs.append(_in_outputs[col])
                    _in_output_list_ready.append(__in_outputs)

                _param_list_ready = []
                for _params in param_list_ready:
                    # Each parameter list is now one element long
                    if isinstance(_params, List):
                        __params = List()
                    else:
                        __params = []
                    __params.append(_params[col])
                    _param_list_ready.append(__params)

                _func_args = func_args
                _func_kwargs = func_kwargs.copy()
                if 'use_cache' in func_kwargs:
                    use_cache = func_kwargs['use_cache']
                    if isinstance(use_cache, list) and len(use_cache) == orig_input_shape_2d[1]:
                        # Pass cache for this column
                        _func_kwargs['use_cache'] = func_kwargs['use_cache'][col]
                if pass_col:
                    _func_kwargs['col'] = col
                col_output = _call_custom_func(
                    _input_list_ready,
                    _in_output_list_ready,
                    _param_list_ready,
                    *_func_args,
                    **_func_kwargs
                )
                output.append(col_output)
        else:
            output = _call_custom_func(
                input_list_ready,
                in_output_list_ready,
                param_list_ready,
                *func_args,
                **func_kwargs
            )

        # Return cache
        if kwargs.get('return_cache', False):
            if use_run_unique and not silence_warnings:
                warnings.warn("Cache is produced by unique parameter "
                              "combinations when run_unique=True", stacklevel=2)
            return output

        def _split_output(output):
            # Post-process results
            if output is None:
                _output_list = []
                _other_list = []
            else:
                if isinstance(output, (tuple, list, List)):
                    _output_list = list(output)
                else:
                    _output_list = [output]
                # Other outputs should be returned without post-processing (for example cache_dict)
                if len(_output_list) > num_ret_outputs:
                    _other_list = _output_list[num_ret_outputs:]
                    if use_run_unique and not silence_warnings:
                        warnings.warn("Additional output objects are produced by unique parameter "
                                      "combinations when run_unique=True", stacklevel=2)
                else:
                    _other_list = []
                # Process only the num_ret_outputs outputs
                _output_list = _output_list[:num_ret_outputs]
            if len(_output_list) != num_ret_outputs:
                raise ValueError("Number of returned outputs other than expected")
            _output_list = list(map(lambda x: reshape_fns.to_2d_array(x), _output_list))
            return _output_list, _other_list

        if per_column:
            output_list = []
            other_list = []
            for _output in output:
                __output_list, __other_list = _split_output(_output)
                output_list.append(__output_list)
                if len(__other_list) > 0:
                    other_list.append(__other_list)
            # Concatenate each output (must be one column wide)
            output_list = [np.hstack(input_group) for input_group in zip(*output_list)]
        else:
            output_list, other_list = _split_output(output)

        # In-place outputs are treated as outputs from here
        output_list = in_output_list + output_list

        # Prepare raw
        param_map = list(zip(*param_list_unique))  # account for use_run_unique
        output_shape = output_list[0].shape
        for output in output_list:
            if output.shape != output_shape:
                raise ValueError("All outputs must have the same shape")
        if per_column:
            n_input_cols = 1
        else:
            n_input_cols = output_shape[1] // n_unique_param_values
        if input_shape_2d is not None:
            if n_input_cols != input_shape_2d[1]:
                if per_column:
                    raise ValueError("All outputs must have one column when per_column=True")
                else:
                    raise ValueError("All outputs must have the number of columns = #input columns x #parameters")
        raw = output_list, param_map, n_input_cols, other_list
        if return_raw:
            if use_run_unique and not silence_warnings:
                warnings.warn("Raw output is produced by unique parameter "
                              "combinations when run_unique=True", stacklevel=2)
            return raw
        if use_run_unique:
            output_list, param_map, n_input_cols, other_list = _use_raw(raw)

    # Update shape and other meta if no inputs
    if input_shape is None:
        if n_input_cols == 1:
            input_shape = (output_list[0].shape[0],)
        else:
            input_shape = (output_list[0].shape[0], n_input_cols)
    else:
        input_shape = orig_input_shape
    if input_index is None:
        input_index = pd.RangeIndex(start=0, step=1, stop=input_shape[0])
    if input_columns is None:
        input_columns = pd.RangeIndex(start=0, step=1, stop=input_shape[1] if len(input_shape) > 1 else 1)

    # Build column hierarchy and create mappers
    if len(param_list) > 0:
        # Build new column levels on top of input levels
        param_indexes, new_columns = build_columns(
            param_list,
            input_columns,
            level_names=level_names,
            hide_levels=hide_levels,
            param_settings=param_settings,
            per_column=per_column,
            **stacking_kwargs
        )
        # Build a mapper that maps old columns in inputs to new columns
        # Instead of tiling all inputs to the shape of outputs and wasting memory,
        # we just keep a mapper and perform the tiling when needed
        input_mapper = None
        if len(input_list) > 0:
            if per_column:
                input_mapper = np.arange(len(input_columns))
            else:
                input_mapper = np.tile(np.arange(len(input_columns)), n_param_values)
        # Build mappers to easily map between parameters and columns
        mapper_list = [param_indexes[i] for i in range(len(param_list))]
    else:
        # Some indicators don't have any params
        new_columns = input_columns
        input_mapper = None
        mapper_list = []

    # Return artifacts: no pandas objects, just a wrapper and NumPy arrays
    new_ndim = len(input_shape) if output_list[0].shape[1] == 1 else output_list[0].ndim
    wrapper = ArrayWrapper(input_index, new_columns, new_ndim, **wrapper_kwargs)

    return wrapper, \
           input_list, \
           input_mapper, \
           output_list[:len(in_output_list)], \
           output_list[len(in_output_list):], \
           param_list, \
           mapper_list, \
           other_list


def combine_objs(obj: tp.SeriesFrame,
                 other: tp.MaybeTupleList[tp.Union[tp.ArrayLike, BaseAccessor]],
                 *args, level_name: tp.Optional[str] = None,
                 keys: tp.Optional[tp.IndexLike] = None,
                 allow_multiple: bool = True,
                 **kwargs) -> tp.SeriesFrame:
    """Combines/compares `obj` to `other`, for example, to generate signals.

    Both will broadcast together.
    Pass `other` as a tuple or a list to compare with multiple arguments.
    In this case, a new column level will be created with the name `level_name`.

    See `vectorbt.base.accessors.BaseAccessor.combine`."""
    if allow_multiple and isinstance(other, (tuple, list)):
        if keys is None:
            keys = index_fns.index_from_values(other, name=level_name)
    return obj.vbt.combine(other, *args, keys=keys, concat=True, allow_multiple=allow_multiple, **kwargs)


IndicatorBaseT = tp.TypeVar("IndicatorBaseT", bound="IndicatorBase")
RunOutputT = tp.Union[IndicatorBaseT, tp.Tuple[tp.Any, ...], RawOutputT, CacheOutputT]
RunCombsOutputT = tp.Tuple[IndicatorBaseT, ...]


class MetaIndicatorBase(type(StatsBuilderMixin), type(PlotsBuilderMixin)):
    pass


class IndicatorBase(Wrapping, StatsBuilderMixin, PlotsBuilderMixin, metaclass=MetaIndicatorBase):
    """Indicator base class.

    Properties should be set before instantiation."""
    _short_name: str
    _level_names: tp.Tuple[str, ...]
    _input_names: tp.Tuple[str, ...]
    _param_names: tp.Tuple[str, ...]
    _in_output_names: tp.Tuple[str, ...]
    _output_names: tp.Tuple[str, ...]
    _output_flags: tp.Kwargs

    @property
    def short_name(self) -> str:
        """Name of the indicator."""
        return self._short_name

    @property
    def level_names(self) -> tp.Tuple[str, ...]:
        """Column level names corresponding to each parameter."""
        return self._level_names

    @classproperty
    def input_names(cls_or_self) -> tp.Tuple[str, ...]:
        """Names of the input arrays."""
        return cls_or_self._input_names

    @classproperty
    def param_names(cls_or_self) -> tp.Tuple[str, ...]:
        """Names of the parameters."""
        return cls_or_self._param_names

    @classproperty
    def in_output_names(cls_or_self) -> tp.Tuple[str, ...]:
        """Names of the in-place output arrays."""
        return cls_or_self._in_output_names

    @classproperty
    def output_names(cls_or_self) -> tp.Tuple[str, ...]:
        """Names of the regular output arrays."""
        return cls_or_self._output_names

    @classproperty
    def output_flags(cls_or_self) -> tp.Kwargs:
        """Dictionary of output flags."""
        return cls_or_self._output_flags

    def __init__(self,
                 wrapper: ArrayWrapper,
                 input_list: InputListT,
                 input_mapper: InputMapperT,
                 in_output_list: InOutputListT,
                 output_list: OutputListT,
                 param_list: ParamListT,
                 mapper_list: MapperListT,
                 short_name: str,
                 level_names: tp.Tuple[str, ...]) -> None:
        Wrapping.__init__(
            self,
            wrapper,
            input_list=input_list,
            input_mapper=input_mapper,
            in_output_list=in_output_list,
            output_list=output_list,
            param_list=param_list,
            mapper_list=mapper_list,
            short_name=short_name,
            level_names=level_names
        )
        StatsBuilderMixin.__init__(self)
        PlotsBuilderMixin.__init__(self)

        if input_mapper is not None:
            checks.assert_equal(input_mapper.shape[0], wrapper.shape_2d[1])
        for ts in input_list:
            checks.assert_equal(ts.shape[0], wrapper.shape_2d[0])
        for ts in in_output_list + output_list:
            checks.assert_equal(ts.shape, wrapper.shape_2d)
        for params in param_list:
            checks.assert_len_equal(param_list[0], params)
        for mapper in mapper_list:
            checks.assert_equal(len(mapper), wrapper.shape_2d[1])
        checks.assert_instance_of(short_name, str)
        checks.assert_len_equal(level_names, param_list)

        setattr(self, '_short_name', short_name)
        setattr(self, '_level_names', level_names)

        for i, ts_name in enumerate(self.input_names):
            setattr(self, f'_{ts_name}', input_list[i])
        setattr(self, '_input_mapper', input_mapper)
        for i, in_output_name in enumerate(self.in_output_names):
            setattr(self, f'_{in_output_name}', in_output_list[i])
        for i, output_name in enumerate(self.output_names):
            setattr(self, f'_{output_name}', output_list[i])
        for i, param_name in enumerate(self.param_names):
            setattr(self, f'_{param_name}_list', param_list[i])
            setattr(self, f'_{param_name}_mapper', mapper_list[i])
        if len(self.param_names) > 1:
            tuple_mapper = list(zip(*list(mapper_list)))
            setattr(self, '_tuple_mapper', tuple_mapper)

    def indexing_func(self: IndicatorBaseT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> IndicatorBaseT:
        """Perform indexing on `IndicatorBase`."""
        new_wrapper, idx_idxs, _, col_idxs = self.wrapper.indexing_func_meta(pd_indexing_func, **kwargs)
        idx_idxs_arr = reshape_fns.to_1d_array(idx_idxs)
        col_idxs_arr = reshape_fns.to_1d_array(col_idxs)
        if np.array_equal(idx_idxs_arr, np.arange(self.wrapper.shape_2d[0])):
            idx_idxs_arr = slice(None, None, None)
        if np.array_equal(col_idxs_arr, np.arange(self.wrapper.shape_2d[1])):
            col_idxs_arr = slice(None, None, None)

        input_mapper = getattr(self, '_input_mapper', None)
        if input_mapper is not None:
            input_mapper = input_mapper[col_idxs_arr]
        input_list = []
        for input_name in self.input_names:
            input_list.append(getattr(self, f'_{input_name}')[idx_idxs_arr])
        in_output_list = []
        for in_output_name in self.in_output_names:
            in_output_list.append(getattr(self, f'_{in_output_name}')[idx_idxs_arr, :][:, col_idxs_arr])
        output_list = []
        for output_name in self.output_names:
            output_list.append(getattr(self, f'_{output_name}')[idx_idxs_arr, :][:, col_idxs_arr])
        param_list = []
        for param_name in self.param_names:
            param_list.append(getattr(self, f'_{param_name}_list'))
        mapper_list = []
        for param_name in self.param_names:
            # Tuple mapper is a list because of its complex data type
            mapper_list.append(getattr(self, f'_{param_name}_mapper')[col_idxs_arr])

        return self.replace(
            wrapper=new_wrapper,
            input_list=input_list,
            input_mapper=input_mapper,
            in_output_list=in_output_list,
            output_list=output_list,
            param_list=param_list,
            mapper_list=mapper_list
        )

    @classmethod
    def _run(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunOutputT:
        """Private run method."""
        raise NotImplementedError

    @classmethod
    def run(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunOutputT:
        """Public run method."""
        return cls._run(*args, **kwargs)

    @classmethod
    def _run_combs(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunCombsOutputT:
        """Private run combinations method."""
        raise NotImplementedError

    @classmethod
    def run_combs(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunCombsOutputT:
        """Public run combinations method."""
        return cls._run_combs(*args, **kwargs)


class IndicatorFactory:
    def __init__(self,
                 class_name: str = 'Indicator',
                 class_docstring: str = '',
                 module_name: tp.Optional[str] = __name__,
                 short_name: tp.Optional[str] = None,
                 prepend_name: bool = True,
                 input_names: tp.Optional[tp.Sequence[str]] = None,
                 param_names: tp.Optional[tp.Sequence[str]] = None,
                 in_output_names: tp.Optional[tp.Sequence[str]] = None,
                 output_names: tp.Optional[tp.Sequence[str]] = None,
                 output_flags: tp.KwargsLike = None,
                 custom_output_props: tp.KwargsLike = None,
                 attr_settings: tp.KwargsLike = None,
                 metrics: tp.Optional[tp.Kwargs] = None,
                 stats_defaults: tp.Union[None, tp.Callable, tp.Kwargs] = None,
                 subplots: tp.Optional[tp.Kwargs] = None,
                 plots_defaults: tp.Union[None, tp.Callable, tp.Kwargs] = None) -> None:
        """A factory for creating new indicators.

        Initialize `IndicatorFactory` to create a skeleton and then use a class method
        such as `IndicatorFactory.from_custom_func` to bind a calculation function to the skeleton.

        Args:
            class_name (str): Name for the created indicator class.
            class_docstring (str): Docstring for the created indicator class.
            module_name (str): Specify the module the class originates from.
            short_name (str): A short name of the indicator.

                Defaults to lower-case `class_name`.
            prepend_name (bool): Whether to prepend `short_name` to each parameter level.
            input_names (list of str): A list of names of input arrays.
            param_names (list of str): A list of names of parameters.
            in_output_names (list of str): A list of names of in-place output arrays.

                An in-place output is an output that is not returned but modified in-place.
                Some advantages of such outputs include:

                1) they don't need to be returned,
                2) they can be passed between functions as easily as inputs,
                3) they can be provided with already allocated data to safe memory,
                4) if data or default value are not provided, they are created empty to not occupy memory.
            output_names (list of str): A list of names of output arrays.
            output_flags (dict): A dictionary of in-place and regular output flags.
            custom_output_props (dict): A dictionary with user-defined functions that will be
                bound to the indicator class and wrapped with `@cached_property`.
            attr_settings (dict): A dictionary of settings by attribute name.

                Attributes can be `input_names`, `in_output_names`, `output_names` and `custom_output_props`.

                Following keys are accepted:

                * `dtype`: Data type used to determine which methods to generate around this attribute.
                    Set to None to disable. Default is `np.float64`. Can be set to instance of
                    `collections.namedtuple` acting as enumerated type, or any other mapping;
                    It will then create a property with suffix `readable` that contains data in a string format.
            metrics (dict): Metrics supported by `vectorbt.generic.stats_builder.StatsBuilderMixin.stats`.

                If dict, will be converted to `vectorbt.utils.config.Config`.
            stats_defaults (callable or dict): Defaults for `vectorbt.generic.stats_builder.StatsBuilderMixin.stats`.

                If dict, will be converted into a property.
            subplots (dict): Subplots supported by `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots`.

                If dict, will be converted to `vectorbt.utils.config.Config`.
            plots_defaults (callable or dict): Defaults for `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots`.

                If dict, will be converted into a property.

        !!! note
            The `__init__` method is not used for running the indicator, for this use `run`.
            The reason for this is indexing, which requires a clean `__init__` method for creating 
            a new indicator object with newly indexed attributes.
        """
        # Check and save parameters
        self.class_name = class_name
        checks.assert_instance_of(class_name, str)

        self.class_docstring = class_docstring
        checks.assert_instance_of(class_docstring, str)

        self.module_name = module_name
        if module_name is not None:
            checks.assert_instance_of(module_name, str)

        if short_name is None:
            if class_name == 'Indicator':
                short_name = 'custom'
            else:
                short_name = class_name.lower()
        self.short_name = short_name
        checks.assert_instance_of(short_name, str)

        self.prepend_name = prepend_name
        checks.assert_instance_of(prepend_name, bool)

        if input_names is None:
            input_names = []
        else:
            checks.assert_sequence(input_names)
            input_names = list(input_names)
        self.input_names = input_names

        if param_names is None:
            param_names = []
        else:
            checks.assert_sequence(param_names)
            param_names = list(param_names)
        self.param_names = param_names

        if in_output_names is None:
            in_output_names = []
        else:
            checks.assert_sequence(in_output_names)
            in_output_names = list(in_output_names)
        self.in_output_names = in_output_names

        if output_names is None:
            output_names = []
        else:
            checks.assert_sequence(output_names)
            output_names = list(output_names)
        self.output_names = output_names

        all_output_names = in_output_names + output_names
        if len(all_output_names) == 0:
            raise ValueError("Must have at least one in-place or regular output")

        if output_flags is None:
            output_flags = {}
        checks.assert_instance_of(output_flags, dict)
        if len(output_flags) > 0:
            checks.assert_dict_valid(output_flags, all_output_names)
        self.output_flags = output_flags

        if custom_output_props is None:
            custom_output_props = {}
        checks.assert_instance_of(custom_output_props, dict)
        self.custom_output_props = custom_output_props

        if attr_settings is None:
            attr_settings = {}
        checks.assert_instance_of(attr_settings, dict)
        all_attr_names = input_names + all_output_names + list(custom_output_props.keys())
        if len(attr_settings) > 0:
            checks.assert_dict_valid(attr_settings, all_attr_names)
        self.attr_settings = attr_settings

        # Set up class
        ParamIndexer = build_param_indexer(
            param_names + (['tuple'] if len(param_names) > 1 else []),
            module_name=module_name
        )
        Indicator = type(self.class_name, (IndicatorBase, ParamIndexer), {})
        Indicator.__doc__ = self.class_docstring
        if module_name is not None:
            Indicator.__module__ = self.module_name

        # Create read-only properties
        setattr(Indicator, "_input_names", tuple(input_names))
        setattr(Indicator, "_param_names", tuple(param_names))
        setattr(Indicator, "_in_output_names", tuple(in_output_names))
        setattr(Indicator, "_output_names", tuple(output_names))
        setattr(Indicator, "_output_flags", output_flags)

        for param_name in param_names:
            def param_list_prop(self, _param_name=param_name) -> tp.List[tp.Param]:
                return getattr(self, f'_{_param_name}_list')

            param_list_prop.__doc__ = f"List of `{param_name}` values."
            setattr(Indicator, f'{param_name}_list', property(param_list_prop))

        for input_name in input_names:
            def input_prop(self, _input_name: str = input_name) -> tp.SeriesFrame:
                """Input array."""
                old_input = reshape_fns.to_2d_array(getattr(self, '_' + _input_name))
                input_mapper = getattr(self, '_input_mapper')
                if input_mapper is None:
                    return self.wrapper.wrap(old_input)
                return self.wrapper.wrap(old_input[:, input_mapper])

            input_prop.__name__ = input_name
            setattr(Indicator, input_name, cached_property(input_prop))

        for output_name in all_output_names:
            def output_prop(self, _output_name: str = output_name) -> tp.SeriesFrame:
                return self.wrapper.wrap(getattr(self, '_' + _output_name))

            if output_name in in_output_names:
                output_prop.__doc__ = """In-place output array."""
            else:
                output_prop.__doc__ = """Output array."""

            output_prop.__name__ = output_name
            if output_name in output_flags:
                _output_flags = output_flags[output_name]
                if isinstance(_output_flags, (tuple, list)):
                    _output_flags = ', '.join(_output_flags)
                output_prop.__doc__ += "\n\n" + _output_flags
            setattr(Indicator, output_name, property(output_prop))

        # Add __init__ method
        def __init__(self,
                     wrapper: ArrayWrapper,
                     input_list: InputListT,
                     input_mapper: InputMapperT,
                     in_output_list: InOutputListT,
                     output_list: OutputListT,
                     param_list: ParamListT,
                     mapper_list: MapperListT,
                     short_name: str,
                     level_names: tp.Tuple[str, ...]) -> None:
            IndicatorBase.__init__(
                self,
                wrapper,
                input_list,
                input_mapper,
                in_output_list,
                output_list,
                param_list,
                mapper_list,
                short_name,
                level_names
            )
            if len(param_names) > 1:
                tuple_mapper = list(zip(*list(mapper_list)))
            else:
                tuple_mapper = None

            # Initialize indexers
            mapper_sr_list = []
            for i, m in enumerate(mapper_list):
                mapper_sr_list.append(pd.Series(m, index=wrapper.columns))
            if tuple_mapper is not None:
                mapper_sr_list.append(pd.Series(tuple_mapper, index=wrapper.columns))
            ParamIndexer.__init__(self, mapper_sr_list, level_names=[*level_names, level_names])

        setattr(Indicator, '__init__', __init__)

        # Add user-defined outputs
        for prop_name, prop in custom_output_props.items():
            if prop.__doc__ is None:
                prop.__doc__ = f"""Custom property."""
            prop.__name__ = prop_name
            prop = cached_property(prop)
            setattr(Indicator, prop_name, prop)

        # Add comparison & combination methods for all inputs, outputs, and user-defined properties
        def assign_combine_method(func_name: str,
                                  combine_func: tp.Callable,
                                  def_kwargs: tp.Kwargs,
                                  attr_name: str,
                                  docstring: str) -> None:
            def combine_method(self: IndicatorBaseT,
                               other: tp.MaybeTupleList[tp.Union[IndicatorBaseT, tp.ArrayLike, BaseAccessor]],
                               level_name: tp.Optional[str] = None,
                               allow_multiple: bool = True,
                               _prepend_name: bool = prepend_name,
                               **kwargs) -> tp.SeriesFrame:
                if allow_multiple and isinstance(other, (tuple, list)):
                    other = list(other)
                    for i in range(len(other)):
                        if isinstance(other[i], IndicatorBase):
                            other[i] = getattr(other[i], attr_name)
                else:
                    if isinstance(other, IndicatorBase):
                        other = getattr(other, attr_name)
                if level_name is None:
                    if _prepend_name:
                        if attr_name == self.short_name:
                            level_name = f'{self.short_name}_{func_name}'
                        else:
                            level_name = f'{self.short_name}_{attr_name}_{func_name}'
                    else:
                        level_name = f'{attr_name}_{func_name}'
                out = combine_objs(
                    getattr(self, attr_name),
                    other,
                    combine_func=combine_func,
                    level_name=level_name,
                    allow_multiple=allow_multiple,
                    **merge_dicts(def_kwargs, kwargs)
                )
                return out

            combine_method.__qualname__ = f'{Indicator.__name__}.{attr_name}_{func_name}'
            combine_method.__doc__ = docstring
            setattr(Indicator, f'{attr_name}_{func_name}', combine_method)

        for attr_name in all_attr_names:
            _attr_settings = attr_settings.get(attr_name, {})
            checks.assert_dict_valid(_attr_settings, ['dtype'])
            dtype = _attr_settings.get('dtype', np.float64)

            if checks.is_mapping_like(dtype):
                def attr_readable(self,
                                  _attr_name: str = attr_name,
                                  _mapping: tp.MappingLike = dtype) -> tp.SeriesFrame:
                    return getattr(self, _attr_name).vbt(mapping=_mapping).apply_mapping()

                attr_readable.__qualname__ = f'{Indicator.__name__}.{attr_name}_readable'
                attr_readable.__doc__ = inspect.cleandoc(
                    """`{attr_name}` in readable format based on the following mapping: 
                                
                    ```json
                    {dtype}
                    ```"""
                ).format(
                    attr_name=attr_name,
                    dtype=to_doc(to_mapping(dtype))
                )
                setattr(Indicator, f'{attr_name}_readable', property(attr_readable))

                def attr_stats(self, *args,
                               _attr_name: str = attr_name,
                               _mapping: tp.MappingLike = dtype,
                               **kwargs) -> tp.SeriesFrame:
                    return getattr(self, _attr_name).vbt(mapping=_mapping).stats(*args, **kwargs)

                attr_stats.__qualname__ = f'{Indicator.__name__}.{attr_name}_stats'
                attr_stats.__doc__ = inspect.cleandoc(
                    """Stats of `{attr_name}` based on the following mapping: 

                    ```json
                    {dtype}
                    ```"""
                ).format(
                    attr_name=attr_name,
                    dtype=to_doc(to_mapping(dtype))
                )
                setattr(Indicator, f'{attr_name}_stats', attr_stats)

            elif np.issubdtype(dtype, np.number):
                func_info = [
                    ('above', np.greater, dict()),
                    ('below', np.less, dict()),
                    ('equal', np.equal, dict()),
                    ('crossed_above', lambda x, y, wait=0: generic_nb.crossed_above_nb(x, y, wait), dict(to_2d=True)),
                    ('crossed_below', lambda x, y, wait=0: generic_nb.crossed_above_nb(y, x, wait), dict(to_2d=True))
                ]
                for func_name, np_func, def_kwargs in func_info:
                    method_docstring = f"""Return True for each element where `{attr_name}` is {func_name} `other`. 
                
                    See `vectorbt.indicators.factory.combine_objs`."""
                    assign_combine_method(func_name, np_func, def_kwargs, attr_name, method_docstring)

                def attr_stats(self, *args, _attr_name: str = attr_name, **kwargs) -> tp.SeriesFrame:
                    return getattr(self, _attr_name).vbt.stats(*args, **kwargs)

                attr_stats.__qualname__ = f'{Indicator.__name__}.{attr_name}_stats'
                attr_stats.__doc__ = f"""Stats of `{attr_name}` as generic."""
                setattr(Indicator, f'{attr_name}_stats', attr_stats)

            elif np.issubdtype(dtype, np.bool_):
                func_info = [
                    ('and', np.logical_and, dict()),
                    ('or', np.logical_or, dict()),
                    ('xor', np.logical_xor, dict())
                ]
                for func_name, np_func, def_kwargs in func_info:
                    method_docstring = f"""Return `{attr_name} {func_name.upper()} other`. 

                    See `vectorbt.indicators.factory.combine_objs`."""
                    assign_combine_method(func_name, np_func, def_kwargs, attr_name, method_docstring)

                def attr_stats(self, *args, _attr_name: str = attr_name, **kwargs) -> tp.SeriesFrame:
                    return getattr(self, _attr_name).vbt.signals.stats(*args, **kwargs)

                attr_stats.__qualname__ = f'{Indicator.__name__}.{attr_name}_stats'
                attr_stats.__doc__ = f"""Stats of `{attr_name}` as signals."""
                setattr(Indicator, f'{attr_name}_stats', attr_stats)

        # Prepare stats
        if metrics is not None:
            if not isinstance(metrics, Config):
                metrics = Config(metrics, copy_kwargs=dict(copy_mode='deep'))
            setattr(Indicator, "_metrics", metrics.copy())

        if stats_defaults is not None:
            if isinstance(stats_defaults, dict):
                def stats_defaults_prop(self, _stats_defaults: tp.Kwargs = stats_defaults) -> tp.Kwargs:
                    return _stats_defaults
            else:
                def stats_defaults_prop(self, _stats_defaults: tp.Kwargs = stats_defaults) -> tp.Kwargs:
                    return stats_defaults(self)
            stats_defaults_prop.__name__ = "stats_defaults"
            setattr(Indicator, "stats_defaults", property(stats_defaults_prop))

        # Prepare plots
        if subplots is not None:
            if not isinstance(subplots, Config):
                subplots = Config(subplots, copy_kwargs=dict(copy_mode='deep'))
            setattr(Indicator, "_subplots", subplots.copy())

        if plots_defaults is not None:
            if isinstance(plots_defaults, dict):
                def plots_defaults_prop(self, _plots_defaults: tp.Kwargs = plots_defaults) -> tp.Kwargs:
                    return _plots_defaults
            else:
                def plots_defaults_prop(self, _plots_defaults: tp.Kwargs = plots_defaults) -> tp.Kwargs:
                    return plots_defaults(self)
            plots_defaults_prop.__name__ = "plots_defaults"
            setattr(Indicator, "plots_defaults", property(plots_defaults_prop))

        # Save indicator
        self.Indicator = Indicator

    def from_custom_func(self,
                         custom_func: tp.Callable,
                         require_input_shape: bool = False,
                         param_settings: tp.KwargsLike = None,
                         in_output_settings: tp.KwargsLike = None,
                         hide_params: tp.Optional[tp.Sequence[str]] = None,
                         hide_default: bool = True,
                         var_args: bool = False,
                         keyword_only_args: bool = False,
                         **pipeline_kwargs) -> tp.Type[IndicatorBase]:
        """Build indicator class around a custom calculation function.

        In contrast to `IndicatorFactory.from_apply_func`, this method offers full flexibility.
        It's up to we to handle caching and concatenate columns for each parameter (for example,
        by using `vectorbt.base.combine_fns.apply_and_concat_one`). Also, you should ensure that
        each output array has an appropriate number of columns, which is the number of columns in
        input arrays multiplied by the number of parameter combinations.

        Args:
            custom_func (callable): A function that takes broadcast arrays corresponding
                to `input_names`, broadcast in-place output arrays corresponding to `in_output_names`,
                broadcast parameter arrays corresponding to `param_names`, and other arguments and
                keyword arguments, and returns outputs corresponding to `output_names` and other objects
                that are then returned with the indicator instance.

                Can be Numba-compiled.

                !!! note
                    Shape of each output should be the same and match the shape of each input stacked
                    n times (= the number of parameter values) along the column axis.
            require_input_shape (bool): Whether to input shape is required.
            param_settings (dict): A dictionary of parameter settings keyed by name.
                See `run_pipeline` for keys.

                Can be overwritten by any run method.
            in_output_settings (dict): A dictionary of in-place output settings keyed by name.
                See `run_pipeline` for keys.

                Can be overwritten by any run method.
            hide_params (list of str): Parameter names to hide column levels for.

                Can be overwritten by any run method.
            hide_default (bool): Whether to hide column levels of parameters with default value.

                Can be overwritten by any run method.
            var_args (bool): Whether run methods should accept variable arguments (`*args`).

                Set to True if `custom_func` accepts positional arguments that are not listed in the config.
            keyword_only_args (bool): Whether run methods should accept keyword-only arguments (`*`).

                Set to True to force the user to use keyword arguments (e.g., to avoid misplacing arguments).
            **pipeline_kwargs: Keyword arguments passed to `run_pipeline`.

                Can be overwritten by any run method.

                Can contain default values for `param_names` and `in_output_names`,
                but also custom positional and keyword arguments passed to the `custom_func`.

        Returns:
            `Indicator`, and optionally other objects that are returned by `custom_func`
            and exceed `output_names`.

        Usage:
            * The following example produces the same indicator as the `IndicatorFactory.from_apply_func` example.

            ```pycon
            >>> @njit
            >>> def apply_func_nb(i, ts1, ts2, p1, p2, arg1, arg2):
            ...     return ts1 * p1[i] + arg1, ts2 * p2[i] + arg2

            >>> @njit
            ... def custom_func(ts1, ts2, p1, p2, arg1, arg2):
            ...     return vbt.base.combine_fns.apply_and_concat_multiple_nb(
            ...         len(p1), apply_func_nb, ts1, ts2, p1, p2, arg1, arg2)

            >>> MyInd = vbt.IndicatorFactory(
            ...     input_names=['ts1', 'ts2'],
            ...     param_names=['p1', 'p2'],
            ...     output_names=['o1', 'o2']
            ... ).from_custom_func(custom_func, var_args=True, arg2=200)

            >>> myInd = MyInd.run(price, price * 2, [1, 2], [3, 4], 100)
            >>> myInd.o1
            custom_p1              1             2
            custom_p2              3             4
                            a      b      a      b
            2020-01-01  101.0  105.0  102.0  110.0
            2020-01-02  102.0  104.0  104.0  108.0
            2020-01-03  103.0  103.0  106.0  106.0
            2020-01-04  104.0  102.0  108.0  104.0
            2020-01-05  105.0  101.0  110.0  102.0
            >>> myInd.o2
            custom_p1              1             2
            custom_p2              3             4
                            a      b      a      b
            2020-01-01  206.0  230.0  208.0  240.0
            2020-01-02  212.0  224.0  216.0  232.0
            2020-01-03  218.0  218.0  224.0  224.0
            2020-01-04  224.0  212.0  232.0  216.0
            2020-01-05  230.0  206.0  240.0  208.0
            ```

            The difference between `apply_func_nb` here and in `IndicatorFactory.from_apply_func` is that
            here it takes the index of the current parameter combination that can be used for parameter selection.
            You can also remove the entire `apply_func_nb` and define your logic in `custom_func`
            (which shouldn't necessarily be Numba-compiled):

            ```pycon
            >>> @njit
            ... def custom_func(ts1, ts2, p1, p2, arg1, arg2):
            ...     input_shape = ts1.shape
            ...     n_params = len(p1)
            ...     out1 = np.empty((input_shape[0], input_shape[1] * n_params), dtype=np.float64)
            ...     out2 = np.empty((input_shape[0], input_shape[1] * n_params), dtype=np.float64)
            ...     for k in range(n_params):
            ...         for col in range(input_shape[1]):
            ...             for i in range(input_shape[0]):
            ...                 out1[i, input_shape[1] * k + col] = ts1[i, col] * p1[k] + arg1
            ...                 out2[i, input_shape[1] * k + col] = ts2[i, col] * p2[k] + arg2
            ...     return out1, out2
            ```
        """
        Indicator = self.Indicator

        short_name = self.short_name
        prepend_name = self.prepend_name
        input_names = self.input_names
        param_names = self.param_names
        in_output_names = self.in_output_names
        output_names = self.output_names

        all_input_names = input_names + param_names + in_output_names

        setattr(Indicator, 'custom_func', custom_func)

        def _merge_settings(old_settings: tp.KwargsLike,
                            new_settings: tp.KwargsLike,
                            allowed_keys: tp.Optional[tp.Sequence[tp.MaybeSequence[str]]] = None) -> tp.Kwargs:
            new_settings = merge_dicts(old_settings, new_settings)
            if len(new_settings) > 0 and allowed_keys is not None:
                checks.assert_dict_valid(new_settings, allowed_keys)
            return new_settings

        def _resolve_refs(input_list: tp.Sequence[tp.ArrayLike],
                          param_list: tp.Sequence[tp.Param],
                          in_output_list: tp.Sequence[tp.ArrayLike]) \
                -> tp.Tuple[tp.List[tp.ArrayLike], tp.List[tp.Param], tp.List[tp.ArrayLike]]:
            # You can reference anything between inputs, parameters, and in-place outputs
            # even parameter to input (thanks to broadcasting)
            all_inputs = list(input_list) + list(param_list) + list(in_output_list)
            for i in range(len(all_inputs)):
                input = all_inputs[i]
                is_default = False
                if isinstance(input, Default):
                    input = input.value
                    is_default = True
                if isinstance(input, str):
                    if input in all_input_names:
                        new_input = all_inputs[all_input_names.index(input)]
                        if is_default:
                            new_input = Default(new_input)
                        all_inputs[i] = new_input
            input_list = all_inputs[:len(input_list)]
            all_inputs = all_inputs[len(input_list):]
            param_list = all_inputs[:len(param_list)]
            in_output_list = all_inputs[len(param_list):]
            return input_list, param_list, in_output_list

        def _extract_inputs(args: tp.Sequence) \
                -> tp.Tuple[tp.List[tp.ArrayLike], tp.List[tp.Param], tp.List[tp.ArrayLike], tuple]:
            input_list = args[:len(input_names)]
            checks.assert_len_equal(input_list, input_names)
            args = args[len(input_names):]

            param_list = args[:len(param_names)]
            checks.assert_len_equal(param_list, param_names)
            args = args[len(param_names):]

            in_output_list = args[:len(in_output_names)]
            checks.assert_len_equal(in_output_list, in_output_names)
            args = args[len(in_output_names):]
            if not var_args and len(args) > 0:
                raise TypeError("Variable length arguments are not supported by this function "
                                "(var_args is set to False)")

            input_list, param_list, in_output_list = _resolve_refs(input_list, param_list, in_output_list)
            return input_list, param_list, in_output_list, args

        for k, v in pipeline_kwargs.items():
            if k in param_names and not isinstance(v, Default):
                pipeline_kwargs[k] = Default(v)  # track default params
        pipeline_kwargs = merge_dicts({k: None for k in in_output_names}, pipeline_kwargs)

        # Display default parameters and in-place outputs in the signature
        default_kwargs = {}
        for k in list(pipeline_kwargs.keys()):
            if k in input_names or k in param_names or k in in_output_names:
                default_kwargs[k] = pipeline_kwargs.pop(k)

        if var_args and keyword_only_args:
            raise ValueError("var_args and keyword_only_args cannot be used together")

        # Add private run method
        def_run_kwargs = dict(
            short_name=short_name,
            hide_params=hide_params,
            hide_default=hide_default,
            **default_kwargs
        )

        def _run(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunOutputT:
            _short_name = kwargs.pop('short_name', def_run_kwargs['short_name'])
            _hide_params = kwargs.pop('hide_params', def_run_kwargs['hide_params'])
            _hide_default = kwargs.pop('hide_default', def_run_kwargs['hide_default'])
            _param_settings = _merge_settings(
                param_settings,
                kwargs.pop('param_settings', {}),
                [param_names]
            )
            _in_output_settings = _merge_settings(
                in_output_settings,
                kwargs.pop('in_output_settings', {}),
                [in_output_names]
            )

            if _hide_params is None:
                _hide_params = []

            args = list(args)

            # Extract inputs
            input_list, param_list, in_output_list, args = _extract_inputs(args)

            # Prepare column levels
            level_names = []
            hide_levels = []
            for i, pname in enumerate(param_names):
                level_name = _short_name + '_' + pname if prepend_name else pname
                level_names.append(level_name)
                if pname in _hide_params or (_hide_default and isinstance(param_list[i], Default)):
                    hide_levels.append(i)
            param_list = [params.value if isinstance(params, Default) else params for params in param_list]

            # Run the pipeline
            results = run_pipeline(
                len(output_names),  # number of returned outputs
                custom_func,
                *args,
                require_input_shape=require_input_shape,
                input_list=input_list,
                in_output_list=in_output_list,
                param_list=param_list,
                level_names=level_names,
                hide_levels=hide_levels,
                param_settings=[_param_settings.get(n, {}) for n in param_names],
                in_output_settings=[_in_output_settings.get(n, {}) for n in in_output_names],
                **merge_dicts(pipeline_kwargs, kwargs)
            )

            # Return the raw result if any of the flags are set
            if kwargs.get('return_raw', False) or kwargs.get('return_cache', False):
                return results

            # Unpack the result
            wrapper, \
            new_input_list, \
            input_mapper, \
            in_output_list, \
            output_list, \
            new_param_list, \
            mapper_list, \
            other_list = results

            # Create a new instance
            obj = cls(
                wrapper,
                new_input_list,
                input_mapper,
                in_output_list,
                output_list,
                new_param_list,
                mapper_list,
                short_name,
                tuple(level_names)
            )
            if len(other_list) > 0:
                return (obj, *tuple(other_list))
            return obj

        setattr(Indicator, '_run', classmethod(_run))

        # Add public run method
        # Create function dynamically to provide user with a proper signature
        def compile_run_function(func_name: str, docstring: str, _default_kwargs: tp.KwargsLike = None) -> tp.Callable:
            pos_names = []
            main_kw_names = []
            other_kw_names = []
            if _default_kwargs is None:
                _default_kwargs = {}
            for k in input_names + param_names:
                if k in _default_kwargs:
                    main_kw_names.append(k)
                else:
                    pos_names.append(k)
            main_kw_names.extend(in_output_names)  # in_output_names are keyword-only
            for k, v in _default_kwargs.items():
                if k not in pos_names and k not in main_kw_names:
                    other_kw_names.append(k)

            _0 = func_name
            _1 = '*, ' if keyword_only_args else ''
            _2 = []
            if require_input_shape:
                _2.append('input_shape')
            _2.extend(pos_names)
            _2 = ', '.join(_2) + ', ' if len(_2) > 0 else ''
            _3 = '*args, ' if var_args else ''
            _4 = ['{}={}'.format(k, k) for k in main_kw_names + other_kw_names]
            _4 = ', '.join(_4) + ', ' if len(_4) > 0 else ''
            _5 = docstring
            _6 = all_input_names
            _6 = ', '.join(_6) + ', ' if len(_6) > 0 else ''
            _7 = []
            if require_input_shape:
                _7.append('input_shape')
            _7.extend(other_kw_names)
            _7 = ['{}={}'.format(k, k) for k in _7]
            _7 = ', '.join(_7) + ', ' if len(_7) > 0 else ''
            func_str = "@classmethod\n" \
                       "def {0}(cls, {1}{2}{3}{4}**kwargs):\n" \
                       "    \"\"\"{5}\"\"\"\n" \
                       "    return cls._{0}({6}{3}{7}**kwargs)".format(
                _0, _1, _2, _3, _4, _5, _6, _7
            )
            scope = {**dict(Default=Default), **_default_kwargs}
            filename = inspect.getfile(lambda: None)
            code = compile(func_str, filename, 'single')
            exec(code, scope)
            return scope[func_name]

        _0 = self.class_name
        _1 = ''
        if len(self.input_names) > 0:
            _1 += '\n* Inputs: ' + ', '.join(map(lambda x: f'`{x}`', self.input_names))
        if len(self.in_output_names) > 0:
            _1 += '\n* In-place outputs: ' + ', '.join(map(lambda x: f'`{x}`', self.in_output_names))
        if len(self.param_names) > 0:
            _1 += '\n* Parameters: ' + ', '.join(map(lambda x: f'`{x}`', self.param_names))
        if len(self.output_names) > 0:
            _1 += '\n* Outputs: ' + ', '.join(map(lambda x: f'`{x}`', self.output_names))
        run_docstring = """Run `{0}` indicator.
{1}

Pass a list of parameter names as `hide_params` to hide their column levels.
Set `hide_default` to False to show the column levels of the parameters with a default value.

Other keyword arguments are passed to `vectorbt.indicators.factory.run_pipeline`.""".format(_0, _1)
        run = compile_run_function('run', run_docstring, def_run_kwargs)
        setattr(Indicator, 'run', run)

        if len(param_names) > 0:
            # Add private run_combs method
            def_run_combs_kwargs = dict(
                r=2,
                param_product=False,
                comb_func=itertools.combinations,
                run_unique=True,
                short_names=None,
                hide_params=hide_params,
                hide_default=hide_default,
                **default_kwargs
            )

            def _run_combs(cls: tp.Type[IndicatorBaseT], *args, **kwargs) -> RunCombsOutputT:
                _r = kwargs.pop('r', def_run_combs_kwargs['r'])
                _param_product = kwargs.pop('param_product', def_run_combs_kwargs['param_product'])
                _comb_func = kwargs.pop('comb_func', def_run_combs_kwargs['comb_func'])
                _run_unique = kwargs.pop('run_unique', def_run_combs_kwargs['run_unique'])
                _short_names = kwargs.pop('short_names', def_run_combs_kwargs['short_names'])
                _hide_params = kwargs.pop('hide_params', def_run_kwargs['hide_params'])
                _hide_default = kwargs.pop('hide_default', def_run_kwargs['hide_default'])
                _param_settings = _merge_settings(
                    param_settings,
                    kwargs.get('param_settings', {}),  # get, not pop
                    [param_names]
                )

                if _hide_params is None:
                    _hide_params = []
                if _short_names is None:
                    _short_names = [f'{short_name}_{str(i + 1)}' for i in range(_r)]

                args = list(args)

                # Extract inputs
                input_list, param_list, in_output_list, args = _extract_inputs(args)

                # Hide params
                for i, pname in enumerate(param_names):
                    if _hide_default and isinstance(param_list[i], Default):
                        if pname not in _hide_params:
                            _hide_params.append(pname)
                        param_list[i] = param_list[i].value
                checks.assert_len_equal(param_list, param_names)

                # Prepare params
                param_settings_list = [_param_settings.get(n, {}) for n in param_names]
                for i in range(len(param_list)):
                    is_tuple = param_settings_list[i].get('is_tuple', False)
                    is_array_like = param_settings_list[i].get('is_array_like', False)
                    param_list[i] = params_to_list(param_list[i], is_tuple, is_array_like)
                if _param_product:
                    param_list = create_param_product(param_list)
                else:
                    param_list = broadcast_params(param_list)
                if not isinstance(param_list, (tuple, list)):
                    param_list = [param_list]

                # Speed up by pre-calculating raw outputs
                if _run_unique:
                    raw_results = cls._run(
                        *input_list,
                        *param_list,
                        *in_output_list,
                        *args,
                        return_raw=True,
                        run_unique=False,
                        **kwargs
                    )
                    kwargs['use_raw'] = raw_results  # use them next time

                # Generate indicator instances
                instances = []
                if _comb_func == itertools.product:
                    param_lists = zip(*_comb_func(zip(*param_list), repeat=_r))
                else:
                    param_lists = zip(*_comb_func(zip(*param_list), _r))
                for i, param_list in enumerate(param_lists):
                    instances.append(cls._run(
                        *input_list,
                        *zip(*param_list),
                        *in_output_list,
                        *args,
                        short_name=_short_names[i],
                        hide_params=_hide_params,
                        hide_default=_hide_default,
                        run_unique=False,
                        **kwargs
                    ))
                return tuple(instances)

            setattr(Indicator, '_run_combs', classmethod(_run_combs))

            # Add public run_combs method
            _0 = self.class_name
            _1 = ''
            if len(self.input_names) > 0:
                _1 += '\n* Inputs: ' + ', '.join(map(lambda x: f'`{x}`', self.input_names))
            if len(self.in_output_names) > 0:
                _1 += '\n* In-place outputs: ' + ', '.join(map(lambda x: f'`{x}`', self.in_output_names))
            if len(self.param_names) > 0:
                _1 += '\n* Parameters: ' + ', '.join(map(lambda x: f'`{x}`', self.param_names))
            if len(self.output_names) > 0:
                _1 += '\n* Outputs: ' + ', '.join(map(lambda x: f'`{x}`', self.output_names))
            run_combs_docstring = """Create a combination of multiple `{0}` indicators using function `comb_func`.
{1}

`comb_func` must accept an iterable of parameter tuples and `r`. 
Also accepts all combinatoric iterators from itertools such as `itertools.combinations`.
Pass `r` to specify how many indicators to run. 
Pass `short_names` to specify the short name for each indicator. 
Set `run_unique` to True to first compute raw outputs for all parameters, 
and then use them to build each indicator (faster).

Other keyword arguments are passed to `{0}.run`.""".format(_0, _1)
            run_combs = compile_run_function('run_combs', run_combs_docstring, def_run_combs_kwargs)
            setattr(Indicator, 'run_combs', run_combs)

        return Indicator

    def from_apply_func(self,
                        apply_func: tp.Callable,
                        cache_func: tp.Optional[tp.Callable] = None,
                        pass_packed: bool = False,
                        kwargs_to_args: tp.Optional[tp.Sequence[str]] = None,
                        numba_loop: bool = False,
                        **kwargs) -> tp.Type[IndicatorBase]:
        """Build indicator class around a custom apply function.

        In contrast to `IndicatorFactory.from_custom_func`, this method handles a lot of things for you,
        such as caching, parameter selection, and concatenation. Your part is writing a function `apply_func`
        that accepts a selection of parameters (single values as opposed to multiple values in
        `IndicatorFactory.from_custom_func`) and does the calculation. It then automatically concatenates
        the resulting arrays into a single array per output.

        While this approach is simpler, it's also less flexible, since we can only work with
        one parameter selection at a time and can't view all parameters. The UDF `apply_func` also can't
        take keyword arguments, nor it can return anything other than outputs listed in `output_names`.

        !!! note
            If `apply_func` is a Numba-compiled function:

            * All inputs are automatically converted to NumPy arrays
            * Each argument in `*args` must be of a Numba-compatible type
            * You cannot pass keyword arguments
            * Your outputs must be arrays of the same shape, data type and data order

        Args:
            apply_func (callable): A function that takes inputs, selection of parameters, and
                other arguments, and does calculations to produce outputs.

                Arguments are passed to `apply_func` in the following order:

                * `input_shape` if `pass_input_shape` is set to True and `input_shape` not in `kwargs_to_args`
                * `col` if `per_column` and `pass_col` are set to True and `col` not in `kwargs_to_args`
                * broadcast time-series arrays corresponding to `input_names`
                * broadcast in-place output arrays corresponding to `in_output_names`
                * single parameter selection corresponding to `param_names`
                * variable arguments if `var_args` is set to True
                * arguments listed in `kwargs_to_args`
                * `flex_2d` if `pass_flex_2d` is set to True and `flex_2d` not in `kwargs_to_args`
                * keyword arguments if `apply_func` is not Numba-compiled

                Can be Numba-compiled.

                !!! note
                    Shape of each output should be the same and match the shape of each input.
            cache_func (callable): A caching function to preprocess data beforehand.

                Takes the same arguments as `apply_func`. Should return a single object or a tuple of objects.
                All returned objects will be passed unpacked as last arguments to `apply_func`.

                Can be Numba-compiled.
            pass_packed (bool): Whether to pass packed tuples for inputs, in-place outputs, and parameters.
            kwargs_to_args (list of str): Keyword arguments from `kwargs` dict to pass as
                positional arguments to the apply function.

                Should be used together with `numba_loop` set to True since Numba doesn't support
                variable keyword arguments.

                Defaults to []. Order matters.
            numba_loop (bool): Whether to loop using Numba.

                Set to True when iterating large number of times over small input,
                but note that Numba doesn't support variable keyword arguments.
            **kwargs: Keyword arguments passed to `IndicatorFactory.from_custom_func`.

        Returns:
            Indicator

        Additionally, each run method now supports `use_ray` argument, which indicates
        whether to use Ray to execute `apply_func` in parallel. Only works with `numba_loop` set to False.
        See `vectorbt.base.combine_fns.ray_apply` for related keyword arguments.

        Usage:
            * The following example produces the same indicator as the `IndicatorFactory.from_custom_func` example.

            ```pycon
            >>> @njit
            ... def apply_func_nb(ts1, ts2, p1, p2, arg1, arg2):
            ...     return ts1 * p1 + arg1, ts2 * p2 + arg2

            >>> MyInd = vbt.IndicatorFactory(
            ...     input_names=['ts1', 'ts2'],
            ...     param_names=['p1', 'p2'],
            ...     output_names=['o1', 'o2']
            ... ).from_apply_func(
            ...     apply_func_nb, var_args=True,
            ...     kwargs_to_args=['arg2'], arg2=200)

            >>> myInd = MyInd.run(price, price * 2, [1, 2], [3, 4], 100)
            >>> myInd.o1
            custom_p1              1             2
            custom_p2              3             4
                            a      b      a      b
            2020-01-01  101.0  105.0  102.0  110.0
            2020-01-02  102.0  104.0  104.0  108.0
            2020-01-03  103.0  103.0  106.0  106.0
            2020-01-04  104.0  102.0  108.0  104.0
            2020-01-05  105.0  101.0  110.0  102.0
            >>> myInd.o2
            custom_p1              1             2
            custom_p2              3             4
                            a      b      a      b
            2020-01-01  206.0  230.0  208.0  240.0
            2020-01-02  212.0  224.0  216.0  232.0
            2020-01-03  218.0  218.0  224.0  224.0
            2020-01-04  224.0  212.0  232.0  216.0
            2020-01-05  230.0  206.0  240.0  208.0
            ```
        """
        Indicator = self.Indicator

        setattr(Indicator, 'apply_func', apply_func)

        if kwargs_to_args is None:
            kwargs_to_args = []

        module_name = self.module_name
        output_names = self.output_names
        in_output_names = self.in_output_names
        param_names = self.param_names

        num_ret_outputs = len(output_names)

        # Build a function that selects a parameter tuple
        # Do it here to avoid compilation with Numba every time custom_func is run
        _0 = "i"
        _0 += ", args_before"
        _0 += ", input_tuple"
        if len(in_output_names) > 0:
            _0 += ", in_output_tuples"
        if len(param_names) > 0:
            _0 += ", param_tuples"
        _0 += ", *args"
        if not numba_loop:
            _0 += ", **_kwargs"
        _1 = "*args_before"
        if pass_packed:
            _1 += ", input_tuple"
            if len(in_output_names) > 0:
                _1 += ", in_output_tuples[i]"
            else:
                _1 += ", ()"
            if len(param_names) > 0:
                _1 += ", param_tuples[i]"
            else:
                _1 += ", ()"
        else:
            _1 += ", *input_tuple"
            if len(in_output_names) > 0:
                _1 += ", *in_output_tuples[i]"
            if len(param_names) > 0:
                _1 += ", *param_tuples[i]"
        _1 += ", *args"
        if not numba_loop:
            _1 += ", **_kwargs"
        func_str = "def select_params_func({0}):\n   return apply_func({1})".format(_0, _1)
        scope = {'apply_func': apply_func}
        filename = inspect.getfile(lambda: None)
        code = compile(func_str, filename, 'single')
        exec(code, scope)
        select_params_func = scope['select_params_func']
        if module_name is not None:
            select_params_func.__module__ = module_name
        if numba_loop:
            select_params_func = njit(select_params_func)

        def custom_func(input_list: tp.List[tp.AnyArray],
                        in_output_list: tp.List[tp.List[tp.AnyArray]],
                        param_list: tp.List[tp.List[tp.Param]],
                        *args,
                        input_shape: tp.Optional[tp.Shape] = None,
                        col: tp.Optional[int] = None,
                        flex_2d: tp.Optional[bool] = None,
                        return_cache: bool = False,
                        use_cache: tp.Optional[CacheOutputT] = None,
                        use_ray: bool = False,
                        **_kwargs) -> tp.Union[None, CacheOutputT, tp.Array2d, tp.List[tp.Array2d]]:
            """Custom function that forwards inputs and parameters to `apply_func`."""

            if use_ray:
                if len(in_output_names) > 0:
                    raise ValueError("Ray doesn't support in-place outputs")
            if numba_loop:
                if use_ray:
                    raise ValueError("Ray cannot be used within Numba")
                if num_ret_outputs > 1:
                    apply_and_concat_func = combine_fns.apply_and_concat_multiple_nb
                elif num_ret_outputs == 1:
                    apply_and_concat_func = combine_fns.apply_and_concat_one_nb
                else:
                    apply_and_concat_func = combine_fns.apply_and_concat_none_nb
            else:
                if num_ret_outputs > 1:
                    if use_ray:
                        apply_and_concat_func = combine_fns.apply_and_concat_multiple_ray
                    else:
                        apply_and_concat_func = combine_fns.apply_and_concat_multiple
                elif num_ret_outputs == 1:
                    if use_ray:
                        apply_and_concat_func = combine_fns.apply_and_concat_one_ray
                    else:
                        apply_and_concat_func = combine_fns.apply_and_concat_one
                else:
                    if use_ray:
                        raise ValueError("Ray requires regular outputs")
                    apply_and_concat_func = combine_fns.apply_and_concat_none

            n_params = len(param_list[0]) if len(param_list) > 0 else 1
            input_tuple = tuple(input_list)
            in_output_tuples = list(zip(*in_output_list))
            param_tuples = list(zip(*param_list))
            args_before = ()
            if input_shape is not None and 'input_shape' not in kwargs_to_args:
                args_before += (input_shape,)
            if col is not None and 'col' not in kwargs_to_args:
                args_before += (col,)

            # Pass some keyword arguments as positional (required by numba)
            more_args = ()
            for key in kwargs_to_args:
                value = _kwargs.pop(key)  # important: remove from kwargs
                more_args += (value,)
            if flex_2d is not None and 'flex_2d' not in kwargs_to_args:
                more_args += (flex_2d,)

            # Caching
            cache = use_cache
            if cache is None and cache_func is not None:
                _in_output_list = in_output_list
                _param_list = param_list
                if checks.is_numba_func(cache_func):
                    if len(in_output_list) > 0:
                        _in_output_list = [to_typed_list(in_outputs) for in_outputs in in_output_list]
                    if len(param_list) > 0:
                        _param_list = [to_typed_list(params) for params in param_list]
                cache = cache_func(
                    *args_before,
                    *input_tuple,
                    *_in_output_list,
                    *_param_list,
                    *args,
                    *more_args,
                    **_kwargs
                )
            if return_cache:
                return cache
            if cache is None:
                cache = ()
            if not isinstance(cache, tuple):
                cache = (cache,)

            if len(in_output_names) > 0:
                _in_output_tuples = in_output_tuples
                if numba_loop:
                    _in_output_tuples = to_typed_list(_in_output_tuples)
                _in_output_tuples = (_in_output_tuples,)
            else:
                _in_output_tuples = ()
            if len(param_names) > 0:
                _param_tuples = param_tuples
                if numba_loop:
                    _param_tuples = to_typed_list(_param_tuples)
                _param_tuples = (_param_tuples,)
            else:
                _param_tuples = ()

            return apply_and_concat_func(
                n_params,
                select_params_func,
                args_before,
                input_tuple,
                *_in_output_tuples,
                *_param_tuples,
                *args,
                *more_args,
                *cache,
                **_kwargs
            )

        return self.from_custom_func(custom_func, as_lists=True, **kwargs)

    @classmethod
    def get_talib_indicators(cls) -> tp.Set[str]:
        """Get all TA-Lib indicators."""
        import talib

        return set(talib.get_functions())

    @classmethod
    def from_talib(cls, func_name: str, init_kwargs: tp.KwargsLike = None, **kwargs) -> tp.Type[IndicatorBase]:
        """Build an indicator class around a TA-Lib function.

        Requires [TA-Lib](https://github.com/mrjbq7/ta-lib) installed.

        For input, parameter and output names, see [docs](https://github.com/mrjbq7/ta-lib/blob/master/docs/index.md).

        Args:
            func_name (str): Function name.
            init_kwargs (dict): Keyword arguments passed to `IndicatorFactory`.
            **kwargs: Keyword arguments passed to `IndicatorFactory.from_custom_func`.

        Returns:
            Indicator

        Usage:
            ```pycon
            >>> SMA = vbt.IndicatorFactory.from_talib('SMA')

            >>> sma = SMA.run(price, timeperiod=[2, 3])
            >>> sma.real
            sma_timeperiod         2         3
                              a    b    a    b
            2020-01-01      NaN  NaN  NaN  NaN
            2020-01-02      1.5  4.5  NaN  NaN
            2020-01-03      2.5  3.5  2.0  4.0
            2020-01-04      3.5  2.5  3.0  3.0
            2020-01-05      4.5  1.5  4.0  2.0
            ```

            * To get help on running the indicator, use the `help` command:

            ```pycon
            >>> help(SMA.run)
            Help on method run:

            run(close, timeperiod=30, short_name='sma', hide_params=None, hide_default=True, **kwargs) method of builtins.type instance
                Run `SMA` indicator.

                * Inputs: `close`
                * Parameters: `timeperiod`
                * Outputs: `real`

                Pass a list of parameter names as `hide_params` to hide their column levels.
                Set `hide_default` to False to show the column levels of the parameters with a default value.

                Other keyword arguments are passed to `vectorbt.indicators.factory.run_pipeline`.
            ```
        """
        import talib
        from talib import abstract

        func_name = func_name.upper()
        talib_func = getattr(talib, func_name)
        info = abstract.Function(func_name).info
        input_names = []
        for in_names in info['input_names'].values():
            if isinstance(in_names, (list, tuple)):
                input_names.extend(list(in_names))
            else:
                input_names.append(in_names)
        class_name = info['name']
        class_docstring = "{}, {}".format(info['display_name'], info['group'])
        param_names = list(info['parameters'].keys())
        output_names = info['output_names']
        output_flags = info['output_flags']

        def apply_func(input_list: tp.List[tp.AnyArray],
                       in_output_tuple: tp.Tuple[tp.AnyArray, ...],
                       param_tuple: tp.Tuple[tp.Param, ...],
                       **kwargs) -> tp.Union[tp.Array2d, tp.List[tp.Array2d]]:
            # TA-Lib functions can only process 1-dim arrays
            n_input_cols = input_list[0].shape[1]
            outputs = []
            for col in range(n_input_cols):
                output = talib_func(
                    *map(lambda x: x[:, col], input_list),
                    *param_tuple,
                    **kwargs
                )
                outputs.append(output)
            if isinstance(outputs[0], tuple):  # multiple outputs
                outputs = list(zip(*outputs))
                return list(map(np.column_stack, outputs))
            return np.column_stack(outputs)

        TALibIndicator = cls(
            **merge_dicts(
                dict(
                    class_name=class_name,
                    class_docstring=class_docstring,
                    input_names=input_names,
                    param_names=param_names,
                    output_names=output_names,
                    output_flags=output_flags
                ),
                init_kwargs
            )
        ).from_apply_func(
            apply_func,
            pass_packed=True,
            **info['parameters'],
            **kwargs
        )
        return TALibIndicator

    @classmethod
    def parse_pandas_ta_config(cls,
                               func: tp.Callable,
                               test_input_names: tp.Optional[tp.Sequence[str]] = None,
                               test_index_len: int = 100) -> tp.Kwargs:
        """Get the config of a pandas-ta indicator."""
        if test_input_names is None:
            test_input_names = {'open_', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'dividends', 'split'}

        input_names = []
        param_names = []
        defaults = {}
        output_names = []

        # Parse the function signature of the indicator to get input names
        sig = inspect.signature(func)
        for k, v in sig.parameters.items():
            if v.kind not in (v.VAR_POSITIONAL, v.VAR_KEYWORD):
                if v.annotation != inspect.Parameter.empty and v.annotation == pd.Series:
                    input_names.append(k)
                elif k in test_input_names:
                    input_names.append(k)
                elif v.default == inspect.Parameter.empty:
                    # Any positional argument is considered input
                    input_names.append(k)
                else:
                    param_names.append(k)
                    defaults[k] = v.default

        # To get output names, we need to run the indicator
        test_df = pd.DataFrame(
            {c: np.random.uniform(1, 10, size=(test_index_len,)) for c in input_names},
            index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(test_index_len)]
        )
        new_args = {c: test_df[c] for c in input_names}
        try:
            result = func(**new_args)
        except Exception as e:
            raise ValueError("Couldn't parse the indicator: " + str(e))

        # Concatenate Series/DataFrames if the result is a tuple
        if isinstance(result, tuple):
            results = []
            for i, r in enumerate(result):
                if not pd.Index.equals(r.index, test_df.index):
                    warnings.warn(f"Couldn't parse the output at index {i}: mismatching index", stacklevel=2)
                else:
                    results.append(r)
            if len(results) > 1:
                result = pd.concat(results, axis=1)
            elif len(results) == 1:
                result = results[0]
            else:
                raise ValueError("Couldn't parse the output")

        # Test if the produced array has the same index length
        if not pd.Index.equals(result.index, test_df.index):
            raise ValueError("Couldn't parse the output: mismatching index")

        # Standardize output names: remove numbers, remove hyphens, and bring to lower case
        output_cols = result.columns.tolist() if isinstance(result, pd.DataFrame) else [result.name]
        new_output_cols = []
        for i in range(len(output_cols)):
            name_parts = []
            for name_part in output_cols[i].split('_'):
                try:
                    float(name_part)
                    continue
                except:
                    name_parts.append(name_part.replace('-', '_').lower())
            output_col = '_'.join(name_parts)
            new_output_cols.append(output_col)

        # Add numbers to duplicates
        for k, v in Counter(new_output_cols).items():
            if v == 1:
                output_names.append(k)
            else:
                for i in range(v):
                    output_names.append(k + str(i))

        return dict(
            class_name=func.__name__.upper(),
            class_docstring=func.__doc__,
            input_names=input_names,
            param_names=param_names,
            output_names=output_names,
            defaults=defaults
        )

    @classmethod
    def get_pandas_ta_indicators(cls, silence_warnings: bool = True) -> tp.Set[str]:
        """Get all pandas-ta indicators.

        !!! note
            Returns only the indicators that have been successfully parsed."""
        import pandas_ta

        indicators = set()
        for func_name in [_k for k, v in pandas_ta.Category.items() for _k in v]:
            try:
                cls.parse_pandas_ta_config(getattr(pandas_ta, func_name))
                indicators.add(func_name.upper())
            except Exception as e:
                if not silence_warnings:
                    warnings.warn(f"Function {func_name}: " + str(e), stacklevel=2)
        return indicators

    @classmethod
    def from_pandas_ta(cls, func_name: str, parse_kwargs: tp.KwargsLike = None,
                       init_kwargs: tp.KwargsLike = None, **kwargs) -> tp.Type[IndicatorBase]:
        """Build an indicator class around a pandas-ta function.

        Requires [pandas-ta](https://github.com/twopirllc/pandas-ta) installed.

        Args:
            func_name (str): Function name.
            parse_kwargs (dict): Keyword arguments passed to `IndicatorFactory.parse_pandas_ta_config`.
            init_kwargs (dict): Keyword arguments passed to `IndicatorFactory`.
            **kwargs: Keyword arguments passed to `IndicatorFactory.from_custom_func`.

        Returns:
            Indicator

        Usage:
            ```pycon
            >>> SMA = vbt.IndicatorFactory.from_pandas_ta('SMA')

            >>> sma = SMA.run(price, length=[2, 3])
            >>> sma.sma
            sma_length         2         3
                          a    b    a    b
            2020-01-01  NaN  NaN  NaN  NaN
            2020-01-02  1.5  4.5  NaN  NaN
            2020-01-03  2.5  3.5  2.0  4.0
            2020-01-04  3.5  2.5  3.0  3.0
            2020-01-05  4.5  1.5  4.0  2.0
            ```

            * To get help on running the indicator, use the `help` command:

            ```pycon
            >>> help(SMA.run)
            Help on method run:

            run(close, length=None, offset=None, short_name='sma', hide_params=None, hide_default=True, **kwargs) method of builtins.type instance
                Run `SMA` indicator.

                * Inputs: `close`
                * Parameters: `length`, `offset`
                * Outputs: `sma`

                Pass a list of parameter names as `hide_params` to hide their column levels.
                Set `hide_default` to False to show the column levels of the parameters with a default value.

                Other keyword arguments are passed to `vectorbt.indicators.factory.run_pipeline`.
            ```

            * To get the indicator docstring, use the `help` command or print the `__doc__` attribute:

            ```pycon
            >>> print(SMA.__doc__)
            Simple Moving Average (SMA)

            The Simple Moving Average is the classic moving average that is the equally
            weighted average over n periods.

            Sources:
                https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/

            Calculation:
                Default Inputs:
                    length=10
                SMA = SUM(close, length) / length

            Args:
                close (pd.Series): Series of 'close's
                length (int): It's period. Default: 10
                offset (int): How many periods to offset the result. Default: 0

            Kwargs:
                adjust (bool): Default: True
                presma (bool, optional): If True, uses SMA for initial value.
                fillna (value, optional): pd.DataFrame.fillna(value)
                fill_method (value, optional): Type of fill method

            Returns:
                pd.Series: New feature generated.
            ```
        """
        import pandas_ta

        func_name = func_name.lower()
        pandas_ta_func = getattr(pandas_ta, func_name)

        if parse_kwargs is None:
            parse_kwargs = {}
        config = cls.parse_pandas_ta_config(pandas_ta_func, **parse_kwargs)

        def apply_func(input_list: tp.List[tp.SeriesFrame],
                       in_output_tuple: tp.Tuple[tp.SeriesFrame, ...],
                       param_tuple: tp.Tuple[tp.Param, ...],
                       **kwargs) -> tp.Union[tp.Array2d, tp.List[tp.Array2d]]:
            is_series = isinstance(input_list[0], pd.Series)
            n_input_cols = 1 if is_series else len(input_list[0].columns)
            outputs = []
            for col in range(n_input_cols):
                output = pandas_ta_func(
                    **{
                        name: input_list[i] if is_series else input_list[i].iloc[:, col]
                        for i, name in enumerate(config['input_names'])
                    },
                    **{
                        name: param_tuple[i]
                        for i, name in enumerate(config['param_names'])
                    },
                    **kwargs
                )
                if isinstance(output, tuple):
                    _outputs = []
                    for o in output:
                        if pd.Index.equals(input_list[0].index, o.index):
                            _outputs.append(o)
                    if len(_outputs) > 1:
                        output = pd.concat(_outputs, axis=1)
                    elif len(_outputs) == 1:
                        output = _outputs[0]
                    else:
                        raise ValueError("No valid outputs were returned")
                if isinstance(output, pd.DataFrame):
                    output = tuple([output.iloc[:, i] for i in range(len(output.columns))])
                outputs.append(output)
            if isinstance(outputs[0], tuple):  # multiple outputs
                outputs = list(zip(*outputs))
                return list(map(np.column_stack, outputs))
            return np.column_stack(outputs)

        defaults = config.pop('defaults')
        PTAIndicator = cls(
            **merge_dicts(
                config,
                init_kwargs
            )
        ).from_apply_func(
            apply_func,
            pass_packed=True,
            keep_pd=True,
            to_2d=False,
            **defaults,
            **kwargs
        )
        return PTAIndicator

    @classmethod
    def get_ta_indicators(cls) -> tp.Set[str]:
        """Get all ta indicators."""
        import ta

        ta_module_names = [k for k in dir(ta) if isinstance(getattr(ta, k), ModuleType)]
        indicators = set()
        for module_name in ta_module_names:
            module = getattr(ta, module_name)
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) \
                        and obj != ta.utils.IndicatorMixin \
                        and issubclass(obj, ta.utils.IndicatorMixin):
                    indicators.add(obj.__name__)
        return indicators

    @classmethod
    def find_ta_indicator(cls, cls_name: str) -> IndicatorMixinT:
        """Get ta indicator class by its name."""
        import ta

        ta_module_names = [k for k in dir(ta) if isinstance(getattr(ta, k), ModuleType)]
        for module_name in ta_module_names:
            module = getattr(ta, module_name)
            if cls_name in dir(module):
                return getattr(module, cls_name)
        raise ValueError(f"Indicator \"{cls_name}\" not found")

    @classmethod
    def parse_ta_config(cls, ind_cls: IndicatorMixinT) -> tp.Kwargs:
        """Get the config of a ta indicator."""
        input_names = []
        param_names = []
        defaults = {}
        output_names = []

        # Parse the __init__ signature of the indicator class to get input names
        sig = inspect.signature(ind_cls)
        for k, v in sig.parameters.items():
            if v.kind not in (v.VAR_POSITIONAL, v.VAR_KEYWORD):
                if v.annotation == inspect.Parameter.empty:
                    raise ValueError(f"Argument \"{k}\" has no annotation")
                if v.annotation == pd.Series:
                    input_names.append(k)
                else:
                    param_names.append(k)
                    if v.default != inspect.Parameter.empty:
                        defaults[k] = v.default

        # Get output names by looking into instance methods
        for attr in dir(ind_cls):
            if not attr.startswith('_'):
                if inspect.signature(getattr(ind_cls, attr)).return_annotation == pd.Series:
                    output_names.append(attr)
                elif 'Returns:\n            pandas.Series' in getattr(ind_cls, attr).__doc__:
                    output_names.append(attr)

        return dict(
            class_name=ind_cls.__name__,
            class_docstring=ind_cls.__doc__,
            input_names=input_names,
            param_names=param_names,
            output_names=output_names,
            defaults=defaults
        )

    @classmethod
    def from_ta(cls, cls_name: str, init_kwargs: tp.KwargsLike = None, **kwargs) -> tp.Type[IndicatorBase]:
        """Build an indicator class around a ta class.

        Requires [ta](https://github.com/bukosabino/ta) installed.

        Args:
            cls_name (str): Class name.
            init_kwargs (dict): Keyword arguments passed to `IndicatorFactory`.
            **kwargs: Keyword arguments passed to `IndicatorFactory.from_custom_func`.

        Returns:
            Indicator

        Usage:
            ```pycon
            >>> SMAIndicator = vbt.IndicatorFactory.from_ta('SMAIndicator')

            >>> sma = SMAIndicator.run(price, window=[2, 3])
            >>> sma.sma_indicator
            smaindicator_window    2         3
                                   a    b    a    b
            2020-01-01           NaN  NaN  NaN  NaN
            2020-01-02           1.5  4.5  NaN  NaN
            2020-01-03           2.5  3.5  2.0  4.0
            2020-01-04           3.5  2.5  3.0  3.0
            2020-01-05           4.5  1.5  4.0  2.0
            ```

            * To get help on running the indicator, use the `help` command:

            ```pycon
            >>> help(SMAIndicator.run)
            Help on method run:

            run(close, window, fillna=False, short_name='smaindicator', hide_params=None, hide_default=True, **kwargs) method of builtins.type instance
                Run `SMAIndicator` indicator.

                * Inputs: `close`
                * Parameters: `window`, `fillna`
                * Outputs: `sma_indicator`

                Pass a list of parameter names as `hide_params` to hide their column levels.
                Set `hide_default` to False to show the column levels of the parameters with a default value.

                Other keyword arguments are passed to `vectorbt.indicators.factory.run_pipeline`.
            ```

            * To get the indicator docstring, use the `help` command or print the `__doc__` attribute:

            ```pycon
            >>> print(SMAIndicator.__doc__)
            SMA - Simple Moving Average

                Args:
                    close(pandas.Series): dataset 'Close' column.
                    window(int): n period.
                    fillna(bool): if True, fill nan values.
            ```
        """

        ind_cls = cls.find_ta_indicator(cls_name)
        config = cls.parse_ta_config(ind_cls)

        def apply_func(input_list: tp.List[tp.SeriesFrame],
                       in_output_tuple: tp.Tuple[tp.SeriesFrame, ...],
                       param_tuple: tp.Tuple[tp.Param, ...],
                       **kwargs) -> tp.Union[tp.Array2d, tp.List[tp.Array2d]]:
            is_series = isinstance(input_list[0], pd.Series)
            n_input_cols = 1 if is_series else len(input_list[0].columns)
            outputs = []
            for col in range(n_input_cols):
                ind = ind_cls(
                    **{
                        name: input_list[i] if is_series else input_list[i].iloc[:, col]
                        for i, name in enumerate(config['input_names'])
                    },
                    **{
                        name: param_tuple[i]
                        for i, name in enumerate(config['param_names'])
                    },
                    **kwargs
                )
                output = []
                for output_name in config['output_names']:
                    output.append(getattr(ind, output_name)())
                if len(output) == 1:
                    output = output[0]
                else:
                    output = tuple(output)
                outputs.append(output)
            if isinstance(outputs[0], tuple):  # multiple outputs
                outputs = list(zip(*outputs))
                return list(map(np.column_stack, outputs))
            return np.column_stack(outputs)

        defaults = config.pop('defaults')
        TAIndicator = cls(
            **merge_dicts(
                config,
                init_kwargs
            )
        ).from_apply_func(
            apply_func,
            pass_packed=True,
            keep_pd=True,
            to_2d=False,
            **defaults,
            **kwargs
        )
        return TAIndicator
