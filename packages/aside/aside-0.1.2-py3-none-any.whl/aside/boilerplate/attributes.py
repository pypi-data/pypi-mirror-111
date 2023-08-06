"""Convenience wrappers around attr-style dataclasses."""

from functools import partial, wraps
from typing import TYPE_CHECKING, List

import attr
import attrs_strict

__all__ = [
    "attrs",
    "attrib",
]


def set_default_attribs(
    cls: type,
    fields: List["Attribute"],
) -> List["Attribute"]:
    """Initialize all fields with kwargs from the default `attrib` preset.

    See :any:`attrs:transform-fields` for more info.
    """
    del cls
    return [f.evolve(**attrib.keywords) for f in fields]


if TYPE_CHECKING:
    from attr import Attribute

    # ToDo: inline these type hints after Python3.6 is deprecated
    _attrs: partial[attr.s]
    attrib: partial[attr.ib]


_attrs = partial(
    attr.s,
    auto_attribs=True,
    collect_by_mro=True,
    field_transformer=set_default_attribs,
    kw_only=True,
    on_setattr=[
        attr.setters.convert,
        attr.setters.validate,
    ],
)


@wraps(_attrs, assigned=("__annotations__",), updated=())
def attrs(maybe_cls=None, **kwargs):
    """:py:func:`attr.s` but with our preferred default kwargs preset."""
    if maybe_cls is None:
        return partial(attrs, **kwargs)

    cls = _attrs(maybe_cls, **kwargs)

    for field in cls.__attrs_attrs__:
        if field.default is not attr.NOTHING:
            setattr(cls, field.name, field.default)

    return cls


attrib = partial(
    attr.ib,
    validator=attrs_strict.type_validator(),
)
""":py:func:`attr.ib` but with our preferred default kwargs preset."""
