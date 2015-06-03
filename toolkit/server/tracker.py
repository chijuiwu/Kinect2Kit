
from config import kinects, tracking_result
from worldview import WorldViewCoordinateSystem as WorldViewCS
import skeleton
import result

class Tracker(object):

    def __init__(self, calibration_frames):
        self.calibration_frames = calibration_frames
        self.calibrated = False

    def __calibrate_kinect(self, kinect):
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

    def __try_calibrate(self):
        sufficient_frames = True
        for name, kinect in kinects.iteritems():
            if not kinect.get_uncalibrated_frames_count() >= self.calibration_frames:
                sufficient_frames = False
                if not sufficient_frames:
                    return
        if sufficient_frames:
            global tracking_result
            tracking_result = result.create()
            for _, kinect in kinects.iteritems():
                self.__calibrate_kinect(kinect)

    def track(self):
        if not self.calibrated:
            self.__try_calibrate()
        else:
            pass

def create(*args):
    return Tracker(*args)
