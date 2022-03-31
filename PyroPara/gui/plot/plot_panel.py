from PySide6.QtWidgets import QVBoxLayout, QWidget, QTabWidget
from PyroPara.gui.plot.plot_widget import (
    TgPlot,
    DtgPlot,
    DdtgPlot,
)


class TabWidget(QTabWidget):
    def __init__(self, *, plotwidgets=None) -> None:
        super().__init__()
        self.widgets: list = plotwidgets

        for widget in self.widgets:
            self.addTab(widget, widget.tab_label)

    @property
    def index(self):
        return self.wigets[self.currentIndex]


class PlotPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.tg_plot: TgPlot = TgPlot(0)
        self.dtg_plot: DtgPlot = DtgPlot(1)
        self.ddtg_plot: DdtgPlot = DdtgPlot(2)

        self.widgets = (self.tg_plot, self.dtg_plot, self.ddtg_plot)
        self.tab_widget: TabWidget = TabWidget(plotwidgets=self.widgets)

        main_layout.addWidget(self.tab_widget)

    @property
    def current_tab_widget(self) -> QWidget:
        return self.tab_widget.widgets[self.tab_widget.currentIndex]

    def clear_widgets(self, plotwidgets: list) -> None:
        for entry in plotwidgets:
            entry.clear()
