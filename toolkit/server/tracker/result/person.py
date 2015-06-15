class Person(object):
    def __init__(self, name):
        self.name = name
        self.skeletons_dict = dict()

    def get_name(self):
        return self.name

    def add_skeleton(self, is_transformed, kinect_name, kinect_addr, joints_dict):
        self.skeletons_dict[kinect_addr] = {
            "is_transformed": is_transformed,
            "kinect_name": kinect_name,
            "kinect_addr": kinect_addr,
            "joints": joints_dict
        }

    def get_skeletons(self):
        return self.skeletons_dict


def create(*args):
    return Person(*args)
