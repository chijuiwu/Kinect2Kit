# Kinect2Kit
A RESTFul web service for calibrating and tracking with multiple Kinects.

## How does it work?

## Dependencies

#### Server
The server is written in Python. It's recommended that you use Python's virtual environment. You can install it with pip:

- `$ pip install virtualenv`

Then, do:

- `$ virtualenv venv`
- `$ source venv/bin/activate`
- `(venv) $ pip install -r requirements.txt`

To exit the virtual environment:

- `(venv) $ deactivate`

#### Client
The Kinect client is written in C#. Use Visual Studio to build the project at:

- `$ toolkit\client\csharp\Kinect2KitClient\Kinect2KitClient.sln`

Disclaimer: The client application is based on Body Basics-WPF in the Kinect v2 SDK. I do not own the rights to their code.

## How to run?

#### Server

- `$ source venv/bin/activate`
- `(venv) $ python run.py --host=[host] --port=[port]`

#### Client

- `$ toolkit\client\csharp\Kinect2KitClient\Kinect2KitClient\bin\Debug\Kinect2KitClient.exe`

## Applications

* [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker)
