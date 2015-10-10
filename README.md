# Kinect2Kit
A RESTFul web service for calibrating and tracking with multiple Kinects. It also contains a C# client API for developers to call the RESTful API. Used by [Gesture Tracker][Gesture_Tracker_repo].

## Applications
* [Gesture Tracker][Gesture_Tracker_repo]


## Results and papers
My undergraduate thesis, [Tracking People with Multiple Kinects][thesis], discusses the original system. The user studies showed that the average joint difference across different scenarios are within personal space (~15cm). Average joint difference is a person's distance between their Kinect skeletons in different viewing perspectives when merged together.

A new paper is being written about the current toolkit, previous and new user studies.


## Documentation
The API is available [here](http://cjw-charleswu.github.io/Kinect2Kit/).


## Prerequisites
You will need the following software:

- The latest [Kinect v2 SDK][Kinect_SDK]
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

#### Kinect2Kit API
Build Kinect2kitAPI.dll with Visual Studio for the client and your application.

    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitAPI

#### Client
Build the client with Visual Studio.

    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitClient

#### Example Application: Gesture Tracker
Clone the Gesture Tracker application.

	git clone git@github.com:cjw-charleswu/GestureTracker.git

Build the application with Visual Studio.

	$ GestureTracker/GestureTracker/GestureTracker

Note: You may need to fix the Kinect2KitAPI reference path.


## Run
Run the server and the clients.

#### Server
The IP address and port number are optional. By default, the server will run at localhost:8000.

	$ cd Kinect2Kit/
    $ source venv/bin/activate
    (venv) $ python run.py --host=[host] --port=[port]

#### Client
Start the Kinect2KitClient application on machines running the Kinects.

    $ Kinect2Kit/toolkit/client/csharp/Kinect2KitClient/bin/Body-Basics-WPF.exe

#### Example Application: Gesture Tracker
Start the Gesture Tracker application. Read about [configuration](#docs/api/session/configuration) before starting a new session from the user interface.
	
	$ GestureTracker/GestureTracker/GestureTracker/bin/Debug/GestureTracker.exe


## How does it work?
The system calibrates multiple Kinects using [Wei et al.'s][Wei et al.] technique on 3D coordinate transformation. The system then matches the same skeletons from different Kinects. The server provides RESTful APIs for getting the tracking result.


## Limitations
The current approach works best when all Kinects are placed parallel on the same level. The current system will fail when the Kinects are more than 90 degrees apart, for example, when they are opposite of each other.

[Kinect2Kit_repo]: https://github.com/cjw-charleswu/Kinect2Kit/
[Gesture_Tracker_repo]: https://github.com/cjw-charleswu/GestureTracker
[thesis]: https://github.com/cjw-charleswu/KinectMultiTrack/blob/master/Deliverables/Report/Final/thesis.pdf
[Kinect_SDK]: https://www.microsoft.com/en-us/kinectforwindows/develop/
[Wei et al.]: http://www.thinkmind.org/download.php?articleid=mmedia_2014_4_20_50039