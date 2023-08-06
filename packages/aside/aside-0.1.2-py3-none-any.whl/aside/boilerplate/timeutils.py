"""Implements human-readable datetime tools."""

from datetime import datetime
from typing import Dict, Optional

from arrow import Arrow
from dateparser import parse

__all__ = [
    "relative_to_absolute",
    "absolute_to_relative",
]


dateparser_settings: Dict = dict(
    RETURN_AS_TIMEZONE_AWARE=True,
    DATE_ORDER="DMY",
    PREFER_DAY_OF_MONTH="first",
    PREFER_DATES_FROM="future",
    PARSERS=["relative-time", "absolute-time"],
)


def relative_to_absolute(relative: str) -> Optional[datetime]:
    """Try to convert a relative time string like ``in 1 hour`` to a ``datetime``."""
    return parse(
        relative,
        settings=dateparser_settings,
    )


def absolute_to_relative(absolute: datetime) -> str:
    """Convert a ``datetime`` to a relative time string."""
    return Arrow.fromdatetime(absolute).humanize()
