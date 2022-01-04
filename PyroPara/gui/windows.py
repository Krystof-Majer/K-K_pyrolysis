from os.path import join

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow  # type: ignore
from PySide6.QtWidgets import QListWidget, QSplitter

from PyroPara import BASE_DIR, __version__
from PyroPara.gui.base import PlotWidget


def get_icon(name):
    return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)

        self.main_widget: QSplitter

        self.sta_files_widget = QListWidget()
        self.menu_bar = self.menuBar()
        self.read_menu_action: QAction

        self.setup_ui()

    def setup_ui(self) -> None:
        self.main_widget = QSplitter(Qt.Horizontal)
        self.main_widget.setChildrenCollapsible(False)
        self.setCentralWidget(self.main_widget)

        self.plot_widget = PlotWidget()
        self.plot_widget.grid(visible=True)
        self.plot_widget.plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "r-")

        self.main_widget.addWidget(self.sta_files_widget)
        self.main_widget.addWidget(self.plot_widget)

        self.main_widget.setStretchFactor(0, 1)
        self.main_widget.setStretchFactor(1, 3)

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
