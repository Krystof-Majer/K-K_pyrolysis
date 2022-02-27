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

    def load_files(self, directory: str) -> None:

        # glob.glob() return a list of file name with specified pathname
        self.sta_files.clear()

        files = glob.glob(f"{directory}/PYRO**.txt")

        for path in files:
            # Retrieves heating rate (beta)
            beta = get_beta(path)

            default_filter = FILTERS.get(beta)

            if default_filter is None:
                raise Exception("Default filter failed to load")

            # STAfile class initialization and loading
            file = STAfile(path=path, beta=beta, filter=default_filter)
            file.load()

            self.sta_files.append(file)

    def run(self):
        # use process method from STAfile
        for file in self.sta_files:
            file.process()
            file.local_minima()
