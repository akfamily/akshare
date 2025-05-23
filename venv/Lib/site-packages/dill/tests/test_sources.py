#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Copyright (c) 2024-2025 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/dill/blob/master/LICENSE
"""
check that dill.source performs as expected with changes to locals in 3.13.0b1
see: https://github.com/python/cpython/issues/118888
"""
# repeat functions from test_source.py
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

squared = lambda x:x**2

class Bar:
  pass
_bar = Bar()

# repeat, but from test_source.py
import test_source as ts

# test objects created in other test modules
import test_mixins as tm

import dill.source as ds


def test_isfrommain():
  assert ds.isfrommain(add) == True
  assert ds.isfrommain(squared) == True
  assert ds.isfrommain(Bar) == True
  assert ds.isfrommain(_bar) == True
  assert ds.isfrommain(ts.add) == False
  assert ds.isfrommain(ts.squared) == False
  assert ds.isfrommain(ts.Bar) == False
  assert ds.isfrommain(ts._bar) == False
  assert ds.isfrommain(tm.quad) == False
  assert ds.isfrommain(tm.double_add) == False
  assert ds.isfrommain(tm.quadratic) == False
  assert ds.isdynamic(add) == False
  assert ds.isdynamic(squared) == False
  assert ds.isdynamic(ts.add) == False
  assert ds.isdynamic(ts.squared) == False
  assert ds.isdynamic(tm.double_add) == False
  assert ds.isdynamic(tm.quadratic) == False


def test_matchlambda():
  assert ds._matchlambda(f, 'f = lambda x: x**2\n')
  assert ds._matchlambda(squared, 'squared = lambda x:x**2\n')
  assert ds._matchlambda(ts.f, 'f = lambda x: x**2\n')
  assert ds._matchlambda(ts.squared, 'squared = lambda x:x**2\n')


def test_findsource():
  lines, lineno = ds.findsource(add)
  assert lines[lineno] == 'def add(x,y):\n'
  lines, lineno = ds.findsource(ts.add)
  assert lines[lineno] == 'def add(x,y):\n'
  lines, lineno = ds.findsource(squared)
  assert lines[lineno] == 'squared = lambda x:x**2\n'
  lines, lineno = ds.findsource(ts.squared)
  assert lines[lineno] == 'squared = lambda x:x**2\n'
  lines, lineno = ds.findsource(Bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(ts.Bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(_bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(ts._bar)
  assert lines[lineno] == 'class Bar:\n'
  lines, lineno = ds.findsource(tm.quad)
  assert lines[lineno] == 'def quad(a=1, b=1, c=0):\n'
  lines, lineno = ds.findsource(tm.double_add)
  assert lines[lineno] == '    def func(*args, **kwds):\n'
  lines, lineno = ds.findsource(tm.quadratic)
  assert lines[lineno] == '  def dec(f):\n'


def test_getsourcelines():
  assert ''.join(ds.getsourcelines(add)[0]) == 'def add(x,y):\n  return x+y\n'
  assert ''.join(ds.getsourcelines(ts.add)[0]) == 'def add(x,y):\n  return x+y\n'
  assert ''.join(ds.getsourcelines(squared)[0]) == 'squared = lambda x:x**2\n'
  assert ''.join(ds.getsourcelines(ts.squared)[0]) == 'squared = lambda x:x**2\n'
  assert ''.join(ds.getsourcelines(Bar)[0]) == 'class Bar:\n  pass\n'
  assert ''.join(ds.getsourcelines(ts.Bar)[0]) == 'class Bar:\n  pass\n'
  assert ''.join(ds.getsourcelines(_bar)[0]) == 'class Bar:\n  pass\n' #XXX: ?
  assert ''.join(ds.getsourcelines(ts._bar)[0]) == 'class Bar:\n  pass\n' #XXX: ?
  assert ''.join(ds.getsourcelines(tm.quad)[0]) == 'def quad(a=1, b=1, c=0):\n  inverted = [False]\n  def invert():\n    inverted[0] = not inverted[0]\n  def dec(f):\n    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n    func.__wrapped__ = f\n    func.invert = invert\n    func.inverted = inverted\n    return func\n  return dec\n'
  assert ''.join(ds.getsourcelines(tm.quadratic)[0]) == '  def dec(f):\n    def func(*args,**kwds):\n      fx = f(*args,**kwds)\n      return a*fx**2 + b*fx + c\n    return func\n'
  assert ''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0]) == 'def dec(f):\n  def func(*args,**kwds):\n    fx = f(*args,**kwds)\n    return a*fx**2 + b*fx + c\n  return func\n'
  assert ''.join(ds.getsourcelines(tm.quadratic, enclosing=True)[0]) == 'def quad_factory(a=1,b=1,c=0):\n  def dec(f):\n    def func(*args,**kwds):\n      fx = f(*args,**kwds)\n      return a*fx**2 + b*fx + c\n    return func\n  return dec\n'
  assert ''.join(ds.getsourcelines(tm.double_add)[0]) == '    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n'
  assert ''.join(ds.getsourcelines(tm.double_add, enclosing=True)[0]) == 'def quad(a=1, b=1, c=0):\n  inverted = [False]\n  def invert():\n    inverted[0] = not inverted[0]\n  def dec(f):\n    def func(*args, **kwds):\n      x = f(*args, **kwds)\n      if inverted[0]: x = -x\n      return a*x**2 + b*x + c\n    func.__wrapped__ = f\n    func.invert = invert\n    func.inverted = inverted\n    return func\n  return dec\n'


def test_indent():
  assert ds.outdent(''.join(ds.getsourcelines(tm.quadratic)[0])) == ''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0])
  assert ds.indent(''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0]), 2) == ''.join(ds.getsourcelines(tm.quadratic)[0])


