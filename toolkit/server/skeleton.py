
class Skeleton(object):

    def __init__(self, init_angle, init_position):
        self.init_angle = init_angle
        self.init_position = init_position

    def get_init_angle(self):
        return self.init_angle

    def get_init_position(self):
        return self.init_position

def create(*args):
    return Skeleton(*args)
