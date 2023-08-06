"""Contains implementation of observable-related classes."""

import re
import uuid
from bisect import bisect
from collections.abc import Mapping, MutableSet
from enum import Enum, auto
from functools import partial, reduce, wraps
from operator import getitem
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Pattern,
    Set,
    Type,
    Union,
)

import attr
from typing_extensions import Protocol, runtime_checkable

from .attributes import attrib, attrs

__all__ = [
    "observable",
    "Observable",
    "ObservableCollection",
    "Event",
    "EventType",
    "Observer",
    "uuid_attrib",
]


def uuid_str() -> str:
    """Generate a random UUID and convert it into a string."""
    return str(uuid.uuid4())


uuid_attrib = partial(attrib, factory=uuid_str, on_setattr=attr.setters.frozen)


class EventType(Enum):
    """Possible event types."""

    REASSIGN = auto()
    CHANGE = auto()
    ADD = auto()
    DISCARD = auto()


@attrs
class Event:
    """Describes the cause of the observable event."""

    attr_name: str
    obj: "Observable"
    event_type: EventType

    def get_nested_object(self, level: Optional[int] = None):
        """Get nested object of event.

        Args:
            level: Behaves as a list index, negative indices are valid.
        """
        return reduce(getitem, self.split_attr_path[:level], self.obj)

    @property
    def split_attr_path(self):
        """Get list of consecutive attributes leading to source of event."""
        return self.attr_name.split("/")


# ToDo: replace `Optional[Any]` with `None` after
#       [this PR](https://github.com/bloomberg/attrs-strict/pull/66)
#       gets merged.
# FIXME: attrs_strict won't let partial function pass if we specify Callable prototype
ObserverCallable = Callable  # [[Event], Optional[Any]]


@attrs
class Observer:
    """Contains information about a subscribed observer."""

    callback: ObserverCallable
    regexp: Pattern
    order: int
    event_types: Set[EventType]


@runtime_checkable
class Observable(Protocol):
    """Common protocol/interface for all observable classes."""

    uuid: str
    __observers__: List[Observer]
    _owner_handler: Optional[Callable] = None

    @property
    def __owner_handler__(self) -> Optional[Callable]:
        """Access parent's event forwarding function. Needed for event propagation."""
        return self._owner_handler

    @__owner_handler__.setter
    def __owner_handler__(self, value: Optional[Callable]) -> None:
        if value is not None and self._owner_handler is not None:
            raise AttributeError("Observable object is owned by somebody else!")
        self._owner_handler = value

    def __forward_event__(self, event: Event, child_path):
        """Emit event received from child adjusting event's fields."""
        self.__emit_event__(
            Event(
                attr_name=f"{child_path}/{event.attr_name}",
                obj=self,
                event_type=event.event_type,
            )
        )

    def __emit_event__(self, event: Event) -> None:
        """Call all matching subscribers' callbacks."""
        for observer in self.__observers__:
            if (
                observer.regexp.fullmatch(event.attr_name)
                and event.event_type in observer.event_types
            ):
                observer.callback(event)
        if self.__owner_handler__ is not None:
            self.__owner_handler__(event)

    def subscribe(
        self,
        callback,
        regexp: str = ".*",
        order: int = 0,
        event_types: Optional[Iterable[EventType]] = None,
    ) -> None:
        """Subscribe to changes of Observable object."""
        if event_types is None:
            event_types = {
                EventType.REASSIGN,
                EventType.CHANGE,
                EventType.ADD,
                EventType.DISCARD,
            }
        subscriber = Observer(
            callback=callback,
            regexp=re.compile(regexp),
            order=order,
            event_types=set(event_types),
        )
        self.__observers__.insert(
            bisect([el.order for el in self.__observers__], subscriber.order),
            subscriber,
        )

    def drop_observers(self):
        """Drop list of tracked observers, as if no subscription were ever made."""
        self.__observers__ = []


