"""Manages the application configuration."""

from .boilerplate import attrs, hooks

__all__ = [
    "config",
    "register_config",
]


@attrs
class Config:
    """Application configuration specification."""

    verbose: bool = False
    """If enabled, print status/debugging information."""


config: Config = Config()
"""The current application configuration.

Can be overwritten by user with the `register_config` decorator.

:meta hide-value:
"""


def register_config(changed: type) -> object:
    """Mark decorated class as a user config overwrite declaration.

    Example:
        .. code-block:: python

            from aside.config import register_config

            @register_config
            class MyConfig:
                some_changed_setting = "my_custom_value"
    """
    return hooks.update_attrs(
        default=config,
        changed=changed,
        name="configuration",
        verbose=getattr(changed, "verbose", False) or config.verbose,
    )