def test_dumpsource():
  local = {}
  exec(ds.dumpsource(add, alias='raw'), {}, local)
  exec(ds.dumpsource(ts.add, alias='mod'), {}, local)
  assert local['raw'](1,2) == local['mod'](1,2)
  exec(ds.dumpsource(squared, alias='raw'), {}, local)
  exec(ds.dumpsource(ts.squared, alias='mod'), {}, local)
  assert local['raw'](3) == local['mod'](3)
  assert ds._wrap(add)(1,2) == ds._wrap(ts.add)(1,2)
  assert ds._wrap(squared)(3) == ds._wrap(ts.squared)(3)


def test_name():
  assert ds._namespace(add) == ds.getname(add, fqn=True).split('.')
  assert ds._namespace(ts.add) == ds.getname(ts.add, fqn=True).split('.')
  assert ds._namespace(squared) == ds.getname(squared, fqn=True).split('.')
  assert ds._namespace(ts.squared) == ds.getname(ts.squared, fqn=True).split('.')
  assert ds._namespace(Bar) == ds.getname(Bar, fqn=True).split('.')
  assert ds._namespace(ts.Bar) == ds.getname(ts.Bar, fqn=True).split('.')
  assert ds._namespace(tm.quad) == ds.getname(tm.quad, fqn=True).split('.')
  #XXX: the following also works, however behavior may be wrong for nested functions
  #assert ds._namespace(tm.double_add) == ds.getname(tm.double_add, fqn=True).split('.')
  #assert ds._namespace(tm.quadratic) == ds.getname(tm.quadratic, fqn=True).split('.')
  assert ds.getname(add) == 'add'
  assert ds.getname(ts.add) == 'add'
  assert ds.getname(squared) == 'squared'
  assert ds.getname(ts.squared) == 'squared'
  assert ds.getname(Bar) == 'Bar'
  assert ds.getname(ts.Bar) == 'Bar'
  assert ds.getname(tm.quad) == 'quad'
  assert ds.getname(tm.double_add) == 'func' #XXX: ?
  assert ds.getname(tm.quadratic) == 'dec' #XXX: ?


def test_getimport():
  local = {}
  exec(ds.getimport(add, alias='raw'), {}, local)
  exec(ds.getimport(ts.add, alias='mod'), {}, local)
  assert local['raw'](1,2) == local['mod'](1,2)
  exec(ds.getimport(squared, alias='raw'), {}, local)
  exec(ds.getimport(ts.squared, alias='mod'), {}, local)
  assert local['raw'](3) == local['mod'](3)
  exec(ds.getimport(Bar, alias='raw'), {}, local)
  exec(ds.getimport(ts.Bar, alias='mod'), {}, local)
  assert ds.getname(local['raw']) == ds.getname(local['mod'])
  exec(ds.getimport(tm.quad, alias='mod'), {}, local)
  assert local['mod']()(sum)([1,2,3]) == tm.quad()(sum)([1,2,3])
  #FIXME: wrong results for nested functions (e.g. tm.double_add, tm.quadratic)


def test_importable():
  assert ds.importable(add, source=False) == ds.getimport(add)
  assert ds.importable(add) == ds.getsource(add)
  assert ds.importable(squared, source=False) == ds.getimport(squared)
  assert ds.importable(squared) == ds.getsource(squared)
  assert ds.importable(Bar, source=False) == ds.getimport(Bar)
  assert ds.importable(Bar) == ds.getsource(Bar)
  assert ds.importable(ts.add) == ds.getimport(ts.add)
  assert ds.importable(ts.add, source=True) == ds.getsource(ts.add)
  assert ds.importable(ts.squared) == ds.getimport(ts.squared)
  assert ds.importable(ts.squared, source=True) == ds.getsource(ts.squared)
  assert ds.importable(ts.Bar) == ds.getimport(ts.Bar)
  assert ds.importable(ts.Bar, source=True) == ds.getsource(ts.Bar)


if __name__ == '__main__':
  test_isfrommain()
  test_matchlambda()
  test_findsource()
  test_getsourcelines()
  test_indent()
  test_dumpsource()
  test_name()
  test_getimport()
  test_importable()
