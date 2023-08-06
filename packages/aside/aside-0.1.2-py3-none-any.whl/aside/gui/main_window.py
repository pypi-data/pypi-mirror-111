"""Contains main window layout."""

from typing import Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Qt, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap

from ..boilerplate.hooks import get_user_hook_dir, load_user_hooks
from ..boilerplate.observable import Event, EventType
from ..models import models
from ..models.database import Database
from ..resources import get_resource, get_svg
from .common import STYLE_SHEET_NAME, get_icon
from .queue import Queue
from .task import Task

__all__ = [
    "AsideWindow",
    "main",
]


def open_info() -> None:
    """Open the official stable documentation in the users default browser."""
    documentation_url = QUrl("https://aside.rtfd.io/en/stable")
    QDesktopServices.openUrl(documentation_url)


def open_settings() -> None:
    """Open the user hook directory with the users default file manager."""
    user_hook_dir = get_user_hook_dir()
    user_hook_url = QUrl(str(user_hook_dir))
    QDesktopServices.openUrl(user_hook_url)


class AsideWindow(QtWidgets.QMainWindow):
    """Main window of the app."""

    def __init__(
        self, queue_manager_model: models.QueueManager, *args: Any, **kwargs: Any
    ):
        """Initialize main window.

        Args:
            queue_manager_model: Observable model for tracking changes of window.
        """
        super().__init__(*args, **kwargs)
        self.resize(653, 700)
        self.setWindowIcon(get_icon("icon"))
        self.setWindowTitle("aside")
        self.setStyleSheet(get_resource(STYLE_SHEET_NAME))
        self.model = queue_manager_model
        self.timer = QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update_all_timers)
        self.timer.start()

        self.central_widget = QtWidgets.QWidget(self)
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.scrollable_wrapper = QtWidgets.QScrollArea(self.central_widget)
        self.scrollable_wrapper.setWidgetResizable(True)
        self.queue_frame = QtWidgets.QFrame(self.central_widget)
        self.queue_layout = QtWidgets.QVBoxLayout(self.queue_frame)

        self.logo = QtWidgets.QLabel(self.central_widget)
        self.logo.setObjectName("Logo")
        pixmap = QPixmap()
        pixmap.loadFromData(get_svg("logo"))
        pixmap = pixmap.scaledToHeight(125, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)

        self.settings = QtWidgets.QToolButton(self.central_widget)
        self.settings.setIcon(get_icon("settings"))
        self.settings.clicked.connect(open_settings)
        self.info = QtWidgets.QToolButton(self.central_widget)
        self.info.setIcon(get_icon("info"))
        self.info.clicked.connect(open_info)
        self.add_queue = QtWidgets.QToolButton(self.central_widget)
        self.add_queue.setIcon(get_icon("queue_add"))
        self.add_queue.clicked.connect(self.on_adding_queue)

        self.grid_layout.addWidget(self.logo, 0, 0, 3, 2, Qt.AlignCenter)
        self.grid_layout.addWidget(self.info, 0, 2)
        self.grid_layout.addWidget(self.settings, 1, 2)
        self.grid_layout.addWidget(self.add_queue, 2, 2)

        self.queue_layout.setAlignment(Qt.AlignTop)
        self.queue_layout.addStretch(1)

        self.scrollable_wrapper.setWidget(self.queue_frame)
        self.grid_layout.addWidget(self.scrollable_wrapper, 3, 0, 1, 3)
        self.setCentralWidget(self.central_widget)

        self.model.queues.subscribe(
            self.manager_add_queue_observer,
            regexp="[^/]*",
            event_types=[EventType.ADD],
        )

        self.model.queues.subscribe(
            self.manager_delete_queue_observer,
            regexp="[^/]*",
            event_types=[EventType.DISCARD],
        )

        QMetaObject.connectSlotsByName(self)

    def on_adding_queue(self):
        self.model.queues.add(models.Queue())

    def manager_add_queue_observer(self, event: Event) -> None:
        """Add new queue to GUI on model change.

        Args:
            event: An incoming event for changed property.
        """
        queue = Queue(event.get_nested_object(), self.queue_frame)
        self.queue_layout.insertWidget(0, queue)

    def manager_delete_queue_observer(self, event: Event) -> None:
        """Delete a queue on model change.

        Args:
            event: An incoming event for changed property.
        """
        attr_name = event.attr_name
        for widget in self.queue_frame.findChildren(Queue):
            if widget.model.uuid == attr_name:
                widget.deleteLater()
                break

    def update_all_timers(self) -> None:
        """Update the human-readable timer on all tasks."""
        for task in self.findChildren(Task):
            if task.time.isVisible() and not task.time.hasFocus():
                task.update_task_time()


def main(*argv: str) -> int:  # pragma: no cover
    """Execute the main GUI entrypoint."""
    load_user_hooks()
    app = QtWidgets.QApplication(list(argv))
    aside_window = AsideWindow(models.queue_manager)
    aside_window.show()
    with Database(models.queue_manager):
        return app.exec_()
