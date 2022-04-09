import glob
from typing import List

from PyroPara.filter import HANNING, Filter
from PyroPara.stafile import STAfile
from PyroPara.utils import get_beta


class Analysis:
    def __init__(self) -> None:
        self.sta_files: List[STAfile] = []

    def __len__(self) -> int:
        return len(self.sta_files)

    def load_all_files(self, directory: str):
        """Loads all files from given directory.
        Assigns default filters

        Args:
            directory (str): Directory path

        Raises:
            Exception: Default filter failed to load
        """

        self.sta_files.clear()

        files = glob.glob(f"{directory}/PYRO**.txt")
        self._default_filter = HANNING

        for path in files:

            # Retrieves heating rate (beta)
            beta = get_beta(path)

            filter = self._default_filter.get(beta)

            if filter is None:
                raise Exception("Default filter failed to load")

            # STAfile class initialization and loading
            file = STAfile(path=path, beta=beta, filter=filter)
            file.load()

            self.sta_files.append(file)

    def load_file(self, path: str, filter: Filter = None):
        """Loads single file from directory and assigns given filter.

        Args:
            path (str): File path
            filter (Filter, optional): Filter:class to assign.
                Defaults to None.
        """
        self._default_filter = HANNING

        beta = get_beta(path)
        if filter is None:
            default_filter = self._default_filter.get(beta)
        file = STAfile(path=path, beta=beta, filter=default_filter)
        file.load()

        self.sta_files.append(file)

    def run(self):
        """Runs process method for all stafiles:STAfile in self.sta_files"""
        for file in self.sta_files:
            file.process()
            file.calculate_local_minima()

    def change_filter(
        self, sta_file: STAfile, type: str, cutoff: float, winsize: int
    ):
        if sta_file is None:
            raise Exception("file not found")
        elif sta_file is not isinstance(sta_file, STAfile):
            raise Exception("wrong file type")

        filter = Filter(type, cutoff, winsize)
        sta_file.filter(filter)

    @property
    def default_filter(self):
        return self._default_filter

    @default_filter.setter
    def default_filter(self, default_filter: dict):
        self._default_filter = default_filter.upper()
