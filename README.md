# Kinect2Kit
A RESTFul web service for calibrating and tracking with multiple Kinects. Used by [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker).

## How does it work?

## Applications

* [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker)

## How to run?
#### Server

- `$ source venv/bin/activate`
- `(venv) $ python run.py --host=[host] --port=[port]`

#### Client

- `$ toolkit\client\csharp\Kinect2KitClient\Kinect2KitClient\bin\Release\Kinect2KitClient.exe`


## Dependencies
#### Server
The server is written in Python, and all required modules are listed inside `requirements.txt`. Use (virtualenv)[http://docs.python-guide.org/en/latest/dev/virtualenvs/].

- `$ virtualenv venv`
- `$ source venv/bin/activate`
- `(venv) $ pip install -r requirements.txt`

#### Client
The Kinect client is written in C#. Use Visual Studio to build the project at:

- `$ Kinect2Kit\toolkit\client\csharp\Kinect2KitClient\Kinect2KitClient.sln`

Disclaimer: The client application is based on Body Basics-WPF in the Kinect v2 SDK. I do not own the rights to their code.

#### Client API

You can find the Kinect2Kit API for the client at:

- `$ Kinect2Kit\toolkit\client\csharp\Kinect2KitAPI\Kinect2KitAPI.sln`
