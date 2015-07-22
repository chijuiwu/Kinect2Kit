class Session(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.killed = False

    def get_addr(self):
        return self.addr

    def kill(self):
        self.killed = True


def create(*args):
    return Session(*args)
