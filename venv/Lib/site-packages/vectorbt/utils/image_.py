# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for images."""

import imageio
import numpy as np
import plotly.graph_objects as go
from tqdm.auto import tqdm

from vectorbt import _typing as tp


def hstack_image_arrays(a: tp.Array3d, b: tp.Array3d) -> tp.Array3d:
    """Stack NumPy images horizontally."""
    h1, w1, d = a.shape
    h2, w2, _ = b.shape
    c = np.full((max(h1, h2), w1 + w2, d), 255, np.uint8)
    c[:h1, :w1, :] = a
    c[:h2, w1:w1 + w2, :] = b
    return c


def vstack_image_arrays(a: tp.Array3d, b: tp.Array3d) -> tp.Array3d:
    """Stack NumPy images vertically."""
    h1, w1, d = a.shape
    h2, w2, _ = b.shape
    c = np.full((h1 + h2, max(w1, w2), d), 255, np.uint8)
    c[:h1, :w1, :] = a
    c[h1:h1 + h2, :w2, :] = b
    return c


def save_animation(fname: str,
                   index: tp.ArrayLikeSequence,
                   plot_func: tp.Callable,
                   *args,
                   delta: tp.Optional[int] = None,
                   step: int = 1,
                   fps: int = 3,
                   writer_kwargs: dict = None,
                   show_progress: bool = True,
                   tqdm_kwargs: tp.KwargsLike = None,
                   to_image_kwargs: tp.KwargsLike = None,
                   **kwargs) -> None:
    """Save animation to a file.

    Args:
        fname (str): File name.
        index (iterable): Index to iterate over.
        plot_func (callable): Plotting function.

            Should take subset of `index`, `*args`, and `**kwargs`, and return either a Plotly figure,
            image that can be read by `imageio.imread`, or a NumPy array.
        *args: Positional arguments passed to `plot_func`.
        delta (int): Window size of each iteration.
        step (int): Step of each iteration.
        fps (int): Frames per second.

            Will be translated to `duration` by `1000 / fps`.
        writer_kwargs (dict): Keyword arguments passed to `imageio.get_writer`.
        show_progress (bool): Whether to show the progress bar.
        tqdm_kwargs (dict): Keyword arguments passed to `tqdm`.
        to_image_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.to_image`.
        **kwargs: Keyword arguments passed to `plot_func`.
    """
    if writer_kwargs is None:
        writer_kwargs = {}
    if "duration" not in writer_kwargs:
        writer_kwargs["duration"] = 1000 / fps
    if tqdm_kwargs is None:
        tqdm_kwargs = {}
    if to_image_kwargs is None:
        to_image_kwargs = {}
    if delta is None:
        delta = len(index) // 2

    with imageio.get_writer(fname, **writer_kwargs) as writer:
        for i in tqdm(range(0, len(index) - delta, step), disable=not show_progress, **tqdm_kwargs):
            fig = plot_func(index[i:i + delta], *args, **kwargs)
            if isinstance(fig, (go.Figure, go.FigureWidget)):
                fig = fig.to_image(format="png", **to_image_kwargs)
            if not isinstance(fig, np.ndarray):
                fig = imageio.imread(fig)
            writer.append_data(fig)
