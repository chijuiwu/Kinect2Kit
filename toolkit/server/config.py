
from flask import Flask

kinect2kit_server = Flask(__name__)
kinect2kit_server.config.from_object(__name__)

viewers = list()
kinects = dict()
