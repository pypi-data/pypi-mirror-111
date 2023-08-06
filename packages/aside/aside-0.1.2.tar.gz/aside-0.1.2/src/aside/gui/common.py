"""Contains common functions and variables for GUI layout."""

from typing import Callable, Dict

from PyQt5.QtCore import QEasingCurve, QVariant, QVariantAnimation
from PyQt5.QtGui import QIcon, QPixmap

from ..resources import get_svg

__all__ = [
    "STYLE_SHEET_NAME",
    "get_icon",
    "setup_animation",
]


STYLE_SHEET_NAME: str = "style_sheet.qss"
"""The style sheet resource name.

:meta hide-value:
"""

_get_icon_cache: Dict[str, QIcon] = {}
"""A cache for svg resource `QIcon`s, loaded by name.

:meta hide-value:
"""


def get_icon(name: str) -> QIcon:
    """Create a :py:class:`QIcon` from an svg resource.

    Args:
        name: The name of svg resource (without file extension).

    Returns:
        The created :py:class:`QIcon`.
    """
    icon = _get_icon_cache.get(name, None)
    if icon is None:
        pixmap = QPixmap()
        pixmap.loadFromData(get_svg(name))
        icon = QIcon()
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        _get_icon_cache[name] = icon
    return icon


def setup_animation(
    anim: QVariantAnimation,
    duration: int,
    start_value: QVariant,
    end_value: QVariant,
    on_change_value: Callable[[QVariant], None],
    easing_curve: QEasingCurve = QEasingCurve.OutCubic,
) -> None:
    """Set parameters of the specified animation.

    Args:
        anim: Animation that is going to be set up.
        duration: Duration of animation in msec.
        start_value: Initial value of widget property, which will be animated.
        end_value: Resulting value of widget property, which will be animated.
        on_change_value: Callable, executed when animated value has changed.
        easing_curve: Easing curve for animation.
    """
    anim.setDuration(duration)
    anim.setStartValue(start_value)
    anim.setEndValue(end_value)
    if on_change_value is not None:
        anim.valueChanged.connect(on_change_value)
    anim.setEasingCurve(easing_curve)
