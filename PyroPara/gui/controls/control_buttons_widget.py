from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

FONT = QFont("Times", 10)


class ControlButtons(QWidget):
    def __init__(self) -> None:
        super().__init__()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding)
        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout.addItem(spacer)

        self.plot_button = QPushButton("Plot")
        self.plot_button.setFont(FONT)

        self.plot_minima_button = QPushButton("Plot minima")
        self.plot_minima_button.setFont(FONT)
        self.plot_minima_button.setCheckable(True)

        self.buttons_layout.addWidget(self.plot_minima_button)
        self.buttons_layout.addWidget(self.plot_button)

        self.set_button_enabled(self.plot_button, is_enabled=False)
        self.set_button_enabled(self.plot_minima_button, is_enabled=False)

    def set_button_enabled(self, button, *, is_enabled=True) -> None:
        button.setEnabled(is_enabled)
