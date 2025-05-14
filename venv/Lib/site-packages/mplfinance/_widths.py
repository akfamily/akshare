import pandas as pd
from mplfinance._arg_validators import _process_kwargs, _validate_vkwargs_dict

def _get_widths_df():
    '''
    Provide a dataframe of width data that appropriate scales widths of
    various aspects of the plot (candles,ohlc bars,volume bars) based on
    the amount or density of data.  These numbers were arrived at by 
    carefully testing many use-cases of plots with various styles, 
    and observing which numbers gave the "best" appearance.
    '''
    numpoints = [n for n in range(30,241,30)]
    volume_width     = (0.98, 0.96,  0.95,  0.925,  0.9,  0.9,  0.875, 0.825 )
    volume_linewidth = tuple([0.65]*8)
    candle_width     = (0.65, 0.575, 0.50, 0.445, 0.435, 0.425, 0.420, 0.415)
    candle_linewidth = (1.00, 0.875, 0.75, 0.625, 0.500, 0.438, 0.435, 0.435)
    ohlc_tickwidth   = tuple([0.35]*8)
    ohlc_linewidth   = (1.50, 1.175, 0.85, 0.525, 0.525, 0.525, 0.525, 0.525)
    line_width       = (2.25, 1.8, 1.3, 0.813, 0.807, 0.801, 0.796, 0.791)
    widths = {}
    widths['vw']  = volume_width
    widths['vlw'] = volume_linewidth
    widths['cw']  = candle_width
    widths['clw'] = candle_linewidth
    widths['ow']  = ohlc_tickwidth
    widths['olw'] = ohlc_linewidth
    widths['lw']  = line_width
    return pd.DataFrame(widths,index=numpoints)

_widths = _get_widths_df()


def _valid_scale_width_kwargs():
    vkwargs = {
        'ohlc'             : { 'Default'     : None,
                               'Description' : 'length of horizontal open/close tickmarks on ohlc bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'volume'           : { 'Default'     : None,
                               'Description' : 'width of volume bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'candle'           : { 'Default'     : None,
                               'Description' : 'width of candles',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'lines'            : { 'Default'     : None,
                               'Description' : 'width of lines (for line plots and moving averages)',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'volume_linewidth' : { 'Default'     : None,
                               'Description' : 'width of edges of volume bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'ohlc_linewidth'   : { 'Default'     : None,
                               'Description' : 'width (thickness) of ohlc bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'candle_linewidth' : { 'Default'     : None,
                               'Description' : 'width of candle edges and wicks',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs


def _valid_update_width_kwargs():
    vkwargs = {

        'ohlc_ticksize'    : { 'Default'     : None,
                               'Description' : 'length of horizontal open/close tickmarks on ohlc bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'ohlc_linewidth'   : { 'Default'     : None,
                               'Description' : 'width (thickness) of ohlc bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'volume_width'     : { 'Default'     : None,
                               'Description' : 'width of volume bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'volume_linewidth' : { 'Default'     : None,
                               'Description' : 'width of edges of volume bars',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'candle_width'     : { 'Default'     : None,
                               'Description' : 'width of candles',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'candle_linewidth' : { 'Default'     : None,
                               'Description' : 'width of candle edges and wicks',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },

        'line_width'       : { 'Default'     : None,
                               'Description' : 'width of lines (for line plots and moving averages)',
                               'Validator'   : lambda value: isinstance(value,(float,int)) },
    }

    _validate_vkwargs_dict(vkwargs)

    return vkwargs

def _scale_width_config(scale,width_config):
    if scale['volume'] is not None:
        width_config['volume_width']  *= scale['volume']
    if scale['ohlc'] is not None:
        width_config['ohlc_ticksize'] *= scale['ohlc']
    if scale['candle'] is not None:
        width_config['candle_width']  *= scale['candle']
    if scale['lines'] is not None:
        width_config['line_width']    *= scale['lines']
    if scale['volume_linewidth'] is not None:
        width_config['volume_linewidth']  *= scale['volume_linewidth']
    if scale['ohlc_linewidth'] is not None: 
        width_config['ohlc_linewidth'  ]  *= scale['ohlc_linewidth']
    if scale['candle_linewidth'] is not None:
        width_config['candle_linewidth']  *= scale['candle_linewidth']

def _determine_width_config( xdates, config ):
    '''
    Given x-axis xdates, and `mpf.plot()` kwargs config,
    determine the widths and linewidths for candles,
    volume bars, ohlc bars, etc.
    '''
    datalen = len(xdates)
    avg_dist_between_points = (xdates[-1] - xdates[0]) / float(datalen)

    tweak  = 1.06 if datalen > 100 else 1.03

    adjust = tweak*avg_dist_between_points if config['show_nontrading'] else 1.0

    width_config = {}

    if config['width_adjuster_version'] == 'v0':  # Behave like original version of code:

        width_config['volume_width'    ] = 0.5*avg_dist_between_points
        width_config['volume_linewidth'] = None
        width_config['ohlc_ticksize'   ] = avg_dist_between_points / 2.5
        width_config['ohlc_linewidth'  ] = None
        width_config['candle_width'    ] = avg_dist_between_points / 2.0
        width_config['candle_linewidth'] = None
        width_config['line_width'      ] = None

    else: # config['width_adjuster_version'] == 'v1'

        width_config['volume_width'    ] = _dfinterpolate(_widths,datalen,'vw' ) * adjust
        width_config['volume_linewidth'] = _dfinterpolate(_widths,datalen,'vlw')
        width_config['ohlc_ticksize'   ] = _dfinterpolate(_widths,datalen,'ow' ) * adjust
        width_config['ohlc_linewidth'  ] = _dfinterpolate(_widths,datalen,'olw')
        width_config['candle_width'    ] = _dfinterpolate(_widths,datalen,'cw' ) * adjust
        width_config['candle_linewidth'] = _dfinterpolate(_widths,datalen,'clw')
        width_config['line_width'      ] = _dfinterpolate(_widths,datalen,'lw')

    if 'scale_width_adjustment' in config['style']: 
        scale = _process_kwargs(config['style']['scale_width_adjustment'],_valid_scale_width_kwargs())
        _scale_width_config(scale,width_config)

    if config['scale_width_adjustment'] is not None:
        scale = _process_kwargs(config['scale_width_adjustment'],_valid_scale_width_kwargs())
        _scale_width_config(scale,width_config)

    if config['update_width_config'] is not None:
     
        update = _process_kwargs(config['update_width_config'],_valid_update_width_kwargs())
        uplist = [ (k,v) for k,v in update.items() if v is not None ]
        width_config.update(uplist)

    return width_config


def _dfinterpolate(df,key,column):
    '''
    Given a DataFrame, with all values and the Index as floats,
    and given a float key, find the row that matches the key, or 
    find the two rows surrounding that key, and return the interpolated
    value for the specified column, based on where the key falls between
    the two rows.  If they key is an exact match for a key in the index,
    the return the exact value from the column.  If the key is less than
    or greater than any key in the index, then return either the first
    or last value for the column.
    '''
    s = df[column]
    s1 = s.loc[:key]
    if len(s1) < 1:
        return s.iloc[0]
    j1 = s1.index[-1]
    v1 = s1.iloc[-1]
    
    s2 = s.loc[key:]
    if len(s2) < 1:
        return s.iloc[-1]
    j2 = s2.index[0]
    v2 = s2.iloc[0]

    if j1 == j2:
        return v1
    delta   = j2 - j1
    portion = (key - j1)/delta
    ans = v1 + (v2-v1)*portion
    return ans
