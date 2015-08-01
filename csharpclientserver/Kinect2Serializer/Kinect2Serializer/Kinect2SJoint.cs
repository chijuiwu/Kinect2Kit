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
    public class Kinect2SJoint : ISerializable
    {
        public const string KEY_TrackingState = "TrackingState";
        public const string KEY_JointType = "JointType";
        public const string KEY_CameraSpacePoint = "CameraSpacePoint";
        public const string KEY_Orientation = "Orientation";

        public TrackingState TrackingState { get; private set; }
        public JointType JointType { get; private set; }
        public CameraSpacePoint CameraSpacePoint { get; private set; }
        public JointOrientation Orientation { get; private set; }

        private Kinect2SJoint()
        {

        }

        public static Kinect2SJoint MakeInstance(Joint joint, JointOrientation orientation)
        {
            Kinect2SJoint serializableJoint = new Kinect2SJoint();
            serializableJoint.TrackingState = joint.TrackingState;
            serializableJoint.JointType = joint.JointType;
            serializableJoint.CameraSpacePoint = joint.Position;
            serializableJoint.Orientation = orientation;
            return serializableJoint;
        }

        protected Kinect2SJoint(SerializationInfo info, StreamingContext ctx)
        {
            this.TrackingState = (TrackingState)info.GetValue(Kinect2SJoint.KEY_TrackingState, typeof(TrackingState));
            this.JointType = (JointType)info.GetValue(Kinect2SJoint.KEY_JointType, typeof(JointType));
            this.CameraSpacePoint = (CameraSpacePoint)info.GetValue(Kinect2SJoint.KEY_CameraSpacePoint, typeof(CameraSpacePoint));
            this.Orientation = ((JointOrientation)info.GetValue(Kinect2SJoint.KEY_Orientation, typeof(JointOrientation)));
        }

        [SecurityPermission(SecurityAction.Demand, SerializationFormatter = true)]
        public void GetObjectData(SerializationInfo info, StreamingContext ctx)
        {
            info.AddValue(Kinect2SJoint.KEY_TrackingState, this.TrackingState, typeof(TrackingState));
            info.AddValue(Kinect2SJoint.KEY_JointType, this.JointType, typeof(JointType));
            info.AddValue(Kinect2SJoint.KEY_CameraSpacePoint, this.CameraSpacePoint, typeof(CameraSpacePoint));
            info.AddValue(Kinect2SJoint.KEY_Orientation, this.Orientation, typeof(JointOrientation));
        }
    }
}
