""" from https://github.com/mfouesneau/asciiplot
Package that allows you to plot simple graphs in ASCII, a la matplotlib.

This package is a inspired from Imri Goldberg's ASCII-Plotter 1.0
(https://pypi.python.org/pypi/ASCII-Plotter/1.0)

At a time I was enoyed by security not giving me direct access to my computer,
and thus to quickly make figures from python, I looked at how I could make
quick and dirty ASCII figures. But if I were to develop something, I wanted
something that can be used with just python and possible standard-ish packages
(numpy, scipy).

So I came up with this package after many iterations based of ASCII-plotter.
I added the feature to show multiple curves on one plot with different markers.
And I also made the usage, close to matplotlib, such that there is a plot,
hist, hist2d and imshow functions.
"""
import math as _math
import numpy as np


__version__ = 0.9
__author__ = 'M. Fouesneau'

__all__ = ['markers', 'ACanvas', 'AData', 'AFigure',
           'hist', 'hist2d', 'imshow', 'percentile_imshow',
           'plot', 'stem', 'stemify', 'step', 'steppify',
           '__version__', '__author__']


markers = { '-' : u'None' ,     # solid line style
            ',': u'\u2219',     # point marker
            '.': u'\u2218',     # pixel marker
            '.f': u'\u2218',    # pixel marker
            'o': u'\u25CB',     # circle marker
            'of': u'\u25CF',    # circle marker
            'v': u'\u25BD',     # triangle_down marker
            'vf': u'\u25BC',    # filler triangle_down marker
            '^': u'\u25B3',     # triangle_up marker
            '^f': u'\u25B2',    # filled triangle_up marker
            '<':  u'\u25C1',    # triangle_left marker
            '<f': u'\u25C0',    # filled triangle_left marker
            '>': u'\u25B7',     # triangle_right marker
            '>f': u'\u25B6',    # filled triangle_right marker
            's': u'\u25FD',     # square marker
            'sf': u'\u25FC',    # square marker
            '*': u'\u2606',     # star marker
            '*f': u'\u2605',    # star marker
            '+': u'\u271A',     # plus marker
            'x': u'\u274C',     # x marker
            'd':  u'\u25C7',    # diamond marker
            'df':  u'\u25C6'    # filled diamond marker
            }


def _sign(x):
    """ Return the sign of x
    INPUTS
    ------
    x: number
        value to get the sign of

    OUTPUTS
    -------
    s: signed int
        -1, 0 or 1 if negative, null or positive
    """

    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1


def _transpose(mat):
    """ Transpose matrice made of lists
    INPUTS
    ------
    mat: iterable 2d list like

    OUTPUTS
    -------
    r: list of list, 2d list like
        transposed matrice
    """
    r = [ [x[i] for x in mat] for i in range(len(mat[0])) ]
    return r


def _y_reverse(mat):
    """ Reverse the y axis of a 2d list-like
    INPUTS
    ------
    mat: list of lists
        the matrix to reverse on axis 0
    OUTPUTS
    -------
    r: list of lists
        the reversed version
    """
    r = [ list(reversed(mat_i)) for mat_i in mat ]
    return r


