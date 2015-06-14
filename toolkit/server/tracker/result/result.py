class Result(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.perspectives_dict = dict()

    def add_perspective(self, perspective):
        self.perspectives_dict[perspective.get_namme()] = perspective

    def get_perspectives(self):
        return self.perspectives_dict


def create(*args):
    return Result(*args)
