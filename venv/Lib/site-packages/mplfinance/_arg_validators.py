import matplotlib.dates  as mdates
import pandas   as pd
import numpy    as np
import datetime
from   mplfinance._helpers import _list_of_dict, _mpf_is_color_like
from   mplfinance._helpers import _num_or_seq_of_num
import matplotlib as mpl
import warnings


def _check_and_prepare_data(data, config):
    '''
    Check and Prepare the data input:
    For now, data must be a Pandas DataFrame with a DatetimeIndex
    and columns named 'Open', 'High', 'Low', 'Close', and optionally 'Volume'

    Later (if there is demand for it) we may accept all of the following data formats:
      1. Pandas DataFrame with DatetimeIndex (as described above)
      2. Pandas Series with DatetimeIndex:
             Values are close prices, and Series generates a line plot
      3. Tuple of Lists, or List of Lists:
             The inner Lists are each columns, in the order: DateTime, Open, High, Low, Close, Volume
      4. Tuple of Tuples or List of Tuples:
             The inner tuples are each row, containing values in the order: DateTime, Open, High, Low, Close, Volume

    Return a Tuple of Lists: datetimes, opens, highs, lows, closes, volumes
    '''
    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError('Expect data as DataFrame')

    if not isinstance(data.index,pd.core.indexes.datetimes.DatetimeIndex):
        raise TypeError('Expect data.index as DatetimeIndex')

    # We will not be fully case-insensitive (since Pandas columns as NOT case-insensitive)
    # but because so many people have requested it, for the default column names we will
    # try both Capitalized and lower case:
    columns = config['columns']
    if columns is None:
        columns =  ('Open', 'High', 'Low', 'Close', 'Volume')
        if all([c.lower() in data for c in columns[0:4]]):
            columns =  ('open', 'high', 'low', 'close', 'volume')
        
    o, h, l, c, v = columns
    cols = [o, h, l, c]

    if config['volume'] != False:
        expect_cols = columns
    else:
        expect_cols = cols
     
    for col in expect_cols:
        if col not in data.columns:
            for dc in data.columns:
                if dc.strip() != dc:
                    warnings.warn('\n ================================================================= '+
                                  '\n   Input DataFrame column name "'+dc+'" '+
                                  '\n   contains leading and/or trailing whitespace.',category=UserWarning)
            raise ValueError('Column "'+col+'" NOT FOUND in Input DataFrame!'+
                             '\n            CHECK that your column names are correct AND/OR'+
                             '\n            CHECK for leading or trailing blanks in your column names.')

    opens   = data[o].values
    highs   = data[h].values
    lows    = data[l].values
    closes  = data[c].values
    if v in data.columns:
        volumes = data[v].values
        cols.append(v)
    else:
        volumes = None

    for col in cols:
        if not all( isinstance(v,(float,int)) for v in data[col] ):
            raise ValueError('Data for column "'+str(col)+'" must be ALL float or int.')

    if config['tz_localize']:
        dates   = mdates.date2num(data.index.tz_localize(None).to_pydatetime())
    else:  # Just in case someone was depending on this bug (Issue 236)
        dates   = mdates.date2num(data.index.to_pydatetime())

    if (len(data.index) > config['warn_too_much_data'] and
        (config['type']=='candle' or config['type']=='ohlc' or config['type']=='hollow_and_filled')
       ):
        warnings.warn('\n\n ================================================================= '+
                      '\n\n   WARNING: YOU ARE PLOTTING SO MUCH DATA THAT IT MAY NOT BE'+
                        '\n            POSSIBLE TO SEE DETAILS (Candles, Ohlc-Bars, Etc.)'+
                        '\n   For more information see:'+
                        '\n   - https://github.com/matplotlib/mplfinance/wiki/Plotting-Too-Much-Data'+
                        '\n   '+
                        '\n   TO SILENCE THIS WARNING, set `type=\'line\'` in `mpf.plot()`'+
                        '\n   OR set kwarg `warn_too_much_data=N` where N is an integer '+
                        '\n   LARGER than the number of data points you want to plot.'+
                      '\n\n ================================================================ ',
                  category=UserWarning)

    return dates, opens, highs, lows, closes, volumes


def _label_validator(label_value):
    ''' Validates the input of [legend] label for added plots.
    label_value may be a str or a sequence of str.
    '''
    if isinstance(label_value,str):
        return True
    if isinstance(label_value,(list,tuple,np.ndarray)):
        if all([isinstance(v,str) for v in label_value]):
            return True
    return False