class AData(object):
    """ Data container for ascii AFigure """
    def __init__(self, x, y, marker='_.', plot_slope=True):
        """ Constructor
        INPUTS
        ------
        x: iterable
            x values
        y: iterable
            y values

        KEYWORDS
        --------
        marker: str
            marker for the data.
            if None or empty, the curve will be plotted
            if the first character of the marker is '_' then unicode markers will be called:

                marker      repr                description
               ========  ===========   =============================
                '-'       u'None'       solid line style
                ','       u'\u2219'     point marker
                '.'       u'\u2218'     pixel marker
                '.f'      u'\u2218'     pixel marker
                'o'       u'\u25CB'     circle marker
                'of'      u'\u25CF'     circle marker
                'v'       u'\u25BD'     triangle_down marker
                'vf'      u'\u25BC'     filler triangle_down marker
                '^'       u'\u25B3'     triangle_up marker
                '^f'      u'\u25B2'     filled triangle_up marker
                '<'       u'\u25C1'     triangle_left marker
                '<f'      u'\u25C0'     filled triangle_left marker
                '>'       u'\u25B7'     triangle_right marker
                '>f'      u'\u25B6'     filled triangle_right marker
                's'       u'\u25FD'     square marker
                'sf'      u'\u25FC'     square marker
                '*'       u'\u2606'     star marker
                '*f'      u'\u2605'     star marker
                '+'       u'\u271A'     plus marker
                'x'       u'\u274C'     x marker
                'd'       u'\u25C7'     diamond marker
                'df'      u'\u25C6'     filled diamond marker

        plot_slope: bool
            if set, the curve will be plotted
        """
        self.x = x
        self.y = y
        self.plot_slope = plot_slope
        self.set_marker(marker)

    def set_marker(self, marker):
        """ set the marker of the data
        INPUTS
        ------
        marker: str
            marker for the data.
            see constructor for marker descriptions
        """
        if marker in [None, 'None', u'None', '']:
            self.plot_slope = True
            self.marker = ''
        elif marker[0] == '_':
            self.marker = markers[marker[1:]]
        else:
            self.marker = marker

    def extent(self):
        """ return the extention of the data
        OUPUTS
        ------
        e: list
           [ min(x), max(x), min(y), max(y) ]
        """
        return [min(self.x), max(self.x), min(self.y), max(self.y)]

    def __repr__(self):
        s = 'AData: %s\n' % object.__repr__(self)
        return s


