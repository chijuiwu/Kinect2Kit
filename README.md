# Kinect2Kit
A RESTFul web service for calibrating and tracking with multiple Kinects. Used by [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker).


## How does it work?
The calibration procedure is based on 3D coordinate transformation proposed in [Wei et al's paper on Kinect Skeleton Coordinate Calibration for Remote Physical Training](http://www.thinkmind.org/download.php?articleid=mmedia_2014_4_20_50039).


## Applications
* [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker)


## Results and papers
You can find my undergraduate thesis titled Tracking People with Multiple Kinects [here](https://github.com/cjw-charleswu/KinectMultiTrack/blob/master/Deliverables/Report/Final/thesis.pdf). The user studies showed that the average joint difference across different scenarios are within personal space (~15cm). Average joint difference is a person's distance between their Kinect skeletons in different viewing perspectives when merged together.


## Documentation
The API is available [here](http://cjw-charleswu.github.io/Kinect2Kit/).


## Prerequisites
You will need the following software:

- The latest [Kinect v2 SDK](https://www.microsoft.com/en-us/kinectforwindows/develop/)
- Windows 8 or abvoe
- USB 3.0
- Visual Studio
- Python 2.7x


## Install
Git clone the repository and install the dependencies.

    $ git clone git@github.com:cjw-charleswu/Kinect2Kit.git
    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

#### Server
Host address and port numbers are optional. By default, the server will run @ localhost:8000

    $ source venv/bin/activate
    (venv) $ python run.py --host=[host] --port=[port]

#### Client
Use Visual Studio to build the projects:

    $ toolkit/client/csharp/Kinect2KitAPI
    $ toolkit/client/csharp/Kinect2KitClient


## Limitations
The current approach works best when all Kinects are placed on the same level. In addition, it will fail when the Kinects are more than 90 degrees apart, e.g. two Kinects opposite of each other.
