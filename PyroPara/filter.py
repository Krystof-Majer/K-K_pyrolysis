from scipy import signal

"""
Class for defining filters to by used on STAfila class during process method

args

type  = type of window of filter
cutoff = frequency at which to start the filter
winsize =  size of filter window
"""

# TODO: place checks and confirmations to improve stability. Write tests


class Filters:
    def __init__(self, name: str, type: str, cutoff: int, winsize: int):
        self.type = type
        self.cutoff = cutoff
        self.winsize = winsize
        self.name = name

    def f_sample(self, x: int):
        """
        Takes in the time axis of data and samples the freqency
        """
        self.sample = 1 / (x[1] - x[0])
        return self.sample

    def filt(self, y: int):

        self.sample = Filters.f_sample()
        w = signal.firwin(
            self.winsize, self.cutoff / (0.5 * self.sample), window=self.type
        )
        return signal.filtfilt(w, 1, y)
