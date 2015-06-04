
import json
from flask import request, jsonify
from .config import kinect2kit_server, current_session, tracker
from .exceptions import InvalidClientException
from . import session

@kinect2kit_server.route("/new", methods=["POST"])
def new():
    """
    Creates a new viewing session
    """
    try:
        name = request.form["name"]
        addr = request.remote_addr
        global current_session
        current_session = session.create(name, addr)
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400

@kinect2kit_server.route("/terminate", methods=["POST"])
def terminate():
    """
    Terminates the viewing session
    """
    try:
        addr = request.remote_addr
        if current_session.get_addr() == addr:
            current_session.terminate()
        else:
            raise InvalidClientException
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400
    except InvalidClientException:
        return jsonify(message="Unauthorized access"), 401

@kinect2kit_server.route("/stream", methods=["POST"])
def stream():
    """
    Streams the latest Kinect inputs to the server
    """
    try:
        name = request.form["name"]
        addr = request.remote_addr
        k = kinects[name]
        if k.get_addr == addr:
            body_frame = json.loads(request.form["body_frame"])
            k.update_body_frame(body_frame)
            tracker.track()
        else:
            raise InvalidClientException
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400
    except InvalidClientException:
        return jsonify(message="Unauthorized access"), 401

@kinect2kit_server.route("/connect", methods=["POST"])
def connect():
    """
    Connects a Kinect to the session
    """
    try:
        name = request.form["name"]
        addr = request.remote_addr
        tilt_angle = request.form["tilt_angle"]
        height = request.form["height"]
        depth_frame_width = request.form["depth_frame_width"]
        depth_frame_height = request.form["depth_frame_height"]
        k = kinect.create(name, addr, tilt_angle, height, depth_frame_width, depth_frame_height)
        kinects[name] = k
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400

@kinect2kit_server.route("/disconnect", methods=["POST"])
def disconnect():
    """
    Disconnects a Kinect from the session
    """
    try:
        name = request.form["name"]
        addr = request.remote_addr
        k = kinects[name]
        if k.get_addr == addr:
            k.disconnect()
        else:
            raise InvalidClientException
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400
    except InvalidClientException:
        return jsonify(message="Unauthorized access"), 401

@kinect2kit_server.route("/info", methods=["GET"])
def get_info():
    """
    Gets the current setup summary
    """

    pass

@kinect2kit_server.route("/result", methods=["GET"])
def get_result():
    """
    Gets the latest tracking result
    """

    pass
