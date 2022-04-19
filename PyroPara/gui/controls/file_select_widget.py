from typing import List
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
)


class FileSelectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        file_list_group = QGroupBox()
        file_list_group.setTitle("STA files")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(file_list_group)
        main_layout.setContentsMargins(8, 0, 8, 0)

        vertical_layout = QVBoxLayout(file_list_group)

        self.file_list = QListWidget(self)
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        vertical_layout.addWidget(self.file_list)

        button_group = QFrame(self)
        vertical_layout.addWidget(button_group)

        self.button_layout: QHBoxLayout = QHBoxLayout(button_group)
        self.button_layout.addItem(
            QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        self.button_layout.setContentsMargins(60, 2, 5, 2)

        self.create_buttons()

    def create_buttons(self) -> None:
        self.delete_selection_button = QPushButton("◻")
        self.delete_selection_button.setToolTip("Delete selected")
        self.delete_selection_button.setFixedSize(18, 18)
        self.delete_selection_button.clicked.connect(
            self.delete_selection_clicked
        )

        deselect_all_button = QPushButton("☒")
        deselect_all_button.setToolTip("Deselect all")
        deselect_all_button.setFixedSize(18, 18)
        deselect_all_button.clicked.connect(self.deselect_all_clicked)

        select_all_button = QPushButton("◼")
        select_all_button.setToolTip("Select all")
        select_all_button.setFixedSize(18, 18)
        select_all_button.clicked.connect(self.select_all_clicked)

        invert_button = QPushButton("◩")
        invert_button.setToolTip("Invert selected")
        invert_button.setFixedSize(18, 18)
        invert_button.clicked.connect(self.invert_clicked)

        self.button_layout.addWidget(select_all_button)
        self.button_layout.addWidget(invert_button)
        self.button_layout.addWidget(deselect_all_button)
        # self.button_layout.addWidget(self.delete_selection_button)

    @property
    def selected_indices(self) -> List[int]:
        selected_indices = self.file_list.selectedIndexes()

        if selected_indices:
            return sorted(index.row() for index in selected_indices)

        return []

    def clear(self) -> None:
        self.file_list.clear()

    def deselect_all_clicked(self) -> None:
        for i in range(self.file_list.count()):
            file = self.file_list.item(i)
            file.setSelected(False)

    def select_all_clicked(self) -> None:
        self.file_list.selectAll()

    def delete_selection_clicked(self) -> None:
        list_items = self.file_list.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.file_list.takeItem(self.file_list.row(item))

    def invert_clicked(self) -> None:
        for i in range(self.file_list.count()):
            file = self.file_list.item(i)
            file.setSelected(not file.isSelected())

    def add_files(self, file_names: List[str]) -> None:
        if file_names:
            self.file_list.addItems(file_names)
