"""Contains tasks layout."""

from datetime import datetime
from typing import Any, Tuple

from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    Qt,
    QVariant,
    QVariantAnimation,
)

from ..boilerplate.observable import Event, EventType
from ..boilerplate.timeutils import absolute_to_relative, relative_to_absolute
from ..models import models
from .common import get_icon, setup_animation

__all__ = [
    "Task",
]


class Task(QtWidgets.QFrame):
    """Horizontal container that stores information about task."""

    def __init__(
        self,
        task_model: models.Task,
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize task.

        Args:
            task_model: Observable model for tracking changes of task.
        """
        super().__init__(*args, **kwargs)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.model = task_model

        self.button = QtWidgets.QToolButton(self)
        self.button.setIcon(get_icon("task"))
        self.button.clicked.connect(self.on_task_change_state)

        self.description = QtWidgets.QLineEdit(self)
        self.description.setProperty("class", "TaskText")
        self.description.editingFinished.connect(
            self.on_finish_editing_task_description
        )

        self.time = QtWidgets.QLineEdit(self)
        self.time.setProperty("class", "TaskTime")
        self.time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time.editingFinished.connect(self.on_finish_editing_task_time)

        self.delete_button = QtWidgets.QToolButton(self)
        self.delete_button.setIcon(get_icon("delete"))
        self.delete_button.clicked.connect(self.on_task_deletion)
        self.delete_button.hide()

        self.horizontal_layout.addWidget(self.button)
        self.horizontal_layout.addWidget(self.description)
        self.horizontal_layout.addWidget(self.time)
        self.horizontal_layout.addWidget(self.delete_button)

        self.adding_animation = QVariantAnimation(self)
        setup_animation(
            self.adding_animation,
            750,
            0.0,
            1.0,
            self.set_task_height,
        )

        effect = QtWidgets.QGraphicsOpacityEffect()
        effect.setOpacity(1.0)
        self.setGraphicsEffect(effect)
        fading_animation = QPropertyAnimation(effect, b"opacity")
        setup_animation(
            fading_animation,
            750,
            1.0,
            0.0,
            None,
        )
        hiding_animation = QVariantAnimation(self)  # FIXME can be optimized
        setup_animation(
            hiding_animation,
            750,
            1.0,
            0.0,
            self.set_task_height,
        )
        self.delete_animation = QParallelAnimationGroup(self)
        self.delete_animation.addAnimation(fading_animation)
        self.delete_animation.addAnimation(hiding_animation)
        self.delete_animation.finished.connect(self.delete_task_gui)

        self.model.subscribe(
            self.task_text_observer,
            "text",
            event_types=[EventType.CHANGE],
        )
        self.model.subscribe(
            self.task_time_observer,
            "deadline",
            event_types=[EventType.CHANGE],
        )

        self.model.subscribe(
            self.task_state_observer,
            "done",
            event_types=[EventType.CHANGE],
        )

    def queue_order_key(self) -> Tuple[bool, datetime, str, str]:
        """Construct the key, that is used for ordering tasks in the queue."""
        return (
            self.model.done,
            self.model.deadline,
            self.model.text,
            self.model.uuid,
        )

    def set_task_height(self, val: QVariant) -> None:
        """Change task widget height on adding new task to the queue.

        Args:
            val: Multiplier in range [0,1] for height-to-be-set.
        """
        height = int(val * self.minimumSizeHint().height())
        self.setFixedHeight(height)

    def update_task_time(self):
        self.time.setText(absolute_to_relative(self.model.deadline))

    def on_finish_editing_task_description(self) -> None:
        """Set task observer description text after editing."""
        self.model.text = self.description.text()

    def on_finish_editing_task_time(self) -> None:
        """Set task observer time after editing."""
        date_deadline = relative_to_absolute(self.time.text())
        if date_deadline is not None:
            self.model.deadline = date_deadline
        else:
            self.update_task_time()

    def task_text_observer(self, event: Event) -> None:
        """Change GUI task description on task model change.

        Args:
            event: An incoming event for changed property.
        """
        self.description.setText(event.get_nested_object())

    def task_time_observer(self, event: Event) -> None:
        """Change GUI task time on task model change.

        Args:
            event: An incoming event for changed property.
        """
        del event
        self.update_task_time()

    def on_task_change_state(self) -> None:
        self.model.done = not self.model.done

    def task_state_observer(self, event: Event) -> None:
        state = event.get_nested_object()
        if state:
            self.button.setIcon(get_icon("task_done"))
            self.time.hide()
            self.delete_button.show()
        else:
            self.button.setIcon(get_icon("task"))
            self.time.show()
            self.delete_button.hide()

    def on_task_deletion(self):
        parent_queue = self.parent().parent()
        parent_queue.model.tasks.discard(self.model)

    def start_fading_out_task(self):
        self.delete_animation.start()

    def delete_task_gui(self):
        self.deleteLater()
