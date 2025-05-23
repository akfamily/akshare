# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Class and function decorators."""

import inspect

from vectorbt import _typing as tp
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, Config, get_func_arg_names

WrapperFuncT = tp.Callable[[tp.Type[tp.T]], tp.Type[tp.T]]


def attach_nb_methods(config: Config) -> WrapperFuncT:
    """Class decorator to add Numba methods.

    `config` should contain target method names (keys) and dictionaries (values) with the following keys:

    * `func`: Function that should be wrapped. The first argument should expect a 2-dim array.
    * `is_reducing`: Whether the function is reducing. Defaults to False.
    * `path`: Path to the function for documentation. Defaults to `func.__name__`.
    * `replace_signature`: Whether to replace the target signature with the source signature. Defaults to True.
    * `wrap_kwargs`: Default keyword arguments for wrapping. Will be merged with the dict supplied by the user.
        Defaults to `dict(name_or_index=target_name)` for reducing functions.

    The class should be a subclass of `vectorbt.base.array_wrapper.Wrapping`.
    """

    def wrapper(cls: tp.Type[tp.T]) -> tp.Type[tp.T]:
        from vectorbt.base.array_wrapper import Wrapping

        checks.assert_subclass_of(cls, Wrapping)

        for target_name, settings in config.items():
            func = settings['func']
            is_reducing = settings.get('is_reducing', False)
            path = settings.get('path', func.__name__)
            replace_signature = settings.get('replace_signature', True)
            default_wrap_kwargs = settings.get('wrap_kwargs', dict(name_or_index=target_name) if is_reducing else None)

            def new_method(self,
                           *args,
                           _target_name: str = target_name,
                           _func: tp.Callable = func,
                           _is_reducing: bool = is_reducing,
                           _default_wrap_kwargs: tp.KwargsLike = default_wrap_kwargs,
                           wrap_kwargs: tp.KwargsLike = None,
                           **kwargs) -> tp.SeriesFrame:
                args = (self.to_2d_array(),) + args
                inspect.signature(_func).bind(*args, **kwargs)

                a = _func(*args, **kwargs)
                wrap_kwargs = merge_dicts(_default_wrap_kwargs, wrap_kwargs)
                if _is_reducing:
                    return self.wrapper.wrap_reduced(a, **wrap_kwargs)
                return self.wrapper.wrap(a, **wrap_kwargs)

            if replace_signature:
                # Replace the function's signature with the original one
                source_sig = inspect.signature(func)
                new_method_params = tuple(inspect.signature(new_method).parameters.values())
                self_arg = new_method_params[0]
                wrap_kwargs_arg = new_method_params[-2]
                source_sig = source_sig.replace(
                    parameters=(self_arg,) + tuple(source_sig.parameters.values())[1:] + (wrap_kwargs_arg,))
                new_method.__signature__ = source_sig

            new_method.__doc__ = f"See `{path}`."
            new_method.__qualname__ = f"{cls.__name__}.{target_name}"
            new_method.__name__ = target_name
            setattr(cls, target_name, new_method)
        return cls

    return wrapper


def attach_transform_methods(config: Config) -> WrapperFuncT:
    """Class decorator to add transformation methods.

    `config` should contain target method names (keys) and dictionaries (values) with the following keys:

    * `transformer`: Transformer class/object.
    * `docstring`: Method docstring. Defaults to "See `{transformer}.__name__`.".
    * `replace_signature`: Whether to replace the target signature. Defaults to True.

    The class should be a subclass of `vectorbt.generic.accessors.GenericAccessor`.
    """

    def wrapper(cls: tp.Type[tp.T]) -> tp.Type[tp.T]:
        from vectorbt.generic.accessors import TransformerT

        checks.assert_subclass_of(cls, "GenericAccessor")

        for target_name, settings in config.items():
            transformer = settings['transformer']
            docstring = settings.get('docstring', f"See `{transformer.__name__}`.")
            replace_signature = settings.get('replace_signature', True)

            def new_method(self,
                           _target_name: str = target_name,
                           _transformer: tp.Union[tp.Type[TransformerT], TransformerT] = transformer,
                           **kwargs) -> tp.SeriesFrame:
                if inspect.isclass(_transformer):
                    arg_names = get_func_arg_names(_transformer.__init__)
                    transformer_kwargs = dict()
                    for arg_name in arg_names:
                        if arg_name in kwargs:
                            transformer_kwargs[arg_name] = kwargs.pop(arg_name)
                    return self.transform(_transformer(**transformer_kwargs), **kwargs)
                return self.transform(_transformer, **kwargs)

            if replace_signature:
                source_sig = inspect.signature(transformer.__init__)
                new_method_params = tuple(inspect.signature(new_method).parameters.values())
                if inspect.isclass(transformer):
                    transformer_params = tuple(source_sig.parameters.values())
                    source_sig = inspect.Signature(
                        (new_method_params[0],) + transformer_params[1:] + (new_method_params[-1],))
                    new_method.__signature__ = source_sig
                else:
                    source_sig = inspect.Signature((new_method_params[0],) + (new_method_params[-1],))
                    new_method.__signature__ = source_sig

            new_method.__doc__ = docstring
            new_method.__qualname__ = f"{cls.__name__}.{target_name}"
            new_method.__name__ = target_name
            setattr(cls, target_name, new_method)
        return cls

    return wrapper
