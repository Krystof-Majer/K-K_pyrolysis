from PySide6.QtWidgets import QVBoxLayout, QWidget

from PyroPara.gui.base import TabWidget
from PyroPara.gui.plot.plot_widget import (
    DdtgPlotWidget,
    DtgPlotWidget,
    TgPlotWidget,
)


class PlotPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.tg_widget: TgPlotWidget = TgPlotWidget(0)
        self.dtg_widget: DtgPlotWidget = DtgPlotWidget(1)
        self.ddtg_widget: DdtgPlotWidget = DdtgPlotWidget(2)

        self.widgets = (self.tg_widget, self.dtg_widget, self.ddtg_widget)
        self.tab_widget: TabWidget = TabWidget(widgets=self.widgets)
        self.connect_signals()

        for widget in self.widgets[1:]:
            widget.is_enabled = False

        main_layout.addWidget(self.tab_widget)

    @property
    def current_widget(self) -> QWidget:
        return self.tab_widget.current

    def connect_signals(self) -> None:
        for widget in self.widgets:
            widget.enabled_changed.connect(self.enabled_changed)

    def clear_widgets(self, widgets) -> None:
        for widget in widgets:
            widget.clear()

    def enabled_changed(self, tab, is_enabled) -> None:
        self.tab_widget.setTabEnabled(tab.order, is_enabled)
