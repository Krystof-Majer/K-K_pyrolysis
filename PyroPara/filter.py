import pandas as pd
from scipy import signal


class Filter:
    def __init__(
        self, *, type_: str = None, cutoff: float = None, winsize: int = None
    ):
        self.type = type_
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


FILTERS = {
    5.0: Filter(type_="hanning", cutoff=0.2, winsize=191),
    30.0: Filter(type_="hanning", cutoff=2.5, winsize=41),
    50.0: Filter(type_="hanning", cutoff=3.6, winsize=33),
    10.0: Filter(type_="hanning", cutoff=0.25, winsize=87),
}
