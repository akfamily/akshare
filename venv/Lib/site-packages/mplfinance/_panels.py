from mplfinance._helpers import _list_of_dict
from mplfinance._arg_validators import _valid_panel_id
import pandas as pd

def _build_panels( figure, config ):
    """
    Create and return a DataFrame containing panel information
    and Axes objects for each panel, etc.

    We allow up to 32 panels, identified by their panel id (panid)
    which is an integer 0 through 31.  

    Parameters
    ----------
    figure       : pyplot.Figure
        figure on which to create the Axes for the panels

    config       : dict
        config dict from `mplfinance.plot()`
        
    Config
    ------
    The following items are used from `config`:

    num_panels   : integer (0-31) or None
        number of panels to create

    addplot      : dict or None
        value for the `addplot=` kwarg passed into `mplfinance.plot()`

    volume_panel : integer (0-31) or None
        panel id (0-number_of_panels)

    main_panel   : integer (0-31) or None
        panel id (0-number_of_panels)

    panel_ratios : sequence or None
        sequence of relative sizes for the panels;

        NOTE: If len(panel_ratios) == number of panels (regardless
        of whether number of panels was specified or inferred),
        then panel ratios are the relative sizes of each panel,
        in panel id order, 0 through N (where N = number of panels).

        If len(panel_ratios) != number of panels, then len(panel_ratios)
        must equal 2, and panel_ratios[0] is the relative size for the 'main'
        panel, and panel_ratios[1] is the relative size for all other panels.

        If the number of panels == 1, the panel_ratios is ignored.

    
Returns
    ----------
    panels  : pandas.DataFrame
        dataframe indexed by panel id (panid) and having the following columns:
          axes           : tuple of matplotlib.Axes (primary and secondary) for each column.
          used secondary : bool indicating whether or not the seconday Axes is in use.
          relative size  : height of panel as proportion of sum of all relative sizes

    """

    num_panels   = config['num_panels']
    addplot      = config['addplot']
    volume       = config['volume']
    volume_panel = config['volume_panel']
    num_panels   = config['num_panels']
    main_panel   = config['main_panel']
    panel_ratios = config['panel_ratios']

    if not _valid_panel_id(main_panel):
        raise ValueError('main_panel id must be integer 0 to 31, but is '+str(main_panel))

    if num_panels is None:  # then infer the number of panels:
        pset = {0} # start with a set including only panel zero
        if addplot is not None:
            if isinstance(addplot,dict):
                addplot = [addplot,]   # make list of dict to be consistent
            elif not _list_of_dict(addplot):
                raise TypeError('addplot must be `dict`, or `list of dict`, NOT '+str(type(addplot)))

            backwards_panel_compatibility = {'main':0,'lower':1,'A':0,'B':1,'C':2}

            for apdict in addplot:
                panel = apdict['panel']
                if panel in backwards_panel_compatibility:
                    panel = backwards_panel_compatibility[panel]
                if not _valid_panel_id(panel):
                    raise ValueError('addplot panel must be integer 0 to 31, but is "'+str(panel)+'"')
                pset.add(panel)

        if volume is True:
            if not _valid_panel_id(volume_panel):
                raise ValueError('volume_panel must be integer 0 to 31, but is "'+str(volume_panel)+'"')
            pset.add(volume_panel)

        pset.add(main_panel)

        pset = sorted(pset)
        missing = [m for m in range(len(pset)) if m not in pset]
        if len(missing) != 0:
            raise ValueError('inferred panel list is missing panels: '+str(missing))

    else:
        if not isinstance(num_panels,int) or num_panels < 1 or num_panels > 32:
            raise ValueError('num_panels must be integer 1 to 32, but is "'+str(volume_panel)+'"')
        pset = range(0,num_panels)

    _nones = [None]*len(pset)
    panels = pd.DataFrame(dict(axes=_nones,
                               relsize=_nones,
                               lift=_nones,
                               height=_nones,
                               used2nd=[False]*len(pset),
                               title=_nones,
                               y_on_right=_nones),
                          index=pset)
    panels.index.name = 'panid'

    # Now determine the height for each panel:
    # ( figure, num_panels='infer', addplot=None, volume_panel=None, main_panel=0, panel_ratios=None ):

    if panel_ratios is not None:
        if not isinstance(panel_ratios,(list,tuple)):
            raise TypeError('panel_ratios must be a list or tuple')
        if len(panel_ratios) != len(panels) and not (len(panel_ratios)==2 and len(panels) > 2):
            err  = 'len(panel_ratios) must be 2, or must be same as number of panels'
            err += '\nlen(panel_ratios)='+str(len(panel_ratios))+'  num panels='+str(len(panels))
            raise ValueError(err)
        if len(panel_ratios) == 2 and len(panels) > 2:
            pratios = [panel_ratios[1]]*len(panels)
            pratios[main_panel] = panel_ratios[0]
        else:
            pratios = panel_ratios
    else:
        pratios = [2]*len(panels)
        pratios[main_panel] = 5

    panels['relsize'] = pratios
    #print('len(panels)=',len(panels))
    #print('len(pratios)=',len(pratios))

    #print('pratios=')
    #print(pratios)

    #print('panels=')
    #print(panels)

    # TODO:  Throughout this section, right_pad is intentionally *less* 
    #        than left_pad.  This assumes that the y-axis labels are on
    #        the left, which is true for many mpf_styles, but *not* all.
    #        Ideally need to determine which side has the axis labels.
    #        And keep in mind, if secondary_y is in effect, then both
    #        sides can have axis labels.

    left_pad    = 0.18
    right_pad   = 0.10
    top_pad     = 0.12
    bot_pad     = 0.18

    scale_left = scale_right = scale_top = scale_bot = 1.0

    scale_padding = config['scale_padding']
    if isinstance(scale_padding,dict):
        if 'left'   in scale_padding: scale_left  = scale_padding['left']
        if 'right'  in scale_padding: scale_right = scale_padding['right']
        if 'top'    in scale_padding: scale_top   = scale_padding['top']
        if 'bottom' in scale_padding: scale_bot   = scale_padding['bottom']
    else: # isinstance(scale_padding,(int,float):
        scale_left = scale_right = scale_top = scale_bot = scale_padding
        
    if config['tight_layout']:
        right_pad   *= 0.4
        top_pad     *= 0.4
        scale_left  *= 0.6
        scale_right *= 0.6
        scale_top   *= 0.6
        scale_bot   *= 0.6

    left_pad  *= scale_left
    right_pad *= scale_right
    top_pad   *= scale_top
    bot_pad   *= scale_bot

    plot_height = 1.0 - (bot_pad  + top_pad  )
    plot_width  = 1.0 - (left_pad + right_pad)

    #   print('scale_padding=',scale_padding)
    #   print('left_pad =',left_pad)
    #   print('right_pad=',right_pad)
    #   print('top_pad  =',top_pad)
    #   print('bot_pad  =',bot_pad)
    #   print('plot_height =',plot_height)
    #   print('plot_width  =',plot_width)
        
    psum = sum(pratios)
    for panid,size in enumerate(pratios):
        panels.at[panid,'height'] = plot_height * size / psum

    # Now create the Axes:

    for panid,row in panels.iterrows():
        height = row.height
        lift   = panels['height'].loc[panid+1:].sum()
        panels.at[panid,'lift'] = lift
        if panid == 0:
            # rect = [left, bottom, width, height] 
            ax0 = figure.add_axes( [left_pad, bot_pad+lift, plot_width, height] )
        else:
            ax0 = figure.add_axes( [left_pad, bot_pad+lift, plot_width, height], sharex=panels.at[0,'axes'][0] )
        ax1 = ax0.twinx()
        ax1.grid(False)
        if config['saxbelow']:      # issue#115 issuecomment-639446764
            ax0.set_axisbelow(True) # so grid does not show through plot data on any panel.
        elif panid == volume_panel:
            ax0.set_axisbelow(True) # so grid does not show through volume bars.
        panels.at[panid,'axes'] = (ax0,ax1)

    return panels
    

def _set_ticks_on_bottom_panel_only(panels,formatter,rotation=45,xlabel=None):

    bot = panels.index.values[-1]
    ax  = panels.at[bot,'axes'][0]
    ax.tick_params(axis='x',rotation=rotation)
    ax.xaxis.set_major_formatter(formatter)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if len(panels) == 1: return

    # [::-1] reverses the order of the panel id's
    # [1:] all but the first element, which, since the array
    #      is reversed, means we take all but the LAST panel id.
    # Thus, only the last (bottom) panel id gets tick labels:
    for panid in panels.index.values[::-1][1:]:
        panels.at[panid,'axes'][0].tick_params(axis='x',labelbottom=False)

