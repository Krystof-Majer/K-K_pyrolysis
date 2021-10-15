from PySide6.QtWidgets import QApplication

from PyroPara.gui.windows import MainWindow


def show():
    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec_()
