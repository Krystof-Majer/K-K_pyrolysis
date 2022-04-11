from os.path import join

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QSplitter

from PyroPara import BASE_DIR, __version__
from PyroPara.gui.controls.left_panel import LeftPanel
from PyroPara.gui.plot.plot_panel import PlotPanel


def get_icon(name):
    return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))


class MainWindow(QMainWindow):
    def __init__(
        self, *, plot_panel: PlotPanel = None, left_panel: LeftPanel = None
    ) -> None:
        super().__init__()
        self.plot_panel = plot_panel
        self.left_panel = left_panel
        self.main_widget: QSplitter = QSplitter(Qt.Horizontal)

        self.menu_bar = self.menuBar()
        self.read_menu_action: QAction

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setChildrenCollapsible(False)

        self.main_widget.addWidget(self.left_panel)
        self.main_widget.addWidget(self.plot_panel)

        self.main_widget.setStretchFactor(0, 1)
        self.main_widget.setStretchFactor(1, 7)

        self.create_menus()

    def create_menus(self) -> None:
        self.create_file_menu()

    def get_icon(name):
        return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))

    def create_file_menu(self) -> None:
        file_menu = self.menu_bar.addMenu("&File")

        self.read_menu_action = QAction(
            get_icon("open"), "Read STA files...", self
        )
        self.read_menu_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_R))

        file_menu.addAction(self.read_menu_action)
