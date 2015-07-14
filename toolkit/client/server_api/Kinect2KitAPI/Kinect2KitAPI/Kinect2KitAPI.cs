using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using Microsoft.Kinect;
using Newtonsoft.Json;

namespace Kinect2KitAPI
{
    public class Kinect2KitAPI
    {
        public static string Server_Address { get; set; }

        #region RESTful Web APIs
        public static readonly string API_New_Session = "/session/new";
        public static readonly string API_Acquire_Calibration = "calibration/acquire";
        public static readonly string API_Resolve_Calibration = "calibration/resolve";
        public static readonly string API_Start_Tracking = "/track/start";
        public static readonly string API_Stream_BodyFrame = "/track/stream";        
        #endregion

        public static string URL_For(string api)
        {
            return Kinect2KitAPI.Server_Address + api;
        }

        public static dynamic GetPOSTResponseJSON(string api)
        {
            return Kinect2KitAPI.GetPOSTResponseJSON(api, new List<KeyValuePair<string, string>>());
        }

        public static dynamic GetPOSTResponseJSON(string api, List<KeyValuePair<string, string>> values)
        {
            string url = Kinect2KitAPI.URL_For(api);
            System.Diagnostics.Debug.WriteLine(url);
            using (var client = new HttpClient())
            {
                var data = new FormUrlEncodedContent(values);
                var response = client.PostAsync(url, data).Result;
                return JsonConvert.DeserializeObject(response.Content.ReadAsStringAsync().Result);
            };
        }

        public static dynamic StreamBodyFrame(double timestamp, Body[] bodies)
        {
            string bodyframeJSON = Kinect2KitAPI.GetBodyFrameJSON(timestamp, bodies);
            var values = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("bodyframe", bodyframeJSON)
            };
            return Kinect2KitAPI.GetPOSTResponseJSON(Kinect2KitAPI.API_Stream_BodyFrame, values);
        }

        public static string GetBodyFrameJSON(double timestamp, Body[] bodies)
        {
            Kinect2KitBodyFrame toolkitBodyFrame = new Kinect2KitBodyFrame();
            
            // Bodies can be untracked.
            bool containsBodies = false;
            foreach (Body body in bodies)
            {
                if (body.IsTracked)
                {
                    containsBodies = true;
                    Kinect2KitBodyFrame.Kinect2KitBody toolkitBody = new Kinect2KitBodyFrame.Kinect2KitBody();
                    toolkitBody.TrackingId = body.TrackingId.ToString();
                    foreach (JointType jt in body.Joints.Keys)
                    {
                        Kinect2KitBodyFrame.Kinect2KitJoint toolkitJoint = new Kinect2KitBodyFrame.Kinect2KitJoint();
                        toolkitJoint.JointType = jt.ToString();
                        toolkitJoint.TrackingState = body.Joints[jt].TrackingState.ToString();

                        toolkitJoint.Orientation = new Kinect2KitBodyFrame.Kinect2KitJointOrientation();
                        toolkitJoint.Orientation.w = body.JointOrientations[jt].Orientation.W;
                        toolkitJoint.Orientation.x = body.JointOrientations[jt].Orientation.X;
                        toolkitJoint.Orientation.y = body.JointOrientations[jt].Orientation.Y;
                        toolkitJoint.Orientation.z = body.JointOrientations[jt].Orientation.Z;

                        toolkitJoint.CameraSpacePoint.x = body.Joints[jt].Position.X;
                        toolkitJoint.CameraSpacePoint.y = body.Joints[jt].Position.Y;
                        toolkitJoint.CameraSpacePoint.z = body.Joints[jt].Position.Z;

                        toolkitBody.Joints[jt.ToString()] = toolkitJoint;
                    }
                    toolkitBodyFrame.Bodies.Add(toolkitBody);
                }
            }

            if (containsBodies)
            {
                return JsonConvert.SerializeObject(toolkitBodyFrame);
            }
            else
            {
                return "";
            }
        }
    }
}
