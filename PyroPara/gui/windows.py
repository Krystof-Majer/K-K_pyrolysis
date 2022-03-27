from os.path import join
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

from PyroPara import BASE_DIR, __version__
from PyroPara.gui.panel.plot_panel import PlotPanel


def get_icon(name):
    return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))


class MainWindow(QMainWindow):
    def __init__(self, *, plot_panel: PlotPanel = None) -> None:
        super().__init__()
        self.plot_panel = plot_panel

        self.main_widget: QWidget = QWidget()
        self.main_layout: QGridLayout = QGridLayout()

        self.sta_files_widget: QListWidget = QListWidget()
        self.plot_button: QPushButton = QPushButton("Plot")

        self.menu_bar = self.menuBar()
        self.read_menu_action: QAction

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # self.plot_widget.plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "r-")

        buttons_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        self.set_button_enabled(self.plot_button, is_enabled=False)
        buttons_layout.addItem(horizontal_spacer)
        buttons_layout.addWidget(self.plot_button)

        self.sta_files_widget.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.main_layout.addWidget(self.sta_files_widget, 0, 0, 1, 1)
        self.main_layout.addLayout(buttons_layout, 1, 0, 1, 1)
        self.main_layout.addWidget(self.plot_panel, 0, 1, 2, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 6)

        self.create_menus()

    def create_menus(self) -> None:
        self.create_file_menu()

    def create_file_menu(self) -> None:
        file_menu = self.menu_bar.addMenu("&File")

        self.read_menu_action = QAction(
            get_icon("open"), "Read STA files...", self
        )
        self.read_menu_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_R))

        file_menu.addAction(self.read_menu_action)

    @property
    def selected_files(self) -> List[int]:
        selected_indices = self.sta_files_widget.selectedIndexes()

        return sorted(index.row() for index in selected_indices)

    def set_button_enabled(self, button, *, is_enabled=True) -> None:
        button.setEnabled(is_enabled)
