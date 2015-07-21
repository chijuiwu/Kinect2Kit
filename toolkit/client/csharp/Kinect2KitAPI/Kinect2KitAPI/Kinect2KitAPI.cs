using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using Microsoft.Kinect;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Kinect2KitAPI.Exceptions;
using System.Xml.Linq;

namespace Kinect2KitAPI
{
    public class Kinect2KitAPI
    {
        /// <summary>
        /// Kinect2Kit server
        /// </summary>
        public static string ServerIPAddress { get; private set; }
        public static uint ServerPort { get; private set; }
        public static string ServerEndpoint { get; private set; }

        /// <summary>
        /// Kinect clients
        /// </summary>
        private static List<ClientInfo> clientsList = new List<ClientInfo>();
        public static List<ClientInfo> Clients
        {
            get
            {
                return Kinect2KitAPI.clientsList;
            }
        }
        public struct ClientInfo
        {
            public string Name { get; set; }
            public string IPAddress { get; set; }
        }

        #region RESTful Web APIs
        public static readonly string API_NewSession = "/session/new";
        public static readonly string API_StartCalibration = "/calibration/start";
        public static readonly string API_CalibrationStatus = "/calibration/status";
        public static readonly string API_StartTracking = "/track/start";
        public static readonly string API_StreamBodyFrame = "/track/stream";
        #endregion

        private static readonly List<KeyValuePair<string, string>> EmptyParameters = new List<KeyValuePair<string, string>>();

        public class Response
        {
            public HttpResponseMessage HttpMessage { get; private set; }
            public bool IsSuccessful { get; private set; }

            public Response(HttpResponseMessage httpMessage)
            {
                this.HttpMessage = httpMessage;
                this.IsSuccessful = httpMessage.IsSuccessStatusCode;
            }
        }

        public class ServerSimpleMessage : Response
        {
            public string ServerMessage { get; private set; }

            public ServerSimpleMessage(HttpResponseMessage httpMessage, string message)
                : base(httpMessage)
            {
                this.ServerMessage = message;
            }
        }

        public class ServerCalibrationMessage : Response
        {
            public bool AcquiringCalibrationFrames { get; private set; }
            public int RequiredCalibrationFrames { get; private set; }
            public int RemainCalibrationFrames { get; private set; }
            public bool ResolvingCalibrationFrames { get; private set; }

            public ServerCalibrationMessage(HttpResponseMessage httpMessage, dynamic serverResponseJSON)
                : base(httpMessage)
            {

            }
        }

        public static bool Has_ServerEndpoint
        {
            get
            {
                return Kinect2KitAPI.ServerEndpoint != null;
            }
        }


        #region Clients APIs

        /// <summary>
        /// 
        /// </summary>
        /// <param name="address"></param>
        /// <param name="port"></param>
        public static void SetServerEndpoint(string address, uint port)
        {
            Kinect2KitAPI.ServerIPAddress = address;
            Kinect2KitAPI.ServerPort = port;
            Kinect2KitAPI.ServerEndpoint = "http://" + Kinect2KitAPI.ServerIPAddress + ":" + Kinect2KitAPI.ServerPort;
        }