def _get_valid_plot_types(plottype=None):

    _alias_types = {
        'candlestick'       : 'candle',
        'ohlc_bars'         : 'ohlc',
        'hollow_candle'     : 'hollow_and_filled',
        'hollow'            : 'hollow_and_filled',
        'hnf'               : 'hollow_and_filled',
    }

    _valid_types = ['candle','ohlc', 'line','renko','pnf','hollow_and_filled']

    _valid_types_all = _valid_types.copy()
    _valid_types_all.extend(_alias_types.keys())

    if plottype is None:
        return _valid_types_all
    elif plottype in _alias_types:
        return _alias_types[plottype]
    return plottype
        

def _mav_validator(mav_value):
    '''
    Value for mav (moving average) keyword may be:
    scalar int greater than 1, or tuple of ints, or list of ints (each greater than 1)
    or a dict of `period` and `shift` each of which may be:
    scalar int, or tuple of ints, or list of ints: each `period` int must be greater than 1
    '''
    def _valid_mav(value, is_period=True):
        if not isinstance(value,(tuple,list,int)):
            return False
        if isinstance(value,int):
            return (value >= 2 or not is_period)
        # Must be a tuple or list here:
        for num in value:
            if not isinstance(num,int) or (is_period and num < 2):
                return False
        return True

    if not isinstance(mav_value,(tuple,list,int,dict)):
        return False

    if not isinstance(mav_value,dict):
        return _valid_mav(mav_value)

    else: #isinstance(mav_value,dict)
        if 'period' not in mav_value: return False

        period = mav_value['period']
        if not _valid_mav(period): return False

        if 'shift' not in mav_value: return True

        shift  = mav_value['shift']
        if not _valid_mav(shift, False):  return False
        if isinstance(period,int) and isinstance(shift,int): return True
        if isinstance(period,(tuple,list)) and isinstance(shift,(tuple,list)):
            if len(period) != len(shift): return False
            return True
        return False


def _hlines_validator(value):
    if isinstance(value,dict):
        if 'hlines' in value:
            value = value['hlines']
        else:
            return False
    return ( isinstance(value,(float,int)) or (isinstance(value,(list,tuple)) and
             all([isinstance(v,(float,int)) for v in value])) )

def _is_datelike(value):
    if isinstance(value, (pd.Timestamp,datetime.datetime,datetime.date)):
        return True
    if isinstance(value,str):
        try:
            dt = pd.to_datetime(value)
            return True
        except:
            return False
    return False

def _xlim_validator(value):
    return (isinstance(value, (list,tuple)) and len(value) == 2
            and (all([isinstance(v,(int,float)) for v in value])
                 or all([_is_datelike(v) for v in value])))

def _vlines_validator(value):
    '''Validate `vlines` kwarg value:  must be "datelike" or sequence of "datelike"
    '''
    if isinstance(value,dict):
        if 'vlines' in value:
            value = value['vlines']
        else:
            return False
    if _is_datelike(value): return True
    if not isinstance(value,(list,tuple)): return False
    if not all([_is_datelike(v) for v in value]): return False
    return True

def _alines_validator(value, returnStandardizedValue=False):
    '''
    Value for segments to be passed into LineCollection constructor must be:
    - a sequence of `lines`, where
    - a `lines` is a sequence of 2 or more vertices, where
    - a vertex is a `pair`, aka a sequence of two values, an x and a y point.

    From matplotlib.collections:
        `segments` are:
        A sequence of (line0, line1, line2), where:

        linen = (x0, y0), (x1, y1), ... (xm, ym)
       
        or the equivalent numpy array with two columns. Each line can be a different length.

    The above is from the matplotlib LineCollection documentation.
    It basically says that the "segments" passed into the LineCollection constructor 
    must be a Sequence of Sequences of 2 or more xy Pairs.  However here in `mplfinance`
    we want to allow that (seq of seq of xy pairs) _as well as_ just a sequence of pairs.
    Therefore here in the validator we will allow both:
       (a) seq of at least 2 date,float pairs         (this is a 'line'    as defined above)
       (b) seq of seqs of at least 2 date,float pairs (this is a 'seqment' as defined above)
    '''
    if isinstance(value,dict):
        if 'alines' in value:
            value = value['alines']
        else:
            return False

    if not isinstance(value,(list,tuple)):
        return False if not returnStandardizedValue else None

    if not all([isinstance(line,(list,tuple)) and len(line) > 1 for line in value]):
        return False if not returnStandardizedValue else None

    # now, were the above really `lines`, or were they simply `vertices`
    if all( [ isinstance(point,(list,tuple)) and len(point)==2 and
              _is_datelike(point[0]) and isinstance(point[1],(float,int))
              for line in value for point in line ] ):
        # they were lines:
        return True if not returnStandardizedValue else value

    # here, if valid, we have a sequence of vertices (points)
    if all( [ isinstance(point,(list,tuple)) and len(point)==2 and
              _is_datelike(point[0]) and isinstance(point[1],(float,int))
              for point in value ] ):
        return True if not returnStandardizedValue else [value,]

    return False if not returnStandardizedValue else None

