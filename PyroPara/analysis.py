from PyroPara.stafile import STAfile
from PyroPara.filter import Filter
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from os import listdir
import glob

# dictionary of default filter parameters to be used if not specified by user
# {beta:(cutoff,window_size)}
DEFAULT_FILTER_PARAMS = {
    "5": (0.2, 191),
    "10": (0.25, 87),
    "30": (2.5, 41),
    "50": (3.6, 33),
}


class analysis:
    def __init__(self) -> None:
        self.stafile_list = []  # (file,filter)
        self.filter_list = []

    def get_data(self, path: str):
        # glob.glob() return a list of file name with specified pathname
        file_list = glob.glob(f"{path}/PYRO**.txt")
        for f in file_list:
            # STAfile.load_data(f)
            # STAfile.beta(f)
            self.stafile.append([f])  # Appends to list as another list
        return self.stafile

    def assign_filter(self, index: int, filter):
        """assign filter object to stafile object in list

        Args:
            index (int): position of stafile object in list
            filter (Class | list): filter objects to by assigned

        Raises:
            TypeError: filter object is not of correct type
        """
        if isinstance(filter, Filter):
            if len(self.stafile[index]) == 1:
                self.stafile[index].append(filter)
            else:
                self.stafile[index][1] = self.stafile[index][filter]
        elif isinstance(filter, list):
            for entry in filter:
                i = index
                if not isinstance(filter, Filter):
                    raise TypeError("incorect filter...")
                if len(self.stafile[i]) == 1:
                    if not isinstance(filter, Filter):
                        raise TypeError("incorect filter...")
                    self.stafile[i].append(filter[entry])
                    i += 1
                else:
                    self.stafile[i][1] = self.stafile[i][entry]

    def run(self):

        # TODO: check internal logic and data handeling

        for pair in self.stafile:
            if len(pair) == 1:
                beta = DEFAULT_FILTER_PARAMS.get(str(STAfile.beta(pair)))
                self.stafile[pair][1].append(
                    Filter(DEFAULT_FILTER_PARAMS(beta))
                )
            self.df = STAfile.load_data(pair[0])

    def plot():
        pass
