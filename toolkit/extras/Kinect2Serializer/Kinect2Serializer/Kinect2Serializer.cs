using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

namespace Kinect2Serializer
{
    public class Kinect2Serializer
    {

        public static byte[] Serialize(double timestamp, Body[] bodies)
        {
            Kinect2SBodyFrame serializableBodyFrame = Kinect2SBodyFrame.MakeInstance(timestamp, bodies);
            BinaryFormatter bf = new BinaryFormatter();
            try
            {
                using (MemoryStream ms = new MemoryStream())
                {
                    bf.Serialize(ms, serializableBodyFrame);
                    return ms.ToArray();
                }
            }
            catch (SerializationException e)
            {
                System.Diagnostics.Debug.WriteLine("Kinect2Serialization exception!!");
                System.Diagnostics.Debug.WriteLine(e.Message);
                System.Diagnostics.Debug.WriteLine(e.StackTrace);
                return new byte[] { };
            }
        }

        public static Kinect2SBodyFrame Deserialize(Stream stream)
        {
            BinaryFormatter bf = new BinaryFormatter();
            try
            {
                return (Kinect2SBodyFrame)bf.Deserialize(stream);
            }
            catch (SerializationException e)
            {
                System.Diagnostics.Debug.WriteLine("Kinect2Deserialization exception!!");
                System.Diagnostics.Debug.WriteLine(e.Message);
                System.Diagnostics.Debug.WriteLine(e.StackTrace);
                return null;
            }
        }
    }
}
