import time
import itertools
from .worldview import WorldViewCoordinateSystem as WorldViewCS
from .kinect import KinectCoordinateSystem as KinectCS
from . import skeleton
from . import kinect
from . import session
from . import result


class Tracker(object):
    def __init__(self, calibration_frames_count):
        self.calibration_frames_count = calibration_frames_count
        self.session = None
        self.kinects_dict = dict()
        self.acquiring_calibration_frames = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.calibration_error = ""
        self.tracking = False
        self.result = None
        self.results_list = list()

    def reset(self):
        self.session = None
        self.kinects_dict = dict()
        self.acquiring_calibration_frames = False
        self.calibration_acquired = False
        self.calibration_resolved = False
        self.calibration_error = ""
        self.tracking = False
        self.result = None

    def set_session(self, name, addr):
        self.session = session.create(name, addr)

    def stop_session(self):
        self.session = None
        self.reset()

    def authenticate(self, addr):
        if self.session is not None and self.session.get_addr() == addr:
            return True
        else:
            return False

    def add_kinect(self, name, addr, tilt_angle=None, height=None):
        k = kinect.create(name, addr, tilt_angle, height)
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
        return self.acquiring_calibration_frames

    def is_resolving_calibration(self):
        return self.calibration_acquired and not self.calibration_resolved

    def has_finished_calibration(self):
        return self.calibration_resolved

    def get_calibration_error(self):
        return self.calibration_error

    def get_required_calibration_frames(self):
        return self.calibration_frames_count

    def get_remained_calibration_frames(self):
        """
        The number of calibration frames remained is the maximum number of bodyframes required for any Kinect
        """

        remained_frames = 0
        for camera in self.kinects_dict.itervalues():
            remaining_frames = self.calibration_frames_count - len(camera.get_uncalibrated_bodyframes())
            if remaining_frames > remained_frames:
                remained_frames = remaining_frames
        return remained_frames

    def start_acquiring_calibration_frames(self):
        """
        Start acquiring frames for calibration
        """
        self.acquiring_calibration_frames = True

    def is_scene_static(self, camera, bodyframe):
        """
        """

        if len(bodyframe["Bodies"]) == 0:
            self.calibration_error = "No one in the scene"
            return False

        for previous_bodyframe in camera.get_uncalibrated_bodyframes():
            previous_bodies_count = len(previous_bodyframe["Bodies"])
            current_bodies_count = len(bodyframe["Bodies"])

            if previous_bodies_count != current_bodies_count:
                self.calibration_error = "Number of people does not match up."
                return False

            for previous_body in previous_bodyframe["Bodies"]:
                current_body = next((b for b in bodyframe["Bodies"] if b["TrackingId"] == previous_body["TrackingId"]),
                                    None)
                if current_body is None:
                    self.calibration_error = "Person missing."
                    return False

                if not KinectCS.is_joint_stationary("Head", previous_body, current_body):
                    self.calibration_error = "Head moved."
                    return False

                if not KinectCS.is_joint_stationary("HandLeft", previous_body, current_body):
                    self.calibration_error = "Hand Left moved."
                    return False

                if not KinectCS.is_joint_stationary("HandRight", previous_body, current_body):
                    self.calibration_error = "Hand Right moved."
                    return False

        return True

    def resolve_calibration(self):
        """
        Run the calibration procedure on the acquired frames
        """

        assert self.calibration_acquired

        # calibrate all Kinects
        for camera in self.kinects_dict.itervalues():
            self._calibrate_kinect(camera)

    def _calibrate_kinect(self, camera):
        """
        Calibrate a single Kinect, calculate the initial angle and center position for every skeleton in the Kinect FOV
        """

        # current time as timestamp
        timestamp = time.time()

        # use most recent frames for calibration
        uncalibrated_frames = camera.get_uncalibrated_bodyframes()
        calibration_frames = list()
        while len(calibration_frames) != self.calibration_frames_count:
            calibration_frames.append(uncalibrated_frames.pop())

        # create a skeleton for each body
        last_frame = calibration_frames[-1]
        bodies_count = len(last_frame["Bodies"])
        for body_idx in xrange(bodies_count):
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

    def _detect_people(self):
        """
        Match skeletons across multiple Kinects and create a tracking result with those skeletons
        """

        assert self.calibration_acquired

        # find the number of people
        total_people_count = len(self.kinects_dict.values()[0].get_skeletons())

        # find all skeletons
        skeletons_list = list()
        for camera in self.kinects_dict.itervalues():
            for s in camera.get_skeletons():
                skeletons_list.append((camera, s))

        # match skeletons by their spatial positions in worldview, stored as list of list,
        # where the inner list contains tuples of (camera, skeleton), as shown above
        people_list = list()

        # for total number of people
        for _ in itertools.repeat(None, total_people_count):
            same_person_skeletons_list = list()
            same_person_addrs_list = list()

            first_skeleton_tuple = skeletons_list[0]
            first_skeleton_worldview = first_skeleton_tuple[1].get_worldview_body()

            # sort skeletons by their positions in worldview
            skeletons_list.sort(key=lambda (_, s): WorldViewCS.calculate_joints_differences(s.get_worldview_body(),
                                                                                            first_skeleton_worldview))

            # for total number of kinects
            for _ in itertools.repeat(None, len(self.kinects_dict)):
                i = 0

                # find next closest skeleton that is in another FOVs
                while True:
                    next_skel_tuple = skeletons_list[i]
                    next_skel_addr = next_skel_tuple[0]
                    if next_skel_addr not in same_person_addrs_list:
                        skeletons_list.remove(next_skel_tuple)
                        same_person_skeletons_list.append(next_skel_tuple)
                        same_person_addrs_list.append(next_skel_addr)
                        break
                    else:
                        i += 1

            people_list.append(same_person_skeletons_list)

        # create a new result
        new_result = result.create_result(time.time())

        # create a perspective for each kinect FOV
        for camera in self.kinects_dict.itervalues():
            camera_name = camera.get_name()
            camera_addr = camera.get_addr()
            perspective = result.create_perspective(camera_name, camera_addr)

            # person id remains the same throughout all different perspectives
            for unique_person_id, same_person_skeletons_list in enumerate(people_list):
                person = result.create_person(unique_person_id)

                # find the person's original skeleton in this FOV
                native_skeleton = next((s for c, s in same_person_skeletons_list if c.get_addr() == camera_addr), None)

                # this person does not have a skeleton in this FOV initially
                if native_skeleton is None:
                    continue

                person.add_skeleton(True, native_skeleton.get_last_updated(), camera_name, camera_addr, native_skeleton.get_kinect_body()["Joints"])

                # find the person's skeletons in other FOVs
                for (c, s) in [skel_tuple for skel_tuple in same_person_skeletons_list if skel_tuple[0].get_addr() != camera_addr]:
                    # convert worldview body to kinect body
                    kinect_body = KinectCS.create_body(s.get_worldview_body(), native_skeleton.get_init_angle(),
                                                       native_skeleton.get_init_center_position())
                    person.add_skeleton(False, s.get_last_updated(), c.get_name(), c.get_addr(), kinect_body["Joints"])

                person.calculate_average_skeleton()
                perspective.add_person(person)

            new_result.add_perspective(perspective)

        self.result = new_result

    def start_tracking(self):
        """
        Set the tracking flag to be true
        """

        assert self.calibration_resolved

        self.tracking = True

    def _update_skeletons(self, camera, bodyframe):
        """
        Update skeletons' spatial positions
        """

        assert self.tracking

        # error handling here, e.g. new skeleton

        # current time as timestamp
        timestamp = time.time()

        skeletons = camera.get_skeletons()

        # update every skeleton's position
        for body_idx in xrange(len(bodyframe["Bodies"])):
            kinect_body = bodyframe["Bodies"][body_idx]
            tracking_id = kinect_body["TrackingId"]

            # find the best skeleton match by their tracking id
            s = next((s for s in skeletons if s.get_tracking_id() == tracking_id), None)
            if s is not None:
                worldview_body = WorldViewCS.create_body(kinect_body, s.get_init_angle(), s.get_init_center_position())
                s.update(timestamp, tracking_id, kinect_body, worldview_body)
                continue

            # find the next best match by their spatial proximity, assume skeletons only move slightly across frames
            other_skeleton_candidates = [s for s in skeletons if s.get_last_updated() != timestamp]
            if len(other_skeleton_candidates) > 0:
                s = min(other_skeleton_candidates,
                        key=lambda other: KinectCS.calculate_joints_differences(other.get_kinect_body(),
                                                                                kinect_body))
                worldview_body = WorldViewCS.create_body(kinect_body, s.get_init_angle(), s.get_init_center_position())
                s.update(timestamp, tracking_id, kinect_body, worldview_body)
                continue

                # do not update missing skeletons

    def on_receive_bodyframe(self, camera, bodyframe):
        """
        Handle the new bodyframe from a Kinect. This function is called when the server receives a new bodyframe.
        """

        if self.acquiring_calibration_frames:
            if self.is_scene_static(camera, bodyframe):
                self.calibration_error = ""
                camera.add_uncalibrated_bodyframe(bodyframe)
            else:
                camera.clear_uncalibrated_bodyframes()

            if self.get_remained_calibration_frames() <= 0:
                self.acquiring_calibration_frames = False
                self.calibration_acquired = True
                self.resolve_calibration()
                # create initial tracking result
                self._detect_people()
                self.calibration_resolved = True

        if self.tracking:
            self._update_skeletons(camera, bodyframe)
            # tracking by detection
            self._detect_people()

    def get_result(self):
        return self.result

    def write_results_to_file(self):
        pass


def create(*args):
    return Tracker(*args)
