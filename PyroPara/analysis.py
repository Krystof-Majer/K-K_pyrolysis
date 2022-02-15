import glob
from typing import List

from PyroPara.filter import FILTERS
from PyroPara.stafile import STAfile
from PyroPara.utils import get_beta


class Analysis:
    def __init__(self) -> None:
        self.sta_files: List[STAfile] = []

    def __len__(self) -> int:
        return len(self.sta_files)

    def load_files(self, directory: str):
        self.sta_files.clear()

        # glob.glob() return a list of file name with specified pathname
        files = glob.glob(f"{directory}/PYRO**.txt")

        for path in files:
            # Retrieves heating rate (beta)
            beta = get_beta(path)

            # Default filter initialization
            default_filter = FILTERS.get(beta)

            if default_filter is None:
                raise Exception("Default filter failed to load")

            # STAfile class initialization and loading
            file = STAfile(path=path, beta=beta, filter=default_filter)
            file.load()

            self.sta_files.append(file)

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
