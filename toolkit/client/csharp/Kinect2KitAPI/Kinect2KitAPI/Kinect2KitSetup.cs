using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect2KitAPI
{
    public class Kinect2KitSetup
    {
        public string ServerAddress { get; set; }
        public uint ServerPort { get; set; }
        private List<Kinect2KitClientSetup> clientsList = new List<Kinect2KitClientSetup>();
        public List<Kinect2KitClientSetup> Clients
        {
            get
            {
                return this.clientsList;
            }
        }
    }

    public class Kinect2KitClientSetup
    {
        public string ClientName { get; set; }
        public string ClientAddress { get; set; }
    }
}
