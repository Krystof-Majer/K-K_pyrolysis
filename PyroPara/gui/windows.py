from os.path import join

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QSplitter,
    QPushButton,
    QVBoxLayout,
)


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
        self.button_widget: QPushButton

        self.L_R_layout = QVBoxLayout()

        self.create_left_panel()
        self.create_right_panel()
        self.create_middle_panel()
        self.setup_ui()

    def create_left_panel(self):
        self.left_panel = QSplitter(Qt.Vertical)
        self.left_panel.setChildrenCollapsible(False)

    def create_right_panel(self):
        self.right_panel = QSplitter(Qt.Vertical)
        self.right_panel.setChildrenCollapsible(False)

    def create_middle_panel(self):
        pass

    def setup_ui(self) -> None:
        # setting up main widget
        self.main_widget = QSplitter(Qt.Horizontal)
        self.main_widget.setChildrenCollapsible(False)
        self.setCentralWidget(self.main_widget)

        # setting up left panel
        self.sta_files_widget = QListWidget()
        self.menu_bar = self.menuBar()
        self.run_button = QPushButton("Run")
        self.left_panel.addWidget(self.sta_files_widget)
        self.left_panel.addWidget(self.run_button)

        # setting up middle panel
        self.plot_widget = PlotWidget()
        self.plot_widget.grid(visible=True)
        self.plot_widget.plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "r-")

        # setting up right panel
        self.local_minima_list = QListWidget()
        self.right_panel.addWidget(self.local_minima_list)

        # setting up main widget
        self.main_widget.addWidget(self.left_panel)
        self.main_widget.addWidget(self.plot_widget)
        self.main_widget.addWidget(self.right_panel)

        self.main_widget.setStretchFactor(0, 1)
        self.main_widget.setStretchFactor(1, 3)

        self.create_menus()
        self.button_actions()

    def create_menus(self) -> None:
        self.create_file_menu()

    def create_file_menu(self) -> None:
        file_menu = self.menu_bar.addMenu("&File")

        self.read_menu_action = QAction(
            get_icon("open"), "Read STA files...", self
        )
        self.read_menu_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_R))

        file_menu.addAction(self.read_menu_action)

    def button_actions(self) -> None:
        self.run_button_widget()

    def run_button_widget(self):
        self.run_button_action = QAction(self)
        self.run_button_action.setShortcut(Qt.Key_F1)
        self.run_button.addAction(self.run_button_action)
