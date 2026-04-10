from __future__ import annotations

import collections
import collections.abc
import typing
from typing import Any

from pydantic_core import PydanticOmit, core_schema

SEQUENCE_ORIGIN_MAP: dict[Any, Any] = {
    typing.Deque: collections.deque,  # noqa: UP006
    collections.deque: collections.deque,
    list: list,
    typing.List: list,  # noqa: UP006
    tuple: tuple,
    typing.Tuple: tuple,  # noqa: UP006
    set: set,
    typing.AbstractSet: set,
    typing.Set: set,  # noqa: UP006
    frozenset: frozenset,
    typing.FrozenSet: frozenset,  # noqa: UP006
    typing.Sequence: list,
    typing.MutableSequence: list,
    typing.MutableSet: set,
    # this doesn't handle subclasses of these
    # parametrized typing.Set creates one of these
    collections.abc.MutableSet: set,
    collections.abc.Set: frozenset,
}


def serialize_sequence_via_list(
    v: Any, handler: core_schema.SerializerFunctionWrapHandler, info: core_schema.SerializationInfo
) -> Any:
    pass
