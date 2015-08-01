from flask import Flask
from .tracker import tracker

CALIBRATION_FRAMES = 120

kinect2kit_server = Flask(__name__)
kinect2kit_server.config.from_object(__name__)

kinect2kit_tracker = tracker.create(CALIBRATION_FRAMES)

bodyframe_format = {
    "Timestamp": "Timestamp",
    "Bodies": [
        {
            "TrackingId": "TrackingId",
            "Joints": {
                "JointType": {
                    "JointType": "JointType",
                    "TrackingState": "TrackingState",
                    "Orientation": {
                        "w": "w",
                        "x": "x",
                        "y": "y",
                        "z": "z"
                    },
                    "CameraSpacePoint": {
                        "x": "x",
                        "y": "y",
                        "z": "z"
                    }
                }
            }
        }
    ]
}

tracking_result_format = {
    "Timestamp": "Timestamp",
    "Perspectives": {
        "KinectName": {
            "KinectName": "Name",
            "KinectIPAddress": "IPAddress",
            "People": [
                {
                    "Id": "Id",
                    "Skeletons": {
                        "KinectName": {
                            "IsOriginal": "True",
                            "KinectName": "Name",
                            "KinectIPAddress": "IPAddress",
                            "Joints": {
                                "JointType": {
                                    "JointType": "JointType",
                                    "TrackingState": "TrackingState",
                                    "CameraSpacePoint": {
                                        "x": "x",
                                        "y": "y",
                                        "z": "z"
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
    }
}
