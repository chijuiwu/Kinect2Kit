using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Net.Http;
using Microsoft.Kinect;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Kinect2KitAPI.Exceptions;
using System.Xml.Linq;

namespace Kinect2KitAPI
{
    public class Kinect2Kit
    {
        /// <summary>
        /// Kinect2Kit server
        /// </summary>
        public static string ServerIPAddress { get; private set; }
        public static int ServerPort { get; private set; }
        public static string ServerEndpoint { get; private set; }

        /// <summary>
        /// Kinect clients
        /// </summary>
        private static List<Kinect2KitClientSetup> kinectClientsList = new List<Kinect2KitClientSetup>();
        public static List<Kinect2KitClientSetup> KinectClients
        {
            get
            {
                return Kinect2Kit.kinectClientsList;
            }
        }

        #region RESTful Web APIs
        public static readonly string API_NewSession = "/session/new";
        public static readonly string API_StopSession = "/session/stop";
        public static readonly string API_StartCalibration = "/calibration/start";
        public static readonly string API_CalibrationStatus = "/calibration/status";
        public static readonly string API_StartTracking = "/track/start";
        public static readonly string API_TrackingResult = "/track/result";
        public static readonly string API_StreamBodyFrame = "/bodyframe/stream";
        #endregion

        private static readonly List<KeyValuePair<string, string>> EmptyParameters = new List<KeyValuePair<string, string>>();

        public static bool Has_ServerEndpoint
        {
            get
            {
                return Kinect2Kit.ServerEndpoint != null;
            }
        }


        #region Clients APIs

