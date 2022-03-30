from os.path import join

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
)


from PyroPara import BASE_DIR, __version__


def get_icon(name):
    return QIcon(join(BASE_DIR, f"gui/icons/{name}.png"))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.main_widget: QWidget = QWidget()
        self.main_layout: QGridLayout = QGridLayout()

        self.setup_ui()

    def setup_ui(self) -> None:
        # setting up main widget
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

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
