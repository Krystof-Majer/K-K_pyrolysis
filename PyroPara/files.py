import numpy as np


class TemperatureFile:
    def __init__(self) -> None:
        self._data = None

    @property
    def rows(self) -> int:
        """Number of data points.

        Raises:
            TypeError: File not loaded.

        Returns:
            int: Number of data points.
        """
        if self._data is None:
            raise TypeError("File is not loaded")

        return self._data.shape[0]

    def load(self, path: str):
        """Load a temperature file.

        Args:
            path (str): Path to a file.
        """
        self._data = np.loadtxt(path, delimiter=",", skiprows=35)