        /// <summary>
        /// 
        /// </summary>
        /// <param name="address"></param>
        /// <param name="port"></param>
        public static bool TrySetServerEndPoint(string address, int port)
        {
            try
            {
                TcpClient client = new TcpClient();
                client.Connect(address, port);
                client.Close();
                Kinect2Kit.ServerIPAddress = address;
                Kinect2Kit.ServerPort = port;
                Kinect2Kit.ServerEndpoint = "http://" + Kinect2Kit.ServerIPAddress + ":" + Kinect2Kit.ServerPort;
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public static void AddKinectClient(string name, string address)
        {
            Kinect2KitClientSetup client = new Kinect2KitClientSetup();
            client.Name = name;
            client.IPAddress = address;
            Kinect2Kit.KinectClients.Add(client);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="setupFilepath"></param>
        /// <returns></returns>
        public static bool TryLoadSetup(string setupFilepath)
        {
            // TODO: validate inputs, check clients

            XDocument setupDoc = XDocument.Load(setupFilepath);
            var root = setupDoc.Element("Kinect2KitSetup");

            var server = root.Element("Server");
            string serverIPAddress = server.Element("IPAddress").Value;
            int serverPort = Convert.ToInt32(server.Element("Port").Value);
            if (!Kinect2Kit.TrySetServerEndPoint(serverIPAddress, serverPort))
            {
                return false;
            }

            var kinects = root.Element("Kinects");
            foreach (var kinect in kinects.Elements("Kinect"))
            {
                string kinectName = kinect.Element("Name").Value;
                string kinectIPAddress = kinect.Element("IPAddress").Value;
                Kinect2Kit.AddKinectClient(kinectName, kinectIPAddress);
            }

            return true;
        }

        public static async Task<Kinect2KitSimpleResponse> StartSessionAsync(string name)
        {
            string clients = JsonConvert.SerializeObject(Kinect2Kit.KinectClients);
            var parameters = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("Name", name),
                new KeyValuePair<string, string>("Clients", clients)
            };
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.POSTAsync(Kinect2Kit.API_NewSession, parameters);
            return new Kinect2KitSimpleResponse(resp.Item1, (string)resp.Item2["message"]);
        }

        public static async Task<Kinect2KitSimpleResponse> StopSessionAsync()
        {
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.POSTAsync(Kinect2Kit.API_StopSession);
            return new Kinect2KitSimpleResponse(resp.Item1, (string)resp.Item2["message"]);
        }

        public static async Task<Kinect2KitSimpleResponse> StartCalibrationAsync()
        {
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.POSTAsync(Kinect2Kit.API_StartCalibration);
            return new Kinect2KitSimpleResponse(resp.Item1, (string)resp.Item2["message"]);
        }

        public static async Task<Kinect2KitCalibrationResponse> GetCalibrationStatusAsync()
        {
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.GETAsync(Kinect2Kit.API_CalibrationStatus);
            bool acquiring = (bool)resp.Item2["acquiring"];
            int requiredFrames = (int)resp.Item2["required_frames"];
            int remainedFrames = (int)resp.Item2["remained_frames"];
            bool resolving = (bool)resp.Item2["resolving"];
            bool finished = (bool)resp.Item2["finished"];
            string error = (string)resp.Item2["error"];
            return new Kinect2KitCalibrationResponse(resp.Item1, acquiring, requiredFrames, remainedFrames, resolving, finished, error);
        }

        public static async Task<Kinect2KitSimpleResponse> StartTrackingAsync()
        {
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.POSTAsync(Kinect2Kit.API_StartTracking);
            return new Kinect2KitSimpleResponse(resp.Item1, (string)resp.Item2["message"]);
        }

        public static async Task<Kinect2KitTrackingResponse> GetTrackingResultAsync()
        {
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.GETAsync(Kinect2Kit.API_TrackingResult);
            
            JToken trackingResult = (JToken)resp.Item2["result"];

            double timestamp = (double)trackingResult["Timestamp"];
            Dictionary<string, Kinect2KitPerspective> perspectivesDict = new Dictionary<string, Kinect2KitPerspective>();

            foreach (JToken resultPerspective in trackingResult["Perspectives"].Values())
            {
                string kinectName = (string)resultPerspective["KinectName"];
                Kinect2KitPerspective perspective = await JsonConvert.DeserializeObjectAsync<Kinect2KitPerspective>(resultPerspective.ToString(), null);
                perspectivesDict[kinectName] = perspective;
            }

            return new Kinect2KitTrackingResponse(resp.Item1, timestamp, perspectivesDict);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="timestamp"></param>
        /// <param name="bodies"></param>
        /// <returns></returns>
        public static async Task<Kinect2KitSimpleResponse> StreamBodyFrame(double timestamp, Body[] bodies)
        {
            var parameters = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("Bodyframe", Kinect2Kit.GetBodyFrameJSON(timestamp, bodies))
            };
            Tuple<HttpResponseMessage, JObject> resp = await Kinect2Kit.POSTAsync(Kinect2Kit.API_StreamBodyFrame, parameters);
            return new Kinect2KitSimpleResponse(resp.Item1, (string)resp.Item2["message"]);
        }
        #endregion

        private static string GetBodyFrameJSON(double timestamp, Body[] bodies)
        {
            Kinect2KitBodyFrame toolkitBodyFrame = new Kinect2KitBodyFrame(timestamp);

            foreach (Body body in bodies)
            {
                if (body.IsTracked)
                {
                    Kinect2KitBody toolkitBody = new Kinect2KitBody(body.TrackingId.ToString(), body.ClippedEdges);
                    foreach (JointType jointType in body.Joints.Keys)
                    {
                        Kinect2KitJoint toolkitJoint = new Kinect2KitJoint();

                        toolkitJoint.JointType = jointType;
                        toolkitJoint.TrackingState = body.Joints[jointType].TrackingState;
                        toolkitJoint.Orientation = body.JointOrientations[jointType].Orientation;
                        toolkitJoint.CameraSpacePoint = body.Joints[jointType].Position;

                        toolkitBody.Joints[jointType] = toolkitJoint;
                    }
                    toolkitBodyFrame.Bodies.Add(toolkitBody);
                }
            }
            return JsonConvert.SerializeObject(toolkitBodyFrame);
        }

        #region HTTP GET, POST for APIs
        private static string URL_For(string api)
        {
            if (!Kinect2Kit.Has_ServerEndpoint)
            {
                throw new Kinect2KitServerNotSetException();
            }
            else
            {
                return Kinect2Kit.ServerEndpoint + api;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, JObject>> GETAsync(string api)
        {
            string url = Kinect2Kit.URL_For(api);
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage httpMessage = await client.GetAsync(url);
                string responseText = await httpMessage.Content.ReadAsStringAsync();
                JObject responseJSON = JObject.Parse(responseText);
                return new Tuple<HttpResponseMessage, JObject>(httpMessage, responseJSON);
            };
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, JObject>> POSTAsync(string api)
        {
            return await Kinect2Kit.POSTAsync(api, Kinect2Kit.EmptyParameters);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <param name="parameters"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, JObject>> POSTAsync(string api, List<KeyValuePair<string, string>> parameters)
        {
            string url = Kinect2Kit.URL_For(api);
            FormUrlEncodedContent data = new FormUrlEncodedContent(parameters);
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage httpMessage = await client.PostAsync(url, data);
                string responseText = await httpMessage.Content.ReadAsStringAsync();
                JObject responseJSON = JObject.Parse(responseText);
                return new Tuple<HttpResponseMessage, JObject>(httpMessage, responseJSON);
            };
        }
        #endregion
    }
}
