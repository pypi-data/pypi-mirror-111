"""Manages the application theme."""

from .boilerplate import attrs, hooks
from .config import config

__all__ = [
    "theme",
    "register_theme",
]


@attrs
class Theme:
    """Application theme specification."""

    # ToDo: validate/convert colors

    background_color: str = "rgb(245, 240, 225)"
    """The css background color of the window."""

    icon_circle_color: str = "rgb(254, 250, 239)"
    """The css color of icon circles."""

    icon_circle_hi_color: str = "rgb(206, 206, 206)"
    """The css color of icon circle highlights."""

    icon_content_color: str = "rgb(209, 86, 47)"
    """The css color of icon contents."""

    icon_accent_content_color: str = "rgb(30, 61, 89)"
    """The css color of accentuated icon contents."""

    icon_positive_content_color: str = "rgb(29, 224, 62)"
    """The css color of positive icon contents."""

    icon_negative_content_color: str = "rgb(224, 18, 59)"
    """The css color of negative icon contents."""

    icon_text_color: str = "rgb(30, 61, 89)"
    """The css color of icon text."""

    icon_shadow_alpha: float = 0.4
    """The css alpha of icon shadow."""

    text_color: str = "rgb(30, 61, 89)"
    """The css color for application text."""


theme: Theme = Theme()
"""The current application theme.

Can be overwritten by user with the `register_theme` decorator.

:meta hide-value:
"""


def register_theme(changed: type) -> object:
    """Mark decorated class as a user theme overwrite declaration.

    Example:
        .. code-block:: python

            from aside.theme import register_theme

            @register_theme
            class MyTheme:
                some_element_color = "#ff0000"
    """
    return hooks.update_attrs(
        default=theme,
        changed=changed,
        name="theme",
        verbose=config.verbose,
    )
