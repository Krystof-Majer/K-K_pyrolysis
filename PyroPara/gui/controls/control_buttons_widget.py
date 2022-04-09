from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

FONT = QFont("Times", 10, QFont.Bold)


class ControlButtons(QWidget):
    def __init__(self) -> None:
        super().__init__()

        spacer = QSpacerItem(0, 0, QSizePolicy.MinimumExpanding)
        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout.addItem(spacer)

        self.plot_button = QPushButton("PLOT")
        self.plot_button.setFont(FONT)
        self.plot_button.resize(40, 30)
        # self.test_button = QPushButton("test")

        self.buttons_layout.addWidget(self.plot_button)
        # self.buttons_layout.addWidget(self.test_button)

        self.set_button_enabled(self.plot_button, is_enabled=False)

    def set_button_enabled(self, button, *, is_enabled=True) -> None:
        button.setEnabled(is_enabled)
