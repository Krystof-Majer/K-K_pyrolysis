from PySide6.QtCore import QAbstractTableModel, Qt
from PyroPara.utils import get_material
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QTableWidget,
)


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


class Table(QTableView):
    def __init__(self, sta_file) -> None:
        super().__init__()
        self.name = sta_file.name
        self.beta = sta_file.beta
        self.type = get_material(sta_file.name)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
