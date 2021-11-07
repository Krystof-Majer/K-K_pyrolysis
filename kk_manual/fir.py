from matplotlib.pyplot import legend
import numpy as np
from numpy.fft import rfft, rfftfreq
import matplotlib.pylab as plt
from math import log10, pi
from scipy import signal


def main():
    # Hz
    fs = 100
    samplingInterval = 1 / fs
    f1 = 4
    f2 = 5
    WINDOW = "hamming"

    ts = np.arange(0, 5, samplingInterval)
    ys1 = np.sin(2 * pi * f1 * ts)
    ys2 = np.sin(2 * pi * f2 * ts)
    ys = ys1 + ys2
    ys_noisy = ys + np.random.normal(0, np.max(ys) * 0.1, len(ys))

    plt.plot(ts, ys_noisy, label="noisy")
    plt.plot(ts, ys1, label=f"{f1} Hz")
    plt.plot(ts, ys2, label=f"{f2} Hz")
    plt.plot(ts, ys, label="clean")
    plt.xlabel("Time [s]")
    plt.legend()

    freq = rfftfreq(len(ys_noisy), d=1 / fs)
    w = signal.get_window(WINDOW, len(ys_noisy))
    # w = np.ones(len(ys_noisy))
    y = np.abs(rfft(ys_noisy * w)) / len(ys_noisy)

    plt.figure()
    plt.plot(freq, y)
    plt.xlabel("Frequency [Hz]")

    # Hz
    # Cutoff is normalized to the Nyquist frequency, which is half the sampling rate.
    CUT_OFF = 15 / (0.5 * fs)
    COEFF_COUNT = 101
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html#scipy.signal.get_window
    fir = signal.firwin(COEFF_COUNT, CUT_OFF, window=WINDOW)
    # y_filtred = signal.lfilter(fir, 1, ys_noisy)
    y_filtred = signal.filtfilt(fir, 1, ys_noisy)
    # https://dsp.stackexchange.com/questions/52219/savitzky-golay-filter-vs-iir-or-fir-linear-filter
    # y_filtred = signal.savgol_filter(ys_noisy, 11, 1)

    plt.figure()
    plt.plot(ts, ys_noisy, label="noisy")
    plt.plot(ts, ys, "-r", label="clean")
    plt.plot(ts, y_filtred, "--k", label="filtred")
    plt.xlabel("Time [s]")
    plt.legend()

    plt.figure()

    for WINDOW in (
        "hann",
        "hamming",
        "blackman",
        ("kaiser", 4),
        ("kaiser", 8),
        ("kaiser", 14),
    ):
        fir = signal.firwin(COEFF_COUNT, CUT_OFF, window=WINDOW)
        w, h = signal.freqz(fir)
        plt.plot(w * fs / 2 / pi, 20 * np.log10(abs(h)), label=WINDOW)

    sg = (COEFF_COUNT, 2)
    fir = signal.savgol_coeffs(*sg)
    w, h = signal.freqz(fir)
    plt.plot(w * fs / 2 / pi, 20 * np.log10(abs(h)), label=f"S-G {sg}")

    plt.grid(True)
    plt.legend()
    plt.title("FIR filter frequency response")
    plt.ylabel("Amplitude [dB]")
    plt.xlabel("Frequency [Hz]")
    print(plt.yticks(np.linspace(-200, 0, 10 + 1)))

    print(f"1:10 = {20 * log10(1 / 10)} dB")
    print(f"1:100 = {20 * log10(1 / 100)} dB")
    print(f"1:1000 = {20 * log10(1 / 1000)} dB")

    plt.show()


if __name__ == "__main__":
    main()
