# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

__pdoc__ = {}

# Import version
from vectorbt._version import __version__ as _version

__version__ = _version

# Most important modules
from vectorbt.generic import nb, plotting
from vectorbt._settings import settings

# Most important classes
from vectorbt.utils import *
from vectorbt.base import *
from vectorbt.data import *
from vectorbt.generic import *
from vectorbt.indicators import *
from vectorbt.signals import *
from vectorbt.records import *
from vectorbt.portfolio import *
from vectorbt.labels import *
from vectorbt.messaging import *

# Import all submodules
from vectorbt.utils.module_ import import_submodules

# silence NumbaExperimentalFeatureWarning
import warnings
from numba.core.errors import NumbaExperimentalFeatureWarning

warnings.filterwarnings("ignore", category=NumbaExperimentalFeatureWarning)

import_submodules(__name__)

__pdoc__['_settings'] = True
