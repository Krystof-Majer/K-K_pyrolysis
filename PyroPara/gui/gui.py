from os.path import basename

from PyroPara.analysis import Analysis
from PyroPara.gui.controls.left_panel import LeftPanel
from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.message_box import warning
from PyroPara.gui.plot.plot_panel import PlotPanel
from PyroPara.gui.windows import MainWindow


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.plot_panel = PlotPanel()
        self.left_panel = LeftPanel()
        self.main_window = MainWindow(
            plot_panel=self.plot_panel, left_panel=self.left_panel
        )
        self.analysis = Analysis()
        self.control_buttons = self.left_panel.control_buttons_widget
        self.connect_signals()

    def show(self) -> None:
        self.main_window.showMaximized()

    def connect_signals(self) -> None:
        window = self.main_window
        controls = self.control_buttons

        window.read_menu_action.triggered.connect(self.open_clicked)
        controls.plot_button.clicked.connect(self.plot_clicked)
        controls.show_minima_button.clicked.connect(self.show_minima_toggle)

    def open_clicked(self) -> None:
        files = ReadDialog(self.main_window).show()
        button = self.control_buttons

        if not files:
            return

        rejected_files = []
        analysis = self.analysis
        for file in files[0]:
            try:
                analysis.load_file(file)
            except:
                rejected_files.append(basename(file))

        if len(rejected_files) > 0:
            warning(
                text="Unable to load files",
                info_text=f"Unsupported files\n {rejected_files}",
            )

        analysis.run()

        self.left_panel.sta_files_widget.clear()

        analysis.sta_files.sort(key=lambda x: x.beta)
        file_names = [sta_file.name for sta_file in analysis.sta_files]

        self.left_panel.sta_files_widget.add_files(file_names)

        if file_names:
            button.set_button_enabled(button.plot_button, is_enabled=True)

    def plot_clicked(self):
        button = self.control_buttons
        selected_indices = self.left_panel.sta_files_widget.selected_indices
        selected_files = [
            self.analysis.sta_files[index] for index in selected_indices
        ]

        plot_panel = self.plot_panel
        plot_panel.clear_widgets(plot_panel.widgets)
        plot_panel.tg_plot.plot(selected_files)
        plot_panel.dtg_plot.plot(selected_files)
        plot_panel.ddtg_plot.plot(selected_files)
        plot_panel.ddtg_plot.plot_minima(selected_files)
        plot_panel.ddtg_plot_normalized.plot(selected_files)
        plot_panel.ddtg_plot_normalized.plot_minima(selected_files)

        button.show_minima_button.setChecked(False)
        self.show_minima_toggle(False)

        if selected_files:
            for widget in plot_panel.widgets:
                widget.is_enabled = True

            button.set_button_enabled(
                button.show_minima_button, is_enabled=True
            )

    def show_minima_toggle(self, checked: bool):
        button = self.control_buttons
        button.show_minima_checked = checked
        button.change_show_minima_text()
        self.plot_panel.ddtg_plot.toggle_lines(checked)
        self.plot_panel.ddtg_plot_normalized.toggle_lines(checked)
