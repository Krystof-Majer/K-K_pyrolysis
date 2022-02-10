import glob
import re
from collections import namedtuple

from PyroPara.filter import Filter
from PyroPara.stafile import STAfile

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

BETA_REGEX = re.compile(r"/(.+)\(K/min\)")


def get_beta(path) -> float:
    """reads beta value from specific place in file"""
    with open(path) as file:
        for line in file:
            if "#RANGE:" in line:
                m = re.search(BETA_REGEX, line)

                if m:
                    return float(m.group(1))

    raise ValueError("Unable to read temperature step from " f"file: {file}")


class Analysis:
    def __init__(self) -> None:
        self.sta_files = []

    def load_files(self, directory: str):
        # glob.glob() return a list of file name with specified pathname
        files = glob.glob(f"{directory}/PYRO**.txt")

        for path in files:
            self.sta_files.append(path)

            # Retrieves heating rate (beta)
            beta = get_beta(path)

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
            path = STAfile(path, default_filter)  # Possible?
            path.load()
            # TODO: make it passable to run method

    def run(self):
        # use process method from STAfile
        for stafile in self.sta_files:
            stafile.process()
        # make data useable to find local minima

    def local_minima(self):  # missing settings as arguments, maybe use default
        # find local minima using argrelextrema
        # save the found points somewhere
        # enable changing point finding settings from argrelestrema
        pass

    def plot():
        # simple placeholder to plot using matplotlib together with points
        # separate graphs, later add show toggle
        pass
