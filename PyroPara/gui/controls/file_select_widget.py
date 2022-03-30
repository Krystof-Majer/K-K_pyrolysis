from typing import List
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
)


class FileSelectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        file_list_group = QGroupBox()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(file_list_group)

        vertical_layout = QVBoxLayout(file_list_group)

        self.file_list = QListWidget(self)
        vertical_layout.addWidget(self.file_list)

        button_group = QFrame(self)
        vertical_layout.addWidget(button_group)

        self.button_layout: QHBoxLayout = QHBoxLayout(button_group)
        self.create_buttons()

    def create_buttons(self) -> None:
        clear_selection_button = QPushButton("clear selected")
        clear_selection_button.setToolTip("clear selection")
        clear_selection_button.clicked.connect(self.clear_selection_clicked)
        self.button_layout.addWidget(clear_selection_button)

        clear_all_button = QPushButton("clear all")
        clear_all_button.setToolTip("clear selection")
        clear_all_button.clicked.connect(self.clear_all_clicked)
        self.button_layout.addWidget(clear_all_button)

        select_all_button = QPushButton("clear all")
        select_all_button.setToolTip("clear selection")
        select_all_button.clicked.connect(self.select_all_clicked)
        self.button_layout.addWidget(select_all_button)

        invert_button = QPushButton("invert")
        invert_button.setToolTip("clear selection")
        invert_button.clicked.connect(self.invert_clicked)
        self.button_layout.addWidget(invert_button)

    def selected_indices(self) -> List[int]:
        selected_indices = self.file_list.selectedIndexes()

        if selected_indices:
            return sorted(index.row() for index in selected_indices)

        return []

    def clear_all_clicked(self) -> None:
        self.file_list.clear()

    def select_all_clicked(self) -> None:
        self.file_list.selectAll()

    def clear_selection_clicked(self) -> None:
        self.file_list.clearSelection()

    def invert_clicked(self) -> None:
        for i in range(self.file_list.count()):
            file = self.file_list.item(i)
            file.setSelected(not file.isSelected())

    def add_files(self, file_names: List[str]) -> None:
        if file_names:
            self.file_list.addItems(file_names)
