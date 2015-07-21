using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect2KitAPI
{
    public struct Kinect2KitClientInfo
    {
        public string Name { get; set; }
        public string IPAddress { get; set; }
        public int TiltAngle { get; set; }
        public int Height { get; set; }
    }
}
