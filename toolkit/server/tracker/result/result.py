class Result(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp


def create(*args):
    return Result(*args)
