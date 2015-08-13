class Session(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.addr


def create(*args):
    return Session(*args)
