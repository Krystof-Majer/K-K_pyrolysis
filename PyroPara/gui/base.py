from typing import Any

import matplotlib as mpl
import matplotlib.ticker as mticker
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

mpl.rcParams.update({"font.size": 14})


class TabStatus:
    enabled_changed: Signal = Signal(object, bool)
    _is_enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value) -> None:
        if value != self._is_enabled:
            self._is_enabled = value
            self.enabled_changed.emit(self, self._is_enabled)


class PlotWidget(QWidget):
    LEFT = 0.08
    RIGHT = 0.965
    TOP = 0.965
    BOTTOM = 0.07

    X_LABEL = "x_label"
    Y_LABEL = "y_label"
    X_UNIT = "unit"
    Y_UNIT = "unit"

    def __init__(self, order) -> None:
        super().__init__()
        self.figure = Figure()
        self.order = order
        self.figure.subplots_adjust(
            left=self.LEFT,
            right=self.RIGHT,
            top=self.TOP,
            bottom=self.BOTTOM,
        )
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.main_layout = QVBoxLayout(self)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.toolbar)
        self.main_layout.addLayout(self.horizontal_layout)
        self.main_layout.addWidget(self.canvas)
        self.axis = self.figure.add_subplot()

        self.setLayout(self.main_layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.axis.format_coord = self.format_coord

    @property
    def xlim(self) -> float:
        return self.axis.get_xlim()

    def set_xlim(self, xlim: float) -> None:
        self.axis.set_xlim(xlim)

    @property
    def ylim(self) -> float:
        return self.axis.get_ylim()

    def set_ylim(self, lower: float, upper: float) -> None:
        self.axis.set_ylim(lower, upper)

    def format_coord(self, x: float, y: float) -> None:
        axial, radial = x, y
        text = f"{self.X_LABEL}={axial:.4f} {self.Y_LABEL}={radial:.4f}"

        return text

    def draw(self) -> None:
        self.canvas.draw()

    def clear(self) -> None:
        self.axis.clear()
        self.set_axis_labels()
        self.draw()

    def grid(self, **kwargs: Any) -> None:
        self.axis.grid(**kwargs)

    def set_title(self, title: str, **kwargs: Any) -> None:
        self.axis.set_title(title, **kwargs)

    def set_x_label(self, label: str) -> None:
        self.axis.set_xlabel(label)

    def set_y_label(self, label: str) -> None:
        self.axis.set_ylabel(label)

    def set_axis_equal(self) -> None:
        self.axis.set_aspect(aspect="equal", adjustable="box")

    def set_major_locator(self) -> None:
        steps = [1, 10]
        self.axis.xaxis.set_major_locator(mticker.MaxNLocator(steps=steps))
        self.axis.yaxis.set_major_locator(mticker.MaxNLocator(steps=steps))

    def set_axis_labels(self) -> None:
        self.set_x_label(self.X_LABEL + " " + f"({self.X_UNIT})")
        self.set_y_label(self.Y_LABEL + " " + f"({self.Y_UNIT})")

    def set_axis_off(self) -> None:
        self.axis.set_axis_off()

    def plot_minima(self, x, _max):
        self.axis.vlines(x, 0, _max, "k", alpha=0.3)

    def plot(
        self,
        *args: Any,
        scalex: bool = True,
        scaley: bool = True,
        xlabel: str = None,
        ylabel: str = None,
        grid: bool = True,
        clear: bool = True,
        axis_equal: bool = False,
        legend: bool = False,
        **kwargs: Any,
    ) -> None:

        if clear:
            self.axis.clear()

        self.axis.plot(*args, scalex=scalex, scaley=scaley, **kwargs)
        self.grid(b=grid)

        if xlabel is not None:
            self.axis.set_xlabel(xlabel)

        if ylabel is not None:
            self.axis.set_ylabel(ylabel)

        if axis_equal:
            self.set_axis_equal()

        if legend:
            ax = self.axis
            ax.legend(loc=0)
