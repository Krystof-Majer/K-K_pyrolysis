from glob import glob
from os import chdir
from os.path import dirname
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
from scipy import signal
from math import pi

WINDOW = "sg"  # sg for savgol filter
WINDOW = "hamming"
WINDOW_SIZE = 41

CUTOFF_FREQ = 2.5  # Hz

SG_POLYORDER = 2
SG_PARAMS = (WINDOW_SIZE, SG_POLYORDER)

USING_SG = WINDOW.lower() == "sg"


def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def freq_analysis(x, y):
    fs = freq_sample(x)

    freq = rfftfreq(len(y), d=1 / fs)
    w = signal.get_window("hamming", len(y))
    yf = np.abs(rfft(y * w)) / len(y)

    return freq, yf


def freq_sample(x):
    return 1 / (x[1] - x[0])


def plot_freq_analysis(x, y):
    plt.figure()
    f, yf = freq_analysis(x, y)
    plt.plot(f, 20 * np.log10(yf), "-o")
    plt.ylabel("Magnitude [dB]")
    plt.xlabel("Frequency [Hz]")


def plot_filter_response(x):
    plt.figure()
    fs = freq_sample(x)

    if USING_SG:
        fir = signal.savgol_coeffs(*SG_PARAMS)
    else:
        fir = signal.firwin(
            WINDOW_SIZE, CUTOFF_FREQ / (0.5 * fs), window=WINDOW
        )

    w, h = signal.freqz(fir)

    plt.plot(w * fs / 2 / pi, 20 * np.log10(abs(h)), label=WINDOW)
    plt.title("FIR filter frequency response")
    plt.ylabel("Amplitude [dB]")
    plt.xlabel("Frequency [Hz]")
    plt.grid(True)


def filter(x, y):
    fs = freq_sample(x)
    if USING_SG:
        return signal.savgol_filter(y, SG_PARAMS[0], SG_PARAMS[1])
    else:
        # Cutoff is normalized to the Nyquist frequency
        # which is half the sampling rate.
        w = signal.firwin(WINDOW_SIZE, CUTOFF_FREQ / (0.5 * fs), window=WINDOW)
        return signal.filtfilt(w, 1, y)


def process_file(file_path):
    print(f"Processing {file_path}")
    df = pd.read_csv(file_path, sep=",", encoding="cp1250", skiprows=34)
    df.rename(
        columns={
            df.columns[0]: "temperature",
            df.columns[1]: "time",
            df.columns[3]: "mass",
        },
        inplace=True,
    )
    df.temperature += 273.15
    df["mass_filtred"] = filter(df.time, df.mass)
    df["mass_diff"] = np.gradient(df.mass_filtred, df.time)
    df["mass_diff_filtred"] = filter(df.time, df.mass_diff)
    df["mass_diff2"] = np.gradient(df.mass_diff_filtred, df.time)
    df["mass_diff2_filtred"] = filter(df.time, df.mass_diff2)

    return df


def plot(df: DataFrame):
    plt.title("TG")
    plt.plot(df.time, df.mass, "o")
    plt.plot(df.time, df.mass_filtred, "-")
    plot_freq_analysis(df.time, df.mass)

    plt.figure()
    plt.title("DTG")
    plt.plot(df.time, df.mass_diff, "o")
    plt.plot(df.time, df.mass_diff_filtred, "-")
    plot_freq_analysis(df.time, df.mass_diff)

    plt.figure()
    plt.title("DDTG")
    plt.plot(df.time, df.mass_diff2, "o")
    plt.plot(df.time, df.mass_diff2_filtred, "-")
    plot_freq_analysis(df.time, df.mass_diff)

    plt.figure()
    plt.plot(df.time, normalize(df.mass_filtred), "-r", label="TG")
    plt.plot(df.time, normalize(df.mass_diff_filtred), "-g", label="DTG")
    plt.plot(df.time, normalize(df.mass_diff2_filtred), "-b", label="DDTG")
    plt.legend()

    plot_filter_response(df.time)


def main():
    # set working directory to where is this script
    chdir(dirname(__file__))

    for file_path in glob("*.txt"):
        df = process_file(file_path)
        plot(df)
        # TODO: remove when done
        break

    plt.show()


if __name__ == "__main__":
    main()
