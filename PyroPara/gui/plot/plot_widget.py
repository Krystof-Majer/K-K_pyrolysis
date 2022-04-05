from PyroPara.gui.base import PlotWidget
from PyroPara.gui.base import TabStatus


class TgPlot(PlotWidget, TabStatus):

    X_LABEL = "T"
    Y_LABEL = "TG"
    X_UNIT = "K"
    Y_UNIT = "-"

    def __init__(self, index) -> None:
        super().__init__(index)

    @property
    def tab_label(self) -> str:
        return "TG"

    def plot(self, files: list) -> None:
        for file in files:
            x = file._df.temperature
            y = file._df.mass_filtered
            label = str(f"{file.beta} K")
            super().plot(x, y, clear=False, legend=True, label=label)
            super().set_ylim(0, 1.1)
        self.draw()


class DtgPlot(PlotWidget, TabStatus):

    X_LABEL = "T"
    Y_LABEL = "DTG"
    X_UNIT = "K"
    Y_UNIT = "1/s"

    def __init__(self, index) -> None:
        super().__init__(index)
        self.set_axis_labels()

    @property
    def tab_label(self) -> str:
        return "DTG"

    def plot(self, files: list) -> None:
        for file in files:
            x = file._df.temperature
            y = file._df.mass_diff_filtered
            label = str(f"{file.beta} K")
            super().plot(x, y, clear=False, legend=True, label=label)
        super().set_axis_labels()
        self.draw()

    @property
    def label(self) -> str:
        return ""


class DdtgPlot(PlotWidget, TabStatus):

    X_LABEL = "T"
    Y_LABEL = "DDTG"
    X_UNIT = "K"
    Y_UNIT = "1/s²"

    def __init__(self, index) -> None:
        super().__init__(index)

    @property
    def tab_label(self) -> str:
        return "DDTG"

    def plot(self, files: list) -> None:
        for file in files:
            x = file._df.temperature
            y = file._df.mass_diff2_filtered
            label = str(f"{file.beta} K")
            super().plot(x, y, clear=False, legend=True, label=label)
        super().set_axis_labels()
        self.draw()
