from os.path import join

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QWidget,
)


from PyroPara import BASE_DIR, __version__
from PyroPara.gui.plot.plot_panel import PlotPanel
from PyroPara.gui.controls.control_buttons_widget import ControlButtons
from PyroPara.gui.controls.file_select_widget import FileSelectWidget


def get_icon(name):
    return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))


class MainWindow(QMainWindow):
    def __init__(self, *, plot_panel: PlotPanel = None) -> None:
        super().__init__()
        self.plot_panel = plot_panel
        self.main_widget: QWidget = QWidget()
        self.main_layout: QGridLayout = QGridLayout()

        self.sta_files_widget: FileSelectWidget = FileSelectWidget()
        self.control_buttons_widget: ControlButtons = ControlButtons()

        self.menu_bar = self.menuBar()
        self.read_menu_action: QAction

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.main_layout.addWidget(self.sta_files_widget, 0, 0)
        self.main_layout.addLayout(
            self.control_buttons_widget.buttons_layout, 1, 0
        )
        self.main_layout.addWidget(self.plot_panel, 0, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 6)

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