class ACanvas(object):
    """ Canvas of a AFigure instance. A Canvas handles all transformations
    between data space and figure space accounting for scaling and pixels

    In general there is no need to access the canvas directly
    """
    def __init__(self, shape=None, margins=None, xlim=None, ylim=None):
        """ Constructor
        KEYWORDS
        --------
        shape: tuple of 2 ints
            shape of the canvas in number of characters: (width, height)

        margins: tuple of 2 floats
            fractional margins

        xlim: tuple of 2 floats
            limits of the xaxis

        ylim: tuple of 2 floats
            limits of the yaxis
        """
        self.shape = shape or (50, 20)
        self.margins = margins or (0.05, 0.1)
        self._xlim = xlim or [0, 1]
        self._ylim = ylim or [0, 1]
        self.auto_adjust = True
        self.margin_factor = 1

    @property
    def x_size(self):
        """ return the width """
        return self.shape[0]

    @property
    def y_size(self):
        """ return the height """
        return self.shape[1]

    @property
    def x_margin(self):
        """ return the margin in x """
        return self.margins[0]

    @property
    def y_margin(self):
        """ return the margin in y """
        return self.margins[1]

    def xlim(self, vmin=None, vmax=None):
        """
        Get or set the *x* limits of the current axes.

        KEYWORDS
        --------
        vmin: float
            lower limit
        vmax: float
            upper limit

        xmin, xmax = xlim()   # return the current xlim
        xlim( (xmin, xmax) )  # set the xlim to xmin, xmax
        xlim( xmin, xmax )    # set the xlim to xmin, xmax
        """
        if vmin is None and vmax is None:
            return self._xlim
        elif hasattr(vmin, '__iter__'):
            self._xlim = vmin[:2]
        else:
            self._xlim = [vmin, vmax]
        if self._xlim[0] == self._xlim[1]:
            self._xlim[1] += 1

        self._xlim[0] -= self.x_mod
        self._xlim[1] += self.x_mod

    def ylim(self, vmin=None, vmax=None):
        """
        Get or set the *y* limits of the current axes.

        KEYWORDS
        --------
        vmin: float
            lower limit
        vmax: float
            upper limit

        ymin, ymax = ylim()   # return the current xlim
        ylim( (ymin, ymax) )  # set the xlim to xmin, xmax
        ylim( ymin, ymax )    # set the xlim to xmin, xmax
        """
        if vmin is None and vmax is None:
            return self._ylim
        elif hasattr(vmin, '__iter__'):
            self._ylim = vmin[:2]
        else:
            self._ylim = [vmin, vmax]
        if self._ylim[0] == self._ylim[1]:
            self._ylim[1] += 1

        self._ylim[0] -= self.y_mod
        self._ylim[1] += self.y_mod

    @property
    def min_x(self):
        """ return the lower x limit """
        return self._xlim[0]

    @property
    def max_x(self):
        """ return the upper x limit """
        return self._xlim[1]

    @property
    def min_y(self):
        """ return the lower y limit """
        return self._ylim[0]

    @property
    def max_y(self):
        """ return the upper y limit """
        return self._ylim[1]

    @property
    def x_step(self):
        return float(self.max_x - self.min_x) / float(self.x_size)

    @property
    def y_step(self):
        return float(self.max_y - self.min_y) / float(self.y_size)

    @property
    def ratio(self):
        return self.y_step / self.x_step

    @property
    def x_mod(self):
        return (self.max_x - self.min_x) * self.x_margin

    @property
    def y_mod(self):
        return (self.max_y - self.min_y) * self.y_margin

    def extent(self, margin_factor=None):
        margin_factor = margin_factor or self.margin_factor
        min_x = (self.min_x + self.x_mod * margin_factor)
        max_x = (self.max_x - self.x_mod * margin_factor)
        min_y = (self.min_y + self.y_mod * margin_factor)
        max_y = (self.max_y - self.y_mod * margin_factor)
        return (min_x, max_x, min_y, max_y)

    def extent_str(self, margin=None):

        def transform(val, fmt):
            if abs(val) < 1:
                _str = "%+.2g" % val
            elif fmt is not None:
                _str = fmt % val
            else:
                _str = None
            return _str

        e = self.extent(margin)

        xfmt = self.x_str()
        yfmt = self.y_str()
        return transform(e[0], xfmt), transform(e[1], xfmt), transform(e[2], yfmt), transform(e[3], yfmt)

    def x_str(self):
        if self.x_size < 16:
            x_str = None
        elif self.x_size < 23:
            x_str = "%+.2g"
        else:
            x_str = "%+g"
        return x_str

    def y_str(self):
        if self.x_size < 8:
            y_str = None
        elif self.x_size < 11:
            y_str = "%+.2g"
        else:
            y_str = "%+g"
        return y_str

    def coords_inside_buffer(self, x, y):
        return (0 <= x < self.x_size) and (0 < y < self.y_size)

    def coords_inside_data(self, x, y):
        """ return if (x,y) covered by the data box
        x, y: float
            coordinates to test
        """
        return (self.min_x <= x < self.max_x) and (self.min_y <= y < self.max_y)

    def _clip_line(self, line_pt_1, line_pt_2):
        """ clip a line to the canvas """

        e = self.extent()
        x_min = min(line_pt_1[0], line_pt_2[0])
        x_max = max(line_pt_1[0], line_pt_2[0])
        y_min = min(line_pt_1[1], line_pt_2[1])
        y_max = max(line_pt_1[1], line_pt_2[1])

        if line_pt_1[0] == line_pt_2[0]:
            return ( ( line_pt_1[0], max(y_min, e[1]) ),
                     ( line_pt_1[0], min(y_max, e[3])   ))

        if line_pt_1[1] == line_pt_2[1]:
            return ( ( max(x_min, e[0]), line_pt_1[1] ),
                     ( min(x_max, e[2]), line_pt_1[1]   ))

        if ( (e[0] <= line_pt_1[0] < e[2]) and
                (e[1] <= line_pt_1[1] < e[3]) and
                (e[0] <= line_pt_2[0] < e[2]) and
                (e[1] <= line_pt_2[1] < e[3]) ):
            return line_pt_1, line_pt_2

        ts = [0.0,
              1.0,
              float(e[0] - line_pt_1[0]) / (line_pt_2[0] - line_pt_1[0]),
              float(e[2] - line_pt_1[0]) / (line_pt_2[0] - line_pt_1[0]),
              float(e[1] - line_pt_1[1]) / (line_pt_2[1] - line_pt_1[1]),
              float(e[3] - line_pt_1[1]) / (line_pt_2[1] - line_pt_1[1])
              ]
        ts.sort()

        if (ts[2] < 0) or (ts[2] >= 1) or (ts[3] < 0) or (ts[2] >= 1):
            return None

        result = [(pt_1 + t * (pt_2 - pt_1)) for t in (ts[2], ts[3]) for (pt_1, pt_2) in zip(line_pt_1, line_pt_2)]

        return ( result[:2], result[2:] )


