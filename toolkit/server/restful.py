import json
from flask import request, jsonify
from .config import kinect2kit_server, kinect2kit_tracker


@kinect2kit_server.route("/session/new", methods=["POST"])
def new_session():
    """
    Create a new application session
    """

    app_addr = request.remote_addr
    try:
        name = request.form["name"]
        kinect2kit_tracker.set_session(name, app_addr)
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Invalid request"), 400


@kinect2kit_server.route("/session/kill", methods=["POST"])
def kill_session():
    """
    Terminate the current session
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        kinect2kit_tracker.kill_session()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/calibration/acquire", methods=["POST"])
def acquire_calibration():
    """
    Acquire the calibration frames
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        kinect2kit_tracker.acquire_calibration()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/calibration/resolve", methods=["POST"])
def resolve_calibration():
    """
    Run the calibration algorithm
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        kinect2kit_tracker.resolve_calibration()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/track/start", methods=["POST"])
def track():
    """
    Start tracking
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        kinect2kit_tracker.start_tracking()
        return jsonify(message="OK")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/track/stream", methods=["POST"])
def stream():
    """
    Stream the latest Kinect output frames to the server, including BodyFrame.
    """

    if not kinect2kit_tracker.is_acquiring_calibration() or not kinect2kit_tracker.is_tracking():
        return jsonify(message="Ignored")
    try:
        kinect_addr = request.remote_addr
        bodyframe = json.loads(request.form["bodyframe"])
        camera = kinect2kit_tracker.get_kinect(kinect_addr)
        if camera is not None:
            kinect2kit_tracker.update_bodyframe(camera, bodyframe)
            return jsonify(message="OK")
        else:
            return jsonify(message="Kinect not found"), 400
    except KeyError:
        return jsonify(message="Invalid request"), 400


@kinect2kit_server.route("/track/result", methods=["GET"])
def get_result():
    """
    Get the latest tracking result
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        # get result
        return jsonify(result="result")
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/kinect/add", methods=["POST"])
def add_kinect():
    """
    Add a Kinect to the current session
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        try:
            name = request.form["name"]
            addr = request.form["addr"]
            tilt_angle = request.form["tilt_angle"]
            height = request.form["height"]
            depth_frame_width = request.form["depth_frame_width"]
            depth_frame_height = request.form["depth_frame_height"]
            kinect2kit_tracker.add_kinect(name, addr, tilt_angle, height, depth_frame_width, depth_frame_height)
            return jsonify(message="OK")
        except KeyError:
            return jsonify(message="Invalid request"), 400
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/kinect/remove", methods=["POST"])
def remove_kinect():
    """
    Remove a Kinect from the current session
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        try:
            kinect_addr = request.form["addr"]
            if kinect2kit_tracker.authenticate(app_addr):
                kinect2kit_tracker.remove_kinect(kinect_addr)
                return jsonify(message="OK")
            else:
                return jsonify(message="Unauthorized access"), 401
        except KeyError:
            return jsonify(message="Invalid request"), 400
    else:
        return jsonify(message="Unauthorized access"), 401


@kinect2kit_server.route("/api/bodyframe", methods=["GET"])
def get_bodyframe_json():
    pass
