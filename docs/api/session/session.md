# kinect2kit.session
The Kinect2Kit session API allows developers to start a new tracking session with an environment specification.


## POST - "/session/new"


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


## ClientAPI - "public static bool TryLoadSetup(string setupFilepath)"
The client can specify the environment specification inside a configuration file in xml format, see [configuration](#docs/api/session/configuration). This function loads the configuration file into memory. The `Gesture Tracker` user interface allows the user to select the file through the default file explorer.


    Args:

        setupFilepath (str):
            file path to the configuration file

    Returns:

        true if loaded correctly, false otherwise




## ClientAPI - "public static async Task<Kinect2KitSimpleResponse> StartSessionAsync(string name)"