class AFigure(object):

    def __init__(self, shape=(80, 20), margins=(0.05, 0.1), draw_axes=True, newline='\n',
                 plot_labels=True, xlim=None, ylim=None, **kwargs):

        self.canvas = ACanvas(shape, margins=margins, xlim=xlim, ylim=ylim)
        self.draw_axes = draw_axes
        self.new_line = newline
        self.plot_labels = plot_labels
        self.output_buffer = None
        self.tickSymbols = u'\u253C'  # "+"
        self.x_axis_symbol = u'\u2500'  # u"\u23bc"  # "-"
        self.y_axis_symbol = u'\u2502'  # "|"
        self.data = []

    def xlim(self, vmin=None, vmax=None):
        return self.canvas.xlim(vmin, vmax)

    def ylim(self, vmin=None, vmax=None):
        return self.canvas.ylim(vmin, vmax)

    def get_coord(self, val, min, step, limits=None):
        result = int((val - min) / step)
        if limits is not None:
            if result <= limits[0]:
                result = limits[0]
            elif result >= limits[1]:
                result = limits[1] - 1
        return result

    def _draw_axes(self):
        zero_x = self.get_coord(0, self.canvas.min_x, self.canvas.x_step, limits=[1, self.canvas.x_size])
        if zero_x >= self.canvas.x_size:
            zero_x = self.canvas.x_size - 1
        for y in range(self.canvas.y_size):
            self.output_buffer[zero_x][y] = self.y_axis_symbol

        zero_y = self.get_coord(0, self.canvas.min_y, self.canvas.y_step, limits=[1, self.canvas.y_size])
        if zero_y >= self.canvas.y_size:
            zero_y = self.canvas.y_size - 1
        for x in range(self.canvas.x_size):
            self.output_buffer[x][zero_y] = self.x_axis_symbol  # u'\u23bc'

        self.output_buffer[zero_x][zero_y] = self.tickSymbols  # "+"

    def _get_symbol_by_slope(self, slope, default_symbol):
        """ Return a line oriented directed approximatively along the slope value """
        if slope > _math.tan(3 * _math.pi / 8):
            draw_symbol = "|"
        elif _math.tan(_math.pi / 8) < slope < _math.tan(3 * _math.pi / 8):
            draw_symbol = u'\u27cb'  # "/"
        elif abs(slope) < _math.tan(_math.pi / 8):
            draw_symbol = "-"
        elif slope < _math.tan(-_math.pi / 8) and slope > _math.tan(-3 * _math.pi / 8):
            draw_symbol = u'\u27CD'  # "\\"
        elif slope < _math.tan(-3 * _math.pi / 8):
            draw_symbol = "|"
        else:
            draw_symbol = default_symbol
        return draw_symbol

    def _plot_labels(self):

        if self.canvas.y_size < 2:
            return

        act_min_x, act_max_x, act_min_y, act_max_y = self.canvas.extent()

        min_x_coord = self.get_coord(act_min_x, self.canvas.min_x, self.canvas.x_step, limits=[0, self.canvas.x_size])
        max_x_coord = self.get_coord(act_max_x, self.canvas.min_x, self.canvas.x_step, limits=[0, self.canvas.x_size])
        min_y_coord = self.get_coord(act_min_y, self.canvas.min_y, self.canvas.y_step, limits=[1, self.canvas.y_size])
        max_y_coord = self.get_coord(act_max_y, self.canvas.min_y, self.canvas.y_step, limits=[1, self.canvas.y_size])

        x_zero_coord = self.get_coord(0, self.canvas.min_x, self.canvas.x_step, limits=[0, self.canvas.x_size])
        y_zero_coord = self.get_coord(0, self.canvas.min_y, self.canvas.y_step, limits=[1, self.canvas.y_size])

        self.output_buffer[x_zero_coord][min_y_coord] = self.tickSymbols
        self.output_buffer[x_zero_coord][max_y_coord] = self.tickSymbols
        self.output_buffer[min_x_coord][y_zero_coord] = self.tickSymbols
        self.output_buffer[max_x_coord][y_zero_coord] = self.tickSymbols

        min_x_str, max_x_str, min_y_str, max_y_str = self.canvas.extent_str()
        if (self.canvas.x_str() is not None):
            for i, c in enumerate(min_x_str):
                self.output_buffer[min_x_coord + i + 1][y_zero_coord - 1] = c
            for i, c in enumerate(max_x_str):
                self.output_buffer[max_x_coord + i - len(max_x_str)][y_zero_coord - 1] = c

        if (self.canvas.y_str() is not None):
            for i, c in enumerate(max_y_str):
                self.output_buffer[x_zero_coord + i + 1][max_y_coord] = c
            for i, c in enumerate(min_y_str):
                self.output_buffer[x_zero_coord + i + 1][min_y_coord] = c

    def _plot_line(self, start, end, data):
        """ plot a line from start = (x0, y0) to end = (x1, y1) """

        clipped_line = self.canvas._clip_line(start, end)

        if clipped_line is None:
            return False

        start, end = clipped_line

        x0 = self.get_coord(start[0], self.canvas.min_x, self.canvas.x_step)
        y0 = self.get_coord(start[1], self.canvas.min_y, self.canvas.y_step)
        x1 = self.get_coord(end[0], self.canvas.min_x, self.canvas.x_step)
        y1 = self.get_coord(end[1], self.canvas.min_y, self.canvas.y_step)

        if (x0, y0) == (x1, y1):
            return True

        #x_zero_coord = self.get_coord(0, self.canvas.min_x, self.canvas.x_step)
        y_zero_coord = self.get_coord(0, self.canvas.min_y, self.canvas.y_step, limits=[1, self.canvas.y_size])

        if start[0] - end[0] == 0:
            draw_symbol = u"|"
        elif start[1] - end[1] == 0:
            draw_symbol = '-'
        else:
            slope = (1.0 / self.canvas.ratio) * (end[1] - start[1]) / (end[0] - start[0])
            draw_symbol = self._get_symbol_by_slope(slope, data.marker)

        dx = x1 - x0
        dy = y1 - y0
        if abs(dx) > abs(dy):
            s = _sign(dx)
            slope = float(dy) / dx
            for i in range(0, abs(int(dx))):
                cur_draw_symbol = draw_symbol
                x = i * s
                cur_y = int(y0 + slope * x)
                if (self.draw_axes) and (cur_y == y_zero_coord) and (draw_symbol == self.x_axis_symbol):
                    cur_draw_symbol = "-"
                self.output_buffer[x0 + x][cur_y] = cur_draw_symbol
        else:
            s = _sign(dy)
            slope = float(dx) / dy
            for i in range(0, abs(int(dy))):
                y = i * s
                cur_draw_symbol = draw_symbol
                cur_y = y0 + y
                if (self.draw_axes) and (cur_y == y_zero_coord) and (draw_symbol == self.x_axis_symbol):
                    cur_draw_symbol = "-"
                self.output_buffer[int(x0 + slope * y)][cur_y] = cur_draw_symbol

        return False

    def _plot_data_with_slope(self, data):
        xy = list(zip(data.x, data.y))

        #sort according to the x coord
        xy.sort(key=lambda c: c[0])
        prev_p = xy[0]
        e_xy = enumerate(xy)
        e_xy.next()
        for i, (xi, yi) in e_xy:
            line = self._plot_line(prev_p, (xi, yi), data)
            prev_p = (xi, yi)

            # if no line, then symbol
            if not line & self.canvas.coords_inside_data(xi, yi):
                draw_symbol = data.marker

                px, py = xy[i - 1]
                nx, ny = xy[i]

                if abs(nx - px) > 0.000001:
                    slope = (1.0 / self.canvas.ratio) * (ny - py) / (nx - px)
                    draw_symbol = self._get_symbol_by_slope(slope, draw_symbol)

                x_coord = self.get_coord(xi, self.canvas.min_x, self.canvas.x_step)
                y_coord = self.get_coord(yi, self.canvas.min_y, self.canvas.y_step)

                if self.canvas.coords_inside_buffer(x_coord, y_coord):
                    y0_coord = self.get_coord(0, self.canvas.min_y, self.canvas.y_step)
                    if self.draw_axes:
                        if (y_coord == y0_coord) and (draw_symbol == u"\u23bc"):
                            draw_symbol = "="
                    self.output_buffer[x_coord][y_coord] = draw_symbol

    def _plot_data(self, data):
        if data.plot_slope:
            self._plot_data_with_slope(data)
        else:
            for x, y in zip(data.x, data.y):
                if self.canvas.coords_inside_data(x, y):
                    x_coord = self.get_coord(x, self.canvas.min_x, self.canvas.x_step)
                    y_coord = self.get_coord(y, self.canvas.min_y, self.canvas.y_step)

                    if self.canvas.coords_inside_buffer(x_coord, y_coord):
                        self.output_buffer[x_coord][y_coord] = data.marker

    def auto_limits(self):
        if self.canvas.auto_adjust is True:
            min_x = 0.
            max_x = 0.
            min_y = 0.
            max_y = 0.
            for dk in self.data:
                ek = dk.extent()
                min_x = min(min_x, min(ek[:2]))
                min_y = min(min_y, min(ek[2:]))
                max_x = max(max_x, max(ek[:2]))
                max_y = max(max_y, max(ek[2:]))
            self.canvas.xlim(min_x, max_x)
            self.canvas.ylim(min_y, max_y)

    def append_data(self, data):
        self.data.append(data)
        self.auto_limits()

    def plot(self, x_seq, y_seq=None, marker=None, plot_slope=False, xlim=None, ylim=None):

        if y_seq is None:
            y_seq = x_seq[:]
            x_seq = range(len(y_seq))

        data = AData(x_seq, y_seq, marker=marker, plot_slope=plot_slope)
        self.append_data(data)

        if xlim is not None:
            self.canvas.xlim(xlim)

        if ylim is not None:
            self.canvas.ylim(ylim)

        return self.draw()

    def draw(self):
        self.output_buffer = [[" "] * self.canvas.y_size for i in range(self.canvas.x_size)]
        if self.draw_axes:
            self._draw_axes()

        for dk in self.data:
            self._plot_data(dk)

        if self.plot_labels:
            self._plot_labels()
        trans_result = _transpose(_y_reverse(self.output_buffer))
        result = self.new_line.join(["".join(row) for row in trans_result])
        return result


