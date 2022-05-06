import re

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

MATERIAL_REGEX = re.compile(r"_[A-Z]_")


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class MinimaWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.minima_table_group = QGroupBox("Local temperature minimas")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.minima_table_group)
        self.table_layout = QHBoxLayout()

        self.setLayout(self.main_layout)

        self.minima_table_group.setLayout(self.table_layout)

        mockup_button = QPushButton("mockup_section")
        self.main_layout.addWidget(mockup_button)

    def create_table(self, sta_file):
        # type = re.search(MATERIAL_REGEX, sta_file.name)
        # beta = sta_file.beta
        # data = sta_file.local_minima
        data = sta_file

        # box = QGroupBox(f"{type} {beta}K")

        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table_layout.addWidget(self.table)
