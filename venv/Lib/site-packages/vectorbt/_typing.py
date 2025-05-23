# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""General types used in vectorbt."""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame as Frame, Index
from typing import *
from datetime import datetime, timedelta, tzinfo
from mypy_extensions import VarArg, KwArg
from pandas.tseries.offsets import DateOffset
from plotly.graph_objects import Figure, FigureWidget
from plotly.basedatatypes import BaseFigure, BaseTraceType
from numba.core.registry import CPUDispatcher
from numba.typed import List as NumbaList
from pathlib import Path

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

# Generic types
T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

# Scalars
Scalar = Union[str, float, int, complex, bool, object, np.generic]
Number = Union[int, float, complex, np.number, np.bool_]
Int = Union[int, np.integer]
Float = Union[float, np.floating]
IntFloat = Union[Int, Float]

# Basic sequences
MaybeTuple = Union[T, Tuple[T, ...]]
MaybeList = Union[T, List[T]]
TupleList = Union[List[T], Tuple[T, ...]]
MaybeTupleList = Union[T, List[T], Tuple[T, ...]]
MaybeIterable = Union[T, Iterable[T]]
MaybeSequence = Union[T, Sequence[T]]


# Arrays
class SupportsArray(Protocol):
    def __array__(self) -> np.ndarray: ...


DTypeLike = Any
PandasDTypeLike = Any
Shape = Tuple[int, ...]
RelaxedShape = Union[int, Shape]
Array = np.ndarray  # ready to be used for n-dim data
Array1d = np.ndarray
Array2d = np.ndarray
Array3d = np.ndarray
Record = np.void
RecordArray = np.ndarray
RecArray = np.recarray
MaybeArray = Union[T, Array]
SeriesFrame = Union[Series, Frame]
MaybeSeries = Union[T, Series]
MaybeSeriesFrame = Union[T, Series, Frame]
AnyArray = Union[Array, Series, Frame]
AnyArray1d = Union[Array1d, Series]
AnyArray2d = Union[Array2d, Frame]
_ArrayLike = Union[Scalar, Sequence[Scalar], Sequence[Sequence[Any]], SupportsArray]
ArrayLike = Union[_ArrayLike, Array, Index, Series, Frame]  # must be converted
IndexLike = Union[_ArrayLike, Array1d, Index, Series]
ArrayLikeSequence = Union[Sequence[T], Array1d, Index, Series]  # sequence for 1-dim data

# Labels
Label = Hashable
Labels = ArrayLikeSequence[Label]
Level = Union[str, int]
LevelSequence = Sequence[Level]
MaybeLevelSequence = Union[Level, LevelSequence]

# Datetime
FrequencyLike = Union[str, float, pd.Timedelta, timedelta, np.timedelta64, DateOffset]
PandasFrequencyLike = Union[str, pd.Timedelta, timedelta, np.timedelta64, DateOffset]
TimezoneLike = Union[None, str, float, timedelta, tzinfo]
DatetimeLikeIndex = Union[pd.DatetimeIndex, pd.TimedeltaIndex, pd.PeriodIndex]
DatetimeLike = Union[str, float, pd.Timestamp, np.datetime64, datetime]


class SupportsTZInfo(Protocol):
    tzinfo: tzinfo


# Indexing
PandasIndexingFunc = Callable[[SeriesFrame], MaybeSeriesFrame]

# Grouping
GroupByLike = Union[None, bool, MaybeLevelSequence, IndexLike]
PandasGroupByLike = Union[Label, Labels, Callable, Mapping[Label, Any]]

# Wrapping
NameIndex = Union[None, Any, Index]

# Config
DictLike = Union[None, dict]
DictLikeSequence = MaybeSequence[DictLike]
Args = Tuple[Any, ...]
ArgsLike = Union[None, Args]
Kwargs = Dict[str, Any]
KwargsLike = Union[None, Kwargs]
KwargsLikeSequence = MaybeSequence[KwargsLike]
FileName = Union[str, Path]

# Data
Data = Dict[Label, SeriesFrame]

# Plotting
TraceName = Union[str, None]
TraceNames = MaybeSequence[TraceName]

# Generic
I = TypeVar("I")
R = TypeVar("R")
ApplyFunc = Callable[[int, Array1d, VarArg()], MaybeArray]
RowApplyFunc = Callable[[int, Array1d, VarArg()], MaybeArray]
RollApplyFunc = Callable[[int, int, Array1d, VarArg()], Scalar]
RollMatrixApplyFunc = Callable[[int, Array2d, VarArg()], MaybeArray]
GroupByApplyFunc = Callable[[Array1d, int, Array1d, VarArg()], Scalar]
GroupByMatrixApplyFunc = Callable[[Array1d, Array2d, VarArg()], MaybeArray]
ApplyMapFunc = Callable[[int, int, I, VarArg()], Scalar]
FilterFunc = Callable[[int, int, I, VarArg()], bool]
ReduceFunc = Callable[[int, Array1d, VarArg()], Scalar]
ReduceArrayFunc = Callable[[int, Array1d, VarArg()], Array1d]
GroupReduceFunc = Callable[[int, Array2d, VarArg()], Scalar]
FlatGroupReduceFunc = Callable[[int, Array1d, VarArg()], Scalar]
GroupReduceArrayFunc = Callable[[int, Array2d, VarArg()], Array1d]
FlatGroupReduceArrayFunc = Callable[[int, Array1d, VarArg()], Array1d]
GroupSqueezeFunc = Callable[[int, int, Array1d, VarArg()], R]

# Signals
ChoiceFunc = Callable[[int, int, int, VarArg()], Array1d]
RankFunc = Callable[[int, int, int, int, int, VarArg()], int]

# Records
ColRange = Array2d
ColMap = Tuple[Array1d, Array1d]
MappedApplyFunc = Callable[[Array1d, int, Array1d, VarArg()], Array1d]
RecordApplyFunc = Callable[[RecordArray, VarArg()], Array1d]
RecordMapFunc = Callable[[np.void, VarArg()], R]
MaskInOutMapFunc = Callable[[Array1d, Array1d, int, Array1d, VarArg()], None]

# Indicators
Param = Any
Params = Union[List[Param], Tuple[Param, ...], NumbaList, Array1d]

# Mappings
Enum = NamedTuple
MappingLike = Union[str, Mapping, Enum, IndexLike]
