from PySide6.QtWidgets import QVBoxLayout, QWidget

from PyroPara.gui.base import TabWidget


class PlotPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.tg_widget: QWidget = None
        self.dtg_widget: QWidget = None
        self.ddtg_widget: QWidget = None

        self.tab_widget: TabWidget = TabWidget(widgets=self.widgets)
