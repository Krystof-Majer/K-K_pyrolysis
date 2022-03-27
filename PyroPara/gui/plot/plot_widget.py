from PyroPara.gui.base import PlotWidget, Tab


class TgPlotWidget(PlotWidget, Tab):
    def __init__(self, order) -> None:
        super().__init__(order)

    @property
    def tab_label(self):
        return "TG"


class DtgPlotWidget(PlotWidget, Tab):
    def __init__(self, order) -> None:
        super().__init__(order)

    @property
    def tab_label(self):
        return "DTG"


class DdtgPlotWidget(PlotWidget, Tab):
    def __init__(self, order) -> None:
        super().__init__(order)

    @property
    def tab_label(self):
        return "DDTG"
