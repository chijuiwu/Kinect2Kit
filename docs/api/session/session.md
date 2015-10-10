# kinect2kit.session
The Kinect2Kit session API allows developers to start a new tracking session with an environment specification.



POST


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

        with either 200 or 400 status code


The Kinect2Kit client API ..

