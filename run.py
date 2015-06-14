import toolkit
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Runs the Kinect2Kit server"
    )

    parser.add_argument(
        "--host", dest="host", type=str, default="localhost",
        help="Host of the server"
    )

    parser.add_argument(
        "--port", dest="port", type=int, default=8000,
        help="Port of the server"
    )

    args = parser.parse_args()

    toolkit.server.run(args.host, args.port)


if __name__ == "__main__":
    main()
