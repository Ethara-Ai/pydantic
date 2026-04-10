import math
import re
from collections import OrderedDict, deque
from collections.abc import Hashable as CollectionsHashable
from datetime import date, datetime, time, timedelta
from decimal import Decimal, DecimalException
from enum import Enum, IntEnum
from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Deque,
    Dict,
    ForwardRef,
    FrozenSet,
    Generator,
    Hashable,
    List,
    NamedTuple,
    Pattern,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID
from warnings import warn

from pydantic.v1 import errors
from pydantic.v1.datetime_parse import parse_date, parse_datetime, parse_duration, parse_time
from pydantic.v1.typing import (
    AnyCallable,
    all_literal_values,
    display_as_type,
    get_class,
    is_callable_type,
    is_literal_type,
    is_namedtuple,
    is_none_type,
    is_typeddict,
)
from pydantic.v1.utils import almost_equal_floats, lenient_issubclass, sequence_like

if TYPE_CHECKING:
    from typing_extensions import Literal, TypedDict

    from pydantic.v1.config import BaseConfig
    from pydantic.v1.fields import ModelField
    from pydantic.v1.types import ConstrainedDecimal, ConstrainedFloat, ConstrainedInt

    ConstrainedNumber = Union[ConstrainedDecimal, ConstrainedFloat, ConstrainedInt]
    AnyOrderedDict = OrderedDict[Any, Any]
    Number = Union[int, float, Decimal]
    StrBytes = Union[str, bytes]


def str_validator(v: Any) -> Union[str]:
    if isinstance(v, str):
        if isinstance(v, Enum):
            return v.value
        else:
            return v
    elif isinstance(v, (float, int, Decimal)):
        # is there anything else we want to add here? If you think so, create an issue.
        return str(v)
    elif isinstance(v, (bytes, bytearray)):
        return v.decode()
    else:
        raise errors.StrError()


def strict_str_validator(v: Any) -> Union[str]:
    pass


def bytes_validator(v: Any) -> Union[bytes]:
    if isinstance(v, bytes):
        return v
    elif isinstance(v, bytearray):
        return bytes(v)
    elif isinstance(v, str):
        return v.encode()
    elif isinstance(v, (float, int, Decimal)):
        return str(v).encode()
    else:
        raise errors.BytesError()


def strict_bytes_validator(v: Any) -> Union[bytes]:
    pass


BOOL_FALSE = {0, '0', 'off', 'f', 'false', 'n', 'no'}
BOOL_TRUE = {1, '1', 'on', 't', 'true', 'y', 'yes'}


def bool_validator(v: Any) -> bool:
    pass


# matches the default limit cpython, see https://github.com/python/cpython/pull/96500
max_str_int = 4_300


def int_validator(v: Any) -> int:
    pass


def strict_int_validator(v: Any) -> int:
    pass


def float_validator(v: Any) -> float:
    pass


def strict_float_validator(v: Any) -> float:
    pass


def float_finite_validator(v: 'Number', field: 'ModelField', config: 'BaseConfig') -> 'Number':
    pass


def number_multiple_validator(v: 'Number', field: 'ModelField') -> 'Number':
    pass


def number_size_validator(v: 'Number', field: 'ModelField') -> 'Number':
    pass


def constant_validator(v: 'Any', field: 'ModelField') -> 'Any':
    """Validate ``const`` fields.

    The value provided for a ``const`` field must be equal to the default value
    of the field. This is to support the keyword of the same name in JSON
    Schema.
    """
    pass


def anystr_length_validator(v: 'StrBytes', config: 'BaseConfig') -> 'StrBytes':
    pass


def anystr_strip_whitespace(v: 'StrBytes') -> 'StrBytes':
    pass


def anystr_upper(v: 'StrBytes') -> 'StrBytes':
    pass


def anystr_lower(v: 'StrBytes') -> 'StrBytes':
    pass


def ordered_dict_validator(v: Any) -> 'AnyOrderedDict':
    pass


def dict_validator(v: Any) -> Dict[Any, Any]:
    if isinstance(v, dict):
        return v

    try:
        return dict(v)
    except (TypeError, ValueError):
        raise errors.DictError()


def list_validator(v: Any) -> List[Any]:
    pass


def tuple_validator(v: Any) -> Tuple[Any, ...]:
    pass


def set_validator(v: Any) -> Set[Any]:
    pass


def frozenset_validator(v: Any) -> FrozenSet[Any]:
    pass


def deque_validator(v: Any) -> Deque[Any]:
    pass


def enum_member_validator(v: Any, field: 'ModelField', config: 'BaseConfig') -> Enum:
    pass


