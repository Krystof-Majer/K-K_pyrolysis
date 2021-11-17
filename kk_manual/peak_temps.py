import matplotlib.pyplot as plt
from os import chdir
from os.path import dirname
from glob import glob
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from scipy import signal  # No idea why scipy.signal excludes argrelextrema
from scipy.signal import argrelextrema

# Script for manualy finding peak decomposition temperatures from set of files
# Used for tuning the process !!NOT FINAL!!

# number of points to check against VULNERABLE TO DATA SIZE!!!
MINORDER = 7
# Temperature (K) interval to search for mins. Will be bound to filter response
MIN_INTERVAL = (
    500,
    750,
)
CUTOFF = 3  # Hz
WINSIZE = 41
F_TYPE = "hamming"


def filter(x, y):
    sample = 1 / (x[1] - x[0])
    if F_TYPE == "hamming":
        w = signal.firwin(WINSIZE, CUTOFF / (0.5 * sample), window=F_TYPE)
        return signal.filtfilt(w, 1, y)


def _diff(df: DataFrame):  # TODO: make second derivative usable

    # derivatives of unfiltered data series
    df["mass_diff"] = -np.gradient(df.mass)
    df["mass_diff2"] = np.gradient(df.mass_diff)

    # derivatives of filtered data series
    df["mass_filtered"] = filter(df.time, df.mass)
    df["mass_diff_pre"] = -np.gradient(df.mass_filtered)
    df["mass_diff_filtered"] = filter(df.time, df.mass_diff_pre)
    df["mass_diff2_pre"] = np.gradient(df.mass_diff_filtered)
    df["mass_diff2_filtered"] = filter(df.time, df.mass_diff2_pre)


def get_beta(file_path):
    # Gets temperature step used in measurements
    with open(file_path) as file:
        for i, line in enumerate(file):
            if i == 32:
                try:
                    beta = int(
                        f"{line[35]}{line[36]}"
                    )  # Hardcoded position from TGA files
                except ValueError:
                    try:
                        beta = int(f"{line[35]}")
                    except ValueError:
                        beta = int(
                            input(
                                "Unable to read temperature step from file:\n{file}\n please insert manualy "
                            )
                        )
    return beta


def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def process(file_path):
    df = pd.read_csv(file_path, sep=",", encoding="cp1250", skiprows=34)
    df.rename(
        columns={
            df.columns[0]: "temperature",
            df.columns[3]: "mass",
            df.columns[1]: "time",
        },
        inplace=True,
    )
    df.temperature += 273.15
    _diff(df)
    return df


def get_mins(df: DataFrame):
    loc_mins = argrelextrema(
        abs(df.mass_diff2_filtered.to_numpy()), np.less_equal, order=MINORDER
    )
    Mpoints = []
    Tpoints = []
    for mins in loc_mins[0]:
        if (
            df.temperature[mins] >= MIN_INTERVAL[0]
            and df.temperature[mins] <= MIN_INTERVAL[1]
        ):
            Mpoints.append(df.mass_diff2_filtered[mins])
            Tpoints.append(df.temperature[mins])
    tup = zip(Tpoints, Mpoints)
    return list(tup)


def plot(df: DataFrame, beta: int, points: tuple):
    fig, ax = plt.subplots(3, sharex=True)
    fig.suptitle(f"{beta} K", fontsize=16)

    ax[0].title.set_text("TG")
    ax[0].plot(df.temperature, df.mass, "ro", alpha=0.3)
    ax[0].plot(df.temperature, df.mass_filtered, "-")

    ax[1].title.set_text("DTG")
    ax[1].plot(df.temperature, df.mass_diff, "ro", alpha=0.3)
    ax[1].plot(df.temperature, df.mass_diff_filtered, "-")

    ax[2].title.set_text("DDTG")
    ax[2].plot(df.temperature, abs(df.mass_diff2), "ro", alpha=0.3)
    ax[2].plot(df.temperature, abs(df.mass_diff2_filtered), "-")

    ax[2].set_xlabel("Temperature (K)")
    ax[0].set_ylabel("Mass (%)")
    ax[1].set_ylabel("MSL (%)")
    ax[2].set_ylabel("MSL deviation (%)")

    # Plot of local minima points
    x, y = np.array(points).T
    ax[2].plot(x, y, "kx")

    plt.figure()
    plt.title(f"normalized {beta} K")

    plt.plot(
        df.temperature, normalize(df.mass_diff_filtered), "-g", label="DTG"
    )
    plt.plot(
        df.temperature, normalize(df.mass_diff2_filtered), "-b", label="DDTG"
    )
    plt.legend()


def main():
    # set working directory to where is this script
    chdir(dirname(__file__))

    for file_path in glob("*.txt"):
        beta = get_beta(file_path)

        df = process(file_path)
        points = get_mins(df)
        plot(df, beta, points)

        print(f"--- points for: {beta} K step ---")

        #  Output of all found points
        b = [tup[0] for tup in points]
        print(b)
        print(points)
    plt.show()


if __name__ == "__main__":
    main()
