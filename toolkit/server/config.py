
from flask import Flask
import tracker

CALIBRATION_FRAMES = 120

kinect2kit_server = Flask(__name__)
kinect2kit_server.config.from_object(__name__)

current_session = None
kinects = dict()
tracker = tracker.create(CALIBRATION_FRAMES)
tracking_result = None
