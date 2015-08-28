using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;

namespace Kinect2KitAPI
{
    public class Kinect2KitPerspective
    {
        public string KinectName { get; private set; }
        public string KinectIPAddress { get; private set; }
        private List<Kinect2KitPerson> people = new List<Kinect2KitPerson>();
        public List<Kinect2KitPerson> People
        {
            get
            {
                return this.people;
            }
        }
    }

    public class Kinect2KitPerson
    {
        public int Id { get; private set; }
        private Dictionary<string, Kinect2KitSkeleton> skeletons = new Dictionary<string, Kinect2KitSkeleton>();
        public Dictionary<string, Kinect2KitSkeleton> Skeletons
        {
            get
            {
                return this.skeletons;
            }
        }
        private Dictionary<JointType, Kinect2KitJoint> average = new Dictionary<JointType, Kinect2KitJoint>();
        public Dictionary<JointType, Kinect2KitJoint> AverageSkeleton
        {
            get
            {
                return this.average;
            }
        }
    }

    public class Kinect2KitSkeleton
    {
        public bool IsNative { get; private set; }
        public string KinectName { get; private set; }
        public string KinectIPAddress { get; private set; }
        private Dictionary<JointType, Kinect2KitJoint> joints = new Dictionary<JointType, Kinect2KitJoint>();
        public Dictionary<JointType, Kinect2KitJoint> Joints
        {
            get
            {
                return this.joints;
            }
        }
    }
}
