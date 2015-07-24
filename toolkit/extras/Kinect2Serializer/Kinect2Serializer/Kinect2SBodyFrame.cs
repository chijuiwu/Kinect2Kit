using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;
using System.Runtime.Serialization;
using System.Security.Permissions;

namespace Kinect2Serializer
{
    [Serializable]
    public class Kinect2SBodyFrame : ISerializable
    {

        public const string KEY_Timestamp = "Timestamp";
        public const string KEY_Bodies = "Bodies";

        public double Timestamp { get; private set; }
        public List<Kinect2SBody> Bodies { get; private set; }

        private Kinect2SBodyFrame()
        {

        }

        public static Kinect2SBodyFrame MakeInstance(double timestamp, Body[] bodies)
        {
            Kinect2SBodyFrame serializableBodyFrame = new Kinect2SBodyFrame();
            serializableBodyFrame.Timestamp = timestamp;
            serializableBodyFrame.Bodies = new List<Kinect2SBody>();
            foreach (Body body in bodies)
            {
                serializableBodyFrame.Bodies.Add(Kinect2SBody.MakeInstance(body));
            }
            return serializableBodyFrame;
        }

        protected Kinect2SBodyFrame(SerializationInfo info, StreamingContext ctx)
        {
            this.Timestamp = (double)info.GetValue(Kinect2SBodyFrame.KEY_Timestamp, typeof(double));
            this.Bodies = (List<Kinect2SBody>)info.GetValue(Kinect2SBodyFrame.KEY_Bodies, typeof(List<Kinect2SBody>));
        }

        [SecurityPermission(SecurityAction.Demand, SerializationFormatter = true)]
        public void GetObjectData(SerializationInfo info, StreamingContext ctx)
        {
            info.AddValue(Kinect2SBodyFrame.KEY_Timestamp, this.Timestamp, typeof(double));
            info.AddValue(Kinect2SBodyFrame.KEY_Bodies, this.Bodies, typeof(List<Kinect2SBody>));
        }
    }
}
