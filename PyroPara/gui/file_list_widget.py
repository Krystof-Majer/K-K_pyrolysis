from typing import List

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class FileListWidget(QWidget):
    def __init__(self, *, parent=None) -> None:
        super().__init__(parent=parent)

        file_group_box = QGroupBox()
        file_group_box.setTitle("STA files")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(file_group_box)

        vertical_layout = QVBoxLayout(file_group_box)
        self.file_list = QListWidget(self)

        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        vertical_layout.addWidget(self.file_list)

        group_box = QFrame(self)
        vertical_layout.addWidget(group_box)

        self.horizontal_layout: QHBoxLayout = QHBoxLayout(group_box)

        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self.create_buttons()

    def create_buttons(self) -> None:
        all_button = QPushButton()
        all_button.clicked.connect(self.all_clicked)
        all_button.setMaximumHeight(20)
        all_button.setMaximumWidth(20)
        all_button.setAutoDefault(False)
        all_button.setText("◼")
        all_button.setToolTip("Select all")
        self.horizontal_layout.addWidget(all_button)

        clear_button = QPushButton()
        clear_button.clicked.connect(self.clear_clicked)
        clear_button.setMaximumHeight(20)
        clear_button.setMaximumWidth(20)
        clear_button.setAutoDefault(False)
        clear_button.setText("◻")
        clear_button.setToolTip("Deselect all")
        self.horizontal_layout.addWidget(clear_button)

        invert_button = QPushButton()
        invert_button.clicked.connect(self.invert_clicked)
        invert_button.setMaximumHeight(20)
        invert_button.setMaximumWidth(20)
        invert_button.setAutoDefault(False)
        invert_button.setText("⬕")
        invert_button.setToolTip("Invert selection")
        self.horizontal_layout.addWidget(invert_button)

    @property
    def selected_indices(self) -> List[int]:
        selected_indices = self.file_list.selectedIndexes()

        if selected_indices:
            return sorted(index.row() for index in selected_indices)

        return []

    def add_files(self, file_names: List[str]) -> None:
        if file_names:
            self.file_list.addItems(file_names)

    def clear(self) -> None:
        self.file_list.clear()

    def all_clicked(self) -> None:
        self.file_list.selectAll()

    def clear_clicked(self) -> None:
        self.file_list.clearSelection()

    def invert_clicked(self) -> None:
        for i in range(self.file_list.count()):
            file = self.file_list.item(i)
            file.setSelected(not file.isSelected())
