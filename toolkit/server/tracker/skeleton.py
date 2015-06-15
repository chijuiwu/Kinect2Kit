class Skeleton(object):
    def __init__(self, init_timestamp, init_tracking_id, init_kinect_body, init_worldview_body, init_angle,
                 init_center_position):
        self.last_updated = init_timestamp
        self.tracking_id = init_tracking_id
        self.kinect_body = init_kinect_body
        self.worldview_body = init_worldview_body
        self.previous_bodies_list = list()
        self.previous_bodies_list.append((init_kinect_body, init_worldview_body))
        self.init_angle = init_angle
        self.init_center_position = init_center_position

    def update(self, timestamp, tracking_id, kinect_body, worldview_body):
        self.last_updated = timestamp
        self.tracking_id = tracking_id
        self.kinect_body = kinect_body
        self.worldview_body = worldview_body

    def get_last_updated(self):
        return self.last_updated

    def get_tracking_id(self):
        return self.tracking_id

    def get_kinect_body(self):
        return self.kinect_body

    def get_worldview_body(self):
        return self.worldview_body

    def get_previous_bodies(self):
        return self.previous_bodies_list

    def get_init_angle(self):
        return self.init_angle

    def get_init_position(self):
        return self.init_center_position


def create(*args):
    return Skeleton(*args)
