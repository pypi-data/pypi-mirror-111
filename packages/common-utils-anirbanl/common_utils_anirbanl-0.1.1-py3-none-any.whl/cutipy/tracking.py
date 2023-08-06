import time
from collections import OrderedDict

class Timer:
    def __init__(self):
        self.dts = OrderedDict()

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *exc):
        end_time = time.time()
        self.dts[self.name] = end_time - self.start_time
        del self.start_time
        del self.name

    def register(self, name):
        self.name = name

    def __repr__(self):
        s = ''
        for k,v in self.dts.items():
            s = s + f"{k} : {v} secs\n"
        return s

    def purge(self):
        self.dts = OrderedDict()