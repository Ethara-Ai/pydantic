import json
import pickle
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Union

from pydantic.v1.types import StrBytes


class Protocol(str, Enum):
    json = 'json'
    pickle = 'pickle'


def load_str_bytes(
    b: StrBytes,
    *,
    content_type: str = None,
    encoding: str = 'utf8',
    proto: Protocol = None,
    allow_pickle: bool = False,
    json_loads: Callable[[str], Any] = json.loads,
) -> Any:
    pass


def load_file(
    path: Union[str, Path],
    *,
    content_type: str = None,
    encoding: str = 'utf8',
    proto: Protocol = None,
    allow_pickle: bool = False,
    json_loads: Callable[[str], Any] = json.loads,
) -> Any:
    pass
