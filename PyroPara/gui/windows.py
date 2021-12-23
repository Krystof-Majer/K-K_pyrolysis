from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow  # type: ignore

from PyroPara import __version__


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)

        self.menu_bar = self.menuBar()
        self.open_menu_action: QAction

        self.setup_ui()

    def setup_ui(self) -> None:
        self.create_menus()

    def create_menus(self) -> None:
        self.create_file_menu()

    def create_file_menu(self) -> None:
        file_menu = self.menu_bar.addMenu("&File")

        self.open_menu_action = QAction("Open...", self)
        self.open_menu_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))

        file_menu.addAction(self.open_menu_action)