def uuid_validator(v: Any, field: 'ModelField') -> UUID:
    pass


def decimal_validator(v: Any) -> Decimal:
    pass


def hashable_validator(v: Any) -> Hashable:
    pass


def ip_v4_address_validator(v: Any) -> IPv4Address:
    pass


def ip_v6_address_validator(v: Any) -> IPv6Address:
    pass


def ip_v4_network_validator(v: Any) -> IPv4Network:
    """
    Assume IPv4Network initialised with a default ``strict`` argument

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv4Network
    """
    pass


def ip_v6_network_validator(v: Any) -> IPv6Network:
    """
    Assume IPv6Network initialised with a default ``strict`` argument

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv6Network
    """
    pass


def ip_v4_interface_validator(v: Any) -> IPv4Interface:
    pass


def ip_v6_interface_validator(v: Any) -> IPv6Interface:
    pass


def path_validator(v: Any) -> Path:
    pass


def path_exists_validator(v: Any) -> Path:
    pass


def callable_validator(v: Any) -> AnyCallable:
    """
    Perform a simple check if the value is callable.

    Note: complete matching of argument type hints and return types is not performed
    """
    pass


def enum_validator(v: Any) -> Enum:
    pass


def int_enum_validator(v: Any) -> IntEnum:
    pass


def make_literal_validator(type_: Any) -> Callable[[Any], Any]:
    permitted_choices = all_literal_values(type_)

    # To have a O(1) complexity and still return one of the values set inside the `Literal`,
    # we create a dict with the set values (a set causes some problems with the way intersection works).
    # In some cases the set value and checked value can indeed be different (see `test_literal_validator_str_enum`)
    allowed_choices = {v: v for v in permitted_choices}

    def literal_validator(v: Any) -> Any:
        pass

    return literal_validator


