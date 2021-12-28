from os.path import expanduser

from PySide6.QtWidgets import QFileDialog, QMainWindow


class ReadDialog(QFileDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

    def show(self) -> str:
        dir = self.getExistingDirectory(
            self.parent(),
            "Read STA files",
            expanduser("~"),
            self.ShowDirsOnly | self.DontResolveSymlinks,
        )

        return dir
