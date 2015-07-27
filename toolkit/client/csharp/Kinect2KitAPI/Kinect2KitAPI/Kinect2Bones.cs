using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;

namespace Kinect2KitAPI
{
    /// <summary>
    /// This class is based on the BodyBasics-WPF example in the Microsoft Kinect v2 SDK
    /// </summary>
    public class Kinect2Bones
    {
        public static readonly IEnumerable<Tuple<JointType, JointType>> Torso = new List<Tuple<JointType, JointType>>()
        {
            new Tuple<JointType, JointType>(JointType.Head, JointType.Neck),
            new Tuple<JointType, JointType>(JointType.Neck, JointType.SpineShoulder),
            new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.SpineMid),
            new Tuple<JointType, JointType>(JointType.SpineMid, JointType.SpineBase),
            new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.ShoulderRight),
            new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.ShoulderLeft),
            new Tuple<JointType, JointType>(JointType.SpineBase, JointType.HipRight),
            new Tuple<JointType, JointType>(JointType.SpineBase, JointType.HipLeft)
        };

        public static readonly IEnumerable<Tuple<JointType, JointType>> RightArm = new List<Tuple<JointType, JointType>>()
        {
            new Tuple<JointType, JointType>(JointType.ShoulderRight, JointType.ElbowRight),
            new Tuple<JointType, JointType>(JointType.ElbowRight, JointType.WristRight),
            new Tuple<JointType, JointType>(JointType.WristRight, JointType.HandRight),
            new Tuple<JointType, JointType>(JointType.HandRight, JointType.HandTipRight),
            new Tuple<JointType, JointType>(JointType.WristRight, JointType.ThumbRight)
        };

        public static readonly IEnumerable<Tuple<JointType, JointType>> LeftArm = new List<Tuple<JointType, JointType>>()
        {
            new Tuple<JointType, JointType>(JointType.ShoulderLeft, JointType.ElbowLeft),
            new Tuple<JointType, JointType>(JointType.ElbowLeft, JointType.WristLeft),
            new Tuple<JointType, JointType>(JointType.WristLeft, JointType.HandLeft),
            new Tuple<JointType, JointType>(JointType.HandLeft, JointType.HandTipLeft),
            new Tuple<JointType, JointType>(JointType.WristLeft, JointType.ThumbLeft)
        };

        public static readonly IEnumerable<Tuple<JointType, JointType>> RightLeg = new List<Tuple<JointType, JointType>>()
        {
            new Tuple<JointType, JointType>(JointType.HipRight, JointType.KneeRight),
            new Tuple<JointType, JointType>(JointType.KneeRight, JointType.AnkleRight),
            new Tuple<JointType, JointType>(JointType.AnkleRight, JointType.FootRight)

        };

        public static readonly IEnumerable<Tuple<JointType, JointType>> LeftLeg = new List<Tuple<JointType, JointType>>()
        {
            new Tuple<JointType, JointType>(JointType.HipLeft, JointType.KneeLeft),
            new Tuple<JointType, JointType>(JointType.KneeLeft, JointType.AnkleLeft),
            new Tuple<JointType, JointType>(JointType.AnkleLeft, JointType.FootLeft)

        };

        public static readonly IEnumerable<Tuple<JointType, JointType>> All = Torso.Concat(RightArm).Concat(LeftArm).Concat(RightLeg).Concat(LeftLeg);
    }
}
