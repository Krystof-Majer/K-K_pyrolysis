import numpy as np
import pandas as pd

from PyroPara.filter import Filter

# TODO: make proper properties with setter getter methods + tests


class STAfile:
    def __init__(self, path: str, filter: Filter) -> None:
        self._df = None
        self.filter = filter
        self.path = path

    def load(self):
        """Load a STAfile data as pandas dataframe.

        Args:
            path (str): Path to a file.
        """
        self._df = pd.read_csv(
            self.path, sep=",", encoding="cp1250", skiprows=34
        )
        self._df.rename(
            columns={
                self._df.columns[0]: "temperature",
                self._df.columns[3]: "mass",
                self._df.columns[1]: "time",
            },
            inplace=True,
        )
        self._df.temperature += 273.15
        self._df.mass /= 100

    def process(self):
        """Calculates and filters first and second derivatives of df.mass array

        Args:
            Filter (Class): instance of Filter class
        """
        # 1. TG
        self._df["mass_filtered"] = self.filter.apply(
            self._df.time, self._df.mass
        )
        # 2. DTG
        self._df["mass_diff_unfiltered"] = -np.gradient(
            self._df.mass_filtered, self._df.time
        )
        self._df["mass_diff_filtered"] = self.filter.apply(
            self._df.time, self._df.mass_diff_unfiltered
        )
        # 3. DDTG
        self._df["mass_diff2_unfiltered"] = abs(
            np.gradient(self._df.mass_diff_filtered, self._df.time)
        )
        self._df["mass_diff2_filtered"] = abs(
            self.filter.apply(self._df.time, self._df.mass_diff2_unfiltered)
        )
