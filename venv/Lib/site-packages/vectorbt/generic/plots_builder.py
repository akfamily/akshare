# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Mixin for building plots out of subplots."""

import inspect
import string
import warnings
from collections import Counter

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import Wrapping
from vectorbt.utils import checks
from vectorbt.utils.attr_ import get_dict_attr
from vectorbt.utils.config import Config, merge_dicts, get_func_arg_names
from vectorbt.utils.figure import make_subplots, get_domain
from vectorbt.utils.tags import match_tags
from vectorbt.utils.template import deep_substitute


class MetaPlotsBuilderMixin(type):
    """Meta class that exposes a read-only class property `PlotsBuilderMixin.subplots`."""

    @property
    def subplots(cls) -> Config:
        """Subplots supported by `PlotsBuilderMixin.plots`."""
        return cls._subplots


class PlotsBuilderMixin(metaclass=MetaPlotsBuilderMixin):
    """Mixin that implements `PlotsBuilderMixin.plots`.

    Required to be a subclass of `vectorbt.base.array_wrapper.Wrapping`."""

    def __init__(self):
        checks.assert_instance_of(self, Wrapping)

        # Copy writeable attrs
        self._subplots = self.__class__._subplots.copy()

    @property
    def writeable_attrs(self) -> tp.Set[str]:
        """Set of writeable attributes that will be saved/copied along with the config."""
        return {'_subplots'}

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `PlotsBuilderMixin.plots`.

        See `plots_builder` in `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        plots_builder_cfg = settings['plots_builder']

        return merge_dicts(
            plots_builder_cfg,
            dict(settings=dict(freq=self.wrapper.freq))
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        """Subplots supported by `${cls_name}`.

        ```json
        ${subplots}
        ```

        Returns `${cls_name}._subplots`, which gets (deep) copied upon creation of each instance.
        Thus, changing this config won't affect the class.

        To change subplots, you can either change the config in-place, override this property,
        or overwrite the instance variable `${cls_name}._subplots`."""
        return self._subplots

    def plots(self,
              subplots: tp.Optional[tp.MaybeIterable[tp.Union[str, tp.Tuple[str, tp.Kwargs]]]] = None,
              tags: tp.Optional[tp.MaybeIterable[str]] = None,
              column: tp.Optional[tp.Label] = None,
              group_by: tp.GroupByLike = None,
              silence_warnings: tp.Optional[bool] = None,
              template_mapping: tp.Optional[tp.Mapping] = None,
              settings: tp.KwargsLike = None,
              filters: tp.KwargsLike = None,
              subplot_settings: tp.KwargsLike = None,
              show_titles: bool = None,
              hide_id_labels: bool = None,
              group_id_labels: bool = None,
              make_subplots_kwargs: tp.KwargsLike = None,
              **layout_kwargs) -> tp.Optional[tp.BaseFigure]:
        """Plot various parts of this object.

        Args:
            subplots (str, tuple, iterable, or dict): Subplots to plot.

                Each element can be either:

                * a subplot name (see keys in `PlotsBuilderMixin.subplots`)
                * a tuple of a subplot name and a settings dict as in `PlotsBuilderMixin.subplots`.

                The settings dict can contain the following keys:

                * `title`: Title of the subplot. Defaults to the name.
                * `plot_func` (required): Plotting function for custom subplots.
                    Should write the supplied figure `fig` in-place and can return anything (it won't be used).
                * `xaxis_kwargs`: Layout keyword arguments for the x-axis. Defaults to `dict(title='Index')`.
                * `yaxis_kwargs`: Layout keyword arguments for the y-axis. Defaults to empty dict.
                * `tags`, `check_{filter}`, `inv_check_{filter}`, `resolve_plot_func`, `pass_{arg}`,
                    `resolve_path_{arg}`, `resolve_{arg}` and `template_mapping`:
                    The same as in `vectorbt.generic.stats_builder.StatsBuilderMixin` for `calc_func`.
                * Any other keyword argument that overrides the settings or is passed directly to `plot_func`.

                If `resolve_plot_func` is True, the plotting function may "request" any of the
                following arguments by accepting them or if `pass_{arg}` was found in the settings dict:

                * Each of `vectorbt.utils.attr_.AttrResolver.self_aliases`: original object
                    (ungrouped, with no column selected)
                * `group_by`: won't be passed if it was used in resolving the first attribute of `plot_func`
                    specified as a path, use `pass_group_by=True` to pass anyway
                * `column`
                * `subplot_name`
                * `trace_names`: list with the subplot name, can't be used in templates
                * `add_trace_kwargs`: dict with subplot row and column index
                * `xref`
                * `yref`
                * `xaxis`
                * `yaxis`
                * `x_domain`
                * `y_domain`
                * `fig`
                * `silence_warnings`
                * Any argument from `settings`
                * Any attribute of this object if it meant to be resolved
                    (see `vectorbt.utils.attr_.AttrResolver.resolve_attr`)

                !!! note
                    Layout-related resolution arguments such as `add_trace_kwargs` are unavailable
                    before filtering and thus cannot be used in any templates but can still be overridden.

                Pass `subplots='all'` to plot all supported subplots.
            tags (str or iterable): See `tags` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            column (str): See `column` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            group_by (any): See `group_by` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            silence_warnings (bool): See `silence_warnings` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            template_mapping (mapping): See `template_mapping` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.

                Applied on `settings`, `make_subplots_kwargs`, and `layout_kwargs`, and then on each subplot settings.
            filters (dict): See `filters` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            settings (dict): See `settings` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            subplot_settings (dict): See `metric_settings` in `vectorbt.generic.stats_builder.StatsBuilderMixin`.
            show_titles (bool): Whether to show the title of each subplot.
            hide_id_labels (bool): Whether to hide identical legend labels.

                Two labels are identical if their name, marker style and line style match.
            group_id_labels (bool): Whether to group identical legend labels.
            make_subplots_kwargs (dict): Keyword arguments passed to `plotly.subplots.make_subplots`.
            **layout_kwargs: Keyword arguments used to update the layout of the figure.

        !!! note
            `PlotsBuilderMixin` and `vectorbt.generic.stats_builder.StatsBuilderMixin` are very similar.
            Some artifacts follow the same concept, just named differently:

            * `plots_defaults` vs `stats_defaults`
            * `subplots` vs `metrics`
            * `subplot_settings` vs `metric_settings`

            See further notes under `vectorbt.generic.stats_builder.StatsBuilderMixin`.

        Usage:
            See `vectorbt.portfolio.base` for examples.
        """
        from vectorbt._settings import settings as _settings
        plotting_cfg = _settings['plotting']

        # Resolve defaults
        if silence_warnings is None:
            silence_warnings = self.plots_defaults['silence_warnings']
        if show_titles is None:
            show_titles = self.plots_defaults['show_titles']
        if hide_id_labels is None:
            hide_id_labels = self.plots_defaults['hide_id_labels']
        if group_id_labels is None:
            group_id_labels = self.plots_defaults['group_id_labels']
        template_mapping = merge_dicts(self.plots_defaults['template_mapping'], template_mapping)
        filters = merge_dicts(self.plots_defaults['filters'], filters)
        settings = merge_dicts(self.plots_defaults['settings'], settings)
        subplot_settings = merge_dicts(self.plots_defaults['subplot_settings'], subplot_settings)
        make_subplots_kwargs = merge_dicts(self.plots_defaults['make_subplots_kwargs'], make_subplots_kwargs)
        layout_kwargs = merge_dicts(self.plots_defaults['layout_kwargs'], layout_kwargs)

        # Replace templates globally (not used at subplot level)
        if len(template_mapping) > 0:
            sub_settings = deep_substitute(settings, mapping=template_mapping)
            sub_make_subplots_kwargs = deep_substitute(make_subplots_kwargs, mapping=template_mapping)
            sub_layout_kwargs = deep_substitute(layout_kwargs, mapping=template_mapping)
        else:
            sub_settings = settings
            sub_make_subplots_kwargs = make_subplots_kwargs
            sub_layout_kwargs = layout_kwargs

        # Resolve self
        reself = self.resolve_self(
            cond_kwargs=sub_settings,
            impacts_caching=False,
            silence_warnings=silence_warnings
        )

        # Prepare subplots
        if subplots is None:
            subplots = reself.plots_defaults['subplots']
        if subplots == 'all':
            subplots = reself.subplots
        if isinstance(subplots, dict):
            subplots = list(subplots.items())
        if isinstance(subplots, (str, tuple)):
            subplots = [subplots]

        # Prepare tags
        if tags is None:
            tags = reself.plots_defaults['tags']
        if isinstance(tags, str) and tags == 'all':
            tags = None
        if isinstance(tags, (str, tuple)):
            tags = [tags]

        # Bring to the same shape
        new_subplots = []
        for i, subplot in enumerate(subplots):
            if isinstance(subplot, str):
                subplot = (subplot, reself.subplots[subplot])
            if not isinstance(subplot, tuple):
                raise TypeError(f"Subplot at index {i} must be either a string or a tuple")
            new_subplots.append(subplot)
        subplots = new_subplots

        # Handle duplicate names
        subplot_counts = Counter(list(map(lambda x: x[0], subplots)))
        subplot_i = {k: -1 for k in subplot_counts.keys()}
        subplots_dct = {}
        for i, (subplot_name, _subplot_settings) in enumerate(subplots):
            if subplot_counts[subplot_name] > 1:
                subplot_i[subplot_name] += 1
                subplot_name = subplot_name + '_' + str(subplot_i[subplot_name])
            subplots_dct[subplot_name] = _subplot_settings

        # Check subplot_settings
        missed_keys = set(subplot_settings.keys()).difference(set(subplots_dct.keys()))
        if len(missed_keys) > 0:
            raise ValueError(f"Keys {missed_keys} in subplot_settings could not be matched with any subplot")

        # Merge settings
        opt_arg_names_dct = {}
        custom_arg_names_dct = {}
        resolved_self_dct = {}
        mapping_dct = {}
        for subplot_name, _subplot_settings in list(subplots_dct.items()):
            opt_settings = merge_dicts(
                {name: reself for name in reself.self_aliases},
                dict(
                    column=column,
                    group_by=group_by,
                    subplot_name=subplot_name,
                    trace_names=[subplot_name],
                    silence_warnings=silence_warnings
                ),
                settings
            )
            _subplot_settings = _subplot_settings.copy()
            passed_subplot_settings = subplot_settings.get(subplot_name, {})
            merged_settings = merge_dicts(
                opt_settings,
                _subplot_settings,
                passed_subplot_settings
            )
            subplot_template_mapping = merged_settings.pop('template_mapping', {})
            template_mapping_merged = merge_dicts(template_mapping, subplot_template_mapping)
            template_mapping_merged = deep_substitute(template_mapping_merged, mapping=merged_settings)
            mapping = merge_dicts(template_mapping_merged, merged_settings)
            # safe because we will use deep_substitute again once layout params are known
            merged_settings = deep_substitute(merged_settings, mapping=mapping, safe=True)

            # Filter by tag
            if tags is not None:
                in_tags = merged_settings.get('tags', None)
                if in_tags is None or not match_tags(tags, in_tags):
                    subplots_dct.pop(subplot_name, None)
                    continue

            custom_arg_names = set(_subplot_settings.keys()).union(set(passed_subplot_settings.keys()))
            opt_arg_names = set(opt_settings.keys())
            custom_reself = reself.resolve_self(
                cond_kwargs=merged_settings,
                custom_arg_names=custom_arg_names,
                impacts_caching=True,
                silence_warnings=merged_settings['silence_warnings']
            )

            subplots_dct[subplot_name] = merged_settings
            custom_arg_names_dct[subplot_name] = custom_arg_names
            opt_arg_names_dct[subplot_name] = opt_arg_names
            resolved_self_dct[subplot_name] = custom_reself
            mapping_dct[subplot_name] = mapping

        # Filter subplots
        for subplot_name, _subplot_settings in list(subplots_dct.items()):
            custom_reself = resolved_self_dct[subplot_name]
            mapping = mapping_dct[subplot_name]
            _silence_warnings = _subplot_settings.get('silence_warnings')

            subplot_filters = set()
            for k in _subplot_settings.keys():
                filter_name = None
                if k.startswith('check_'):
                    filter_name = k[len('check_'):]
                elif k.startswith('inv_check_'):
                    filter_name = k[len('inv_check_'):]
                if filter_name is not None:
                    if filter_name not in filters:
                        raise ValueError(f"Metric '{subplot_name}' requires filter '{filter_name}'")
                    subplot_filters.add(filter_name)

            for filter_name in subplot_filters:
                filter_settings = filters[filter_name]
                _filter_settings = deep_substitute(filter_settings, mapping=mapping)
                filter_func = _filter_settings['filter_func']
                warning_message = _filter_settings.get('warning_message', None)
                inv_warning_message = _filter_settings.get('inv_warning_message', None)
                to_check = _subplot_settings.get('check_' + filter_name, False)
                inv_to_check = _subplot_settings.get('inv_check_' + filter_name, False)

                if to_check or inv_to_check:
                    whether_true = filter_func(custom_reself, _subplot_settings)
                    to_remove = (to_check and not whether_true) or (inv_to_check and whether_true)
                    if to_remove:
                        if to_check and warning_message is not None and not _silence_warnings:
                            warnings.warn(warning_message)
                        if inv_to_check and inv_warning_message is not None and not _silence_warnings:
                            warnings.warn(inv_warning_message)

                        subplots_dct.pop(subplot_name, None)
                        custom_arg_names_dct.pop(subplot_name, None)
                        opt_arg_names_dct.pop(subplot_name, None)
                        resolved_self_dct.pop(subplot_name, None)
                        mapping_dct.pop(subplot_name, None)
                        break

        # Any subplots left?
        if len(subplots_dct) == 0:
            if not silence_warnings:
                warnings.warn("No subplots to plot", stacklevel=2)
            return None

        # Set up figure
        rows = sub_make_subplots_kwargs.pop('rows', len(subplots_dct))
        cols = sub_make_subplots_kwargs.pop('cols', 1)
        specs = sub_make_subplots_kwargs.pop('specs', [[{} for _ in range(cols)] for _ in range(rows)])
        row_col_tuples = []
        for row, row_spec in enumerate(specs):
            for col, col_spec in enumerate(row_spec):
                if col_spec is not None:
                    row_col_tuples.append((row + 1, col + 1))
        shared_xaxes = sub_make_subplots_kwargs.pop('shared_xaxes', True)
        shared_yaxes = sub_make_subplots_kwargs.pop('shared_yaxes', False)
        default_height = plotting_cfg['layout']['height']
        default_width = plotting_cfg['layout']['width'] + 50
        min_space = 10  # space between subplots with no axis sharing
        max_title_spacing = 30
        max_xaxis_spacing = 50
        max_yaxis_spacing = 100
        legend_height = 50
        if show_titles:
            title_spacing = max_title_spacing
        else:
            title_spacing = 0
        if not shared_xaxes and rows > 1:
            xaxis_spacing = max_xaxis_spacing
        else:
            xaxis_spacing = 0
        if not shared_yaxes and cols > 1:
            yaxis_spacing = max_yaxis_spacing
        else:
            yaxis_spacing = 0
        if 'height' in sub_layout_kwargs:
            height = sub_layout_kwargs.pop('height')
        else:
            height = default_height + title_spacing
            if rows > 1:
                height *= rows
                height += min_space * rows - min_space
                height += legend_height - legend_height * rows
                if shared_xaxes:
                    height += max_xaxis_spacing - max_xaxis_spacing * rows
        if 'width' in sub_layout_kwargs:
            width = sub_layout_kwargs.pop('width')
        else:
            width = default_width
            if cols > 1:
                width *= cols
                width += min_space * cols - min_space
                if shared_yaxes:
                    width += max_yaxis_spacing - max_yaxis_spacing * cols
        if height is not None:
            if 'vertical_spacing' in sub_make_subplots_kwargs:
                vertical_spacing = sub_make_subplots_kwargs.pop('vertical_spacing')
            else:
                vertical_spacing = min_space + title_spacing + xaxis_spacing
            if vertical_spacing is not None and vertical_spacing > 1:
                vertical_spacing /= height
            legend_y = 1 + (min_space + title_spacing) / height
        else:
            vertical_spacing = sub_make_subplots_kwargs.pop('vertical_spacing', None)
            legend_y = 1.02
        if width is not None:
            if 'horizontal_spacing' in sub_make_subplots_kwargs:
                horizontal_spacing = sub_make_subplots_kwargs.pop('horizontal_spacing')
            else:
                horizontal_spacing = min_space + yaxis_spacing
            if horizontal_spacing is not None and horizontal_spacing > 1:
                horizontal_spacing /= width
        else:
            horizontal_spacing = sub_make_subplots_kwargs.pop('horizontal_spacing', None)
        if show_titles:
            _subplot_titles = []
            for i in range(len(subplots_dct)):
                _subplot_titles.append('$title_' + str(i))
        else:
            _subplot_titles = None
        fig = make_subplots(
            rows=rows,
            cols=cols,
            specs=specs,
            shared_xaxes=shared_xaxes,
            shared_yaxes=shared_yaxes,
            subplot_titles=_subplot_titles,
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing,
            **sub_make_subplots_kwargs
        )
        sub_layout_kwargs = merge_dicts(dict(
            showlegend=True,
            width=width,
            height=height,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=legend_y,
                xanchor="right",
                x=1,
                traceorder='normal'
            )
        ), sub_layout_kwargs)
        fig.update_layout(**sub_layout_kwargs)  # final destination for sub_layout_kwargs

        # Plot subplots
        arg_cache_dct = {}
        for i, (subplot_name, _subplot_settings) in enumerate(subplots_dct.items()):
            try:
                final_kwargs = _subplot_settings.copy()
                opt_arg_names = opt_arg_names_dct[subplot_name]
                custom_arg_names = custom_arg_names_dct[subplot_name]
                custom_reself = resolved_self_dct[subplot_name]
                mapping = mapping_dct[subplot_name]

                # Compute figure artifacts
                row, col = row_col_tuples[i]
                xref = 'x' if i == 0 else 'x' + str(i + 1)
                yref = 'y' if i == 0 else 'y' + str(i + 1)
                xaxis = 'xaxis' + xref[1:]
                yaxis = 'yaxis' + yref[1:]
                x_domain = get_domain(xref, fig)
                y_domain = get_domain(yref, fig)
                subplot_layout_kwargs = dict(
                    add_trace_kwargs=dict(row=row, col=col),
                    xref=xref,
                    yref=yref,
                    xaxis=xaxis,
                    yaxis=yaxis,
                    x_domain=x_domain,
                    y_domain=y_domain,
                    fig=fig,
                    pass_fig=True  # force passing fig
                )
                for k in subplot_layout_kwargs:
                    opt_arg_names.add(k)
                    if k in final_kwargs:
                        custom_arg_names.add(k)
                final_kwargs = merge_dicts(subplot_layout_kwargs, final_kwargs)
                mapping = merge_dicts(subplot_layout_kwargs, mapping)
                final_kwargs = deep_substitute(final_kwargs, mapping=mapping)

                # Clean up keys
                for k, v in list(final_kwargs.items()):
                    if k.startswith('check_') or k.startswith('inv_check_') or k in ('tags',):
                        final_kwargs.pop(k, None)

                # Get subplot-specific values
                _column = final_kwargs.get('column')
                _group_by = final_kwargs.get('group_by')
                _silence_warnings = final_kwargs.get('silence_warnings')
                title = final_kwargs.pop('title', subplot_name)
                plot_func = final_kwargs.pop('plot_func', None)
                xaxis_kwargs = final_kwargs.pop('xaxis_kwargs', None)
                yaxis_kwargs = final_kwargs.pop('yaxis_kwargs', None)
                resolve_plot_func = final_kwargs.pop('resolve_plot_func', True)
                use_caching = final_kwargs.pop('use_caching', True)

                if plot_func is not None:
                    # Resolve plot_func
                    if resolve_plot_func:
                        if not callable(plot_func):
                            passed_kwargs_out = {}

                            def _getattr_func(obj: tp.Any,
                                              attr: str,
                                              args: tp.ArgsLike = None,
                                              kwargs: tp.KwargsLike = None,
                                              call_attr: bool = True,
                                              _final_kwargs: tp.Kwargs = final_kwargs,
                                              _opt_arg_names: tp.Set[str] = opt_arg_names,
                                              _custom_arg_names: tp.Set[str] = custom_arg_names,
                                              _arg_cache_dct: tp.Kwargs = arg_cache_dct) -> tp.Any:
                                if attr in final_kwargs:
                                    return final_kwargs[attr]
                                if args is None:
                                    args = ()
                                if kwargs is None:
                                    kwargs = {}
                                if obj is custom_reself and _final_kwargs.pop('resolve_path_' + attr, True):
                                    if call_attr:
                                        return custom_reself.resolve_attr(
                                            attr,
                                            args=args,
                                            cond_kwargs={k: v for k, v in _final_kwargs.items() if k in _opt_arg_names},
                                            kwargs=kwargs,
                                            custom_arg_names=_custom_arg_names,
                                            cache_dct=_arg_cache_dct,
                                            use_caching=use_caching,
                                            passed_kwargs_out=passed_kwargs_out
                                        )
                                    return getattr(obj, attr)
                                out = getattr(obj, attr)
                                if callable(out) and call_attr:
                                    return out(*args, **kwargs)
                                return out

                            plot_func = custom_reself.deep_getattr(
                                plot_func,
                                getattr_func=_getattr_func,
                                call_last_attr=False
                            )

                            if 'group_by' in passed_kwargs_out:
                                if 'pass_group_by' not in final_kwargs:
                                    final_kwargs.pop('group_by', None)
                        if not callable(plot_func):
                            raise TypeError("plot_func must be callable")

                        # Resolve arguments
                        func_arg_names = get_func_arg_names(plot_func)
                        for k in func_arg_names:
                            if k not in final_kwargs:
                                if final_kwargs.pop('resolve_' + k, False):
                                    try:
                                        arg_out = custom_reself.resolve_attr(
                                            k,
                                            cond_kwargs=final_kwargs,
                                            custom_arg_names=custom_arg_names,
                                            cache_dct=arg_cache_dct,
                                            use_caching=use_caching
                                        )
                                    except AttributeError:
                                        continue
                                    final_kwargs[k] = arg_out
                        for k in list(final_kwargs.keys()):
                            if k in opt_arg_names:
                                if 'pass_' + k in final_kwargs:
                                    if not final_kwargs.get('pass_' + k):  # first priority
                                        final_kwargs.pop(k, None)
                                elif k not in func_arg_names:  # second priority
                                    final_kwargs.pop(k, None)
                        for k in list(final_kwargs.keys()):
                            if k.startswith('pass_') or k.startswith('resolve_'):
                                final_kwargs.pop(k, None)  # cleanup

                        # Call plot_func
                        plot_func(**final_kwargs)
                    else:
                        # Do not resolve plot_func
                        plot_func(custom_reself, _subplot_settings)

                # Update global layout
                for annotation in fig.layout.annotations:
                    if 'text' in annotation and annotation['text'] == '$title_' + str(i):
                        annotation['text'] = title
                subplot_layout = dict()
                subplot_layout[xaxis] = merge_dicts(dict(title='Index'), xaxis_kwargs)
                subplot_layout[yaxis] = merge_dicts(dict(), yaxis_kwargs)
                fig.update_layout(**subplot_layout)
            except Exception as e:
                warnings.warn(f"Subplot '{subplot_name}' raised an exception", stacklevel=2)
                raise e

        # Remove duplicate legend labels
        found_ids = dict()
        unique_idx = 0
        for trace in fig.data:
            if 'name' in trace:
                name = trace['name']
            else:
                name = None
            if 'marker' in trace:
                marker = trace['marker']
            else:
                marker = {}
            if 'symbol' in marker:
                marker_symbol = marker['symbol']
            else:
                marker_symbol = None
            if 'color' in marker:
                marker_color = marker['color']
            else:
                marker_color = None
            if 'line' in trace:
                line = trace['line']
            else:
                line = {}
            if 'dash' in line:
                line_dash = line['dash']
            else:
                line_dash = None
            if 'color' in line:
                line_color = line['color']
            else:
                line_color = None

            id = (name, marker_symbol, marker_color, line_dash, line_color)
            if id in found_ids:
                if hide_id_labels:
                    trace['showlegend'] = False
                if group_id_labels:
                    trace['legendgroup'] = found_ids[id]
            else:
                if group_id_labels:
                    trace['legendgroup'] = unique_idx
                found_ids[id] = unique_idx
                unique_idx += 1

        # Remove all except the last title if sharing the same axis
        if shared_xaxes:
            i = 0
            for row in range(rows):
                for col in range(cols):
                    if specs[row][col] is not None:
                        xaxis = 'xaxis' if i == 0 else 'xaxis' + str(i + 1)
                        if row < rows - 1:
                            fig.layout[xaxis]['title'] = None
                        i += 1
        if shared_yaxes:
            i = 0
            for row in range(rows):
                for col in range(cols):
                    if specs[row][col] is not None:
                        yaxis = 'yaxis' if i == 0 else 'yaxis' + str(i + 1)
                        if col > 0:
                            fig.layout[yaxis]['title'] = None
                        i += 1

        # Return the figure
        return fig

    # ############# Docs ############# #

    @classmethod
    def build_subplots_doc(cls, source_cls: tp.Optional[type] = None) -> str:
        """Build subplots documentation."""
        if source_cls is None:
            source_cls = PlotsBuilderMixin
        return string.Template(
            inspect.cleandoc(get_dict_attr(source_cls, 'subplots').__doc__)
        ).substitute(
            {'subplots': cls.subplots.to_doc(), 'cls_name': cls.__name__}
        )

    @classmethod
    def override_subplots_doc(cls, __pdoc__: dict, source_cls: tp.Optional[type] = None) -> None:
        """Call this method on each subclass that overrides `subplots`."""
        __pdoc__[cls.__name__ + '.subplots'] = cls.build_subplots_doc(source_cls=source_cls)


__pdoc__ = dict()
PlotsBuilderMixin.override_subplots_doc(__pdoc__)
