# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for constructing and displaying figures."""

from plotly.graph_objects import Figure as _Figure, FigureWidget as _FigureWidget
from plotly.subplots import make_subplots as _make_subplots

from vectorbt import _typing as tp
from vectorbt.utils.config import merge_dicts


def get_domain(ref: str, fig: tp.BaseFigure) -> tp.Tuple[int, int]:
    """Get domain of a coordinate axis."""
    axis = ref[0] + 'axis' + ref[1:]
    if axis in fig.layout:
        if 'domain' in fig.layout[axis]:
            if fig.layout[axis]['domain'] is not None:
                return fig.layout[axis]['domain']
    return 0, 1


class FigureMixin:
    def show(self, *args, **kwargs) -> None:
        """Display the figure in PNG format."""
        raise NotImplementedError

    def show_png(self, **kwargs) -> None:
        """Display the figure in PNG format."""
        self.show(renderer="png", **kwargs)

    def show_svg(self, **kwargs) -> None:
        """Display the figure in SVG format."""
        self.show(renderer="svg", **kwargs)


class Figure(_Figure, FigureMixin):
    """Figure."""

    def __init__(self, *args, **kwargs) -> None:
        """Extends `plotly.graph_objects.Figure`."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        layout = kwargs.pop('layout', {})
        super().__init__(*args, **kwargs)
        self.update_layout(**merge_dicts(plotting_cfg['layout'], layout))

    def show(self, *args, **kwargs) -> None:
        """Show the figure."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        fig_kwargs = dict(width=self.layout.width, height=self.layout.height)
        show_kwargs = merge_dicts(fig_kwargs, plotting_cfg['show_kwargs'], kwargs)
        _Figure.show(self, *args, **show_kwargs)


class FigureWidget(_FigureWidget, FigureMixin):
    """Figure widget."""

    def __init__(self, *args, **kwargs) -> None:
        """Extends `plotly.graph_objects.FigureWidget`."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        layout = kwargs.pop('layout', {})
        super().__init__(*args, **kwargs)
        self.update_layout(**merge_dicts(plotting_cfg['layout'], layout))

    def show(self, *args, **kwargs) -> None:
        """Show the figure."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        fig_kwargs = dict(width=self.layout.width, height=self.layout.height)
        show_kwargs = merge_dicts(fig_kwargs, plotting_cfg['show_kwargs'], kwargs)
        _Figure.show(self, *args, **show_kwargs)


def make_figure(*args, **kwargs) -> tp.BaseFigure:
    """Make new figure.

    Returns either `Figure` or `FigureWidget`, depending on `use_widgets`
    defined under `plotting` in `vectorbt._settings.settings`."""
    from vectorbt._settings import settings
    plotting_cfg = settings['plotting']

    if plotting_cfg['use_widgets']:
        return FigureWidget(*args, **kwargs)
    return Figure(*args, **kwargs)


def make_subplots(*args, **kwargs) -> tp.BaseFigure:
    """Makes subplots and passes them to `FigureWidget`."""
    return make_figure(_make_subplots(*args, **kwargs))
