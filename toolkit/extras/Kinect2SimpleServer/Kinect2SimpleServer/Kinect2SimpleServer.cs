using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Kinect2Serializer;

namespace Kinect2SimpleServer
{
    public class Kinect2SimpleServer
    {
        public IPEndPoint HostEndPoint { get; private set; }
        private TcpListener server;
        private Thread serverThread;

        public event KinectSBodyFrameReceivedHandler BodyFrameReceived;
        public delegate void KinectSBodyFrameReceivedHandler(Kinect2SBodyFrame serializableBodyFrame);

        public Kinect2SimpleServer(string address, int port)
        {
            this.HostEndPoint = new IPEndPoint(IPAddress.Parse(address), port);
        }

        public void Start()
        {
            this.server = new TcpListener(this.HostEndPoint);
            this.server.Start();
            this.serverThread = new Thread(new ThreadStart(this.ServerWorkerThread));
            this.serverThread.Start();
        }

        public void Stop()
        {
            if (this.serverThread != null)
            {
                this.serverThread.Abort();
            }
            if (this.server != null)
            {
                this.server.Stop();
            }
        }

        private void ServerWorkerThread()
        {
            while (true)
            {
                TcpClient client = this.server.AcceptTcpClient();
                NetworkStream clientStream = client.GetStream();
                try
                {
                    if (!client.Connected) continue;

                    while (!clientStream.DataAvailable) ;

                    Kinect2SBodyFrame serializableBodyFrame = Kinect2Serializer.Kinect2Serializer.Deserialize(clientStream);
                    this.BodyFrameReceived(serializableBodyFrame);

                    byte[] response = Encoding.Default.GetBytes("OK");
                    clientStream.Write(response, 0, response.Length);
                    clientStream.Flush();
                }
                catch (Exception)
                {
                    System.Diagnostics.Debug.WriteLine("Server exception", "Kinect2SimpleServer");
                    clientStream.Close();
                    client.Close();
                }
            }
        }
    }
}
