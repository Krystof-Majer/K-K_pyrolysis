from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QWidget


class MinimaWidget(QWidget):
    def __init__(self, tab_label) -> None:
        super().__init__(tab_label)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.box = QGroupBox()
        self.box.setTitle("tab_label")
        main_layout.addWidget(self.box)
