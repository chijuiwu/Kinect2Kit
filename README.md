# Kinect2Kit
A RESTFul web service for calibrating and tracking with multiple Kinects. Used by [Gesture Tracker][1].

## Applications
* [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker)


## Results and papers
My undergraduate thesis, [Tracking People with Multiple Kinects][2], discusses the original system. The user studies showed that the average joint difference across different scenarios are within personal space (~15cm). Average joint difference is a person's distance between their Kinect skeletons in different viewing perspectives when merged together.

A new paper is being written about the current toolkit, previous and new user studies.


## Documentation
The API is available [here](http://cjw-charleswu.github.io/Kinect2Kit/).


## Prerequisites
You will need the following software:

- The latest [Kinect v2 SDK][3]
- Windows 8 or abvoe
- USB 3.0
- Visual Studio
- Python 2.7x


## Install
Git clone the repository and install the dependencies.

#### Server
Create a virtual environment for the server.

    git clone git@github.com:cjw-charleswu/Kinect2Kit.git
    cd Kinect2Kit/
    virtualenv venv
    source venv/bin/activate
    (venv) pip install -r requirements.txt

#### Client
Use Visual Studio to build the following projects. You may build either the debug or release version. 

    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitAPI
    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitClient

#### Example Application: Gesture Tracker
Build the Kinect2KitAPI from the Kinect2Kit using Visual Studio.

	$ Kinect2Kit/toolkit/client/csharp/Kinect2KitAPI

Clone the Gesture Tracker application.

	git clone git@github.com:cjw-charleswu/GestureTracker.git

Build the the application using Visual Studio. You may need to fix the Kinect2KitAPI reference path.

	$ GestureTracker/GestureTracker/GestureTracker


## Run
The server is a Python Flask application. The clients are C# WPF applications.

#### Server
The IP address and port number are optional.  By default, the server will run @ localhost:8000.

	$ cd Kinect2Kit/
    $ source venv/bin/activate
    (venv) $ python run.py --host=[host] --port=[port]

#### Client
Start the Kinect2KitClient application.

    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitClient/bin/AnyCPU/Debug/Body-Basics-WPF.exe

#### Example Application: Gesture Tracker
Start the Gesture Tracker application. It uses a [configuration file][4].
	
	$ GestureTracker/GestureTracker/GestureTracker/bin/Debug/GestureTracker.exe
	

## How does it work?
The calibration procedure is based on 3D coordinate transformation proposed in [Wei et al's paper on Kinect Skeleton Coordinate Calibration for Remote Physical Training][5].

## Limitations
The current approach works best when all Kinects are placed on the same level. In addition, it will fail when the Kinects are more than 90 degrees apart, for example, when they are opposite of each other.

[1]: https://github.com/cjw-charleswu/GestureTracker
[2]: https://github.com/cjw-charleswu/KinectMultiTrack/blob/master/Deliverables/Report/Final/thesis.pdf
[3]: https://www.microsoft.com/en-us/kinectforwindows/develop/
[4]: http://cjw-charleswu.github.io/Kinect2Kit/#docs/api/configuration/configuration
[5]: http://www.thinkmind.org/download.php?articleid=mmedia_2014_4_20_50039