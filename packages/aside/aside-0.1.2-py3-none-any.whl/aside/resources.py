"""Manages the package resource files."""

try:
    from importlib.abc import Traversable
except ImportError:
    from importlib_resources.abc import Traversable

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from .config import config
from .theme import theme

__all__ = [
    "get_resource",
    "get_svg",
]


root: Traversable = files(__package__) / "_resources"
"""The root traversable resource location.

See :any:`importlib_resources<importlib_resources:using>`
and :py:mod:`importlib.resources` for more information.

:meta hide-value:
"""


def str_replace_swap(string: str, this: str, that: str) -> str:
    """Replace all ``this`` and ``that`` tokens in the ``string``, swapping them."""
    # Sanity checks
    assert "%placeholder%" not in string
    assert this != that
    assert this not in that

    string = string.replace(this, "%placeholder%")
    string = string.replace(that, this)
    string = string.replace("%placeholder%", that)

    return string


def find_resource(
    name: str,
    interpolated: bool,
) -> Traversable:
    """Find the resource location given the resource name.

    See `get_resource` for more info.
    """
    res = [name]

    if interpolated:
        res.extend([n + ".int" for n in res])

    res = [root / n for n in res]
    res = [p for p in res if p.exists()]
    if not res:
        raise RuntimeError(f"Missing resource '{name}'")

    return res[-1]


def load_resource(
    path: Traversable,
    do_interpolate: bool,
) -> str:
    """Load the resource contents given the traversable resource path.

    See `get_resource` for more info.
    """
    contents = path.read_text(encoding="utf-8")

    if do_interpolate:
        contents = str_replace_swap(contents, "{{", "{")
        contents = str_replace_swap(contents, "}}", "}")
        contents = contents.format(config=config, theme=theme)

    return contents


def get_resource(
    name: str,
    interpolated: bool = True,
) -> str:
    """Find and load the resource given its name.

    This function also takes into account interpolatable resource overrides.

    **Interpolatable** resources are resource files which have an extra ``.int``
    file extension. After loading an interpolatable resource, all strings of the
    form ``{{config.something}}`` and ``{{theme.other}}`` are interpolated with
    the values from the current `aside.config.config` and `aside.theme.theme`.

    Args:
        name: The name of the resource to load.
        interpolated: Whether to search for interpolatable resources.

    Returns:
        The loaded resource contents.
    """
    res = find_resource(name, interpolated=interpolated)
    res = load_resource(res, do_interpolate=res.suffix == ".int")
    return res


def get_svg(name: str) -> bytes:
    """Find and load an svg resource specified by ``name``.

    Args:
        name: The name of the svg resource without the file extension.

    Returns:
        The contents of the resource, suitable to be loaded with
        :py:meth:`PyQt5.QtGui.QPixmap.loadFromData`.
    """
    return get_resource(name + ".svg").encode()
