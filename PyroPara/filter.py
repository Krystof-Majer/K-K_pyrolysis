import pandas as pd
from scipy import signal


class Filter:
    def __init__(
        self, *, type: str = None, cutoff: float = None, winsize: int = None
    ):
        self.type = type
        self.cutoff = cutoff
        self.winsize = winsize

    def apply(self, time: pd.array, mass: pd.array):

        """samples frequency of given data and filters with
           specified window with cuttof of half of Nqyst frequency

        Args:
            x (pd.array): time array
            y (pd.array): mass array
        Returns:
            (pd.array): filtered _df.mass array
        """
        self.sample = 1 / (time[1] - time[0])
        w = signal.firwin(
            self.winsize, self.cutoff / (0.5 * self.sample), window=self.type
        )
        return signal.filtfilt(w, 1, mass)


# settings for beta, only for Hamming window
# 50 K  cutoff = 3.6 window = 33
# 30 K  cutoff = 2.5 window = 41
# 10 K  cutoff = 0.25 window = 87
# 05 K  cutoff = 0.2 window = 191

FILTERS = {
    50.0: Filter(type="hanning", cutoff=3.6, winsize=33),
}
