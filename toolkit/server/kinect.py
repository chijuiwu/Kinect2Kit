class Kinect(object):
    def __init__(self, name, addr, tilt_angle, height, depth_frame_width, depth_frame_height):
        self.name = name
        self.addr = addr
        self.tilt_angle = tilt_angle
        self.height = height
        self.depth_frame_width = depth_frame_width
        self.depth_frame_height = depth_frame_height
        self.calibrated = False
        self.uncalibrated_frames = list()
        self.body_frames = list()

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.addr

    def get_tilt_angle(self):
        return self.tilt_angle

    def get_height(self):
        return self.height

    def get_uncalibrated_frames_count(self):
        return self.uncalibrated_frames.count()

    def get_uncalibrated_frames(self):
        return self.uncalibrated_frames

    def update_body_stream(self, body_frame):
        if not self.calibrated:
            self.uncalibrated_frames.append(body_frame)
        else:
            self.body_frames.append(body_frame)

    def disconnect(self):
        pass


def create(*args):
    return Kinect(*args)
