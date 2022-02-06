from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.windows import MainWindow


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.main_window = MainWindow()

        self.connect_signals()

    def show(self) -> None:
        self.main_window.showMaximized()

    def connect_signals(self) -> None:
        window = self.main_window

        window.read_menu_action.triggered.connect(self.open_clicked)

    def open_clicked(self) -> None:
        dir = ReadDialog(self.main_window).show()

        if not dir:
            return

        self.main_window.sta_files_widget.clear()
        self.main_window.sta_files_widget.addItem(dir)
