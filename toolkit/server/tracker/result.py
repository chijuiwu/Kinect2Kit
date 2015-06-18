class Result(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.perspectives_dict = dict()

    def get_timestamp(self):
        return self.timestamp

    def add_perspective(self, perspective):
        self.perspectives_dict[perspective.get_namme()] = perspective

    def get_perspectives(self):
        return self.perspectives_dict


def create_result(*args):
    return Result(*args)


class Perspective(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.people_dict = dict()

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.name

    def add_person(self, person):
        self.people_dict[person.get_name()] = person

    def get_people(self):
        return self.people_dict


def create_perspective(*args):
    return Perspective(*args)


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


def create_person(*args):
    return Person(*args)


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


def create_joint(*args):
    return Joint(*args)
