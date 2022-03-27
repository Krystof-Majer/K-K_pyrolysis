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

    def plot(self) -> None:
        super().plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "r-")
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

    def plot(self) -> None:
        super().plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "g-")
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

    def plot(self) -> None:
        super().plot((0, 0.5, 1, 0), (0, 0.5, 0, 0), "b-")
        super().set_axis_labels()
        self.draw()
