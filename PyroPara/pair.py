from stafile import STAfile
from filter import Filter


class Pair:
    """Associative class to keep together stafiles with assigned filters"""

    def __init__(self, stafile, filter=None):

        if isinstance(stafile, STAfile):
            self.stafile = stafile
        else:
            raise AttributeError("Invalid stafile")

        if not isinstance(filter, Filter):
            raise AttributeError("Invalid filter")
        elif isinstance(filter, Filter):
            self.filter = filter
        else:
            self.filter = None

    def get_stafile(self):
        return self.stafile

    def get_filter(self):
        return self.filter
