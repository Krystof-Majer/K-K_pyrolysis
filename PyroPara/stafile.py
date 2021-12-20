import numpy as np
import pandas as pd
from filter import Filters

# TODO: make sure the approach is not dead end. Write tests


class STAfile:
    list_of_files = []
    dict_of_filters = {}

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

        STAfile.list_of_files.append(path)
        return self._df

    def add_filter(self, filter_to_add):
        """adds Filters class instance to dict paired with is name attribute as key"""
        if isinstance(filter_to_add, Filters):
            STAfile.list_of_filters.update(filter_to_add.name, filter_to_add)

    def process(self, filter_to_use: str):
        """
        Differentiation of mass data series

        args:
        filter_to_use: key string
            indicates which filter to use forom list filters added to STAfile instance

        """
        filter_in_use = STAfile.dict_of_filters[filter_to_use]

        # 1. TG
        self._df["mass_filtered"] = filter_in_use.filt(
            self._df.time, self._df.mass
        )
        # 2. DTG
        self._df["mass_diff_unfiltered"] = -np.gradient(
            self._df.mass_filtered, self._df.time
        )
        self._df["mass_diff_filtered"] = filter_in_use.filt(
            self._df.time, self._df.mass_diff_unfiltered
        )
        # 3. DDTG
        self._df["mass_diff2_unfiltered"] = abs(
            np.gradient(self._df.mass_diff_filtered, self._df.time)
        )
        self._df["mass_diff2_filtered"] = abs(
            filter_in_use.filt(self._df.time, self._df.mass_diff2_unfiltered)
        )
