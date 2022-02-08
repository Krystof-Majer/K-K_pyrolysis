from PyroPara.stafile import STAfile
from PyroPara.filter import Filter
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from collections import namedtuple
import glob

# dictionary of default filter parameters to be used if not specified by user
# {beta:(cutoff,window_size)}

Params = namedtuple("Params", ["cutoff", "winsize", "filtertype"])
beta5 = Params(0.2, 191, "hanning")
beta10 = Params(0.25, 87, "hanning")
beta30 = Params(2.5, 41, "hanning")
beta50 = Params(3.6, 33, "hanning")


DEFAULT_FILTER_PARAMS = {
    5.0: beta5,
    10.0: beta10,
    30.0: beta30,
    50.0: beta50,
}


def get_beta(path):  # Placeholder method
    """reads beta value from specific place in file"""
    with open(path) as file:
        for i, line in enumerate(file):
            if i == 32:
                try:
                    beta = float(
                        f"{line[35]}{line[36]}"
                    )  # Hardcoded position from TGA files
                except ValueError:
                    try:
                        beta = float(f"{line[35]}")
                    except ValueError:
                        beta = float(
                            input(
                                "Unable to read temperature step from file:\n{file}\n please insert manualy "
                            )
                        )
    return beta


class Analysis:
    def __init__(self) -> None:
        self.stafiles = []

    def get_files(self, path: str):
        # glob.glob() return a list of file name with specified pathname
        files = glob.glob(f"{path}/PYRO**.txt")
        for path_ in files:
            self.stafiles.append(path_)

            # Retrieves heating rate (beta)
            beta = get_beta(path_)

            # Looks up default filter parameters
            params = DEFAULT_FILTER_PARAMS.get(beta)
            winsize = params.winsize
            cutoff = params.cutoff
            filter_type = params.type

            # Default filter initialization
            if params is not None:
                default_filter = Filter(filter_type, cutoff, winsize)
            else:
                raise Exception("Default filter failed to load")

            # STAfile class initialization and loading
            path_ = STAfile(path_, default_filter)  # Possible?
            path_.load()
            # TODO: make it passable to run method

    def run(self):
        # use process method from STAfile
        for stafile in self.stafiles:
            stafile.process()
        # make data useable to find local minima
        pass

    def local_minima(self):  # missing settings as arguments, maybe use default
        # find local minima using argrelextrema
        # save the found points somewhere
        # enable changing point finding settings from argrelestrema
        pass

    def plot():
        # simple placeholder to plot using matplotlib together with points
        # separate graphs, later add show toggle
        pass
