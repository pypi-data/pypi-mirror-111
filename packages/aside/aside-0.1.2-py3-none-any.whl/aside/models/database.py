"""Methods for serialization of Task and Queue."""
import json
import shutil
from datetime import datetime, timezone
from functools import wraps
from os import PathLike
from typing import Optional

import attr
from xdg import xdg_data_home

from aside.models.models import Queue, QueueManager, Task

from ..boilerplate.observable import Event, EventType

__all__ = [
    "Database",
]


def check_locking(func):
    @wraps(func)
    def checked(self: "Database", *args, **kwargs):
        if self.locked:
            return func(self, *args, **kwargs)
        raise RuntimeError("Database is not controlling the lock!")

    return checked


class Database:
    """Serialize into files on disk in tree-like directories."""

    def __enter__(self):
        """Obtain lock on disk database representation."""
        try:
            (self.data_dir / ".lock").touch(exist_ok=False)
        except FileExistsError as exist_err:
            raise RuntimeError("Another aside instance is running!") from exist_err
        self.locked = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock on disk database representation."""
        self.locked = False
        (self.data_dir / ".lock").unlink()

    def __init__(
        self, queue_manager: QueueManager, data_dir: Optional[PathLike] = None
    ):
        """Set up data directory."""
        self.locked = False
        self.data_dir = (xdg_data_home() if data_dir is None else data_dir) / "aside"
        self.data_dir.mkdir(exist_ok=True)
        self.populate_manager_from_disk(queue_manager)
        queue_manager.subscribe(self.observe_queue, "queues/[^/]*")
        queue_manager.subscribe(self.observe_queue_metadata, "queues/[^/]*/[^/]*")
        queue_manager.subscribe(self.observe_task, ".*/tasks/[^/]*")
        queue_manager.subscribe(self.observe_task_metadata, ".*/tasks/[^/]*/[^/]*")

    @check_locking
    def observe_task(self, event: Event):
        """Observe tasks collection events raised by queue manager.

        Regexp string for matching events: ``.*/tasks/[^/]*``
        """
        task_uuid = event.split_attr_path[-1]
        queue = event.get_nested_object(2)
        if event.event_type is EventType.ADD:
            self._dump_task(queue, event.get_nested_object())
        elif event.event_type is EventType.DISCARD:
            self._drop_task(queue, task_uuid)
        else:
            pass  # pragma: no cover

    @check_locking
    def observe_task_metadata(self, event: Event):
        """Observe task events raised by queue manager.

        Regexp string for matching events: ``.*/tasks/[^/]*/[^/]*``
        """
        queue = event.get_nested_object(2)
        if event.event_type is EventType.CHANGE:
            self._dump_task(queue, event.get_nested_object(-1))
        else:
            pass  # pragma: no cover

    @check_locking
    def observe_queue(self, event: Event):
        """Observe queue collection events raised by queue manager.

        Regexp string for matching events: ``queues/[^/]*``
        """
        queue_uuid = event.split_attr_path[-1]
        if event.event_type is EventType.ADD:
            self._dump_queue(event.get_nested_object())
        elif event.event_type is EventType.DISCARD:
            self._drop_queue(queue_uuid)
        else:
            pass  # pragma: no cover

    @check_locking
    def observe_queue_metadata(self, event: Event):
        """Observe queue events raised by queue manager.

        Regexp string for matching events: ``queues/[^/]*/[^/]*``
        """
        if event.event_type is EventType.CHANGE:
            self._dump_queue(event.get_nested_object(-1))
        else:
            pass  # pragma: no cover

    @check_locking
    def _dump_queue(self, queue: Queue):
        self._dump_queue_metadata(queue)
        queue_dir = self.data_dir / queue.uuid
        queue_dir.mkdir(exist_ok=True)
        for task in queue.tasks.keys():
            self._dump_task(queue, queue.tasks[task])

    @check_locking
    def _dump_queue_metadata(self, queue: Queue):
        metadata_dict = attr.asdict(
            queue, filter=lambda x, _: x.name not in queue.__observable_attrs__
        )
        with (self.data_dir / f"{queue.uuid}.json").open("w") as out_file:
            json.dump(metadata_dict, out_file, ensure_ascii=False, indent=4)

    @check_locking
    def _drop_queue(self, queue_uuid: str):
        queue_dir = self.data_dir / queue_uuid
        (self.data_dir / f"{queue_uuid}.json").unlink()
        shutil.rmtree(queue_dir)

    @check_locking
    def _dump_task(self, queue: Queue, task: Task):
        queue_path = self.data_dir / queue.uuid
        queue_path.mkdir(exist_ok=True)

        with (queue_path / f"{task.uuid}.json").open("w") as out_file:
            attr_asdict = attr.asdict(task)
            attr_asdict["deadline"] = (
                attr_asdict["deadline"]
                .astimezone(timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%S")
            )
            json.dump(attr_asdict, out_file, ensure_ascii=False, indent=4)

    @check_locking
    def _drop_task(self, queue: Queue, task_uuid: str):
        (self.data_dir / queue.uuid / f"{task_uuid}.json").unlink()

    def populate_manager_from_disk(self, queue_manager: QueueManager):
        """Take queue manager and fill it with queues from disk."""
        for queue_path in self.data_dir.glob("*.json"):
            with (self.data_dir / queue_path).open("r") as readfile:
                queue_metadata = json.load(readfile)
            queue = Queue(uuid=queue_metadata["uuid"])
            queue_manager.queues.add(queue)
            for k in queue_metadata:
                if not k == "uuid":
                    setattr(queue, k, queue_metadata[k])
            self.populate_queue_from_disk(queue)

    def populate_queue_from_disk(self, queue: Queue) -> None:
        """Read queue by id from disk."""
        for task_path in (self.data_dir / queue.uuid).iterdir():
            with task_path.open("r") as readfile:
                task_metadata = json.load(readfile)
                task_metadata["deadline"] = datetime.strptime(
                    task_metadata["deadline"], "%Y-%m-%dT%H:%M:%S"
                ).astimezone()
                task = Task(uuid=task_metadata["uuid"])
                queue.tasks.add(task)
                for k in task_metadata:
                    if not k == "uuid":
                        setattr(task, k, task_metadata[k])
