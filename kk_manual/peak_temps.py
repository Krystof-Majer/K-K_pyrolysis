import matplotlib.pyplot as plt
import numpy as np
import os.path
from scipy.signal import savgol_filter, argrelmin

# Script for manualy finding peak decomposition temperatures from set of files
# Used for tuning the process !!NOT FINAL!!


def Mass_diff(MASS, TIME):
    """
    function to manualy calculate finite difference

    """
    diff = []
    for i in range(1, len(MASS) - 1):
        m_loss = -(MASS[i + 1] - MASS[i - 1]) / (TIME[i + 1] - TIME[i - 1])
        diff.append(m_loss)
    return diff


# file init#
STA_file = [
    "kk_manual\PYRO_MDF_30_900_N2_10Kmin_01.txt",
    "kk_manual\PYRO_MDF_30_900_N2_30Kmin_recal_02.txt",
    "kk_manual\PYRO_MDF_30_700_N2_50_Kmin_recal_02.txt",
]

# decimation factor for data reduction
dec_koef = 3

# Searching for local minima in given temperature range between low and high
low = 450
high = 750

# order by which to search minima, higher -> more selective
minorder = 5

#  True to show plots
show = True

for file in STA_file:
    exists = os.path.isfile(file)

    temperature_step = int(f"{file[29]}{file[30]}")  # Temperature step of data
    dec_koef = 3  # decimation factor for data reduction

    # reading file
    if exists:
        DATA = np.loadtxt(file, delimiter=",", skiprows=35)
        TEMPERATURE = DATA[::dec_koef, 0] + 273.15
        MASS = DATA[::dec_koef, 3]
        TIME = DATA[::dec_koef, 1]

    MSL_1 = Mass_diff(MASS, TIME)
    MSL_2 = Mass_diff(MSL_1, TIME)

    # doubeling filters
    MASS_f = savgol_filter(MASS, 21, 3)
    MASS_f = savgol_filter(MASS_f, 11, 3)
    # MASS_f = MASS

    MSL_1_f = Mass_diff(MASS_f, TIME)

    MSL_1_f = savgol_filter(MSL_1_f, 21, 3)
    MSL_1_f = savgol_filter(MSL_1_f, 11, 3)

    MSL_2_f = Mass_diff(MSL_1_f, TIME)

    MSL_2_f = savgol_filter(MSL_2_f, 31, 3)
    MSL_2_f = savgol_filter(MSL_2_f, 11, 3)

    # temperatures had to be cut due to shrinking of mass fraction array from differentiations
    TEMPERATURE_1 = TEMPERATURE[2::]
    TEMPERATURE_2 = TEMPERATURE_1[2::]

    #  Ploting all curves in subplot
    fig, ax = plt.subplots(3, sharex=True)
    if exists:
        ax[0].plot(
            TEMPERATURE, MASS, "r", label="unfiltered", alpha=0.3, zorder=1
        )
        ax[0].plot(TEMPERATURE, MASS_f, "g", label="filtered", zorder=2)
        ax[0].legend()
        ax[0].title.set_text("Mass fraction to Temperature")

        ax[1].plot(TEMPERATURE_1, MSL_1, "r", alpha=0.3, zorder=1)
        ax[1].plot(TEMPERATURE_1, MSL_1_f, "g", zorder=2)
        ax[1].title.set_text("First derivative")

        ax[2].plot(TEMPERATURE_2, MSL_2, "r", alpha=0.3, zorder=1)
        ax[2].plot(TEMPERATURE_2, MSL_2_f, zorder=2)
        ax[2].title.set_text("Second derivative")

        minTemp = argrelmin(MSL_2_f, order=minorder)
        Mpoints = []
        Tpoints = []
        for mins in minTemp[0]:
            if TEMPERATURE_2[mins] >= low and TEMPERATURE_2[mins] <= high:
                Mpoints.append(MSL_2_f[mins])
                Tpoints.append(TEMPERATURE_2[mins])

        # ploting local minima points for visual confirmation
        ax[2].plot(
            Tpoints, Mpoints, "k", linestyle="none", marker="x", zorder=3
        )

        #  Axis labels
        ax[2].set_xlabel("Temperature (K)")
        ax[0].set_ylabel("Mass (%)")
        ax[1].set_ylabel("Mass loss rate (%)")
        ax[2].set_ylabel("MSL deviation (%)")
        fig.suptitle(file, fontsize=16)

        print(f"--- points for: {temperature_step} K step ---")

        #  Output of all found points
        for i in range(len(Mpoints)):
            print([Tpoints[i], Mpoints[i]])

        if show:
            plt.show()
