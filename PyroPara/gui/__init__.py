from PySide6.QtWidgets import QApplication

from PyroPara.gui.gui import Gui


def show():
    app = QApplication()

    gui = Gui()
    gui.show()

    app.exec_()
