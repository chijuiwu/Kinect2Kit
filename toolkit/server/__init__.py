
__all__ = ["config", "pageserver", "restful", "session", "tracker", "exceptions"]

from .config import kinect2kit_server
from . import pageserver
from . import restful
from . import session
from . import tracker
from . import exceptions

def run(host, port):
    """
    Runs the Kinect2Kit server

    @:param host Host of the server
    @:param port Port of the server
    """

    kinect2kit_server.run(host=host, port=port, debug=True)
