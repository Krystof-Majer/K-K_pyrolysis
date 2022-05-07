from PySide6.QtWidgets import QVBoxLayout, QWidget

from PyroPara.gui.outputs.minima_widget import MinimaWidget


class RightPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.minima_widget: MinimaWidget = MinimaWidget()
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.minima_widget)

        data = [
            (1, 0, 0),
            (3, 5, 0),
            (3, 3, 2),
            (7, 8, 9),
            (4, 9, 2),
        ]

        # Test
        # table = self.minima_widget.create_table(data)
