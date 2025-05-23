#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2016 California Institute of Technology.
# Copyright (c) 2016-2025 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/dill/blob/master/LICENSE

from dill.source import getsource, getname, _wrap, getimport
from dill.source import importable
from dill._dill import IS_PYPY

import sys
PY310b = 0x30a00b1

f = lambda x: x**2
def g(x): return f(x) - x

def h(x):
  def g(x): return x
  return g(x) - x

class Foo(object):
  def bar(self, x):
    return x*x+x
_foo = Foo()

def add(x,y):
  return x+y

# yes, same as 'f', but things are tricky when it comes to pointers
squared = lambda x:x**2

class Bar:
  pass
_bar = Bar()

                       # inspect.getsourcelines # dill.source.getblocks
def test_getsource():
  assert getsource(f) == 'f = lambda x: x**2\n'
  assert getsource(g) == 'def g(x): return f(x) - x\n'
  assert getsource(h) == 'def h(x):\n  def g(x): return x\n  return g(x) - x\n'
  assert getname(f) == 'f'
  assert getname(g) == 'g'
  assert getname(h) == 'h'
  assert _wrap(f)(4) == 16
  assert _wrap(g)(4) == 12
  assert _wrap(h)(4) == 0

  assert getname(Foo) == 'Foo'
  assert getname(Bar) == 'Bar'
  assert getsource(Bar) == 'class Bar:\n  pass\n'
  assert getsource(Foo) == 'class Foo(object):\n  def bar(self, x):\n    return x*x+x\n'
  #XXX: add getsource for  _foo, _bar

# test itself
def test_itself():
  assert getimport(getimport)=='from dill.source import getimport\n'

# builtin functions and objects
def test_builtin():
  assert getimport(pow) == 'pow\n'
  assert getimport(100) == '100\n'
  assert getimport(True) == 'True\n'
  assert getimport(pow, builtin=True) == 'from builtins import pow\n'
  assert getimport(100, builtin=True) == '100\n'
  assert getimport(True, builtin=True) == 'True\n'
  # this is kinda BS... you can't import a None
  assert getimport(None) == 'None\n'
  assert getimport(None, builtin=True) == 'None\n'


# other imported functions
def test_imported():
  from math import sin
  assert getimport(sin) == 'from math import sin\n'

# interactively defined functions
def test_dynamic():
  assert getimport(add) == 'from %s import add\n' % __name__
  # interactive lambdas
  assert getimport(squared) == 'from %s import squared\n' % __name__

# classes and class instances
def test_classes():
  from io import BytesIO as StringIO
  y = "from _io import BytesIO\n"
  x = y if (IS_PYPY or sys.hexversion >= PY310b) else "from io import BytesIO\n"
  s = StringIO()

  assert getimport(StringIO) == x
  assert getimport(s) == y
  # interactively defined classes and class instances
  assert getimport(Foo) == 'from %s import Foo\n' % __name__
  assert getimport(_foo) == 'from %s import Foo\n' % __name__


# test importable
def test_importable():
  assert importable(add, source=False) == 'from %s import add\n' % __name__
  assert importable(squared, source=False) == 'from %s import squared\n' % __name__
  assert importable(Foo, source=False) == 'from %s import Foo\n' % __name__
  assert importable(Foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(_foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(None, source=False) == 'None\n'
  assert importable(100, source=False) == '100\n'

  assert importable(add, source=True) == 'def add(x,y):\n  return x+y\n'
  assert importable(squared, source=True) == 'squared = lambda x:x**2\n'
  assert importable(None, source=True) == 'None\n'
  assert importable(Bar, source=True) == 'class Bar:\n  pass\n'
  assert importable(Foo, source=True) == 'class Foo(object):\n  def bar(self, x):\n    return x*x+x\n'
  assert importable(Foo.bar, source=True) == 'def bar(self, x):\n  return x*x+x\n'
  assert importable(Foo.bar, source=False) == 'from %s import bar\n' % __name__
  assert importable(Foo.bar, alias='memo', source=False) == 'from %s import bar as memo\n' % __name__
  assert importable(Foo, alias='memo', source=False) == 'from %s import Foo as memo\n' % __name__
  assert importable(squared, alias='memo', source=False) == 'from %s import squared as memo\n' % __name__
  assert importable(squared, alias='memo', source=True) == 'memo = squared = lambda x:x**2\n'
  assert importable(add, alias='memo', source=True) == 'def add(x,y):\n  return x+y\n\nmemo = add\n'
  assert importable(None, alias='memo', source=True) == 'memo = None\n'
  assert importable(100, alias='memo', source=True) == 'memo = 100\n'
  assert importable(add, builtin=True, source=False) == 'from %s import add\n' % __name__
  assert importable(squared, builtin=True, source=False) == 'from %s import squared\n' % __name__
  assert importable(Foo, builtin=True, source=False) == 'from %s import Foo\n' % __name__
  assert importable(Foo.bar, builtin=True, source=False) == 'from %s import bar\n' % __name__
  assert importable(_foo.bar, builtin=True, source=False) == 'from %s import bar\n' % __name__
  assert importable(None, builtin=True, source=False) == 'None\n'
  assert importable(100, builtin=True, source=False) == '100\n'


def test_numpy():
  try:
    import numpy as np
    y = np.array
    x = y([1,2,3])
    assert importable(x, source=False) == 'from numpy import array\narray([1, 2, 3])\n'
    assert importable(y, source=False) == 'from %s import array\n' % y.__module__
    assert importable(x, source=True) == 'from numpy import array\narray([1, 2, 3])\n'
    assert importable(y, source=True) == 'from %s import array\n' % y.__module__
    y = np.int64
    x = y(0)
    assert importable(x, source=False) == 'from numpy import int64\nint64(0)\n'
    assert importable(y, source=False) == 'from %s import int64\n' % y.__module__
    assert importable(x, source=True) == 'from numpy import int64\nint64(0)\n'
    assert importable(y, source=True) == 'from %s import int64\n' % y.__module__
    y = np.bool_
    x = y(0)
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        if hasattr(np, 'bool'): b = 'bool_' if np.bool is bool else 'bool'
        else: b = 'bool_'
    assert importable(x, source=False) == 'from numpy import %s\n%s(False)\n' % (b,b)
    assert importable(y, source=False) == 'from %s import %s\n' % (y.__module__,b)
    assert importable(x, source=True) == 'from numpy import %s\n%s(False)\n' % (b,b)
    assert importable(y, source=True) == 'from %s import %s\n' % (y.__module__,b)
  except ImportError: pass

#NOTE: if before getimport(pow), will cause pow to throw AssertionError
def test_foo():
  assert importable(_foo, source=True).startswith("import dill\nclass Foo(object):\n  def bar(self, x):\n    return x*x+x\ndill.loads(")

if __name__ == '__main__':
    test_getsource()
    test_itself()
    test_builtin()
    test_imported()
    test_dynamic()
    test_classes()
    test_importable()
    test_numpy()
    test_foo()
