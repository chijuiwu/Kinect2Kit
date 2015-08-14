using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Microsoft.Samples.Kinect.BodyBasics
{
    /// <summary>
    /// Interaction logic for SetupKinect2KitServerDialog.xaml
    /// </summary>
    public partial class SetupKinect2KitServerDialog : Window
    {
        public SetupKinect2KitServerDialog(string address, int port)
        {
            InitializeComponent();
            // default
            this.entryIPAddress.Text = address;
            if (port == 0)
            {
                this.entryPort.Text = "8000";
            }
            else
            {
                this.entryPort.Text = port.ToString();
            }
        }

        private void OK_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = true;
        }
    }
}
