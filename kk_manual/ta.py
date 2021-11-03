from glob import glob
from os import chdir
from os.path import dirname
import pandas as pd
import numpy as np


def process_file(file_path):
    df = pd.read_csv(file_path, sep=",", encoding="cp1250", skiprows=34)
    df.rename(
        columns={
            df.columns[0]: "temperature",
            df.columns[1]: "time",
            df.columns[2]: "mass",
        },
        inplace=True,
    )
    df.temperature += 273.15
    df["mass_diff"] = np.gradient(df.mass, df.time)
    df["mass_diff2"] = np.gradient(df.mass_diff, df.time)
    print(df.head())


def main():
    # set working directory to where is this script
    chdir(dirname(__file__))

    for file_path in glob("*.txt"):
        process_file(file_path)
        # TODO: remove when done
        break


if __name__ == "__main__":
    main()
