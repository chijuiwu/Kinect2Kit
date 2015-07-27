using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Kinect2Serializer;
using Kinect2SimpleServer;

namespace ExampleServer
{
    class Program
    {
        static void Main(string[] args)
        {
            Kinect2SimpleServer.Kinect2SimpleServer server = new Kinect2SimpleServer.Kinect2SimpleServer(8000);
            server.BodyFrameReceived += server_BodyFrameReceived;
            server.Start();
        }

        static void server_BodyFrameReceived(Kinect2SBodyFrame serializableBodyFrame)
        {
            System.Diagnostics.Debug.WriteLine("something");
        }
    }
}
