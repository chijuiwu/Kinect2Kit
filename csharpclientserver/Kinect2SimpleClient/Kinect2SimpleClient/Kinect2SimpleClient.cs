using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Microsoft.Kinect;
using Kinect2Serializer;

namespace Kinect2SimpleClient
{
    public class Kinect2SimpleClient
    {
        public IPEndPoint HostEndPoint { get; private set; }
        private TcpClient client;
        private Thread clientThread;
        private NetworkStream clientStream;

        public event KinectSBodyFrameSentHandler BodyFrameSent;
        public delegate void KinectSBodyFrameSentHandler(double timestamp);

        public Kinect2SimpleClient(string host, int port)
        {
            this.HostEndPoint = new IPEndPoint(IPAddress.Parse(host), port);
        }

        public void Start()
        {
            this.Stop();   
            this.client = new TcpClient();
            this.clientThread = new Thread(new ThreadStart(this.ClientWorkerThread));
            this.clientThread.Start();
        }

        public void Stop()
        {
            if (this.clientThread != null)
            {
                this.clientThread.Abort();
            }
            if (this.clientStream != null)
            {
                this.clientStream.Close();
                this.clientStream.Dispose();
            }
            if (this.client != null)
            {
                this.client.Close();
            }
        }

        private void ClientWorkerThread()
        {
            while (true)
            {
                if (this.CanWriteToServer())
                {
                    continue;
                }
                try
                {
                    this.client.Connect(this.HostEndPoint);
                    this.clientStream = this.client.GetStream();
                    System.Diagnostics.Debug.WriteLine("Connected to the server.", "Kinect2SimpleClient");
                }
                catch (Exception)
                {
                    System.Diagnostics.Debug.WriteLine("Failed to connect to the server. Re-trying...", "Kinect2SimpleClient");
                }
            }
        }

        private bool CanWriteToServer()
        {
            if (this.client == null || this.clientStream == null)
            {
                return false;
            }
            else
            {
                return this.client.Connected && this.clientStream.CanWrite;
            }
        }

        public void SendKinectBodyFrame(double timestamp, Body[] bodies)
        {
            if (!this.CanWriteToServer())
            {
                System.Diagnostics.Debug.WriteLine("Unable to write to the server.", "Kinect2SimpleClient");
                return;
            }
            try
            {
                // Send BodyFrame as byte array
                byte[] bodyFrameInBytes = Kinect2Serializer.Kinect2Serializer.Serialize(timestamp, bodies);
                this.clientStream.Write(bodyFrameInBytes, 0, bodyFrameInBytes.Length);
                this.clientStream.Flush();

                // Ignore response
                byte[] response = new byte[256];
                this.clientStream.Read(response, 0, response.Length);
                
                if (this.BodyFrameSent != null)
                {
                    this.BodyFrameSent(timestamp);
                }
                System.Diagnostics.Debug.WriteLine("BodyFrame sent! Timestamp: " + timestamp, "Kinect2SimpleClient");
            }
            catch (Exception)
            {
                System.Diagnostics.Debug.WriteLine("Network failure.", "Kinect2SimpleClient");
            }
        }
    }
}
