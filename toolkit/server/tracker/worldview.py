import math


class WorldViewCoordinateSystem:
    def __init__(self):
        pass

    @staticmethod
    def calculate_init_angle(skeletons):
        total_angle = 0
        for s in skeletons:
            shoulder_l = s["Joints"]["ShoulderLeft"]
            shoulder_r = s["Joints"]["ShoulderRight"]
            if shoulder_l["TrackingState"] == "NotTracked" or shoulder_r["TrackingState"] == "NotTracked":
                # exception
                pass
            shoulder_l_pos = shoulder_l["CameraSpacePoint"]
            shoulder_r_pos = shoulder_r["CameraSpacePoint"]
            length_opposite = float(shoulder_r_pos.z) - float(shoulder_l_pos.z)
            length_adjacent = float(shoulder_r_pos.x) - float(shoulder_l_pos.x)
            total_angle += math.atan2(length_opposite, length_adjacent)
        return total_angle / float(len(skeletons))

    @staticmethod
    def calculate_init_center_position(skeletons):
        total_body_x = 0
        total_body_y = 0
        total_body_z = 0
        for s in skeletons:
            total_joint_x = 0
            total_joint_y = 0
            total_joint_z = 0
            for jt in s["Joints"].itervalues():
                total_joint_x += float(jt["CameraSpacePoint"].x)
                total_joint_y += float(jt["CameraSpacePoint"].y)
                total_joint_z += float(jt["CameraSpacePoint"].z)
            total_body_x += total_joint_x / float(len(s["Joints"]))
            total_body_y += total_joint_y / float(len(s["Joints"]))
            total_body_z += total_joint_z / float(len(s["Joints"]))
        center_x = total_body_x / float(len(skeletons))
        center_y = total_body_y / float(len(skeletons))
        center_z = total_body_z / float(len(skeletons))
        return WorldViewCoordinate(center_x, center_y, center_z)

    @staticmethod
    def create_body(kinect_body, init_angle, init_center_position):
        joints_dict = dict()
        for jt_type, joint in kinect_body["Joints"]:
            position = joint["CameraSpacePoint"]
            # translation
            translate_x = position - init_center_position.x
            translate_y = position - init_center_position.y
            translate_z = position - init_center_position.z
            # rotation
            rotate_x = translate_x * math.cos(init_angle) + translate_z * math.sin(init_angle)
            rotate_y = translate_y
            rotate_z = translate_z * math.cos(init_angle) - translate_x * math.sin(init_angle)
            joints_dict[jt_type] = WorldViewJoint(WorldViewCoordinate(rotate_x, rotate_y, rotate_z))
        return WorldViewBody(joints_dict)

    @staticmethod
    def calculate_joints_differences(worldview_body1, worldview_body2):
        if worldview_body1 is None or worldview_body2 is None:
            return float("inf")
        total_difference = 0
        body_joints_union = worldview_body1["Joints"].viewkeys() & worldview_body2["Joints"].viewkeys()
        for joint_type in body_joints_union:
            joint_1_coordinate = worldview_body1["Joints"][joint_type]["WorldViewPoint"]
            joint_2_coordinate = worldview_body2["Joints"][joint_type]["WorldViewPoint"]
            total_difference += math.sqrt(
                math.pow(joint_1_coordinate.x - joint_2_coordinate.x, 2) +
                math.pow(joint_1_coordinate.y - joint_2_coordinate.y, 2) +
                math.pow(joint_1_coordinate.z - joint_2_coordinate.z, 2))
        return total_difference


class WorldViewBody(object):
    def __init__(self, joints_dict):
        self.joints_dict = joints_dict

    def __getitem__(self, item):
        if item == "Joints":
            return self.joints_dict


class WorldViewJoint(object):
    def __init__(self, position):
        self.position = position

    def __getitem__(self, item):
        if item == "WorldViewPoint":
            return self.position


class WorldViewCoordinate(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