def plot(x, y=None, marker=None, shape=(50, 20), draw_axes=True,
         newline='\n', plot_slope=False, x_margin=0.05,
         y_margin=0.1, plot_labels=True, xlim=None, ylim=None):

    flags = {'shape': shape,
             'draw_axes': draw_axes,
             'newline': newline,
             'marker': marker,
             'plot_slope': plot_slope,
             'margins': (x_margin, y_margin),
             'plot_labels': plot_labels }

    p = AFigure(**flags)

    print(p.plot(x, y, marker=marker, plot_slope=plot_slope))


def steppify(x, y):
    """ Steppify a curve (x,y). Useful for manually filling histograms """
    dx = 0.5 * (x[1:] + x[:-1])
    xx = np.zeros( 2 * len(dx), dtype=float)
    yy = np.zeros( 2 * len(y), dtype=float)
    xx[0::2], xx[1::2] = dx, dx
    yy[0::2], yy[1::2] = y, y
    xx = np.concatenate(([x[0] - (dx[0] - x[0])], xx, [x[-1] + (x[-1] - dx[-1])]))
    return xx, yy


def stemify(x, y):
    """ Steppify a curve (x,y). Useful for manually filling histograms """
    xx = np.zeros( 3 * len(x), dtype=float)
    yy = np.zeros( 3 * len(y), dtype=float)
    xx[0::3], xx[1::3], xx[2::3] = x, x, x
    yy[1::3] = y
    return xx, yy


