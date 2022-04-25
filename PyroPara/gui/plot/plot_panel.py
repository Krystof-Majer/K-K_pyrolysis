from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from PyroPara.gui.plot.plot_widget import (
    DdtgPlot,
    DtgPlot,
    TgPlot,
    DdtgPlotNormalized,
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
        self.ddtg_plot_normalized: DdtgPlotNormalized = DdtgPlotNormalized(3)

        self.widgets = (
            self.tg_plot,
            self.dtg_plot,
            self.ddtg_plot,
            self.ddtg_plot_normalized,
        )
        self.tab_widget: TabWidget = TabWidget(plotwidgets=self.widgets)
        main_layout.addWidget(self.tab_widget)
        self.connect_signals()

        for widget in self.widgets[1:]:
            widget.is_enabled = False

    @property
    def current_tab_widget(self) -> QWidget:
        return self.tab_widget.widgets[self.tab_widget.currentIndex]

    def clear_widgets(self, plotwidgets: list) -> None:
        for entry in plotwidgets:
            entry.clear()

    def enabled_change(self, tab, is_enabled) -> None:
        self.tab_widget.setTabEnabled(tab.order, is_enabled)

    def connect_signals(self) -> None:
        for widget in self.widgets:
            widget.enabled_changed.connect(self.enabled_change)
