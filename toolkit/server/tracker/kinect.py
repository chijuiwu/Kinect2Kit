import math
import numpy as np


class Kinect(object):
    def __init__(self, name, addr, tilt_angle=None, height=None):
        self.name = name
        self.addr = addr
        self.tilt_angle = tilt_angle
        self.height = height
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

    def clear_uncalibrated_bodyframes(self):
        del self.uncalibrated_bodyframes_list[:]

    def get_skeletons(self):
        return self.skeletons_list

    def add_skeleton(self, skeleton):
        self.skeletons_list.append(skeleton)


def create(*args):
    return Kinect(*args)


class KinectCoordinateSystem:
    def __init__(self):
        pass

    @staticmethod
    def create_body(worldview_body, init_angle, init_center_position):
        """
        {
            "Joints": {
                "JointType": {
                    "JointType": "JointType",
                    "TrackingState": "TrackingState",
                    "CameraSpacePoint": {
                        "X": X,
                        "Y": Y,
                        "Z": Z
                    }
                }
            }
        }
        """

        kinect_body = dict()
        kinect_body["Joints"] = dict()

        for joint_type, joint in worldview_body["Joints"].iteritems():
            worldview_coordinate = joint["WorldViewPoint"]

            sin_angle = math.sin(init_angle)
            cos_angle = math.cos(init_angle)
            angle_matrix = np.matrix(((cos_angle, -sin_angle), (sin_angle, cos_angle)))
            inverse_angle_matrix = angle_matrix.I

            translated_x = float(worldview_coordinate["X"] * inverse_angle_matrix.item(0, 0) +
                                 worldview_coordinate["Z"] * inverse_angle_matrix.item(1, 0))
            translated_y = worldview_coordinate["Y"]
            translated_z = float(worldview_coordinate["X"] * inverse_angle_matrix.item(0, 1) +
                                 worldview_coordinate["Z"] * inverse_angle_matrix.item(1, 1))

            final_x = translated_x + init_center_position["X"]
            final_y = translated_y + init_center_position["Y"]
            final_z = translated_z + init_center_position["Z"]

            kinect_joint = dict()
            kinect_joint["JointType"] = joint_type
            kinect_joint["TrackingState"] = joint["TrackingState"]
            kinect_joint["CameraSpacePoint"] = dict()
            kinect_joint["CameraSpacePoint"]["x"] = final_x
            kinect_joint["CameraSpacePoint"]["Y"] = final_y
            kinect_joint["CameraSpacePoint"]["Z"] = final_z

            kinect_body["Joints"][joint_type] = kinect_joint

        return kinect_body

    @staticmethod
    def calculate_joints_differences(kinect_body_1, kinect_body_2):
        if kinect_body_1 is None or kinect_body_2 is None:
            return float("inf")

        total_difference = 0
        body_joints_union = kinect_body_1["Joints"].viewkeys() & kinect_body_2["Joints"].viewkeys()
        for joint_type in body_joints_union:
            joint_1_coordinate = kinect_body_1["Joints"][joint_type]["CameraSpacePoint"]
            joint_2_coordinate = kinect_body_2["Joints"][joint_type]["CameraSpacePoint"]
            total_difference += math.sqrt(
                math.pow(joint_1_coordinate["X"] - joint_2_coordinate["X"], 2) +
                math.pow(joint_1_coordinate["Y"] - joint_2_coordinate["Y"], 2) +
                math.pow(joint_1_coordinate["Z"] - joint_2_coordinate["Z"], 2))

        return total_difference

    @staticmethod
    def is_joint_stationary(joint_type, kinect_body_1, kinect_body_2):
        if joint_type not in kinect_body_1["Joints"] or joint_type not in kinect_body_2["Joints"]:
            return False

        joint_1_coordinate = kinect_body_1["Joints"][joint_type]["CameraSpacePoint"]
        joint_2_coordinate = kinect_body_2["Joints"][joint_type]["CameraSpacePoint"]

        difference = math.sqrt(
            math.pow(joint_1_coordinate["X"] - joint_2_coordinate["X"], 2) +
            math.pow(joint_1_coordinate["Y"] - joint_2_coordinate["Y"], 2) +
            math.pow(joint_1_coordinate["Z"] - joint_2_coordinate["Z"], 2))

        if difference > 0.1:
            return False

        return True
