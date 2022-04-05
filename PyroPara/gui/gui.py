from PyroPara.analysis import Analysis
from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.windows import MainWindow
from PyroPara.gui.plot.plot_panel import PlotPanel


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.plot_panel = PlotPanel()
        self.main_window = MainWindow(plot_panel=self.plot_panel)
        self.analysis = Analysis()
        self.control_buttons = self.main_window.control_buttons_widget
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
        button = self.control_buttons

        if not dir:
            return

        analysis = self.analysis
        analysis.load_all_files(dir)
        analysis.run()

        self.main_window.sta_files_widget.clear()

        file_names = [sta_file.name for sta_file in analysis.sta_files]
        self.main_window.sta_files_widget.add_files(file_names)

        if file_names:
            button.set_button_enabled(button.plot_button, is_enabled=True)
            return

    def plot_clicked(self):
        selected_indices = self.main_window.sta_files_widget.selected_indices
        selected_files = [
            self.analysis.sta_files[index] for index in selected_indices
        ]

        plot_panel = self.plot_panel
        plot_panel.clear_widgets(plot_panel.widgets)
        plot_panel.tg_plot.plot(selected_files)
        plot_panel.dtg_plot.plot(selected_files)
        plot_panel.ddtg_plot.plot(selected_files)

        for widget in plot_panel.widgets:
            widget.is_enabled = True
