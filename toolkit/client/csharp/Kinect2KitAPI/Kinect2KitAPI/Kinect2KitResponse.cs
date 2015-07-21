using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;

namespace Kinect2KitAPI
{
    public abstract class Kinect2KitServerResponse
    {
        public HttpResponseMessage HttpMessage { get; private set; }
        public bool IsSuccessful { get; private set; }

        public Kinect2KitServerResponse(HttpResponseMessage httpMessage)
        {
            this.HttpMessage = httpMessage;
            this.IsSuccessful = httpMessage.IsSuccessStatusCode;
        }
    }

    public class Kinect2KitSimpleResponse : Kinect2KitServerResponse
    {
        public string ServerMessage { get; private set; }

        public Kinect2KitSimpleResponse(HttpResponseMessage httpMessage, string message)
            : base(httpMessage)
        {
            this.ServerMessage = message;
        }
    }

    public class Kinect2KitCalibrationResponse : Kinect2KitServerResponse
    {
        public bool AcquiringFrames { get; private set; }
        public int RequiredFrames { get; private set; }
        public int RemainedFrames { get; private set; }
        public bool ResolvingFrames { get; private set; }
        public bool Finished { get; private set; }

        public Kinect2KitCalibrationResponse(HttpResponseMessage httpMessage, bool acquiring, int requiredFrames, int remainFrames, bool resolving, bool finished)
            : base(httpMessage)
        {
            this.AcquiringFrames = acquiring;
            this.RequiredFrames = requiredFrames;
            this.RemainedFrames = remainFrames;
            this.ResolvingFrames = resolving;
            this.Finished = finished;
        }
    }
}
