using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect2KitAPI.Exceptions
{
    [Serializable]
    public class Kinect2KitServerNotSetException: Exception
    {

        public Kinect2KitServerNotSetException()
        { 
        }

        public Kinect2KitServerNotSetException(string message) : base(message)
        {
        }

        public Kinect2KitServerNotSetException(string message, Exception inner) : base(message, inner)
        {
        }
    }
}
