import glob
import numpy as np
from PyroPara.stafile import STAfile
from PyroPara.filter import FILTERS
from PyroPara.utils import get_beta
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from typing import List

"""
Params = namedtuple("Params", ["cutoff", "winsize", "filtertype"])
beta5 = Params(0.2, 191, "hanning")
beta10 = Params(0.25, 87, "hanning")
beta30 = Params(2.5, 41, "hanning")
beta50 = Params(3.6, 33, "hanning")


DEFAULT_FILTER_PARAMS = {
    5.0: beta5,
    10.0: beta10,
    30.0: beta30,
    50.0: beta50,
}
"""
MINORDER = 10


class Analysis:
    def __init__(self) -> None:
        self.sta_files: List[STAfile] = []  #  any effect?

    def __len__(self) -> int:
        return len(self.sta_files)

    def load_files(self, directory: str):

        # glob.glob() return a list of file name with specified pathname
        self.sta_files.clear()

        files = glob.glob(f"{directory}/PYRO**.txt")

        for path in files:

            # Retrieves heating rate (beta)
            beta = get_beta(path)

            default_filter = FILTERS.get(beta)

            if default_filter is None:
                raise Exception("Default filter failed to load")

            # STAfile class initialization and loading
            file = STAfile(path=path, beta=beta, filter=default_filter)
            file.load()

            self.sta_files.append(file)

    def run(self):
        # use process method from STAfile
        for file in self.sta_files:
            file.process()
            self.local_minima(file)
            self.plot(file)

    def local_minima(
        self,
        *,
        stafile: STAfile,
        minorder: int = 7,
        min_temp: float = 500,
        max_temp: float = 750,
        autofind: bool = False,
    ):
        mass_array = stafile._df.mass_diff2_filtered.to_numpy()
        temperature_array = stafile._df.temperature.to_numpy()
        stafile.local_minima.clear()
        Mpoints = []
        Tpoints = []
        if autofind == False:
            temp_minima = argrelextrema(
                mass_array, np.less_equal, order=minorder
            )
            for min_ in temp_minima[0]:
                if (
                    temperature_array[min_] >= min_temp
                    and temperature_array[min_] <= max_temp
                ):
                    Mpoints.append(mass_array[min_])
                    Tpoints.append(temperature_array[min_])
                stafile.local_minima.append.zip(Tpoints, Mpoints)
        else:
            while (
                len(stafile.local_minima) > 10
                or len(stafile.local_minima) == 0
            ):  # Inefficient!
                temp_minima = argrelextrema(
                    mass_array, np.less_equal, order=minorder
                )
                for min_ in temp_minima[0]:
                    if (
                        temperature_array[min_] >= min_temp
                        and temperature_array[min_] <= max_temp
                    ):
                        Mpoints.append(mass_array[min_])
                        Tpoints.append(temperature_array[min_])
                    stafile.local_minima.append.zip(Tpoints, Mpoints)
                minorder += 1
        return stafile.local_minima

    def plot(self, stafile: STAfile):

        plt.figure()
        plt.plot(stafile._df.temperature, stafile._df.mass_filtered, "-")
        plt.plot(
            stafile._df.temperature,
            stafile._df.mass_diff_unfiltered,
            "r",
            alpha=0.3,
        )
        plt.plot(stafile._df.temperature, stafile._df.mass_diff_filtered, "-")
        plt.plot(
            stafile._df.temperature,
            stafile._df.mass_diff2_unfiltered,
            "r",
            alpha=0.3,
        )
        plt.plot(stafile._df.temperature, stafile._df.mass_diff2_filtered, "-")

        plt.title(f"{stafile.path}")
        plt.set_xlabel("Temperature (K)")
        plt.set_ylabel("MSL (0-1))")

        # Plot of local minima points/lines #
        temperature, mass = np.array(stafile.local_minima).T
        plt.plot(temperature, mass, "kx")
        plt.vlines(
            temperature,
            0,
            max(stafile._df.mass_diff2_unfiltered),
            "k",
            alpha=0.7,
        )
        plt.legend()
