import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from PyroPara.filter import Filter


class STAfile:
    def __init__(
        self, *, path: str, beta: float = None, filter: Filter = None
    ) -> None:
        self._df = None
        self.filter = filter
        self.path = path
        self.beta = beta
        self.local_minima = []

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

    def local_minima(
        self,
        *,
        minorder: int = 7,
        min_temp: float = 500,
        max_temp: float = 750,
        autofind: bool = False,
    ):
        mass_array = self._df.mass_diff2_filtered.to_numpy()
        temperature_array = self._df.temperature.to_numpy()
        self.local_minima.clear()
        m_points = []
        t_points = []
        if not autofind:
            temp_minima = argrelextrema(
                mass_array, np.less_equal, order=minorder
            )
            for min_ in temp_minima[0]:
                if (
                    temperature_array[min_] >= min_temp
                    and temperature_array[min_] <= max_temp
                ):
                    m_points.append(mass_array[min_])
                    t_points.append(temperature_array[min_])
                self.local_minima.append.zip(t_points, m_points)
        else:
            while len(self.local_minima) > 10 or len(self.local_minima) == 0:
                temp_minima = argrelextrema(
                    mass_array, np.less_equal, order=minorder
                )
                for min_ in temp_minima[0]:
                    if (
                        temperature_array[min_] >= min_temp
                        and temperature_array[min_] <= max_temp
                    ):
                        m_points.append(mass_array[min_])
                        t_points.append(temperature_array[min_])
                    self.local_minima.append.zip(t_points, m_points)
                minorder += 1

    def plot(self):

        y_filtered = self._df.mass_filterd
        x = self._df.temperature
        y = self._df.mass_unfiltered

        plt.figure()
        plt.plot(x, y_filtered, "-")
        plt.plot(
            x,
            y,
            "r",
            alpha=0.3,
        )
        plt.plot(x, y_filtered, "-")
        plt.plot(
            x,
            y,
            "r",
            alpha=0.3,
        )
        plt.plot(x, y_filtered, "-")
        plt.title(f"{self.path}")
        plt.set_xlabel("Temperature (K)")
        plt.set_ylabel("MSL (0-1))")

        # Plot of local minima points/lines #
        temperature, mass = np.array(self.local_minima).T
        plt.plot(temperature, mass, "kx")
        plt.vlines(
            temperature,
            0,
            max(y),
            "k",
            alpha=0.7,
        )
        plt.legend()
