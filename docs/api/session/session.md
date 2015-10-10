# kinect2kit.session
The Kinect2Kit session API allows developers to start a new tracking session with an environment specification.


## POST


    Parameters:

        {
            "Name": "The session name",
            "Clients": [
                {
                    "Name": "The Kinect client name",
                    "IPAddress": "The Kinect client IP address"
                }
            ]
        }

    Returns:

        {
            "message": "Response"
        }

        HTTP status code 200 or 400


## C# Client

The client can specify the environment specification inside a configuration file in xml format, see [configuration](#docs/api/session/configuration)