class Joint(object):
    def __init__(self, joint_type, kinect_coordinate, worldview_coordinate):
        self.joint_type = joint_type
        self.kinect_coordinate = kinect_coordinate
        self.worldview_coordinate = worldview_coordinate

    def get_joint_type(self):
        return self.joint_type

    def get_kinect_coordinate(self):
        return self.kinect_coordinate

    def get_worldview_coordinate(self):
        return self.worldview_coordinate


def create(*args):
    return Joint(*args)