def wrap_init(old_init: Callable) -> Callable:
    @wraps(old_init)
    def new_init(self, *args, **kwargs) -> None:
        self.__observers__ = []
        old_init(self, *args, **kwargs)
        for name in self.__observable_attrs__:
            getattr(self, name).__owner_handler__ = partial(
                self.__forward_event__, child_path=name
            )

    return new_init


def wrap_setattr(old_setattr: Callable) -> Callable:
    @wraps(old_setattr)
    def observable_setattr(self, name, value) -> None:
        if name not in self.__attrs_names__:
            old_setattr(self, name, value)
            return

        old_value = getattr(self, name)
        is_observable = name in self.__observable_attrs__
        if is_observable:
            old_value.__owner_handler__ = None

        old_setattr(self, name, value)
        new_value = getattr(self, name)

        if old_value == new_value:
            event_type = EventType.REASSIGN
        else:
            event_type = EventType.CHANGE
        self.__emit_event__(Event(attr_name=name, obj=self, event_type=event_type))
        if is_observable:
            new_value.__owner_handler__ = partial(
                self.__forward_event__, child_path=name
            )

    return observable_setattr


def observable(cls: type) -> Union[Type[Observable], type]:
    """Make the attributes of an attrs-style `Observable` class also observable."""
    assert Observable in cls.__bases__

    def observable_getitem(self, name):
        if name in self.__attrs_names__:
            return getattr(self, name)
        raise AttributeError

    cls.__getitem__ = observable_getitem
    cls.__observable_attrs__ = frozenset(
        attr.name for attr in cls.__attrs_attrs__ if Observable in attr.type.__bases__
    )
    cls.__attrs_names__ = frozenset(attr.name for attr in cls.__attrs_attrs__)
    cls.__init__ = wrap_init(cls.__init__)
    cls.__setattr__ = wrap_setattr(cls.__setattr__)
    return cls


# pylint: disable=too-many-ancestors
class ObservableCollection(MutableSet, Mapping, Observable):
    """Observable collection of Observable objects."""

    def __init__(self, init_vals: Optional[Iterable[Observable]] = None):
        """Construct collection and populate it from init_vals, if any."""
        self._storage: Dict[str, Observable] = {}
        self.__observers__: List[Observer] = []
        if init_vals is not None:
            for elem in init_vals:
                self.add(elem)

    def add(self, value: Observable) -> None:
        """Add value to collection, overwriting old value with same UUID, if any."""
        was_already_in = value.uuid in self._storage
        if was_already_in:
            self._storage[value.uuid].__owner_handler__ = None
            if self._storage[value.uuid] == value:
                event_type = EventType.REASSIGN
            else:
                self.discard(value)
                event_type = EventType.ADD
        else:
            event_type = EventType.ADD
        self._storage[value.uuid] = value
        value.__owner_handler__ = partial(self.__forward_event__, child_path=value.uuid)
        self.__emit_event__(
            Event(attr_name=value.uuid, obj=self, event_type=event_type)
        )

    def discard(self, value: Observable) -> None:
        """Discard object with same UUID from collection."""
        if value.uuid in self._storage:
            self._storage[value.uuid].__owner_handler__ = None
            self._storage.pop(value.uuid)
            self.__emit_event__(
                Event(attr_name=value.uuid, obj=self, event_type=EventType.DISCARD)
            )

    def __contains__(self, x: Observable) -> bool:
        """Check if object with same UUID is in collection."""
        return x.uuid in self._storage

    def __getitem__(self, k: str):
        """Get object by it's UUID."""
        return self._storage[k]

    def __len__(self) -> int:
        """Return number of objects on collection."""
        return len(self._storage)

    def __iter__(self) -> Iterator[str]:
        """Return iterator for objects in collection, with no particular order."""
        return iter(self._storage.keys())

    def __repr__(self):
        """Return string representation of collection and its contents.

        Can be `eval`ed to get equal collection.
        """
        return (
            f"ObservableCollection(["
            f"{', '.join(repr(self[elem]) for elem in self.__iter__())}"
            f"])"
        )
