"""
Some helper functions for mplfinance.
NOTE: This is the lowest level in mplfinance:
      This file should have NO dependencies on
      any other mplfinance files.
"""

import datetime
import matplotlib.dates  as mdates
import matplotlib.colors as mcolors
import numpy as np

def _adjust_color_brightness(color,amount=0.5):
    
    def _adjcb(c1, amount):
        import matplotlib.colors as mc
        import colorsys
        # mc.is_color_like(value)
        try:
            c = mc.cnames[c1]
        except:
            c = c1
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

    if not isinstance(color,(list,tuple)):
        return _adjcb(color,amount)
        
    cout = []
    cadj = {}
    for c1 in color:
        if c1 in cadj:
            cout.append(cadj[c1])
        else:
            newc = _adjcb(c1,amount)
            cadj[c1] = newc
            cout.append(cadj[c1])
    return cout


def _determine_format_string( dates, datetime_format=None ):
    """
    Determine the datetime format string based on the averge number
    of days between data points, or if the user passed in kwarg
    datetime_format, use that as an override.
    """
    avg_days_between_points = (dates[-1] - dates[0]) / float(len(dates))

    if datetime_format is not None:
        return datetime_format

    # avgerage of 3 or more data points per day we will call intraday data:
    if avg_days_between_points < 0.33:  # intraday
        if mdates.num2date(dates[-1]).date() != mdates.num2date(dates[0]).date():
            # intraday data for more than one day:
            fmtstring = '%b %d, %H:%M'
        else:  # intraday data for a single day
            fmtstring = '%H:%M'
    else:  # 'daily' data (or could be weekly, etc.)
        if mdates.num2date(dates[-1]).date().year != mdates.num2date(dates[0]).date().year:
           fmtstring = '%Y-%b-%d'
        else:
           fmtstring = '%b %d'
    return fmtstring


def _list_of_dict(x):
    '''
    Return True if x is a list of dict's
    '''
    return isinstance(x,list) and all([isinstance(item,dict) for item in x])

def _num_or_seq_of_num(value):
    return ( isinstance(value,(int,float,np.integer,np.floating))  or
             (isinstance(value,(list,tuple,np.ndarray)) and
             all([isinstance(v,(int,float,np.integer,np.floating)) for v in value]))
           )

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt is None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


def _is_uint8_rgb_or_rgba(tup):
    """ Deterine if rgb or rgba is in (0-255) format:
    Matplotlib expects rgb (and rgba) tuples to contain
    three (or four) floats between 0.0 and 1.0 
    
    Some people express rgb as tuples of three integers
    between 0 and 255.
    (In rgba, alpha is still a float from 0.0 to 1.0)
    """
    if isinstance(tup,str):  return False
    if not np.iterable(tup): return False
    L = len(tup)
    if L < 3 or L > 4: return False
    if L == 4 and (tup[3] < 0 or tup[3] > 1): return False
    return not any([not isinstance(v,(int,np.unsignedinteger)) or v<0 or v>255 for v in tup[0:3]])

def _mpf_is_color_like(c):
    """Determine if an object is a color.
    
    Identical to `matplotlib.colors.is_color_like()`
    BUT ALSO considers int (0-255) rgb and rgba colors.
    """
    if mcolors.is_color_like(c): return True
    return _is_uint8_rgb_or_rgba(c)
    
def _mpf_to_rgba(c, alpha=None):
    cnew = c
    if _is_uint8_rgb_or_rgba(c) and any(e>1 for e in c[:3]):
        cnew = tuple([e/255. for e in c[:3]])
        if len(c) == 4: cnew += c[3:]
    return mcolors.to_rgba(cnew, alpha)
