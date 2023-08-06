"""Observable data models for aside."""

from datetime import datetime

import attr

from ..boilerplate.attributes import attrib, attrs
from ..boilerplate.observable import (
    Observable,
    ObservableCollection,
    observable,
    uuid_attrib,
)

__all__ = [
    "Task",
    "Queue",
    "QueueManager",
    "queue_manager",
]


def here_and_now() -> datetime:
    """Initialize the datetime with current time and timezone."""
    return datetime.now().replace(microsecond=0).astimezone()


@observable
@attrs
class Task(Observable):
    """Data model for an individual task."""

    uuid: str = uuid_attrib()
    text: str = ""
    done: bool = False
    deadline: datetime = attrib(factory=here_and_now)


@observable
@attrs
class Queue(Observable):
    """Data model for a queue of tasks."""

    uuid: str = uuid_attrib()
    name: str = ""
    tasks: ObservableCollection = attrib(
        factory=ObservableCollection,
        converter=ObservableCollection,
        on_setattr=attr.setters.frozen,
    )


@observable
@attrs
class QueueManager(Observable):
    """Data model for the collection of all queues (singleton)."""

    uuid: str = uuid_attrib()
    queues: ObservableCollection = attrib(
        factory=ObservableCollection,
        converter=ObservableCollection,
        on_setattr=attr.setters.frozen,
    )


queue_manager = QueueManager()
