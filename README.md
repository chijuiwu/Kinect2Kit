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
The Kinect client is written in C#

## How to run?

#### Server

- `$ source venv/bin/activate`
- `(venv) $ python run.py --host=[host] --port=[port]`

#### Client



## Applications

* [Gesture Tracker](https://github.com/cjw-charleswu/GestureTracker)