def _tlines_validator(value):
    '''
    Validate `tlines` kwarg value: must be sequence of "datelike" pairs.
    '''
    def _tlines_subvalidator(value):
        if isinstance(value,dict):
            if 'tlines' in value:
                value = value['tlines']
            else:
                return False
        if not isinstance(value,(list,tuple)):
            return False
        if not all([isinstance(pair,(list,tuple)) and len(pair) == 2 and
                    _is_datelike(pair[0]) and _is_datelike(pair[1]) for pair in value]):
            return False
        return True

    if isinstance(value,(list,tuple)) and all([isinstance(v,dict) for v in value]):
        for v in value:
            if not _tlines_subvalidator(v):
                return False
        return True
    else:
        return _tlines_subvalidator(value)

def _bypass_kwarg_validation(value):
    ''' For some kwargs, we either don't know enough, or
        the validation is too complex to make it worth while,
        so we bypass kwarg validation.  If the kwarg is 
        invalid, then eventually an exception will be 
        raised at the time the kwarg value is actually used.
    '''
    return True

def _kwarg_not_implemented(value):
    ''' If you want to list a kwarg in a valid_kwargs dict for a given
        function, but you have not yet, or don't yet want to, implement
        the kwarg; or you simply want to (temporarily) disable the kwarg,
        then use this function as the kwarg validator
    '''
    raise NotImplementedError('kwarg NOT implemented.')

def _validate_vkwargs_dict(vkwargs):
    """
    Check that we didn't make a typo in any of the things
    that should be the same for all vkwargs dict items:

    {kwarg : {'Default': ... , 'Description': ... , 'Validator': ...} }
    """
    for key, value in vkwargs.items():
        # has been changed to 3 to support descriptions
        if len(value) != 3:
            raise ValueError('Items != 3 in valid kwarg table, for kwarg "'+key+'"')
        if 'Default' not in value:
            raise ValueError('Missing "Default" value for kwarg "'+key+'"')
        if 'Description' not in value:
            raise ValueError('Missing "Description" value for kwarg "'+key+'"')
        if 'Validator' not in value:
            raise ValueError('Missing "Validator" function for kwarg "'+key+'"')

def _process_kwargs(kwargs, vkwargs):
    '''
    Given a "valid kwargs table" and some kwargs, verify that each key-word
    is valid per the kwargs table, and that the value of the kwarg is the
    correct type.  Fill a configuration dictionary with the default value
    for each kwarg, and then substitute in any values that were provided 
    as kwargs and return the configuration dictionary.
    '''
    # initialize configuration from valid_kwargs_table:
    config  = {}
    for key, value in vkwargs.items():
        config[key] = value['Default']

    # now validate kwargs, and for any valid kwargs
    #  replace the appropriate value in config:
    for key in kwargs.keys():
        if key not in vkwargs:
            raise KeyError('Unrecognized kwarg="'+str(key)+'"')
        else:
            value = kwargs[key]
            try:
                valid = vkwargs[key]['Validator'](value)
            except Exception as ex:
                ex.extra_info = 'kwarg "'+key+'" validator raised exception to value: "'+str(value)+'"'
                raise
            if not valid:
                import inspect
                v = inspect.getsource(vkwargs[key]['Validator']).strip()
                raise TypeError('kwarg "'+key+'" validator returned False for value: "'+str(value)+'"\n    '+v)

       # ---------------------------------------------------------------
       #  At this point in the loop, if we have not raised an exception,
       #      then kwarg is valid as far as we can tell, therefore, 
       #      go ahead and replace the appropriate value in config:

        config[key] = value

    return config

def _valid_panel_id(panid):
    return panid in ['main','lower'] or (isinstance(panid,int) and panid >= 0 and panid < 32)

