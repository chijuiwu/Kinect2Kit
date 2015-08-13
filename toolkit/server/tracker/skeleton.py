class Skeleton(object):
    def __init__(self, timestamp, tracking_id, kinect_body, worldview_body, init_angle, init_center_position):
        self.last_updated = timestamp
        self.tracking_id = tracking_id
        self.kinect_body = kinect_body
        self.worldview_body = worldview_body
        self.init_angle = init_angle
        self.init_center_position = init_center_position

    def update(self, timestamp, tracking_id=None, kinect_body=None, worldview_body=None):
        self.last_updated = timestamp

        if tracking_id is not None:
            self.tracking_id = tracking_id

        if kinect_body is not None:
            self.kinect_body = kinect_body

        if worldview_body is not None:
            self.worldview_body = worldview_body

    def get_last_updated(self):
        return self.last_updated

    def get_tracking_id(self):
        return self.tracking_id

    def get_kinect_body(self):
        return self.kinect_body

    def get_worldview_body(self):
        return self.worldview_body

    def get_init_angle(self):
        return self.init_angle

    def get_init_center_position(self):
        return self.init_center_position


def create(*args):
    return Skeleton(*args)
