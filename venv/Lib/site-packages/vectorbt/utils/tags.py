# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with tags."""

import ast

from vectorbt import _typing as tp
from vectorbt.utils.template import RepEval


def match_tags(tags: tp.MaybeIterable[str], in_tags: tp.MaybeIterable[str]) -> bool:
    """Match tags in `tags` to that in `in_tags`.

    Multiple tags in `tags` are combined using OR rule, that is, returns True if any of them is found in `in_tags`.
    If any tag is not an identifier, evaluates it as a boolean expression.
    All tags in `in_tags` should be identifiers.

    Usage:
        ```pycon
        >>> from vectorbt.utils.tags import match_tags

        >>> match_tags('hello', 'hello')
        True
        >>> match_tags('hello', 'world')
        False
        >>> match_tags(['hello', 'world'], 'world')
        True
        >>> match_tags('hello', ['hello', 'world'])
        True
        >>> match_tags('hello and world', ['hello', 'world'])
        True
        >>> match_tags('hello and not world', ['hello', 'world'])
        False
        ```
    """
    if isinstance(tags, str):
        tags = [tags]
    if isinstance(in_tags, str):
        in_tags = [in_tags]
    for in_t in in_tags:
        if not in_t.isidentifier():
            raise ValueError(f"Tag '{in_t}' must be an identifier")

    for t in tags:
        if not t.isidentifier():
            node_ids = [node.id for node in ast.walk(ast.parse(t)) if type(node) is ast.Name]
            eval_mapping = {id_: id_ in in_tags for id_ in node_ids}
            eval_result = RepEval(t).eval(eval_mapping)
            if not isinstance(eval_result, bool):
                raise TypeError(f"Tag expression '{t}' must produce a boolean")
            if eval_result:
                return True
        else:
            if t in in_tags:
                return True
    return False
