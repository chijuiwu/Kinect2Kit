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
    public class Kinect2SBody : ISerializable
    {
        public const string KEY_IsTracked = "IsTracked";
        public const string KEY_TrackingId = "TrackingId";
        public const string KEY_Joints = "Joints";
        public const string KEY_ClippedEdges = "ClippedEdges";

        public bool IsTracked { get; private set; }
        public ulong TrackingId { get; private set; }
        public Dictionary<JointType, Kinect2SJoint> Joints { get; private set; }
        public FrameEdges ClippedEdges { get; private set; }

        private Kinect2SBody()
        {

        }

        public static Kinect2SBody MakeInstance(Body body)
        {
            Kinect2SBody serializableBody = new Kinect2SBody();
            serializableBody.IsTracked = body.IsTracked;
            serializableBody.TrackingId = body.TrackingId;
            serializableBody.Joints = new Dictionary<JointType, Kinect2SJoint>();
            foreach (KeyValuePair<JointType, Joint> joint in body.Joints)
            {
                serializableBody.Joints.Add(joint.Key, Kinect2SJoint.MakeInstance(joint.Value));
            }
            serializableBody.ClippedEdges = body.ClippedEdges;
            return serializableBody;
        }

        protected Kinect2SBody(SerializationInfo info, StreamingContext ctx)
        {
            this.IsTracked = (bool)info.GetValue(Kinect2SBody.KEY_IsTracked, typeof(bool));
            this.TrackingId = (ulong)info.GetValue(Kinect2SBody.KEY_TrackingId, typeof(ulong));
            this.Joints = (Dictionary<JointType, Kinect2SJoint>)info.GetValue(Kinect2SBody.KEY_Joints, typeof(Dictionary<JointType, Kinect2SJoint>));
            this.ClippedEdges = (FrameEdges)info.GetValue(Kinect2SBody.KEY_ClippedEdges, typeof(FrameEdges));
        }

        [SecurityPermission(SecurityAction.Demand, SerializationFormatter = true)]
        public void GetObjectData(SerializationInfo info, StreamingContext ctx)
        {
            info.AddValue(Kinect2SBody.KEY_IsTracked, this.IsTracked, typeof(bool));
            info.AddValue(Kinect2SBody.KEY_TrackingId, this.TrackingId, typeof(ulong));
            info.AddValue(Kinect2SBody.KEY_Joints, this.Joints, typeof(Dictionary<JointType, Kinect2SJoint>));
            info.AddValue(Kinect2SBody.KEY_ClippedEdges, this.ClippedEdges, typeof(FrameEdges));
        }
    }
}
