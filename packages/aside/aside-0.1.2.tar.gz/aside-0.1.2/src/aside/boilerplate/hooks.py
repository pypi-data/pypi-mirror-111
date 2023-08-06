"""Common code for user hooks."""

from importlib import util
from os import PathLike
from typing import Any, Dict, List, Optional, Tuple

from xdg import xdg_config_dirs, xdg_config_home

__all__ = [
    "update_attrs",
    "load_user_hooks",
    "get_user_hook_dir",
]


def public_attrs(obj: object) -> Dict[str, Any]:
    """Extract all object attributes and values, which are considered public."""
    return {attr: val for attr, val in vars(obj).items() if not attr.startswith("_")}


def update_attrs(default: object, changed: type, name: str, verbose: bool):
    """Propagate the user-defined attribute changes to the default object."""
    if verbose:
        print(f"Loading {name} from user overwrite {changed}")

    default_attrs = public_attrs(default)
    changed_attrs = public_attrs(changed)

    unknown = set(changed_attrs) - set(default_attrs)
    if unknown:
        raise AttributeError(f"Unknown {name} attributes: {', '.join(unknown)}.")

    for attr in default_attrs:
        if attr in changed_attrs:
            # Update the changed attribute
            val = changed_attrs[attr]
            if verbose:
                print(f"Setting {name} attribute {attr}={val!r}")
            setattr(default, attr, val)
        else:
            # Populate the user overwrite with the default value
            # (this is probably pointless, but we do it just in case)
            setattr(changed, attr, default_attrs[attr])

    return default


def load_user_hooks(hook_dirs: Optional[List[PathLike]] = None) -> None:
    """Import and load the user hook files.

    User hook files are searched in all the configuration directories, as
    specified by the `XDG Base Directory Specification`_. The hook files
    (if present) are loaded in the following order:

    - ``aside/**.py`` in every directory specified in ``${XDG_CONFIG_DIRS}``
      in order of preference
    - ``${XDG_CONFIG_HOME}/aside/**.py``

    The hook files in each directory are imported and evaluated in lexicographic
    order. To overwrite the application configuration and theme, the
    `aside.config.register_config` and `aside.theme.register_theme` hooks can be
    used.

    .. _XDG Base Directory Specification: \
        https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest
    """
    # load current config on-demand to avoid circular import
    from ..config import config  # pylint: disable=import-outside-toplevel

    if hook_dirs is None:  # pragma: no cover
        hook_dirs = xdg_config_dirs()[::-1] + [xdg_config_home()]

    for hook_dir in hook_dirs:
        hook_dir = hook_dir / __package__.split(".", 1)[0]
        if config.verbose:
            print(f"Searching for hooks in {hook_dir}.")

        hook_paths = hook_dir.rglob("*.py")
        for hook_path in sorted(hook_paths):
            hook_path = str(hook_path)
            if config.verbose:
                print(f"Loading hooks from {hook_path}.")

            try:
                spec = util.spec_from_file_location(hook_path, hook_path)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)

            except Exception as exc:
                raise RuntimeError(
                    f"Failed to load user hooks from {hook_path}."
                ) from exc


def make_default_class_def(cls: type) -> Tuple[str, str]:
    """Generate default imports and ``register_*`` class definition for ``cls``."""
    clsname = cls.__name__
    modname = clsname.lower()
    imports_ = f"from aside.{modname} import register_{modname}\n"
    register = f"@register_{modname}\n"
    cls_head = f"class {clsname}:\n"
    cls_attr = cls.__attrs_attrs__
    just = max(len(attr.name) for attr in cls_attr)

    attrs = [f"    {attr.name:<{just}} = {attr.default!r}\n" for attr in cls_attr]
    return (
        imports_,
        "".join([register, cls_head] + attrs),
    )


def get_user_hook_dir(
    init_missing: bool = True,
    hook_dir: Optional[PathLike] = None,
) -> PathLike:
    """Get the default user hook directory.

    Args:
        init_missing: Whether to initialize the user hook directory if it's missing.
        hook_dir: Use this directory instead of the ``${XDG_CONFIG_HOME}``.

    """
    hook_dir = (xdg_config_home() if hook_dir is None else hook_dir) / "aside"
    if init_missing and not hook_dir.exists():
        hook_dir.mkdir(parents=True)

        # load config and theme defaults on-demand to avoid circular import
        from ..config import Config  # pylint: disable=import-outside-toplevel
        from ..theme import Theme  # pylint: disable=import-outside-toplevel

        header = []
        content = []

        for cls in [Config, Theme]:
            imports, body = make_default_class_def(cls)
            header.append(imports)
            content.append(body)

        header.append(
            "\n\n"
            "# We have initialized a default hook configuration file for you.\n"
            "# You can customize aside by changing the default values below.\n"
            "# For more information, see\n"
            "# https://aside.rtfd.io/en/stable/usrdoc/02-configuration/\n"
        )

        header = "".join(header)
        content = "\n\n".join(content)

        (hook_dir / "config.py").write_text(header + "\n\n" + content)
    return hook_dir
