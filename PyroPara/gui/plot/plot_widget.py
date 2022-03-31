from PyroPara.gui.base import PlotWidget
from PySide6.QtCore import Signal

# Unused
class Tab:
    _is_enabled: bool = True
    enabled_changed: Signal = Signal(object, bool)

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value) -> None:
        if value != self._is_enabled:
            self._is_enabled = value
            self.enabled_changed.emit(self, self._is_enabled)


class TgPlot(PlotWidget, Tab):

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
        super().set_axis_labels()
        self.draw()


class DtgPlot(PlotWidget, Tab):

    X_LABEL = "T"
    Y_LABEL = "DTG"
    X_UNIT = "K"
    Y_UNIT = "1/s"

    def __init__(self, index) -> None:
        super().__init__(index)

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


class DdtgPlot(PlotWidget, Tab):

    X_LABEL = "T"
    Y_LABEL = "DDTG"
    X_UNIT = "K"
    Y_UNIT = "1/s^2"

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
