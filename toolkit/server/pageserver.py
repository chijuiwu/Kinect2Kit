
from flask import render_template
from .config import kinect2kit_server

@kinect2kit_server.route("/", methods=["GET"])
@kinect2kit_server.route("/index", methods=["GET"])
def get_index():
    """
    Returns the front page
    """

    return render_template("index.html")
