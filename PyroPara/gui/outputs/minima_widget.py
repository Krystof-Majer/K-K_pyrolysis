from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QTabWidget, QVBoxLayout, QWidget

from PyroPara.gui.outputs.table_view_widget import Table, TableModel
from PyroPara.utils import get_material, round_all


class MinimaWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.tab_widget: QTabWidget = QTabWidget()

        main_layout = QVBoxLayout(self)
        minima_table_group = QGroupBox("Local temperature minimas")
        vertical_layout = QVBoxLayout(minima_table_group)
        main_layout.addWidget(minima_table_group)
        vertical_layout.addWidget(self.tab_widget)

    def create_table(self, sta_file):
        table = Table()
        data = round_all(sta_file.local_minima)

        beta = sta_file.beta
        type = get_material(sta_file.name)

        self.model = TableModel(data)
        self.model.setHeaderData(0, Qt.Horizontal, "T (K)")
        self.model.setHeaderData(1, Qt.Horizontal, "1/s²")

        table.setModel(self.model)
        self.tab_widget.addTab(table, f"{type} {beta} K/s")
