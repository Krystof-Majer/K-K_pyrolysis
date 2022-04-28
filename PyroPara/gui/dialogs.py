from os.path import expanduser

from PySide6.QtWidgets import QFileDialog, QMainWindow


class ReadDialog(QFileDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

    def show(self) -> str:
        files = self.getOpenFileNames(
            self.parent(),
            "Read STA files",
            "",
            "Text files (*.txt)",
            "",
        )

        return files
