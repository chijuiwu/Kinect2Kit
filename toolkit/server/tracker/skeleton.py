class Skeleton(object):
    def __init__(self, timestamp, init_tracking_id, init_body, init_angle, init_center_position):
        self.last_updated = timestamp
        self.tracking_id = init_tracking_id
        self.body = init_body
        self.previous_bodies = list()
        self.previous_bodies.append(init_body)
        self.init_angle = init_angle
        self.init_center_position = init_center_position

    def get_tracking_id(self):
        return self.tracking_id

    def get_body(self):
        return self.body

    def get_previous_bodies(self):
        return self.previous_bodies

    def get_init_angle(self):
        return self.init_angle

    def get_init_position(self):
        return self.init_center_position


def create(*args):
    return Skeleton(*args)
