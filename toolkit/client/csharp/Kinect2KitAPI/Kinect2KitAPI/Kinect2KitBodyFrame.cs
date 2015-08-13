using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;

namespace Kinect2KitAPI
{
    public class Kinect2KitBodyFrame
    {
        public double Timestamp { get; private set; }

        private List<Kinect2KitBody> bodies = new List<Kinect2KitBody>();
        public List<Kinect2KitBody> Bodies
        {
            get
            {
                return this.bodies;
            }
        }

        public Kinect2KitBodyFrame(double timestamp)
        {
            this.Timestamp = timestamp;
        }
    }

    public class Kinect2KitBody
    {
        public string TrackingId { get; private set; }
        public FrameEdges ClippedEdges { get; private set; }
        private Dictionary<JointType, Kinect2KitJoint> joints = new Dictionary<JointType, Kinect2KitJoint>();
        public Dictionary<JointType, Kinect2KitJoint> Joints
        {
            get
            {
                return this.joints;
            }
        }

        public Kinect2KitBody(string trackingId, FrameEdges clippedEdges)
        {
            this.TrackingId = trackingId;
            this.ClippedEdges = clippedEdges;
        }
    }

    public class Kinect2KitJoint
    {
        public JointType JointType { get; set; }
        public TrackingState TrackingState { get; set; }
        public Vector4 Orientation { get; set; }
        public CameraSpacePoint CameraSpacePoint { get; set; }
    }
}
