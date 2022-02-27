from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.windows import MainWindow
from PyroPara.analysis import Analysis


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.main_window = MainWindow()
        self.analysis = Analysis()

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

        analysis = self.analysis
        analysis.load_files(dir)

        self.main_window.sta_files_widget.clear()

        names = [sta_file.name for sta_file in analysis.sta_files]
        self.main_window.sta_files_widget.addItems(names)
