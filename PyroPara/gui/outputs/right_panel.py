from PySide6.QtWidgets import QGroupBox, QTabWidget, QVBoxLayout, QWidget


class RightPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        minima_table_group = QGroupBox()
        minima_table_group.setTitle("Local temperature minimas")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(minima_table_group)

        vertical_layout = QVBoxLayout(minima_table_group)

        self.minima_tab = QTabWidget()
        vertical_layout.addWidget(self.minima_tab)

    def create_tabs(self, minima_widgets: list):
        self.minima_tab.clear()
        for widget in minima_widgets:
            self.minima_tab.addTab(widget, widget.tab_label)
