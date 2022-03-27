from PyroPara.analysis import Analysis
from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.message_box import warning
from PyroPara.gui.panel.plot_panel import PlotPanel
from PyroPara.gui.windows import MainWindow


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.plot_panel = PlotPanel()

        self.main_window = MainWindow(plot_panel=self.plot_panel)
        self.analysis = Analysis()

        self.connect_signals()

    def show(self) -> None:
        self.main_window.showMaximized()

    def connect_signals(self) -> None:
        window = self.main_window

        window.read_menu_action.triggered.connect(self.open_clicked)
        window.plot_button.clicked.connect(self.plot_clicked)

    def open_clicked(self) -> None:
        main_window = self.main_window

        dir = ReadDialog(main_window).show()

        if not dir:
            return

        analysis = self.analysis
        analysis.load_files(dir)

        main_window.sta_files_widget.clear()

        names = [sta_file.name for sta_file in analysis.sta_files]
        main_window.sta_files_widget.addItems(names)

        if names:
            main_window.set_button_enabled(
                main_window.plot_button, is_enabled=True
            )
            return

        main_window.set_button_enabled(
            main_window.plot_button, is_enabled=False
        )

    def plot_clicked(self) -> None:
        print(self.main_window.selected_files)
        if not self.main_window.selected_files:
            warning(text="Select STA file(s)")

            return

        plot_panel = self.plot_panel
        plot_panel.clear_widgets(plot_panel.widgets)

        plot_panel.tg_widget.plot()
        plot_panel.dtg_widget.plot()
        plot_panel.ddtg_widget.plot()

        for widget in plot_panel.widgets:
            widget.is_enabled = True