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

        public Kinect2SimpleServer(int port)
        {
            this.HostEndPoint = new IPEndPoint(IPAddress.Any, port);
        }

        public Kinect2SimpleServer(string address, int port)
        {
            this.HostEndPoint = new IPEndPoint(IPAddress.Parse(address), port);
        }

        public void Start()
        {
            this.Stop();
            this.server = new TcpListener(this.HostEndPoint);
            this.server.Start();
            this.serverThread = new Thread(new ThreadStart(this.ServerWorkerThread));
            this.serverThread.Start();
            System.Diagnostics.Debug.WriteLine("Server running...", "Kinect2SimpleServer");
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
                Thread handleClientThread = new Thread(() => this.ServerHandleClientThread(client));
                handleClientThread.Start();
            }
        }

        private void ServerHandleClientThread(TcpClient client)
        {
            NetworkStream clientStream = client.GetStream();

            while (true)
            {
                try
                {
                    if (!client.Connected) break;

                    while (!clientStream.DataAvailable) ;
                    
                    // Receive bodyframe as byte array
                    Kinect2SBodyFrame serializableBodyFrame = Kinect2Serializer.Kinect2Serializer.Deserialize(clientStream);
                    if (this.BodyFrameReceived != null)
                    {
                        this.BodyFrameReceived(serializableBodyFrame);
                    }
                    System.Diagnostics.Debug.WriteLine("BodyFrame received! Timestamp: " + serializableBodyFrame.Timestamp, "Kinect2SimpleServer");

                    // Trivial response
                    byte[] response = Encoding.Default.GetBytes("OK");
                    clientStream.Write(response, 0, response.Length);
                    clientStream.Flush();
                }
                catch (Exception)
                {
                    System.Diagnostics.Debug.WriteLine("Server exception", "Kinect2SimpleServer");
                    clientStream.Close();
                    clientStream.Dispose();
                    client.Close();
                }
            }

            clientStream.Close();
            clientStream.Dispose();
            client.Close();
        }
    }
}
