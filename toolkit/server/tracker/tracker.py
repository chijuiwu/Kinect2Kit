from .worldview import WorldViewCoordinateSystem as WorldViewCS
from . import skeleton
from . import kinect
from . import session
from .result import result


class Tracker(object):
    def __init__(self, calibration_frames):
        self.session = None
        self.kinects_dict = dict()
        self.calibration_frames = calibration_frames
        self.calibration_started = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.tracking = False
        self.result = None

    def reset(self):
        self.session = None
        self.kinects_dict = dict()
        self.calibration_started = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.tracking = False
        self.result = False

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
        self.kinects_dict[addr] = k

    def get_kinect(self, addr):
        if addr in self.kinects_dict:
            return self.kinects_dict[addr]
        else:
            return None

    def remove_kinect(self, camera):
        del self.kinects_dict[camera.addr]

    def is_tracking(self):
        return self.tracking

    def is_acquiring_calibration(self):
        return self.calibration_started and not self.calibration_acquired

    def acquire_calibration(self):
        self.calibration_started = True

    def __calibrate_kinect(self, camera):
        uncalibrated_frames = camera.get_uncalibrated_frames()
        frames = list()
        while len(frames) != self.calibration_frames:
            frames.append(uncalibrated_frames.pop())
        last_frame = frames[-1]
        timestamp = last_frame["TimeStamp"]
        for body_idx in xrange(last_frame["Bodies"]["Count"]):
            skeletons = list()
            for frame_idx in xrange(len(frames)):
                skeletons.append(frames[frame_idx]["Bodies"][body_idx])
            body = last_frame["Bodies"][body_idx]
            init_tracking_id = body["TrackingId"]
            init_angle = WorldViewCS.calculate_init_angle(skeletons)
            init_center_position = WorldViewCS.calculate_init_center_position(skeletons)
            init_body = WorldViewCS.create_body(body, init_angle, init_center_position)
            camera.add_skeleton(
                skeleton.create(timestamp, init_tracking_id, init_body, init_angle, init_center_position))

    def resolve_calibration(self):
        assert self.calibration_acquired
        for camera in self.kinects_dict.itervalues():
            self.__calibrate_kinect(camera)
        self.calibration_resolved = True

    def track(self):
        assert self.calibration_resolved
        self.tracking = True

    def _calibration_ready(self):
        for camera in self.kinects_dict.itervalues():
            if not len(camera.get_bodyframes()) >= self.calibration_frames:
                return False
        return True

    def _detect_people(self):
        return result.create()

    def update_result(self, camera, body_frame):
        camera.update_bodyfrmae(body_frame)
        if not self.calibration_acquired and self._calibration_ready():
            self.calibration_acquired = True
        if self.tracking:
            self.result = self._detect_people()


def create(*args):
    return Tracker(*args)
