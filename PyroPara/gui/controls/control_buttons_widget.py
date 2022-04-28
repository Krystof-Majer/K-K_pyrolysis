from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

FONT = QFont("Times", 10.5)


class ControlButtons(QWidget):
    def __init__(self) -> None:
        super().__init__()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding)
        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout.addItem(spacer)

        self.plot_button = QPushButton("Plot")
        self.plot_button.setFont(FONT)
        self.plot_button.setFixedSize(90, 30)

        self.show_minima_button = QPushButton()
        self.show_minima_button.setFont(FONT)
        self.show_minima_button.setFixedSize(100, 30)
        self.show_minima_checked = False
        self.show_minima_button.setCheckable(True)
        self.show_minima_button.setChecked(self.show_minima_checked)
        self.show_minima_button.setText("Show minima ☐")
        self.change_show_minima_style()

        self.buttons_layout.addWidget(self.show_minima_button)
        self.buttons_layout.addWidget(self.plot_button)

        self.set_button_enabled(self.plot_button, is_enabled=False)
        self.set_button_enabled(self.show_minima_button, is_enabled=False)

    def set_button_enabled(self, button, is_enabled=True) -> None:
        button.setEnabled(is_enabled)

    def change_show_minima_style(self):
        if self.show_minima_checked:
            self.show_minima_button.setStyleSheet("background-color:#70cc54")
            self.show_minima_button.setText("Show minima ☑")
        else:
            self.show_minima_button.setStyleSheet("background-color:#D3D3D3")
            self.show_minima_button.setText("Show minima ☐")
