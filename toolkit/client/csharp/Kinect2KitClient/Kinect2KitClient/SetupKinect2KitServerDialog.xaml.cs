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
        public SetupKinect2KitServerDialog()
        {
            InitializeComponent();
            this.valServerAddress.Text = "localhost";
            this.valServerPort.Text = "8000";
        }

        private void OK_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = true;
        }
    }
}
