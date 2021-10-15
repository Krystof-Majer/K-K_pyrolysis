from PySide6.QtWidgets import QMainWindow  # type: ignore

from PyroPara import __version__


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PyroPara {__version__}")
        self.resize(1024, 768)
