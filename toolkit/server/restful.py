import json
from flask import request, jsonify
from .config import kinect2kit_server, kinect2kit_tracker


@kinect2kit_server.route("/new", methods=["POST"])
def new():
    """
    Create a new viewing session
    """

    try:
        name = request.form["name"]
        addr = request.remote_addr
        kinect2kit_tracker.set_session(name, addr)
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400


@kinect2kit_server.route("/kill", methods=["POST"])
def kill():
    """
    Terminate the viewing session
    """

    addr = request.remote_addr
    if kinect2kit_tracker.authenticate(addr):
        kinect2kit_tracker.kill_session()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/calibrate/acquire", methods=["POST"])
def calibrate_acquire():
    addr = request.remote_addr
    if kinect2kit_tracker.authenticate(addr):
        kinect2kit_tracker.acquire_calibration()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/calibrate/resolve", methods=["POST"])
def calibrate_resolve():
    addr = request.remote_addr
    if kinect2kit_tracker.authenticate(addr):
        kinect2kit_tracker.resolve_calibration()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/track", methods=["POST"])
def track():
    addr = request.remote_addr
    if kinect2kit_tracker.authenticate(addr):
        kinect2kit_tracker.start_tracking()
        return jsonify(message="OK")
    else:
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
        kinect2kit_tracker.add_kinect(name, addr, tilt_angle, height, depth_frame_width, depth_frame_height)
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed"), 400


@kinect2kit_server.route("/disconnect", methods=["POST"])
def disconnect():
    """
    Disconnects a Kinect from the session
    """

    addr = request.remote_addr
    k = kinect2kit_tracker.get_kinect(addr)
    if k is not None:
        kinect2kit_tracker.remove_kinect(k)
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/stream", methods=["POST"])
def stream():
    """
    Streams the latest Kinect inputs to the server
    """

    try:
        addr = request.remote_addr
        camera = kinect2kit_tracker.get_kinect(addr)
        if camera is not None:
            if kinect2kit_tracker.is_tracking() or kinect2kit_tracker.is_acquiring_calibration():
                body_frame = json.loads(request.form["body_frame"])
                kinect2kit_tracker.update_result(camera, body_frame)
                return jsonify(message="OK")
            else:
                return jsonify(message="Not required"), 400
        else:
            return jsonify(message="Unauthorized access"), 401
    except KeyError:
        return jsonify(message="Failed"), 400


@kinect2kit_server.route("/bodyframe", methods=["GET"])
def get_bodyframe_structure():
    pass


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


@kinect2kit_server.route("/result/<int:session_id>", methods=["GET"])
def get_session_result(session_id):
    pass
