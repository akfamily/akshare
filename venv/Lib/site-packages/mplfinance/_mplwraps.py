import matplotlib.pyplot as plt
import matplotlib.figure as mplfigure
import matplotlib.axes   as mpl_axes
from   mplfinance import _styles
import numpy as np

"""
    This file contains:

    (1) A wrapper of method `matplotlib.pyplot.figure()` that creates a 
        `mplfinance.Mpf_Figure` which is derived from `matplotlib.figure.Figure`
        The wrapper function is the same as `matplotlib.pyplot.figure()` except
        that it additionally accepts kwarg `style=` to set the mplfinance style.

    (2) Class `mplfinance.Mpf_Figure` derived from `matplotlib.figure.Figure`
        which has the following overrides:
        - Attribute `mpfstyle` indicating the mplfinance style used at Figure creation.
        - Methods (listed below) which are identical to the same method in class
          `matplotlib.figure.Figure` except that the `mplfinance.Mpf_Figure` versions:
            - accept kwarg `style=` to set the mplfinance style of Subplot Axes, or
            - if `style=` is not specified, then the attribute
              `mplfinance.Mpf_Figure.mpfstyle` is used for the Subplot Axes style.
          - Figure.add_subplot() 
          - Figure.add_axes() 
          - Figure.subplot()  (this is analogous to pyplot.subplot() which calls Figure.add_subplot())
          - Figure.subplots() 

     (3) A wrapper to matplot.pyplot.show(), because it happens often enough, when using mplfinance,
         that sometimes one has to import matplotlib.pyplot *ONLY* for the purpose of calling .show()
"""

show = plt.show  # Not a true wrapper, rather an assignment.

def _check_for_and_apply_style(kwargs):

    if 'style' in kwargs:
        style = kwargs['style']
        del kwargs['style']
    else:
        style = 'default'

    if not _styles._valid_mpf_style(style):
        raise TypeError('Invalid mplfinance style')

    if isinstance(style,str):
        style = _styles._get_mpfstyle(style)

    if isinstance(style,dict):
        _styles._apply_mpfstyle(style)
    else:
        raise TypeError('style should be a `dict`; why is it not?')

    return style


def figure(*args,**kwargs):

    style = _check_for_and_apply_style(kwargs)

    f = plt.figure(FigureClass=Mpf_Figure,*args,**kwargs)
    f.mpfstyle = style
    return f


class Mpf_Figure(mplfigure.Figure):

    def add_subplot(self,*args,**kwargs):

        if 'style' in kwargs or not hasattr(self,'mpfstyle'):
            style = _check_for_and_apply_style(kwargs)
        else:
            style = _check_for_and_apply_style(dict(style=self.mpfstyle))

        ax = mplfigure.Figure.add_subplot(self,*args,**kwargs)
        ax.mpfstyle = style
        return ax

    def add_axes(self,*args,**kwargs):
    
        if 'style' in kwargs or not hasattr(self,'mpfstyle'):
            style = _check_for_and_apply_style(kwargs)
        else:
            style = _check_for_and_apply_style(dict(style=self.mpfstyle))

        ax = mplfigure.Figure.add_axes(self,*args,**kwargs)
        ax.mpfstyle = style
        return ax

    def subplot(self,*args,**kwargs):
    
        plt.figure(self.number)  # make it the current Figure

        if 'style' in kwargs or not hasattr(self,'mpfstyle'):
            style = _check_for_and_apply_style(kwargs)
        else:
            style = _check_for_and_apply_style(dict(style=self.mpfstyle))

        ax = plt.subplot(*args,**kwargs)
        ax.mpfstyle = style
        return ax


    def subplots(self,*args,**kwargs):
    
        if 'style' in kwargs or not hasattr(self,'mpfstyle'):
            style = _check_for_and_apply_style(kwargs)
            self.mpfstyle = style
        else:
            style = _check_for_and_apply_style(dict(style=self.mpfstyle))
    
        axlist = mplfigure.Figure.subplots(self,*args,**kwargs)

        if isinstance(axlist,mpl_axes.Axes):
            axlist.mpfstyle = style
        elif isinstance(axlist,np.ndarray):
            for ax in axlist.flatten():
                ax.mpfstyle = style
        else:
           raise TypeError('Unexpected type ('+str(type(axlist))+') '+
                           'returned from "matplotlib.figure.Figure.subplots()"')
        return axlist
