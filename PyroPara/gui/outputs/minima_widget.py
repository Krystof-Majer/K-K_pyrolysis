from PyroPara.gui.outputs.table_view_widget import Table, TableModel
from PyroPara.utils import round_all
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
)


class MinimaWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.table_list = []

        minima_table_group = QGroupBox("Local temperature minimas")
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(minima_table_group)

        self.setLayout(main_layout)

        self.table_layout = QHBoxLayout()
        minima_table_group.setLayout(self.table_layout)

        button_group = QFrame(self)
        main_layout.addWidget(button_group)
        self.button_layout = QHBoxLayout(button_group)
        self.button_layout.addItem(
            QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        mockup_button = QPushButton("mockup_section")
        self.button_layout.addWidget(mockup_button)

    def create_table(self, sta_file):
        table = Table(sta_file)
        data = round_all(sta_file.local_minima)

        self.model = TableModel(data)
        table.setModel(self.model)

        self.table_layout.addWidget(table)
        self.table_list.append(table)
