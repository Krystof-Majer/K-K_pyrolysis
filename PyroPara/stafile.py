import os

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from PyroPara.filter import Filter
from PyroPara.utils import normalize


class STAfile:
    def __init__(
        self, *, path: str, beta: float = None, filter: Filter = None
    ) -> None:
        self._df: pd.DataFrame = None
        self.is_processed = False
        self._filter = filter
        self.path = path
        self.beta = beta
        self.name = os.path.basename(path)
        self.local_minima: list = []

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter: Filter):
        self._filter = filter

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
        self._df["mass_filtered"] = self._filter.apply(
            self._df.time, self._df.mass
        )
        # 2. DTG
        self._df["mass_diff_unfiltered"] = -np.gradient(
            self._df.mass_filtered, self._df.time
        )
        self._df["mass_diff_filtered"] = self._filter.apply(
            self._df.time, self._df.mass_diff_unfiltered
        )
        # 3. DDTG
        self._df["mass_diff2_unfiltered"] = abs(
            np.gradient(self._df.mass_diff_filtered, self._df.time)
        )
        self._df["mass_diff2_filtered"] = abs(
            self._filter.apply(self._df.time, self._df.mass_diff2_unfiltered)
        )
        # 4. DDTG normalized
        self._df["mass_diff2_normalized"] = normalize(
            self._df.mass_diff2_filtered
        )

        self.is_processed = True

    def calculate_local_minima(
        self,
        *,
        minorder: int = 7,
        min_temp: float = 500,
        max_temp: float = 750,
    ):
        """Calculates <= 10 local minima in DDTG curve for a given
        stafile, appends to stafile.local_minima

        Args:
            minorder (int, optional): Number of nearby points to consider
            for possible local minimum. Defaults to 7.

            min_temp (float, optional): Lower bound of temperature interval.
                Defaults to 500.

            max_temp (float, optional): Upper bound of temperature interval.
                Defaults to 750.
        """
        if not self.is_processed:
            self.process()

        self.local_minima.clear()
        points = []

        while True:
            points = self.find_local_minima(minorder, min_temp, max_temp)
            if len(points) < 11 and len(points) > 0:
                break
            minorder = +1

        self.local_minima.extend(points)

    def find_local_minima(
        self,
        minorder: int,
        min_temp: int,
        max_temp: int,
    ):
        """Calculates local minima for given DDTG stafile with fixed parameters

        Args:
            minorder (int): Number of nearby points to consider
            for possible local minimum.

            min_temp (int): Lower bound of temperature interval.
            max_temp (int): Upper bound of temperature interval.

        Returns:
            _type_: _description_
        """
        mass_array = self._df.mass_diff2_filtered.to_numpy()
        temperature_array = self._df.temperature
        points = []

        temp_minima = argrelextrema(mass_array, np.less_equal, order=minorder)
        for min_ in temp_minima[0]:
            if (
                temperature_array[min_] >= min_temp
                and temperature_array[min_] <= max_temp
            ):
                tup = (temperature_array[min_], mass_array[min_])
                points.append(tup)

        return points
