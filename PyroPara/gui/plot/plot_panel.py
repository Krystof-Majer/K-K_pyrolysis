from PySide6.QtWidgets import QGridLayout, QWidget, QTabWidget
from matplotlib import widgets
from PyroPara.gui.plot.plot_widget import (
    TgPlot,
    DtgPlot,
    DdtgPlot,
)

# Unused
class TabWidget(QTabWidget):
    def __init__(self, *, plotwidgets=None) -> None:
        super().__init__()
        self.widgets: list = plotwidgets

        for widget in self.widgets:
            self.addTab(widget, widget.label)

    @property
    def index(self):
        return self.wigets[self.currentIndex]


class PlotPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.Tg_plot: TgPlot = TgPlot()
        self.Dtg_plot: DtgPlot = DtgPlot()
        self.Ddtg_plot: DdtgPlot = DdtgPlot()

        self.widgets = (self.Tg_plot, self.Dtg_plot, self.Ddtg_plot)
        self.tab_widget: TabWidget = QTabWidget(self.widgets)

        for widget in self.widgets:
            self.tab_widget.addTab(widget, widget.label)

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.tab_widget)

    @property
    def current_tab_widget(self) -> QWidget:
        return self.tab_widget.widgets[self.tab_widget.currentIndex]

    def clear_widgets(self, widgets: list) -> None:
        for entry in widgets:
            entry.clear()
