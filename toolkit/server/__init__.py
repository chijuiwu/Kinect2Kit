
__all__ = ["config", "pageserver", "restful"]

from config import kinect2kit_server
import pageserver
import restful

def run(host, port):
    """
    Runs the Kinect2Kit server

    @:param host Host of the server
    @:param port Port of the server
    """

    kinect2kit_server.run(host=host, port=port, debug=True, use_reloader=False)
