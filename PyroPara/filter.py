import pandas as pd
from scipy import signal


class Filter:
    def __init__(
        self, type: str = None, cutoff: float = None, winsize: int = None
    ):
        self.set_parameters(type=type, cutoff=cutoff, winsize=winsize)

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

    def set_parameters(
        self, *, type: str = None, cutoff: float = None, winsize: int = None
    ):
        if type is not None:
            self.type = type

        if cutoff is not None:
            self.cutoff = cutoff

        if winsize is not None:
            self.winsize = winsize


HANNING = {
    5.0: Filter(type="hanning", cutoff=0.1, winsize=191),
    30.0: Filter(type="hanning", cutoff=1.2, winsize=41),
    50.0: Filter(type="hanning", cutoff=1.6, winsize=33),
    10.0: Filter(type="hanning", cutoff=0.15, winsize=87),
}

BLACKMAN = {
    5.0: Filter(type="blackman", cutoff=0.2, winsize=191),
    30.0: Filter(type="blackman", cutoff=2.5, winsize=41),
    50.0: Filter(type="blackman", cutoff=3.6, winsize=33),
    10.0: Filter(type="blackman", cutoff=0.25, winsize=87),
}
