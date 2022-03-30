from PyroPara.analysis import Analysis
from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.windows import MainWindow
from PyroPara.gui.plot.plot_panel import PlotPanel
from PyroPara.gui.controls.control_buttons_widget import ControlButtons


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.plot_panel = PlotPanel()
        self.main_window = MainWindow(plot_panel=self.plot_panel)
        self.analysis = Analysis()
        self.control_buttons = ControlButtons()
        self.connect_signals()

    def show(self) -> None:
        self.main_window.showMaximized()

    def connect_signals(self) -> None:
        window = self.main_window
        controls = self.control_buttons

        window.read_menu_action.triggered.connect(self.open_clicked)
        controls.plot_button.clicked.connect(self.plot_clicked)

    def open_clicked(self) -> None:
        dir = ReadDialog(self.main_window).show()

        if not dir:
            return

        analysis = self.analysis
        analysis.load_all_files(dir)

        self.main_window.sta_files_widget.clear()

        names = [sta_file.name for sta_file in analysis.sta_files]
        self.main_window.sta_files_widget.addItems(names)

    def plot_clicked(self):
        pass
