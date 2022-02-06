from pair import Pair


class Analysis:
    def __init__(self):
        self.pair = []

    def add_pair(self, pair):
        if isinstance(pair, Pair):
            self.pair.append(pair)
        elif isinstance(pair, list):
            for entry in pair:
                if not isinstance(pair, Pair):
                    raise AttributeError("Invalid pair")

            self.pair.append(entry)
        else:
            raise AttributeError("Invalid pair")

    def load_all_files():
        pass

    def run():
        pass

    def plot():
        pass
