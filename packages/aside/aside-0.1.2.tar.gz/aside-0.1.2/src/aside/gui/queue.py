"""Contains layouts for queue and queue header."""

from typing import Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractAnimation, Qt, QVariant, QVariantAnimation

from ..boilerplate.observable import Event, EventType
from ..models import models
from .common import get_icon, setup_animation
from .task import Task

__all__ = [
    "QueueHeader",
    "Queue",
]


class QueueHeader(QtWidgets.QFrame):
    """Horizontal container that stores queue name and control buttons."""

    def __init__(self, queue_model: models.Queue, *args: Any, **kwargs: Any):
        """Initialize queue header."""
        super().__init__(*args, **kwargs)
        self.model = queue_model
        self.collapse_queue = QtWidgets.QToolButton(self)
        self.collapse_queue.setIcon(get_icon("queue"))
        self.collapse_queue.setProperty("class", "CollapseQueue")
        self.name = QtWidgets.QLineEdit(self)
        self.name.editingFinished.connect(self.on_finish_editing_queue_name)

        self.add_task = QtWidgets.QToolButton(self)
        self.add_task.setIcon(get_icon("add"))

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.addWidget(self.collapse_queue)
        self.horizontal_layout.addWidget(self.name)
        self.horizontal_layout.addWidget(self.add_task)

        self.model.subscribe(
            self.queue_name_observer,
            "name",
            event_types=[EventType.CHANGE],
        )

    def on_finish_editing_queue_name(self) -> None:
        """Set queue observer name after editing."""
        self.model.name = self.name.text()

    def queue_name_observer(self, event: Event) -> None:
        """Change GUI queue properties on queue model change.

        Args:
            event: An incoming event for changed property.
        """
        raiser = event.get_nested_object()
        self.name.setText(raiser)


class Queue(QtWidgets.QFrame):
    """Vertical container that stores tasks organized in a queue."""

    def __init__(self, queue_model: models.Queue, *args: Any, **kwargs: Any):
        """Initialize queue.

        Args:
            queue_model: Observable model for tracking property changes.
        """
        super().__init__(*args, **kwargs)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.model = queue_model
        self.header = QueueHeader(queue_model, self)
        self.header.add_task.clicked.connect(self.on_task_addition)
        self.tasks_frame = QtWidgets.QFrame(self)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.tasks_frame.setSizePolicy(size_policy)

        self.vertical_layout.addWidget(self.header, 0, Qt.AlignTop)
        self.vertical_layout.addWidget(self.tasks_frame)

        self.vertical_task_layout = QtWidgets.QVBoxLayout(self.tasks_frame)
        self.vertical_task_layout.setAlignment(Qt.AlignTop)
        self.vertical_task_layout.addStretch(0)

        self.hiding_animation = QVariantAnimation(self)
        setup_animation(self.hiding_animation, 750, 1.0, 0.0, self.set_height)
        self.header.collapse_queue.clicked.connect(self.toggle_collapse_queue)
        self.hiding_animation.finished.connect(self.reset_size_constraints)

        self.model.tasks.subscribe(
            self.queue_add_task_observer,
            event_types=[EventType.ADD],
        )

        self.model.tasks.subscribe(
            self.queue_change_task_observer,
            event_types=[EventType.ADD, EventType.CHANGE],
            order=10,  # run after other observers
        )

        self.model.tasks.subscribe(
            self.queue_delete_task_observer,
            event_types=[EventType.DISCARD],
        )

    def toggle_collapse_queue(self) -> None:
        """React to collapse_queue button click by hiding/showing tasks_frame."""
        if self.tasks_frame.height() == 0:  # is hidden
            self.hiding_animation.setDirection(QAbstractAnimation.Backward)
            self.hiding_animation.start()
            self.tasks_frame.setEnabled(True)
            self.header.collapse_queue.setIcon(get_icon("queue"))
        else:
            self.hiding_animation.setDirection(QAbstractAnimation.Forward)
            self.hiding_animation.start()
            self.tasks_frame.setEnabled(False)
            self.header.collapse_queue.setIcon(get_icon("queue_closed"))

    def set_height(self, val: QVariant) -> None:
        """Change the height of tasks_frame on collapsing.

        Args:
            val: Multiplier in range [0,1] for height-to-be-set.
        """
        height = int(val * self.tasks_frame.minimumSizeHint().height())
        self.tasks_frame.setFixedHeight(height)

    def reset_size_constraints(self):
        """Reset fixed height for tasks_frame widget after un-collapsing."""
        if self.hiding_animation.direction() == QAbstractAnimation.Backward:
            self.tasks_frame.setMaximumSize(
                QtWidgets.QWIDGETSIZE_MAX,
                QtWidgets.QWIDGETSIZE_MAX,
            )
            self.tasks_frame.setMinimumSize(0, 0)

    def on_task_addition(self) -> None:
        """React to add_task button click by adding new task with animation."""
        if not self.tasks_frame.isEnabled():
            return
        self.model.tasks.add(models.Task())

    def queue_add_task_observer(self, event: Event) -> None:
        """Add new task to GUI on model change.

        Args:
            event: An incoming event for changed property.
        """
        task = Task(event.get_nested_object(), self.tasks_frame)
        task.setFixedHeight(0)
        self.vertical_task_layout.insertWidget(0, task)
        task.adding_animation.start()

    def queue_change_task_observer(self, event: Event) -> None:
        """Reorder currently existing tasks on model change.

        Args:
            event: An incoming event for changed property.
        """
        del event

        current_tasks = []
        while True:
            item = self.vertical_task_layout.takeAt(0)
            item = item if item is None else item.widget()
            if item is None:
                break
            current_tasks.append(item)

        current_tasks = sorted(current_tasks, key=Task.queue_order_key, reverse=True)
        for task in current_tasks:
            self.vertical_task_layout.insertWidget(0, task)

    def queue_delete_task_observer(self, event: Event) -> None:
        """Delete a task on model change.

        Args:
            event: An incoming event for changed property.
        """
        attr_name = event.attr_name
        for widget in self.tasks_frame.findChildren(Task):
            if widget.model.uuid == attr_name:
                widget.start_fading_out_task()
                break
