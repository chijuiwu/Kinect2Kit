import math


class Kinect(object):
    def __init__(self, name, addr, tilt_angle, height, depth_frame_width, depth_frame_height):
        self.name = name
        self.addr = addr
        self.tilt_angle = tilt_angle
        self.height = height
        self.depth_frame_width = depth_frame_width
        self.depth_frame_height = depth_frame_height
        self.uncalibrated_bodyframes_list = list()
        self.skeletons_list = list()

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.addr

    def get_tilt_angle(self):
        return self.tilt_angle

    def get_height(self):
        return self.height

    def get_uncalibrated_bodyframes(self):
        return self.uncalibrated_bodyframes_list

    def add_uncalibrated_bodyframe(self, bodyframe):
        self.uncalibrated_bodyframes_list.append(bodyframe)

    def get_skeletons(self):
        return self.skeletons_list

    def add_skeleton(self, skeleton):
        self.skeletons_list.append(skeleton)

    @staticmethod
    def calculate_joints_differences(body_1, body_2):
        total_difference = 0
        body_joints_union = body_1["Joints"].viewkeys() & body_2["Joints"].viewkeys()
        for joint_type in body_joints_union:
            joint_1_coordinate = body_1["Joints"][joint_type]["CameraSpacePoint"]
            joint_2_coordinate = body_2["Joints"][joint_type]["CameraSpacePoint"]
            total_difference += math.sqrt(
                math.pow(joint_1_coordinate.x - joint_2_coordinate.x, 2) +
                math.pow(joint_1_coordinate.y - joint_2_coordinate.y, 2) +
                math.pow(joint_1_coordinate.z - joint_2_coordinate.z, 2))
        return total_difference


def create(*args):
    return Kinect(*args)
