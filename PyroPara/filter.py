import pandas as pd
from scipy import signal

"""
Class for defining filters to by used on STAfila class during process method

args

type  = type of window of filter
cutoff = frequency at which to start the filter
winsize =  size of filter window
"""

# TODO: place checks and confirmations to improve stability. Write tests

# settings for beta, only for Hamming window
# 50 K  cutoff = 3.6 window = 33
# 30 K  cutoff = 2.5 window = 41
# 10 K  cutoff = 0.25 window = 87
# 05 K  cutoff = 0.2 window = 191


class Filter:
    def __init__(self, type: str, cutoff: float, winsize: int):
        self.type = type
        self.cutoff = cutoff
        self.winsize = winsize

    def apply(self, x: pd.array, y: pd.array):
        """samples frequency of given data and filters with
           specified window with cuttof of half of Nqyst frequency

        Args:
            x (pd.array): time array
            y (pd.array): mass array
        Returns:
            (pd.array): filtered _df.mass array
        """
        self.sample = 1 / (x[1] - x[0])
        w = signal.firwin(
            self.winsize, self.cutoff / (0.5 * self.sample), window=self.type
        )
        return signal.filtfilt(w, 1, y)
