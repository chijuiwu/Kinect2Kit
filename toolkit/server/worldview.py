
import math

class WorldViewCoordinateSystem:

    def __init__(self):
        pass

    @staticmethod
    def calculate_init_angle(bodies):
        total_angle = 0
        for body in bodies:
            shoulder_l = body["Joints"]["ShoulderLeft"]
            shoulder_r = body["Joints"]["ShoulderRight"]
            if shoulder_l["TrackingState"] == "NotTracked" or shoulder_r["TrackingState"] == "NotTracked":
                # exception
                pass
            shoulder_l_pos = shoulder_l["CameraSpacePoint"]
            shoulder_r_pos = shoulder_r["CameraSpacePoint"]
            length_opposite = float(shoulder_r_pos.z) - float(shoulder_l_pos.z)
            length_adjacent = float(shoulder_r_pos.x) - float(shoulder_l_pos.x)
            total_angle += math.atan2(length_opposite, length_adjacent)
        return total_angle/len(bodies)

    @staticmethod
    def calculate_init_center_position(bodies):
        total_body_x = 0
        total_body_y = 0
        total_body_z = 0
        for body in bodies:
            total_joint_x = 0
            total_joint_y = 0
            total_joint_z = 0
            for name, joint in body["Joints"]:
                total_joint_x += float(joint["CameraSpacePoint"].x)
                total_joint_y += float(joint["CameraSpacePoint"].y)
                total_joint_z += float(joint["CameraSpacePoint"].z)
            total_body_x += total_joint_x / float(len(body["Joints"]))
            total_body_y += total_joint_y / float(len(body["Joints"]))
            total_body_z += total_joint_z / float(len(body["Joints"]))
        center_x = total_body_x / float(len(bodies))
        center_y = total_body_y / float(len(bodies))
        center_z = total_body_z / float(len(bodies))
        return {"x": center_x, "y": center_y, "z": center_z}

    # @staticmethod
    # def create_body(body, init_angle):

# class WorldViewBody(object):
#
#     def __init__(self, body, init_angle, init_position):
#         self.
#         for name, joint in body["Joints"]:
#             joint_pos = joint["CameraSpacePoint"]
#
# def create_body(*args):
#     return WorldViewBody(*args)
