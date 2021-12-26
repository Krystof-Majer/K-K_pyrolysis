import numpy as np
import pandas as pd
from PyroPara.filter import Filter

# TODO: make proper properties with setter getter methods + tests


class STAfile:
    def __init__(self) -> None:
        self._df = None

    @property
    def rows(self):
        return len(self._df.shape[0])

    def beta(self, path: str):
        """reads beta value from specific place in file"""
        with open(path) as file:
            for i, line in enumerate(file):
                if i == 32:
                    try:
                        self.beta = int(
                            f"{line[35]}{line[36]}"
                        )  # Hardcoded position from TGA files
                    except ValueError:
                        try:
                            self.beta = int(f"{line[35]}")
                        except ValueError:
                            self.beta = int(
                                input(
                                    "Unable to read temperature step from file:\n{file}\n please insert manualy "
                                )
                            )
        return self.beta

    def load_data(self, path: str):
        """Load a STAfile data as pandas dataframe.

        Args:
            path (str): Path to a file.
        """
        self._df = pd.read_csv(path, sep=",", encoding="cp1250", skiprows=34)
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

    def process(self, filter):
        """Calculates and filters first and second derivatives of df.mass array

        Args:
            Filter (Class): instance of Filter class
        """
        # 1. TG
        self._df["mass_filtered"] = filter.apply(self._df.time, self._df.mass)
        # 2. DTG
        self._df["mass_diff_unfiltered"] = -np.gradient(
            self._df.mass_filtered, self._df.time
        )
        self._df["mass_diff_filtered"] = filter.apply(
            self._df.time, self._df.mass_diff_unfiltered
        )
        # 3. DDTG
        self._df["mass_diff2_unfiltered"] = abs(
            np.gradient(self._df.mass_diff_filtered, self._df.time)
        )
        self._df["mass_diff2_filtered"] = abs(
            filter.apply(self._df.time, self._df.mass_diff2_unfiltered)
        )
