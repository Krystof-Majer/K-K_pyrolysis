from PySide6.QtWidgets import QVBoxLayout, QWidget

from PyroPara.gui.controls.control_buttons_widget import ControlButtons
from PyroPara.gui.controls.file_select_widget import FileSelectWidget


class LeftPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.sta_files_widget: FileSelectWidget = FileSelectWidget()
        self.control_buttons_widget: ControlButtons = ControlButtons()

        self.main_layout.addWidget(self.sta_files_widget)
        self.main_layout.addLayout(self.control_buttons_widget.buttons_layout)
