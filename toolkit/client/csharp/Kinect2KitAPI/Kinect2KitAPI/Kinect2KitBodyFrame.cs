using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect2KitAPI
{
    public class Kinect2KitBodyFrame
    {
        public List<Kinect2KitBody> Bodies = new List<Kinect2KitBody>();

        public class Kinect2KitBody
        {
            public string TrackingId;
            public Dictionary<string, Kinect2KitJoint> Joints = new Dictionary<string, Kinect2KitJoint>();
        }

        public class Kinect2KitJoint
        {
            public string JointType;
            public string TrackingState;
            public Kinect2KitJointOrientation Orientation;
            public Kinect2KitJointPosition CameraSpacePoint;
        }

        public class Kinect2KitJointOrientation
        {
            public float w;
            public float x;
            public float y;
            public float z;
        }

        public class Kinect2KitJointPosition
        {
            public float x;
            public float y;
            public float z;
        }
    }


}