def constr_length_validator(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    v_len = len(v)

    min_length = field.type_.min_length if field.type_.min_length is not None else config.min_anystr_length
    if v_len < min_length:
        raise errors.AnyStrMinLengthError(limit_value=min_length)

    max_length = field.type_.max_length if field.type_.max_length is not None else config.max_anystr_length
    if max_length is not None and v_len > max_length:
        raise errors.AnyStrMaxLengthError(limit_value=max_length)

    return v


def constr_strip_whitespace(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    pass


def constr_upper(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    pass


def constr_lower(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    pass


def validate_json(v: Any, config: 'BaseConfig') -> Any:
    if v is None:
        # pass None through to other validators
        return v
    try:
        return config.json_loads(v)  # type: ignore
    except ValueError:
        raise errors.JsonError()
    except TypeError:
        raise errors.JsonTypeError()


T = TypeVar('T')


def make_arbitrary_type_validator(type_: Type[T]) -> Callable[[T], T]:
    def arbitrary_type_validator(v: Any) -> T:
        pass

    return arbitrary_type_validator


def make_class_validator(type_: Type[T]) -> Callable[[Any], Type[T]]:
    def class_validator(v: Any) -> Type[T]:
        pass

    return class_validator


def any_class_validator(v: Any) -> Type[T]:
    pass


def none_validator(v: Any) -> 'Literal[None]':
    pass


def pattern_validator(v: Any) -> Pattern[str]:
    pass


NamedTupleT = TypeVar('NamedTupleT', bound=NamedTuple)


def make_namedtuple_validator(
    namedtuple_cls: Type[NamedTupleT], config: Type['BaseConfig']
) -> Callable[[Tuple[Any, ...]], NamedTupleT]:
    from pydantic.v1.annotated_types import create_model_from_namedtuple

    NamedTupleModel = create_model_from_namedtuple(
        namedtuple_cls,
        __config__=config,
        __module__=namedtuple_cls.__module__,
    )
    namedtuple_cls.__pydantic_model__ = NamedTupleModel  # type: ignore[attr-defined]

    def namedtuple_validator(values: Tuple[Any, ...]) -> NamedTupleT:
        pass

    return namedtuple_validator


def make_typeddict_validator(
    typeddict_cls: Type['TypedDict'], config: Type['BaseConfig']  # type: ignore[valid-type]
) -> Callable[[Any], Dict[str, Any]]:
    from pydantic.v1.annotated_types import create_model_from_typeddict

    TypedDictModel = create_model_from_typeddict(
        typeddict_cls,
        __config__=config,
        __module__=typeddict_cls.__module__,
    )
    typeddict_cls.__pydantic_model__ = TypedDictModel  # type: ignore[attr-defined]

    def typeddict_validator(values: 'TypedDict') -> Dict[str, Any]:  # type: ignore[valid-type]
        pass

    return typeddict_validator


class IfConfig:
    def __init__(self, validator: AnyCallable, *config_attr_names: str, ignored_value: Any = False) -> None:
        self.validator = validator
        self.config_attr_names = config_attr_names
        self.ignored_value = ignored_value

    def check(self, config: Type['BaseConfig']) -> bool:
        return any(getattr(config, name) not in {None, self.ignored_value} for name in self.config_attr_names)


# order is important here, for example: bool is a subclass of int so has to come first, datetime before date same,
# IPv4Interface before IPv4Address, etc
_VALIDATORS: List[Tuple[Type[Any], List[Any]]] = [
    (IntEnum, [int_validator, enum_member_validator]),
    (Enum, [enum_member_validator]),
    (
        str,
        [
            str_validator,
            IfConfig(anystr_strip_whitespace, 'anystr_strip_whitespace'),
            IfConfig(anystr_upper, 'anystr_upper'),
            IfConfig(anystr_lower, 'anystr_lower'),
            IfConfig(anystr_length_validator, 'min_anystr_length', 'max_anystr_length'),
        ],
    ),
    (
        bytes,
        [
            bytes_validator,
            IfConfig(anystr_strip_whitespace, 'anystr_strip_whitespace'),
            IfConfig(anystr_upper, 'anystr_upper'),
            IfConfig(anystr_lower, 'anystr_lower'),
            IfConfig(anystr_length_validator, 'min_anystr_length', 'max_anystr_length'),
        ],
    ),
    (bool, [bool_validator]),
    (int, [int_validator]),
    (float, [float_validator, IfConfig(float_finite_validator, 'allow_inf_nan', ignored_value=True)]),
    (Path, [path_validator]),
    (datetime, [parse_datetime]),
    (date, [parse_date]),
    (time, [parse_time]),
    (timedelta, [parse_duration]),
    (OrderedDict, [ordered_dict_validator]),
    (dict, [dict_validator]),
    (list, [list_validator]),
    (tuple, [tuple_validator]),
    (set, [set_validator]),
    (frozenset, [frozenset_validator]),
    (deque, [deque_validator]),
    (UUID, [uuid_validator]),
    (Decimal, [decimal_validator]),
    (IPv4Interface, [ip_v4_interface_validator]),
    (IPv6Interface, [ip_v6_interface_validator]),
    (IPv4Address, [ip_v4_address_validator]),
    (IPv6Address, [ip_v6_address_validator]),
    (IPv4Network, [ip_v4_network_validator]),
    (IPv6Network, [ip_v6_network_validator]),
]


def find_validators(  # noqa: C901 (ignore complexity)
    type_: Type[Any], config: Type['BaseConfig']
) -> Generator[AnyCallable, None, None]:
    from pydantic.v1.dataclasses import is_builtin_dataclass, make_dataclass_validator

    if type_ is Any or type_ is object:
        return
    type_type = type_.__class__
    if type_type == ForwardRef or type_type == TypeVar:
        return

    if is_none_type(type_):
        yield none_validator
        return
    if type_ is Pattern or type_ is re.Pattern:
        yield pattern_validator
        return
    if type_ is Hashable or type_ is CollectionsHashable:
        yield hashable_validator
        return
    if is_callable_type(type_):
        yield callable_validator
        return
    if is_literal_type(type_):
        yield make_literal_validator(type_)
        return
    if is_builtin_dataclass(type_):
        yield from make_dataclass_validator(type_, config)
        return
    if type_ is Enum:
        yield enum_validator
        return
    if type_ is IntEnum:
        yield int_enum_validator
        return
    if is_namedtuple(type_):
        yield tuple_validator
        yield make_namedtuple_validator(type_, config)
        return
    if is_typeddict(type_):
        yield make_typeddict_validator(type_, config)
        return

    class_ = get_class(type_)
    if class_ is not None:
        if class_ is not Any and isinstance(class_, type):
            yield make_class_validator(class_)
        else:
            yield any_class_validator
        return

    for val_type, validators in _VALIDATORS:
        try:
            if issubclass(type_, val_type):
                for v in validators:
                    if isinstance(v, IfConfig):
                        if v.check(config):
                            yield v.validator
                    else:
                        yield v
                return
        except TypeError:
            raise RuntimeError(f'error checking inheritance of {type_!r} (type: {display_as_type(type_)})')

    if config.arbitrary_types_allowed:
        yield make_arbitrary_type_validator(type_)
    else:
        if hasattr(type_, '__pydantic_core_schema__'):
            warn(f'Mixing V1 and V2 models is not supported. `{type_.__name__}` is a V2 model.', UserWarning)
        raise RuntimeError(f'no validator found for {type_}, see `arbitrary_types_allowed` in Config')