def hist(x, bins=10, normed=False, weights=None, density=None, histtype='stem',
         shape=(50, 20), draw_axes=True, newline='\n',
         marker='_.', plot_slope=False, x_margin=0.05,
         y_margin=0.1, plot_labels=True, xlim=None, ylim=None ):

    from numpy import histogram

    if histtype not in ['None', 'stem', 'step']:
        raise ValueError('histtype must be in [None, stem, step]')

    n, b = histogram(x, bins=bins, range=xlim, normed=normed, weights=weights, density=density)

    _x = 0.5 * ( b[:-1] + b[1:] )
    if histtype == 'step':
        step(_x, n.astype(float))
    elif histtype == 'stem':
        stem(_x, n.astype(float))
    else:
        _y = n.astype(float)
        plot(_x, _y, shape=shape, draw_axes=draw_axes, newline=newline, marker=marker,
             plot_slope=plot_slope, x_margin=x_margin, y_margin=y_margin,
             plot_labels=plot_labels, xlim=xlim, ylim=ylim)


def step(x, y, shape=(50, 20), draw_axes=True,
         newline='\n', marker='_.', plot_slope=True, x_margin=0.05,
         y_margin=0.1, plot_labels=True, xlim=None, ylim=None ):

    _x, _y = steppify(x, y)
    plot(_x, _y, shape=shape, draw_axes=draw_axes, newline=newline, marker=marker,
         plot_slope=plot_slope, x_margin=x_margin, y_margin=y_margin,
         plot_labels=plot_labels, xlim=xlim, ylim=ylim)


