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
        clients = json.loads(request.form["clients"])
        for client in clients:
            kinect2kit_tracker.add_kinect(client["Name"], client["IPAddress"])
        kinect2kit_tracker.set_session(name, app_addr)
        return jsonify(message="OK")
    except KeyError:
        return jsonify(message="Failed, invalid request"), 400


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
        return jsonify(message="Failed, unauthorized access"), 401


@kinect2kit_server.route("/calibration/start", methods=["POST"])
def start_calibration():
    """
    Start acquring calibration frames
    """

    app_addr = request.remote_addr
    if kinect2kit_tracker.authenticate(app_addr):
        kinect2kit_tracker.start_acquiring_calibration_frames()
        return jsonify(message="OK")
    else:
        return jsonify(message="Failed, unauthorized access"), 401


@kinect2kit_server.route("/calibration/status", methods=["GET"])
def get_calibration_status():
    """
    """

    acquring = kinect2kit_tracker.is_acquiring_calibration()
    required_frames = kinect2kit_tracker.get_required_calibration_frames()
    remained_frames = kinect2kit_tracker.get_remained_calibration_frames()
    resolving = kinect2kit_tracker.is_resolving_calibration()
    finished = kinect2kit_tracker.has_finished_calibration()
    return jsonify(acquiring=acquring, required_frames=required_frames, remained_frames=remained_frames,
                   resolving=resolving, finished=finished)


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
        return jsonify(message="Failed, unauthorized access"), 401


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
        return jsonify(message="Failed, unauthorized access"), 401


@kinect2kit_server.route("/bodyframe/stream", methods=["POST"])
def stream_bodyframe():
    """
    Receive a Kinect BodyFrame from a client
    """

    if not kinect2kit_tracker.is_acquiring_calibration() and not kinect2kit_tracker.is_tracking():
        return jsonify(message="Ignored, Server does not require frames"), 400
    try:
        kinect_addr = request.remote_addr
        bodyframe = json.loads(request.form["bodyframe"])
        camera = kinect2kit_tracker.get_kinect(kinect_addr)
        if camera is not None:
            kinect2kit_tracker.update_bodyframe(camera, bodyframe)
            return jsonify(message="OK")
        else:
            return jsonify(message="Ignored, Server does not recognize the client"), 400
    except KeyError:
        return jsonify(message="Failed, Invalid request"), 400


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
            kinect2kit_tracker.add_kinect(name, addr, tilt_angle, height)
            return jsonify(message="OK")
        except KeyError:
            return jsonify(message="Failed, invalid request"), 400
    else:
        return jsonify(message="Failed, unauthorized access"), 401


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
                return jsonify(message="Failed, unauthorized access"), 401
        except KeyError:
            return jsonify(message="Failed, invalid request"), 400
    else:
        return jsonify(message="Failed, unauthorized access"), 401


@kinect2kit_server.route("/api/bodyframe", methods=["GET"])
def get_bodyframe_json():
    pass
