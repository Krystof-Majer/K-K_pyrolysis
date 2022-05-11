from filecmp import cmp
from os.path import basename

from PyroPara.analysis import Analysis
from PyroPara.gui.controls.left_panel import LeftPanel
from PyroPara.gui.dialogs import ReadDialog
from PyroPara.gui.message_box import warning_msg
from PyroPara.gui.outputs.right_panel import RightPanel
from PyroPara.gui.plot.plot_panel import PlotPanel
from PyroPara.gui.windows import MainWindow


class Gui:
    def __init__(self) -> None:
        super().__init__()

        self.plot_panel = PlotPanel()
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()
        self.main_window = MainWindow(
            plot_panel=self.plot_panel,
            left_panel=self.left_panel,
            right_panel=self.right_panel,
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
        analysis = self.analysis
        analysis.sta_files.clear()
        self.right_panel.minima_widget.tab_widget.clear()

        if not files:
            return

        rejected_files = []
        duplicate_files = []
        loaded_files = []

        for sta_file in analysis.sta_files:
            loaded_files.append(sta_file.path)

        files_present = False
        if len(loaded_files) > 0:
            files_present = True

        for file_new in files[0]:
            if files_present:

                if_duplicate = False

                for file_old in loaded_files:

                    if cmp(file_new, file_old):
                        if_duplicate = True

                if if_duplicate:
                    duplicate_files.append(basename(file_new))
                    continue

                else:
                    try:
                        analysis.load_file(file_new)
                    except Exception:
                        rejected_files.append(basename(file_new))
            else:
                try:
                    analysis.load_file(file_new)
                except Exception:
                    rejected_files.append(basename(file_new))

        if len(rejected_files) > 0:
            warning_msg(
                text="Unsupported files error.",
                info_text="Unable to load the following files:",
                details="\n".join(map(str, rejected_files)),
            )

        if len(duplicate_files) > 0:
            warning_msg(
                text="Duplicate files error.",
                info_text="Duplicate files found:",
                details="\n".join(map(str, duplicate_files)),
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

        minima_widget = self.right_panel.minima_widget
        minima_widget.tab_widget.clear()
        for file in selected_files:
            minima_widget.create_table(file)

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
        button.change_show_minima_style()
        self.plot_panel.ddtg_plot.toggle_lines(checked)
        self.plot_panel.ddtg_plot_normalized.toggle_lines(checked)
