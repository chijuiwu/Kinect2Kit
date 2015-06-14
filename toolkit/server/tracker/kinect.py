class Kinect(object):
    def __init__(self, name, addr, tilt_angle, height, depth_frame_width, depth_frame_height):
        self.name = name
        self.addr = addr
        self.tilt_angle = tilt_angle
        self.height = height
        self.depth_frame_width = depth_frame_width
        self.depth_frame_height = depth_frame_height
        self.calibrated = False
        self.body_frames = list()
        self.skeletons = list()

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.addr

    def get_tilt_angle(self):
        return self.tilt_angle

    def get_height(self):
        return self.height

    def get_bodyframes(self):
        return self.body_frames

    def update_bodyframe(self, body_frame):
        self.body_frames.append(body_frame)

    def get_skeletons(self):
        return self.skeletons

    def add_skeleton(self, skeleton):
        self.skeletons.append(skeleton)


def create(*args):
    return Kinect(*args)
