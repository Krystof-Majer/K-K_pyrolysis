from typing import List
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QAbstractItemView,
)


class FileSelectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        file_list_group = QGroupBox()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(file_list_group)

        vertical_layout = QVBoxLayout(file_list_group)

        self.file_list = QListWidget(self)
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        vertical_layout.addWidget(self.file_list)

        button_group = QFrame(self)
        vertical_layout.addWidget(button_group)

        self.button_layout: QHBoxLayout = QHBoxLayout(button_group)
        self.create_buttons()

    def create_buttons(self) -> None:
        clear_selection_button = QPushButton("◻")
        clear_selection_button.setToolTip("clear selected")
        clear_selection_button.clicked.connect(self.clear_selection_clicked)

        clear_all_button = QPushButton("☒")
        clear_all_button.setToolTip("clear all")
        clear_all_button.clicked.connect(self.clear_all_clicked)

        select_all_button = QPushButton("◼")
        select_all_button.setToolTip("select all")
        select_all_button.clicked.connect(self.select_all_clicked)

        invert_button = QPushButton("◩")
        invert_button.setToolTip("invert selected")
        invert_button.clicked.connect(self.invert_clicked)

        self.button_layout.addWidget(select_all_button)
        self.button_layout.addWidget(invert_button)
        self.button_layout.addWidget(clear_selection_button)
        self.button_layout.addWidget(clear_all_button)

    @property
    def selected_indices(self) -> List[int]:
        selected_indices = self.file_list.selectedIndexes()

        if selected_indices:
            return sorted(index.row() for index in selected_indices)

        return []

    def clear(self) -> None:
        self.file_list.clear()

    def clear_all_clicked(self) -> None:
        self.file_list.clear()

    def select_all_clicked(self) -> None:
        self.file_list.selectAll()

    def clear_selection_clicked(self) -> None:
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