        public static void AddClient(string name, string address)
        {
            ClientInfo client = new ClientInfo();
            client.Name = name;
            client.IPAddress = address;
            Kinect2KitAPI.Clients.Add(client);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="setupFilepath"></param>
        /// <returns></returns>
        public static void LoadSetup(string setupFilepath)
        {
            XDocument setupDoc = XDocument.Load(setupFilepath);
            var root = setupDoc.Element("Kinect2KitSetup");

            var server = root.Element("Server");
            string serverIPAddress = server.Element("Address").Value;
            uint serverPort = Convert.ToUInt32(server.Element("Port").Value);
            Kinect2KitAPI.SetServerEndpoint(serverIPAddress, serverPort);

            var clients = root.Element("Clients");
            foreach (var client in clients.Elements("Client"))
            {
                string clientName = client.Element("Name").Value;
                string clientAddress = client.Element("Address").Value;
                Kinect2KitAPI.AddClient(clientName, clientAddress);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="name"></param>
        /// <returns></returns>
        public static async Task<ServerSimpleMessage> StartSessionAsync(string name)
        {
            string clients = JsonConvert.SerializeObject(Kinect2KitAPI.Clients);
            var parameters = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("name", name),
                new KeyValuePair<string, string>("clients", clients)
            };
            Tuple<HttpResponseMessage, JToken> result = await Kinect2KitAPI.POSTAsync(Kinect2KitAPI.API_NewSession, parameters);
            return new ServerSimpleMessage(result.Item1, (string)result.Item2["message"]);
        }

        public static async Task<ServerSimpleMessage> StartCalibrationAsync()
        {
            Tuple<HttpResponseMessage, JToken> result = await Kinect2KitAPI.POSTAsync(Kinect2KitAPI.API_StartCalibration);
            return new ServerSimpleMessage(result.Item1, (string)result.Item2["message"]);
        }

        public static Response GetCalibrationStatus()
        {
            //return Kinect2KitAPI.POSTAsync(Kinect2KitAPI.API_CalibrationStatus, Kinect2KitAPI.EmptyParameters);
            return null;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="timestamp"></param>
        /// <param name="bodies"></param>
        /// <returns></returns>
        public static dynamic StreamBodyFrame(double timestamp, Body[] bodies)
        {
            var values = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("bodyframe", Kinect2KitAPI.GetBodyFrameJSON(timestamp, bodies))
            };
            return Kinect2KitAPI.POSTAsync(Kinect2KitAPI.API_StreamBodyFrame, values);
        }
        #endregion

        private static string GetBodyFrameJSON(double timestamp, Body[] bodies)
        {
            Kinect2KitBodyFrame toolkitBodyFrame = new Kinect2KitBodyFrame();

            // Bodies can be not tracked.
            bool containsBodies = false;
            foreach (Body body in bodies)
            {
                if (body.IsTracked)
                {
                    containsBodies = true;
                    Kinect2KitBody toolkitBody = new Kinect2KitBody();
                    toolkitBody.TrackingId = body.TrackingId.ToString();
                    foreach (JointType jt in body.Joints.Keys)
                    {
                        Kinect2KitJoint toolkitJoint = new Kinect2KitJoint();
                        toolkitJoint.JointType = jt.ToString();
                        toolkitJoint.TrackingState = body.Joints[jt].TrackingState.ToString();

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

        #region HTTP GET, POST for APIs
        private static string URL_For(string api)
        {
            if (!Kinect2KitAPI.Has_ServerEndpoint)
            {
                throw new Kinect2KitServerNotSetException();
            }
            else
            {
                return Kinect2KitAPI.ServerEndpoint + api;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, dynamic>> GETAsync(string api)
        {
            string url = Kinect2KitAPI.URL_For(api);
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage httpMessage = await client.GetAsync(url);
                string content = await httpMessage.Content.ReadAsStringAsync();
                dynamic serverResponseJSON = JObject.Parse(content);
                return new Tuple<HttpResponseMessage, dynamic>(httpMessage, serverResponseJSON);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, JToken>> POSTAsync(string api)
        {
            return await Kinect2KitAPI.POSTAsync(api, Kinect2KitAPI.EmptyParameters);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="api"></param>
        /// <param name="parameters"></param>
        /// <returns></returns>
        private static async Task<Tuple<HttpResponseMessage, JToken>> POSTAsync(string api, List<KeyValuePair<string, string>> parameters)
        {
            string url = Kinect2KitAPI.URL_For(api);
            using (HttpClient client = new HttpClient())
            {
                FormUrlEncodedContent data = new FormUrlEncodedContent(parameters);
                HttpResponseMessage httpMessage = await client.PostAsync(url, data);
                string content = await httpMessage.Content.ReadAsStringAsync();
                JToken serverResponseJSON = JObject.Parse(content);
                return new Tuple<HttpResponseMessage, JToken>(httpMessage, serverResponseJSON);
            };
        }
        #endregion
    }
}
