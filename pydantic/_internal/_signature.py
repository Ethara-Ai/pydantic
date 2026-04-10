from __future__ import annotations

import dataclasses
from inspect import Parameter, Signature
from typing import TYPE_CHECKING, Any, Callable

from pydantic_core import PydanticUndefined

from ._typing_extra import signature_no_eval
from ._utils import is_valid_identifier

if TYPE_CHECKING:
    from ..config import ExtraValues
    from ..fields import FieldInfo


# Copied over from stdlib dataclasses
class _HAS_DEFAULT_FACTORY_CLASS:
    def __repr__(self):
        return '<factory>'


_HAS_DEFAULT_FACTORY = _HAS_DEFAULT_FACTORY_CLASS()


def _field_name_for_signature(field_name: str, field_info: FieldInfo) -> str:
    """Extract the correct name to use for the field when generating a signature.

    Assuming the field has a valid alias, this will return the alias. Otherwise, it will return the field name.
    First priority is given to the alias, then the validation_alias, then the field name.

    Args:
        field_name: The name of the field
        field_info: The corresponding FieldInfo object.

    Returns:
        The correct name to use when generating a signature.
    """
    pass


def _process_param_defaults(param: Parameter) -> Parameter:
    """Modify the signature for a parameter in a dataclass where the default value is a FieldInfo instance.

    Args:
        param (Parameter): The parameter

    Returns:
        Parameter: The custom processed parameter
    """
    pass


def _generate_signature_parameters(  # noqa: C901 (ignore complexity, could use a refactor)
    init: Callable[..., None],
    fields: dict[str, FieldInfo],
    validate_by_name: bool,
    extra: ExtraValues | None,
) -> dict[str, Parameter]:
    """Generate a mapping of parameter names to Parameter objects for a pydantic BaseModel or dataclass."""
    pass


def generate_pydantic_signature(
    init: Callable[..., None],
    fields: dict[str, FieldInfo],
    validate_by_name: bool,
    extra: ExtraValues | None,
    is_dataclass: bool = False,
) -> Signature:
    """Generate signature for a pydantic BaseModel or dataclass.

    Args:
        init: The class init.
        fields: The model fields.
        validate_by_name: The `validate_by_name` value of the config.
        extra: The `extra` value of the config.
        is_dataclass: Whether the model is a dataclass.

    Returns:
        The dataclass/BaseModel subclass signature.
    """
    pass
