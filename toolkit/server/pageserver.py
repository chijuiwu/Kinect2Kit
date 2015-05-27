
from config import kinect2kit_server
from flask import render_template, jsonify

@kinect2kit_server.route("/", methods=["GET"])
@kinect2kit_server.route("/index", methods=["GET"])
def get_index():
    return render_template('index.html')
