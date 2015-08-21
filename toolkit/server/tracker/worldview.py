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

            length_opposite = float(shoulder_r_pos["Z"]) - float(shoulder_l_pos["Z"])
            length_adjacent = float(shoulder_r_pos["X"]) - float(shoulder_l_pos["X"])

            total_angle += math.atan2(length_opposite, length_adjacent)

        return total_angle / float(len(skeletons))

    @staticmethod
    def calculate_init_center_position(skeletons):
        skeletons_count = len(skeletons)
        total_body_x = 0
        total_body_y = 0
        total_body_z = 0

        for s in skeletons:
            joints_count = len(s["Joints"])
            total_joint_x = 0
            total_joint_y = 0
            total_joint_z = 0

            for joint in s["Joints"].itervalues():
                total_joint_x += float(joint["CameraSpacePoint"]["X"])
                total_joint_y += float(joint["CameraSpacePoint"]["Y"])
                total_joint_z += float(joint["CameraSpacePoint"]["Z"])

            total_body_x += total_joint_x / float(joints_count)
            total_body_y += total_joint_y / float(joints_count)
            total_body_z += total_joint_z / float(joints_count)

        center_x = total_body_x / float(skeletons_count)
        center_y = total_body_y / float(skeletons_count)
        center_z = total_body_z / float(skeletons_count)

        return {"X": center_x, "Y": center_y, "Z": center_z}

    @staticmethod
    def create_body(kinect_body, init_angle, init_center_position):
        """
        {
            "Joints": {
                "JointType": {
                    "JointType": "JointType"
                    "TrackingState": "TrackingState"
                    "WorldViewPoint": {
                        "X": X,
                        "Y": Y,
                        "Z": Z
                    }
                }
            }
        }
        """
        worldview_body = dict()
        worldview_body["Joints"] = dict()

        for joint_type, joint in kinect_body["Joints"].iteritems():
            # translation
            translate_x = joint["CameraSpacePoint"]["X"] - init_center_position["X"]
            translate_y = joint["CameraSpacePoint"]["Y"] - init_center_position["Y"]
            translate_z = joint["CameraSpacePoint"]["Z"] - init_center_position["Z"]

            # rotation
            rotate_x = translate_x * math.cos(init_angle) + translate_z * math.sin(init_angle)
            rotate_y = translate_y
            rotate_z = translate_z * math.cos(init_angle) - translate_x * math.sin(init_angle)

            worldview_joint = dict()
            worldview_joint["JointType"] = joint_type
            worldview_joint["TrackingState"] = joint["TrackingState"]
            worldview_joint["WorldViewPoint"] = dict()
            worldview_joint["WorldViewPoint"]["X"] = rotate_x
            worldview_joint["WorldViewPoint"]["Y"] = rotate_y
            worldview_joint["WorldViewPoint"]["Z"] = rotate_z

            worldview_body["Joints"][joint_type] = worldview_joint

        return worldview_body

    @staticmethod
    def calculate_joints_differences(worldview_body1, worldview_body2):
        if worldview_body1 is None or worldview_body2 is None:
            return float("inf")

        total_difference = 0

        body_joints_intersection = set(worldview_body1["Joints"].keys()) & set(worldview_body2["Joints"].keys())

        for joint_type in body_joints_intersection:
            joint_1_coordinate = worldview_body1["Joints"][joint_type]["WorldViewPoint"]
            joint_2_coordinate = worldview_body2["Joints"][joint_type]["WorldViewPoint"]

            total_difference += math.sqrt(
                math.pow(joint_1_coordinate["X"] - joint_2_coordinate["X"], 2) +
                math.pow(joint_1_coordinate["Y"] - joint_2_coordinate["Y"], 2) +
                math.pow(joint_1_coordinate["Z"] - joint_2_coordinate["Z"], 2))

        return total_difference