def stem(x, y, shape=(50, 20), draw_axes=True,
         newline='\n', marker='_.', plot_slope=True, x_margin=0.05,
         y_margin=0.1, plot_labels=True, xlim=None, ylim=None ):

    _x, _y = stemify(x, y)
    plot(_x, _y, shape=shape, draw_axes=draw_axes, newline=newline, marker=marker,
         plot_slope=plot_slope, x_margin=x_margin, y_margin=y_margin,
         plot_labels=plot_labels, xlim=xlim, ylim=ylim)


def hist2d(x, y, bins=[50, 20], range=None, normed=False, weights=None, ncolors=16,
           width=50, percentiles=None):

    im, ex, ey = np.histogram2d(x, y, bins, range=None, normed=normed, weights=weights)

    if percentiles is None:
        imshow(im, extent=[min(ex), max(ex), min(ey), max(ey)],
               ncolors=ncolors, width=width)
    else:
        percentile_imshow(im, levels=percentiles, extent=None,
                          width=width, ncolors=width)


def percentile_imshow(im, levels=[68, 95, 99], extent=None, width=50, ncolors=16):
    _im = im.astype(float)
    _im -= im.min()
    _im /= _im.max()

    n = len(levels)
    for e, lk in enumerate(sorted(levels)):
        _im[ _im <= 0.01 * float(lk) ] = n - e

    imshow(1. - _im, extent=None, width=width, ncolors=ncolors)


def imshow(im, extent=None, width=50, ncolors=16):
    from scipy import ndimage

    width0 = im.shape[0]
    _im = ndimage.zoom(im.astype(float), float(width) / float(width0) )

    _im -= im.min()
    _im /= _im.max()

    width, height = _im.shape[:2]

    if len(im.shape) > 2:
        _clr = True
    else:
        _clr = False

    if ncolors == 16:
        color = "MNHQ$OC?7>!:-;. "[::-1]
    else:
        color = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''[::-1]
    ncolors = len(color)

    string = ""
    if not _clr:
        for h in range(height):  # first go through the height,  otherwise will roate
            for w in range(width):
                string += color[int(_im[w, h] * (ncolors - 1) )]
            string += "\n"
    else:
        for h in range(height):  # first go through the height,  otherwise will roate
            for w in range(width):
                string += color[int(sum(_im[w, h]) * (ncolors - 1) )]
            string += "\n"
    print(string)
