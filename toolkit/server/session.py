
class Session(object):

    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.terminated = False

    def get_addr(self):
        return self.addr

    def terminate(self):
        self.terminated = True

def create(*args):
    return Session(*args)