def _scale_padding_validator(value):
    if isinstance(value,(int,float)):
        return True
    elif isinstance(value,dict):
        valid_keys=('left','right','top','bottom')
        for key in value:
            if key not in valid_keys:
                raise ValueError('Invalid key "'+str(key)+'" found in `scale_padding` dict.')
            if not isinstance(value[key],(int,float)):
                raise ValueError('`scale_padding` dict contains non-number at key "'+str(key)+'"') 
        return True
    else:
        raise ValueError('`scale_padding` kwarg must be a number, or dict of (left,right,top,bottom) numbers.')
    return False

def _yscale_validator(value):
    if isinstance(value,str) and value in ("linear", "log", "symlog", "logit"):
        return True

    if not isinstance(value,dict):
        return False

    # At this point, value is a dict:
    if not 'yscale' in value:
        return False

    yscale = value['yscale']
    if not (isinstance(yscale,str) and yscale in ("linear", "log", "symlog", "logit")):
        return False

    return True


def _is_marketcolor_object(obj):
    if not isinstance(obj,dict): return False
    market_colors_keys = ('candle','edge','wick','ohlc')
    return all([k in obj for k in market_colors_keys])


def _mco_validator(value):        # marketcolor overrides validator
    if isinstance(value,dict):    # not yet supported, but maybe we will have other
        if 'colors' not in value: # kwargs related to mktcolor overrides (ex: `mco_faceonly`)
            raise ValueError('`marketcolor_overrides` as dict must contain `colors` key.')
        colors = value['colors']
    else:
        colors = value
    if not isinstance(colors,(list,tuple,np.ndarray)):
        return False
    return all([(c is None or 
                 _mpf_is_color_like(c) or
                 _is_marketcolor_object(c) ) for c in colors])

def _check_for_external_axes(config):
    '''
    Check that all `fig` and `ax` kwargs are either ALL None, 
    or ALL are valid instances of Figures/Axes:
 
    An external Axes object can be passed in three places:
        - mpf.plot() `ax=` kwarg
        - mpf.plot() `volume=` kwarg
        - mpf.make_addplot() `ax=` kwarg
    ALL three places MUST be an Axes object, OR
    ALL three places MUST be None.  But it may not be mixed.
    '''
    ap_axlist = []
    addplot = config['addplot']
    if addplot is not None:
        if isinstance(addplot,dict):
            addplot = [addplot,]   # make list of dict to be consistent
        elif not _list_of_dict(addplot):
            raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))
        for apd in addplot:
            ap_axlist.append(apd['ax'])
 
    if len(ap_axlist) > 0:
        if config['ax'] is None:
            if not all([ax is None for ax in ap_axlist]):
                raise ValueError('make_addplot() `ax` kwarg NOT all None, while plot() `ax` kwarg IS None')
        else: # config['ax'] is NOT None:
            if not isinstance(config['ax'],mpl.axes.Axes):
                raise ValueError('plot() ax kwarg must be of type `matplotlib.axis.Axes`')
            if not all([isinstance(ax,mpl.axes.Axes) for ax in ap_axlist]):
                raise ValueError('make_addplot() `ax` kwargs must all be of type `matplotlib.axis.Axes`')

    # At this point, if we have not raised an exception, then plot(ax=) and make_addplot(ax=)
    # are in sync: either they are all None, or they are all of type `matplotlib.axes.Axes`.
    # Therefore we only need plot(ax=), i.e. config['ax'], as we check `volume`: ### and `fig`:

    if config['ax'] is None:
        if isinstance(config['volume'],mpl.axes.Axes):
            raise ValueError('`volume` set to external Axes requires all other Axes be external.')
        #if config['fig'] is not None:
        #    raise ValueError('`fig` kwarg must be None if `ax` kwarg is None.')
    else:
        if not isinstance(config['volume'],mpl.axes.Axes) and config['volume'] != False:
            raise ValueError('`volume` must be of type `matplotlib.axis.Axes`')
        #if not isinstance(config['fig'],mpl.figure.Figure):
        #    raise ValueError('`fig` kwarg must be of type `matplotlib.figure.Figure`')
    
    external_axes_mode = True if isinstance(config['ax'],mpl.axes.Axes) else False
    return external_axes_mode

def _valid_fb_dict(value):
    return (isinstance(value,dict) and
            'y1' in value and
            _num_or_seq_of_num(value['y1']))

def _fill_between_validator(value):
    if _num_or_seq_of_num(value): return True
    if _valid_fb_dict(value): return True
    if _list_of_dict(value):
        return all([_valid_fb_dict(v) for v in value])
    return False
