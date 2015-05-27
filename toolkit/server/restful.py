
from config import kinect2kit_server
from flask import request, jsonify

@kinect2kit_server.route("/new", methods=["POST"])
def new():
    """
    Creates a new viewing session
    """

    pass

@kinect2kit_server.route("/delete", methods=["POST"])
def delete():
    """
    Deletes a viewing session
    """

    pass

@kinect2kit_server.route("/stream", methods=["POST"])
def stream():
    """
    Streams the latest Kinect inputs to the server
    """

    pass

@kinect2kit_server.route("/connect", methods=["POST"])
def connect():
    """
    Connects a Kinect to a session
    """

    pass

@kinect2kit_server.route("/disconnect", methods=["POST"])
def disconnect():
    """
    Disconnects a Kinect from a session
    """

    pass

@kinect2kit_server.route("/calibrate", methods=["POST"])
def calibrate():
    """
    Calibrate all the connected Kinects for a session
    """

    pass

@kinect2kit_server.route("/info", methods=["GET"])
def get_info():
    """
    Gets the current setup summary
    """

    pass

@kinect2kit_server.route("/track", methods=["GET"])
def get_track():
    """
    Gets the latest tracking result
    """

    pass
