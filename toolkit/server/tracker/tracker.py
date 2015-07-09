from .worldview import WorldViewCoordinateSystem as WorldViewCS
from . import skeleton
from . import kinect
from . import session
from . import result


class Tracker(object):
    def __init__(self, calibration_frames):
        self.session = None
        self.kinects_dict = dict()
        self.calibration_frames = calibration_frames
        self.acquiring_calibration = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.tracking = False
        self.result = None
        self.results_list = list()

    def reset(self):
        self.session = None
        self.kinects_dict = dict()
        self.acquiring_calibration = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.tracking = False
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
        self.kinects_dict[addr] = k

    def get_kinect(self, addr):
        if addr in self.kinects_dict:
            return self.kinects_dict[addr]
        else:
            return None

    def remove_kinect(self, addr):
        del self.kinects_dict[addr]

    def is_tracking(self):
        return self.tracking

    def is_acquiring_calibration(self):
        return self.acquiring_calibration

    def acquire_calibration(self):
        """
        Start acquiring frames for calibration
        """

        self.acquiring_calibration = True

    def get_required_calibration_frames(self):
        """
        The number of calibration frames still required is the maximum number of bodyframes required for any Kinect
        """

        required_frames = 0
        for camera in self.kinects_dict.itervalues():
            remaining_frames = self.calibration_frames - len(camera.get_bodyframes())
            if remaining_frames > required_frames:
                required_frames = remaining_frames
        return required_frames

    def _calibrate_kinect(self, camera):
        """
        Calibrate a single Kinect, calculate the initial angle and center position for each skeleton
        """

        # use most recent frames for calibration
        uncalibrated_frames = camera.get_uncalibrated_frames()
        calibration_frames = list()
        while len(calibration_frames) != self.calibration_frames:
            calibration_frames.append(uncalibrated_frames.pop())

        # create a skeleton for each body
        last_frame = calibration_frames[-1]
        timestamp = last_frame["Timestamp"]
        for body_idx in xrange(last_frame["Bodies"]["Count"]):
            skeletons = list()
            for frame_idx in xrange(len(calibration_frames)):
                skeletons.append(calibration_frames[frame_idx]["Bodies"][body_idx])
            kinect_body = last_frame["Bodies"][body_idx]
            tracking_id = kinect_body["TrackingId"]
            init_angle = WorldViewCS.calculate_init_angle(skeletons)
            init_center_position = WorldViewCS.calculate_init_center_position(skeletons)
            worldview_body = WorldViewCS.create_body(kinect_body, init_angle, init_center_position)
            init_skeleton = skeleton.create(timestamp, tracking_id, kinect_body, worldview_body, init_angle,
                                            init_center_position)
            camera.add_skeleton(init_skeleton)

    def _detect_people(self, timestamp):
        """
        Match initial skeletons across multiple Kinects. Assume every person is visible to all Kinects.
        """

        assert self.calibration_acquired or self.tracking

        if self.calibration_acquired:
            r = result.create_result(timestamp)
            for base_fov in self.kinects_dict.itervalues():
                perspective = result.create_perspective(base_fov.get_name(), base_fov.get_addr())
                for base_skeleton in base_fov.get_skeletons():
                    person = result.create_person()
                    same_person_skeletons = list()
                    same_person_skeletons.append(base_skeleton)
                    other_fovs = [camera for camera in self.kinects_dict.itervalues() if
                                  camera.get_addr() != base_fov.get_addr()]
                    for other_fov in other_fovs:
                        other_skeletons = other_fov.get_skeletons()
                        other_skeletons.sort(
                            key=lambda s: WorldViewCS.calculate_joints_differences(s.get_worldview_body(0),
                                                                                   base_skeleton.get_worldview_body()))
                        same_person_skeletons.append(next(other_skeletons))

            for fov in self.kinects_dict.itervalues():
                perspective = result.create_perspective(fov.get_name(), fov.get_addr())
                # match by worldview proximity
                for skeleton in skeletons_in_fov:

        else:
            pass

    def resolve_calibration(self):
        """
        Run the calibration procedure on the acquired frames
        """

        assert self.calibration_acquired

        # calibrate all Kinects
        for camera in self.kinects_dict.itervalues():
            self._calibrate_kinect(camera)

        # match initial skeletons
        self._detect_people(None)

        self.calibration_resolved = True

    def start_tracking(self):
        assert self.calibration_resolved
        self.tracking = True

    def _update_skeletons(self, camera, bodyframe):
        """
        Update skeletons' spatial positions
        """

        assert self.tracking

        # error handling here, e.g. new skeleton

        timestamp = bodyframe["Timestamp"]
        skeletons = camera.get_skeletons()

        for body_idx in xrange(bodyframe["Bodies"]["Count"]):
            kinect_body = bodyframe["Bodies"][body_idx]
            tracking_id = kinect_body["TrackingId"]

            # find skeleton by tracking id
            s = next((s for s in skeletons if s.get_tracking_id() == tracking_id), None)
            if s is not None:
                worldview_body = WorldViewCS.create_body(kinect_body, s.get_init_angle(), s.get_init_center_position())
                s.update(timestamp, tracking_id, kinect_body, worldview_body)
                continue

            # find skeleton by spatial proximity
            other_skeletons = [s for s in skeletons if s.get_last_updated() != timestamp]
            other_skeletons.sort(
                key=lambda other: kinect.Kinect.calculate_joints_differences(other.get_kinect_body(), kinect_body))
            s = next(other_skeletons, None)
            if s is not None:
                worldview_body = WorldViewCS.create_body(kinect_body, s.get_init_angle(), s.get_init_center_position())
                s.update(timestamp, tracking_id, kinect_body, worldview_body)
                continue

        # other skeletons are not visible
        lost_track = [s for s in skeletons if s.get_last_updated() != timestamp]
        for s in lost_track:
            s.update(timestamp)

    def update_result(self, camera, bodyframe):
        """
        Update the tracking result
        """

        if self.acquiring_calibration:
            camera.add_uncalibrated_bodyframe(bodyframe)
            if self.get_required_calibration_frames() <= 0:
                self.acquiring_calibration = False
                self.calibration_acquired = True

        if self.tracking:
            self._update_skeletons(camera, bodyframe)
            self._detect_people(bodyframe["Timestamp"])

    def get_result(self):
        pass

    def output_results(self):
        pass


def create(*args):
    return Tracker(*args)
