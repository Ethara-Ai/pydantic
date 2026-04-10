"""Validator functions for standard library types.

Import of this module is deferred since it contains imports of many standard library modules.
"""

from __future__ import annotations as _annotations

import collections.abc
import math
import re
import typing
from collections.abc import Sequence
from decimal import Decimal
from fractions import Fraction
from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from typing import Any, Callable, TypeVar, Union, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import typing_extensions
from pydantic_core import PydanticCustomError, PydanticKnownError, core_schema
from typing_extensions import get_args, get_origin
from typing_inspection import typing_objects

from pydantic._internal._import_utils import import_cached_field_info
from pydantic.errors import PydanticSchemaGenerationError


def sequence_validator(
    input_value: Sequence[Any],
    /,
    validator: core_schema.ValidatorFunctionWrapHandler,
) -> Sequence[Any]:
    """Validator for `Sequence` types, isinstance(v, Sequence) has already been called."""
    pass


def import_string(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return _import_string_logic(value)
        except ImportError as e:
            raise PydanticCustomError('import_error', 'Invalid python path: {error}', {'error': str(e)}) from e
    else:
        # otherwise we just return the value and let the next validator do the rest of the work
        return value


def _import_string_logic(dotted_path: str) -> Any:
    """Inspired by uvicorn — dotted paths should include a colon before the final item if that item is not a module.
    (This is necessary to distinguish between a submodule and an attribute when there is a conflict.).

    If the dotted path does not include a colon and the final item is not a valid module, importing as an attribute
    rather than a submodule will be attempted automatically.

    So, for example, the following values of `dotted_path` result in the following returned values:
    * 'collections': <module 'collections'>
    * 'collections.abc': <module 'collections.abc'>
    * 'collections.abc:Mapping': <class 'collections.abc.Mapping'>
    * `collections.abc.Mapping`: <class 'collections.abc.Mapping'> (though this is a bit slower than the previous line)

    An error will be raised under any of the following scenarios:
    * `dotted_path` contains more than one colon (e.g., 'collections:abc:Mapping')
    * the substring of `dotted_path` before the colon is not a valid module in the environment (e.g., '123:Mapping')
    * the substring of `dotted_path` after the colon is not an attribute of the module (e.g., 'collections:abc123')
    """
    from importlib import import_module

    components = dotted_path.strip().split(':')
    if len(components) > 2:
        raise ImportError(f"Import strings should have at most one ':'; received {dotted_path!r}")
    attribute = None
    if len(components) == 2:
        attribute = components[1]
    module_path = components[0]
    if not module_path:
        raise ImportError(f'Import strings should have a nonempty module name; received {dotted_path!r}')

    try:
        module = import_module(module_path)
    except ModuleNotFoundError:
        if attribute is None and '.' in module_path:
            # Try interpreting the final dotted segment as an attribute, not a submodule
            maybe_module_path, maybe_attribute = module_path.rsplit('.', 1)

            try:
                return _import_string_logic(f'{maybe_module_path}:{maybe_attribute}')
            except ImportError:
                pass
        raise

    if attribute is not None:
        try:
            return getattr(module, attribute)
        except AttributeError as e:
            raise ImportError(f'cannot import name {attribute!r} from {module_path!r}') from e
    else:
        return module


def pattern_either_validator(input_value: Any, /) -> re.Pattern[Any]:
    pass


def pattern_str_validator(input_value: Any, /) -> re.Pattern[str]:
    pass


def pattern_bytes_validator(input_value: Any, /) -> re.Pattern[bytes]:
    pass


PatternType = TypeVar('PatternType', str, bytes)


def compile_pattern(pattern: PatternType) -> re.Pattern[PatternType]:
    pass


def ip_v4_address_validator(input_value: Any, /) -> IPv4Address:
    pass


def ip_v6_address_validator(input_value: Any, /) -> IPv6Address:
    pass


def ip_v4_network_validator(input_value: Any, /) -> IPv4Network:
    """Assume IPv4Network initialised with a default `strict` argument.

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv4Network
    """
    pass


def ip_v6_network_validator(input_value: Any, /) -> IPv6Network:
    """Assume IPv6Network initialised with a default `strict` argument.

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv6Network
    """
    pass


def ip_v4_interface_validator(input_value: Any, /) -> IPv4Interface:
    pass


def ip_v6_interface_validator(input_value: Any, /) -> IPv6Interface:
    pass


def fraction_validator(input_value: Any, /) -> Fraction:
    pass


def forbid_inf_nan_check(x: Any) -> Any:
    pass


def _safe_repr(v: Any) -> int | float | str:
    """The context argument for `PydanticKnownError` requires a number or str type, so we do a simple repr() coercion for types like timedelta.

    See tests/test_types.py::test_annotated_metadata_any_order for some context.
    """
    pass


def greater_than_validator(x: Any, gt: Any) -> Any:
    pass


def greater_than_or_equal_validator(x: Any, ge: Any) -> Any:
    pass


def less_than_validator(x: Any, lt: Any) -> Any:
    pass


def less_than_or_equal_validator(x: Any, le: Any) -> Any:
    pass


def multiple_of_validator(x: Any, multiple_of: Any) -> Any:
    pass


def min_length_validator(x: Any, min_length: Any) -> Any:
    pass


def max_length_validator(x: Any, max_length: Any) -> Any:
    pass


def _extract_decimal_digits_info(decimal: Decimal) -> tuple[int, int]:
    """Compute the total number of digits and decimal places for a given [`Decimal`][decimal.Decimal] instance.

    This function handles both normalized and non-normalized Decimal instances.
    Example: Decimal('1.230') -> 4 digits, 3 decimal places

    Args:
        decimal (Decimal): The decimal number to analyze.

    Returns:
        tuple[int, int]: A tuple containing the number of decimal places and total digits.

    Though this could be divided into two separate functions, the logic is easier to follow if we couple the computation
    of the number of decimals and digits together.
    """
    pass


def max_digits_validator(x: Any, max_digits: Any) -> Any:
    pass


def decimal_places_validator(x: Any, decimal_places: Any) -> Any:
    pass


def deque_validator(input_value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> collections.deque[Any]:
    pass


def defaultdict_validator(
    input_value: Any, handler: core_schema.ValidatorFunctionWrapHandler, default_default_factory: Callable[[], Any]
) -> collections.defaultdict[Any, Any]:
    pass


def get_defaultdict_default_default_factory(values_source_type: Any) -> Callable[[], Any]:
    FieldInfo = import_cached_field_info()

    values_type_origin = get_origin(values_source_type)

    def infer_default() -> Callable[[], Any]:
        allowed_default_types: dict[Any, Any] = {
            tuple: tuple,
            collections.abc.Sequence: tuple,
            collections.abc.MutableSequence: list,
            list: list,
            typing.Sequence: list,
            set: set,
            typing.MutableSet: set,
            collections.abc.MutableSet: set,
            collections.abc.Set: frozenset,
            typing.MutableMapping: dict,
            typing.Mapping: dict,
            collections.abc.Mapping: dict,
            collections.abc.MutableMapping: dict,
            float: float,
            int: int,
            str: str,
            bool: bool,
        }
        values_type = values_type_origin or values_source_type
        instructions = 'set using `DefaultDict[..., Annotated[..., Field(default_factory=...)]]`'
        if typing_objects.is_typevar(values_type):

            def type_var_default_factory() -> None:
                raise RuntimeError(
                    'Generic defaultdict cannot be used without a concrete value type or an'
                    ' explicit default factory, ' + instructions
                )

            return type_var_default_factory
        elif values_type not in allowed_default_types:
            # a somewhat subjective set of types that have reasonable default values
            allowed_msg = ', '.join([t.__name__ for t in set(allowed_default_types.values())])
            raise PydanticSchemaGenerationError(
                f'Unable to infer a default factory for keys of type {values_source_type}.'
                f' Only {allowed_msg} are supported, other types require an explicit default factory'
                ' ' + instructions
            )
        return allowed_default_types[values_type]

    # Assume Annotated[..., Field(...)]
    if typing_objects.is_annotated(values_type_origin):
        field_info = next((v for v in get_args(values_source_type) if isinstance(v, FieldInfo)), None)
    else:
        field_info = None
    if field_info and field_info.default_factory:
        # Assume the default factory does not take any argument:
        default_default_factory = cast(Callable[[], Any], field_info.default_factory)
    else:
        default_default_factory = infer_default()
    return default_default_factory


def validate_str_is_valid_iana_tz(value: Any, /) -> ZoneInfo:
    pass


NUMERIC_VALIDATOR_LOOKUP: dict[str, Callable] = {
    'gt': greater_than_validator,
    'ge': greater_than_or_equal_validator,
    'lt': less_than_validator,
    'le': less_than_or_equal_validator,
    'multiple_of': multiple_of_validator,
    'min_length': min_length_validator,
    'max_length': max_length_validator,
    'max_digits': max_digits_validator,
    'decimal_places': decimal_places_validator,
}

IpType = Union[IPv4Address, IPv6Address, IPv4Network, IPv6Network, IPv4Interface, IPv6Interface]

IP_VALIDATOR_LOOKUP: dict[type[IpType], Callable] = {
    IPv4Address: ip_v4_address_validator,
    IPv6Address: ip_v6_address_validator,
    IPv4Network: ip_v4_network_validator,
    IPv6Network: ip_v6_network_validator,
    IPv4Interface: ip_v4_interface_validator,
    IPv6Interface: ip_v6_interface_validator,
}

MAPPING_ORIGIN_MAP: dict[Any, Any] = {
    typing.DefaultDict: collections.defaultdict,  # noqa: UP006
    collections.defaultdict: collections.defaultdict,
    typing.OrderedDict: collections.OrderedDict,  # noqa: UP006
    collections.OrderedDict: collections.OrderedDict,
    typing_extensions.OrderedDict: collections.OrderedDict,
    typing.Counter: collections.Counter,
    collections.Counter: collections.Counter,
    # this doesn't handle subclasses of these
    typing.Mapping: dict,
    typing.MutableMapping: dict,
    # parametrized typing.{Mutable}Mapping creates one of these
    collections.abc.Mapping: dict,
    collections.abc.MutableMapping: dict,
}
