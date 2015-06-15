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

    def get_remaining_calibration_frames(self):
        required_frames = 0
        for camera in self.kinects_dict.itervalues():
            remaining_frames = self.calibration_frames - len(camera.get_bodyframes())
            if remaining_frames > required_frames:
                required_frames = remaining_frames
        return required_frames

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
            init_kinect_body = last_frame["Bodies"][body_idx]
            init_tracking_id = init_kinect_body["TrackingId"]
            init_angle = WorldViewCS.calculate_init_angle(skeletons)
            init_center_position = WorldViewCS.calculate_init_center_position(skeletons)
            init_worldview_body = WorldViewCS.create_body(init_kinect_body, init_angle, init_center_position)
            init_skeleton = skeleton.create(timestamp, init_tracking_id, init_kinect_body, init_worldview_body,
                                            init_angle, init_center_position)
            camera.add_skeleton(init_skeleton)

    def resolve_calibration(self):
        assert self.calibration_acquired
        for camera in self.kinects_dict.itervalues():
            self.__calibrate_kinect(camera)
        self.calibration_resolved = True

    def start_tracking(self):
        assert self.calibration_resolved
        self.tracking = True

    def _update_skeletons(self, camera, body_frame):
        timestamp = body_frame["Timestamp"]

        skeletons = camera.get_skeletons()
        for body_idx in xrange(body_frame["Bodies"]["Count"]):
            kinect_body = body_frame["Bodies"][body_idx]
            tracking_id = kinect_body["TrackingId"]
            # find by tracking id
            s = next((s for s in skeletons if s.get_tracking_id() == tracking_id), None)
            if s is not None:
                worldview_body = WorldViewCS.create_body(kinect_body, s.get_init_angle(), s.get_init_center_position())
                s.update(timestamp, tracking_id, kinect_body, worldview_body)
                continue
            # find by spatial proximity
            s =
            joints_differences = [
                (s, kinect.Kinect.calculate_joints_differences(s.get_kinect_body(), kinect_body)) for s in skeletons]
            joints_differences.sort(key=lambda tup: tup[1])


    def _detect_people(self):
        tracking_skeletons = [(camera, camera.get_skeletons()) for camera in self.kinects_dict.itervalues()]

    def update_result(self, camera, body_frame):
        if self.is_acquiring_calibration():
            camera.add_uncalibrated_bodyframe(body_frame)
            if self.get_remaining_calibration_frames() <= 0:
                self.calibration_acquired = True
        if self.tracking:
            self._update_skeletons(camera, body_frame)
            self._detect_people()


def create(*args):
    return Tracker(*args)
