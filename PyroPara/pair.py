from stafile import STAfile
from filter import Filter


class Pair:
    def __init__(self, stafile, filter=None):

        if isinstance(stafile, STAfile):
            self.stafile = stafile
        else:
            raise AttributeError("Invalid stafile")
