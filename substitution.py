class Substitution:
    def __init__(self, to_add, to_bench):
        self.to_add = to_add
        self.to_bench = to_bench

    def __str__(self):
        return "subbing in " + self.to_add + " for " + self.to_bench
