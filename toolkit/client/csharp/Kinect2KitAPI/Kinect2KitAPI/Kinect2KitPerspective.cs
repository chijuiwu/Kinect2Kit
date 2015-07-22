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
        public List<Kinect2KitPerson> People { get; private set; }

        public Kinect2KitPerspective(string kinectName, string kinectIPAddress, List<Kinect2KitPerson> people)
        {
            this.KinectName = kinectName;
            this.KinectIPAddress = kinectIPAddress;
            this.People = people;
        }
    }

    public class Kinect2KitPerson
    {
        public int Id { get; private set; }
        public Dictionary<string, Kinect2KitSkeleton> Skeletons { get; private set; }

        public Kinect2KitPerson(int id, Dictionary<string, Kinect2KitSkeleton> skeletons)
        {
            this.Id = id;
            this.Skeletons = skeletons;
        }
    }

    public class Kinect2KitSkeleton
    {
        public bool IsOriginal { get; private set; }
        public string KinectName { get; private set; }
        public string KinectIPAddress { get; private set; }
        public Dictionary<JointType, Joint> Joints { get; private set; }

        public Kinect2KitSkeleton(bool original, string kinectName, string kinectIPAddress, Dictionary<JointType, Joint> joints)
        {
            this.IsOriginal = original;
            this.KinectName = kinectName;
            this.KinectIPAddress = kinectIPAddress;
            this.Joints = joints;
        }
    }
}
