import matplotlib.pyplot as plt
from os import chdir
from os.path import dirname
from glob import glob
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from scipy.signal import argrelextrema

# Script for manualy finding peak decomposition temperatures from set of files
# Used for tuning the process !!NOT FINAL!!

MINORDER = 7  # number of points to check against VULNERABLE TO DATA SIZE!!!
MIN_INTERVAL = (
    300,
    600,
)  # Temperature (K) interval to search for mins. Will be bound to filter response


def filter(x, y):  # Will be implemented in separate file
    return y


def _diff(df: DataFrame):

    # derivatives of unfiltered data series
    df["mass_diff"] = -np.gradient(df.mass, df.time)
    df["mass_diff2"] = abs(np.gradient(df.mass_diff, df.time))

    # derivatives of filtered data series
    df["mass_filtered"] = filter(df.time, df.mass)
    df["mass_diff_pre"] = -np.gradient(df.mass_filtered, df.time)
    df["mass_diff_filtered"] = filter(df.time, df.mass_diff_pre)
    df["mass_diff2_pre"] = abs(np.gradient(df.mass_diff_filtered, df.time))
    df["mass_diff2_filtered"] = filter(df.time, df.mass_diff2_pre)


def get_beta(file_path):
    # Gets temperature step used in measurements
    file = open(file_path)
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
    print(beta)
    return beta


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


def get_mins(df: DataFrame):  # TODO: make it work...
    df["loc_mins"] = argrelextrema(
        df.mass_diff2_filtered.values, np.less_equal, order=MINORDER
    )[0]
    Mpoints = []
    Tpoints = []

    for mins in df.loc_mins[0]:
        if (
            df.temperature[mins] >= MIN_INTERVAL[0]
            and df.temperature[mins] <= MIN_INTERVAL[1]
        ):
            Mpoints.append(df.mass_diff2_filtered[mins])
            Tpoints.append(df.temperature[mins])


def plot(df: DataFrame, beta: int):
    fig, ax = plt.subplots(3, sharex=True)
    fig.suptitle(f"{beta} K", fontsize=16)

    ax[0].title.set_text("TG")
    ax[0].plot(df.temperature, df.mass, "r", alpha=0.3)
    ax[0].plot(df.temperature, df.mass_filtered, "-")

    ax[1].title.set_text("DTG")
    ax[1].plot(df.temperature, df.mass_diff, "r", alpha=0.3)
    ax[1].plot(df.temperature, df.mass_diff_filtered, "-")

    ax[2].title.set_text("DDTG")
    ax[2].plot(df.temperature, df.mass_diff2, "r", alpha=0.3)
    ax[2].plot(df.temperature, df.mass_diff2_filtered, "-")

    ax[2].set_xlabel("Temperature (K)")
    ax[0].set_ylabel("Mass (%)")
    ax[1].set_ylabel("MSL (%)")
    ax[2].set_ylabel("MSL deviation (%)")


def main():
    # set working directory to where is this script
    chdir(dirname(__file__))

    for file_path in glob("*.txt"):
        beta = get_beta(file_path)

        df = process(file_path)
        get_mins(df)
        plot(df, beta)

    plt.show()


if __name__ == "__main__":
    main()
