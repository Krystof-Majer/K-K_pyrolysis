from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QTableView


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.horizontal_headers = [""] * 2

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return float(self._data[index.row()][index.column()])

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignHCenter

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role == Qt.EditRole:
            try:
                self.horizontal_headers[section] = data
                return True
            except Exception:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontal_headers[section]
            except Exception:
                pass
        return super().headerData(section, orientation, role)


class Table(QTableView):
    def __init__(self) -> None:
        super().__init__()

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
