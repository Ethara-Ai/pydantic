"""Experimental module exposing a function to generate a core schema that validates callable arguments."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from pydantic_core import CoreSchema

from pydantic import ConfigDict
from pydantic._internal import _config, _generate_schema, _namespace_utils


def generate_arguments_schema(
    func: Callable[..., Any],
    schema_type: Literal['arguments', 'arguments-v3'] = 'arguments-v3',
    parameters_callback: Callable[[int, str, Any], Literal['skip'] | None] | None = None,
    config: ConfigDict | None = None,
) -> CoreSchema:
    """Generate the schema for the arguments of a function.

    Args:
        func: The function to generate the schema for.
        schema_type: The type of schema to generate.
        parameters_callback: A callable that will be invoked for each parameter. The callback
            should take three required arguments: the index, the name and the type annotation
            (or [`Parameter.empty`][inspect.Parameter.empty] if not annotated) of the parameter.
            The callback can optionally return `'skip'`, so that the parameter gets excluded
            from the resulting schema.
        config: The configuration to use.

    Returns:
        The generated schema.
    """
    pass
