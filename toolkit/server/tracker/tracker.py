
from .worldview import WorldViewCoordinateSystem as WorldViewCS
from . import skeleton
from . import result
from . import kinect
from . import session

class Tracker(object):

    def __init__(self, calibration_frames):
        self.session = None
        self.kinects = dict()
        self.calibration_frames = calibration_frames
        self.calibration_started = False
        self.calibrated = False
        self.result = None

    def set_session(self, name, addr):
        self.session = session.create(name, addr)

    def kill_session(self):
        self.session.kill()
        self.session = None

    def authenticate(self, addr):
        if self.session.get_addr() == addr:
            return True
        else:
            return False

    def add_kinect(self, name, addr, tilt_angle, height, depth_frame_width, depth_frame_height):
        k = kinect.create(name, addr, tilt_angle, height, depth_frame_width, depth_frame_height)
        self.kinects[addr] = k

    def get_kinect(self, addr):
        if addr in self.kinects:
            return self.kinects[addr]
        else:
            return None

    def remove_kinect(self, addr):
        del self.kinects[addr]

    def __calibrate_kinect(self, camera):
        frames = list()
        while len(frames) != self.calibration_frames:
            frames.append(kinect.get_uncalibrated_frames().pop())
        last_frame = frames[-1]
        for person_idx in xrange(last_frame["Bodies"]["Count"]):
            bodies = list()
            for frame_idx in xrange(len(frames)):
                bodies.append(frames.remove())
            init_angle = WorldViewCS.calculate_init_angle(bodies)
            init_position = WorldViewCS.calculate_init_center_position(bodies)
            s = skeleton.create(init_angle, init_position)

    def __try_(self):
        sufficient_frames = True
        for name, kinect in kinects.iteritems():
            if not kinect.get_uncalibrated_frames_count() >= self.calibration_frames:
                sufficient_frames = False
                if not sufficient_frames:
                    return False
        if sufficient_frames:
            for _, kinect in kinects.iteritems():
                self.__calibrate_kinect(kinect)
            return True

    def calibrate(self):
        """
        Starts calibration process
        """

        self.calibration_started = True
        self.calibrated = False
        self.result = None

    def __detect_people(self):
        global tracking_result
        tracking_result = result.create()
        return tracking_result

    def track(self, camera, body_frame):
        """
        Performs tracking
        """

        if self.calibration_started:
            camera.update_body_stream(body_frame)
        if self.calibrated:
            self.__detect_people()
            return result.jsonify(self.result)
        else:
            return result.jsonify(None)

def create(*args):
    return Tracker(*args)
