import numpy as np
import pandas as pd


class STAfile:
    number_of_files = 0
    list_of_files = []

    def __init__(self) -> None:
        self._df = None

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

        STAfile.number_of_files += 1
        STAfile.list_of_files.append(path)
        return self._df

    def process(self):  # Need access to filter function!!!
        """Derivatves of mass data series"""

        # 1. TG
        self._df["mass_filtered"] = filter(self._df.time, self._df.mass)
        # 2. DTG
        self._df["mass_diff_unfiltered"] = -np.gradient(
            self._df.mass_filtered, self._df.time
        )
        self._df["mass_diff_filtered"] = filter(
            self._df.time, self._df.mass_diff_unfiltered
        )
        # 3. DDTG
        self._df["mass_diff2_unfiltered"] = abs(
            np.gradient(self._df.mass_diff_filtered, self._df.time)
        )
        self._df["mass_diff2_filtered"] = abs(
            filter(self._df.time, self._df.mass_diff2_unfiltered)
        )
        return self._df_processed
