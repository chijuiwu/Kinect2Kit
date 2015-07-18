using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect2KitAPI
{
    public class Kinect2KitBodyFrame
    {
        private List<Kinect2KitBody> bodies = new List<Kinect2KitBody>();
        public List<Kinect2KitBody> Bodies
        {
            get
            {
                return this.bodies;
            }
        }
    }

    public class Kinect2KitBody
    {
        public string TrackingId { get; set; }
        private Dictionary<string, Kinect2KitJoint> joints = new Dictionary<string, Kinect2KitJoint>();
        public Dictionary<string, Kinect2KitJoint> Joints
        {
            get
            {
                return this.joints;
            }
        }
    }

    public class Kinect2KitJoint
    {
        public string JointType { get; set; }
        public string TrackingState { get; set; }
        private Kinect2KitJointOrientation orientation = new Kinect2KitJointOrientation();
        public Kinect2KitJointOrientation Orientation
        {
            get
            {
                return this.orientation;
            }
            set
            {
                this.orientation = value;
            }
        }
        private Kinect2KitJointPosition position = new Kinect2KitJointPosition();
        public Kinect2KitJointPosition CameraSpacePoint
        {
            get
            {
                return this.position;
            }
            set
            {
                this.CameraSpacePoint = value;
            }
        }
    }

    public class Kinect2KitJointOrientation
    {
        public float w { get; set; }
        public float x { get; set; }
        public float y { get; set; }
        public float z { get; set; }
    }

    public class Kinect2KitJointPosition
    {
        public float x { get; set; }
        public float y { get; set; }
        public float z { get; set; }
    }
}
