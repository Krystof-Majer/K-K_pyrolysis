from PyroPara.gui.base import PlotWidget, Tab


class TgPlotWidget(PlotWidget, Tab):
    X_LABEL = "T"
    Y_LABEL = "TG"
    X_UNIT = "K"
    Y_UNIT = "-"

    def __init__(self, order) -> None:
        super().__init__(order)
        self.set_axis_labels()

    @property
    def tab_label(self) -> str:
        return "TG"

    def plot(self, selected_files: list) -> None:
        for file in selected_files:
            x = file._df.temperature
            y = file._df.mass_filtered
            label = str(file.beta)
            super().plot(x, y, clear=False, label=label, legend=True)

        super().set_axis_labels()
        self.draw()


class DtgPlotWidget(PlotWidget, Tab):
    X_LABEL = "T"
    Y_LABEL = "DTG"
    X_UNIT = "K"
    Y_UNIT = "1/s"

    def __init__(self, order) -> None:
        super().__init__(order)

    @property
    def tab_label(self) -> str:
        return "DTG"

    def plot(self, selected_files: list) -> None:
        for file in selected_files:
            x = file._df.temperature
            y = file._df.mass_diff_filtered
            label = str(file.beta)
            super().plot(x, y, clear=False, label=label, legend=True)

        super().set_axis_labels()
        self.draw()


class DdtgPlotWidget(PlotWidget, Tab):
    X_LABEL = "T"
    Y_LABEL = "DTG"
    X_UNIT = "K"
    Y_UNIT = "1/s2"

    def __init__(self, order) -> None:
        super().__init__(order)

    @property
    def tab_label(self) -> str:
        return "DDTG"

    def plot(self, selected_files: list) -> None:
        for file in selected_files:
            x = file._df.temperature
            y = file._df.mass_diff2_filtered
            label = str(file.beta)
            super().plot(x, y, clear=False, label=label, legend=True)

        super().set_axis_labels()
        self.draw()
