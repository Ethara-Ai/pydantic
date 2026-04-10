__all__ = 'compiled', 'VERSION', 'version_info'

VERSION = '1.10.26'

try:
    import cython  # type: ignore
except ImportError:
    compiled: bool = False
else:  # pragma: no cover
    try:
        compiled = cython.compiled
    except AttributeError:
        compiled = False


def version_info() -> str:
    pass
