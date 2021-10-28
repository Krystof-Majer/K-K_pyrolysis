import matplotlib.pyplot as plt
import numpy as np
import os.path
from scipy.signal import savgol_filter

from PyroPara.files import TemperatureFile

# file init#
STA_file = ""

STA_file = "kk_manual\PYRO_MDF_30_900_N2_10Kmin_01.txt"
exists = os.path.isfile(STA_file)


""" def TemperatureStep():
    file = open(STA_file, "r")
    to_read = [30]
    for position, line in enumerate(file):
        if position in to_read:
            TEMPERATURE_STEP = float(line(36, 38))
    return TEMPERATURE_STEP


TemperatureStep()
print(TEMPERATURE_STEP) """  # not working


def Mass_diff(MASS, TIME):
    diff = []
    for i in range(1, len(MASS) - 1):
        m_loss = -(MASS[i + 1] - MASS[i - 1]) / (TIME[i + 1] - TIME[i - 1])
        diff.append(m_loss)
    return diff


temperature_step = 10
dec_koef = 3


# reading file
if exists:
    DATA = np.loadtxt(STA_file, delimiter=",", skiprows=35)
    TEMPERATURE = DATA[::dec_koef, 0]
    MASS = DATA[::dec_koef, 3]
    TIME = DATA[::dec_koef, 1]

MSL_1 = Mass_diff(MASS, TIME)
MSL_2 = Mass_diff(MSL_1, TIME)

MASS_f = savgol_filter(MASS, 41, 3)

MSL_1_f = Mass_diff(MASS_f, TIME)
MSL_1_f = savgol_filter(MSL_1_f, 41, 3)

MSL_2_f = Mass_diff(MSL_1_f, TIME)
MSL_2_f = savgol_filter(MSL_2_f, 41, 3)


TEMPERATURE_1 = TEMPERATURE[2::]
TEMPERATURE_2 = TEMPERATURE_1[2::]

fig, ax = plt.subplots(3)
if exists:
    ax[0].plot(TEMPERATURE, MASS, "r", alpha=0.3, zorder=1)
    ax[0].plot(TEMPERATURE, MASS_f, "g", zorder=2)
    ax[1].plot(TEMPERATURE_1, MSL_1, "r", alpha=0.3, zorder=1)
    ax[1].plot(TEMPERATURE_1, MSL_1_f, "g", zorder=2)
    ax[2].plot(TEMPERATURE_2, MSL_2, "r", alpha=0.3, zorder=1)
    ax[2].plot(TEMPERATURE_2, MSL_2_f, "g", zorder=2)
    plt.show()
