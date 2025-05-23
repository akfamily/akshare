# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules with utilities that are used throughout vectorbt."""

from vectorbt.utils.config import atomic_dict, merge_dicts, Config, Configured, AtomicConfig
from vectorbt.utils.decorators import CacheCondition, cached_property, cached_method
from vectorbt.utils.figure import Figure, FigureWidget, make_figure, make_subplots
from vectorbt.utils.image_ import save_animation
from vectorbt.utils.random_ import set_seed
from vectorbt.utils.schedule_ import AsyncJob, AsyncScheduler, CancelledError, ScheduleManager
from vectorbt.utils.template import Sub, Rep, RepEval, RepFunc, deep_substitute

__all__ = [
    'atomic_dict',
    'merge_dicts',
    'Config',
    'Configured',
    'AtomicConfig',
    'Sub',
    'Rep',
    'RepEval',
    'RepFunc',
    'deep_substitute',
    'CacheCondition',
    'cached_property',
    'cached_method',
    'Figure',
    'FigureWidget',
    'make_figure',
    'make_subplots',
    'set_seed',
    'save_animation',
    'AsyncJob',
    'AsyncScheduler',
    'CancelledError',
    'ScheduleManager'
]

__pdoc__ = {k: False for k in __all__}
