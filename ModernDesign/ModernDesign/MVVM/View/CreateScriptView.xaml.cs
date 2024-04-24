using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
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
using System.Windows.Navigation;
using System.Windows.Shapes;
using static System.Net.Mime.MediaTypeNames;

namespace ModernDesign.MVVM.View
{
    /// <summary>
    /// Interaction logic for CreateScriptView.xaml
    /// </summary>
    public partial class CreateScriptView : UserControl
    {
        public CreateScriptView()
        {
            InitializeComponent();
        }

        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            {
                SaveFileDialog saveFileDialog = new SaveFileDialog
                {
                    Filter = "Script files (*.txt)|*.txt|All files (*.*)|*.*",
                    DefaultExt = "txt"
                };
                if (saveFileDialog.ShowDialog() == true)
                {
                    try
                    {
                        System.IO.File.WriteAllText(saveFileDialog.FileName, ScriptTextBox.Text);
                        MessageBox.Show($"Script '{saveFileDialog.FileName}' saved.", "Info", MessageBoxButton.OK);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error saving script: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }
        private void run_cmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    MessageBox.Show(result);
                }
            }
        }

        private void CheckBox(object sender, RoutedEventArgs e)
        {

            //ScriptTextBox.Text 
            string path = $"C:/Users/joshu/Desktop/{fileName.Text}.txt";
            File.WriteAllText(path, ScriptTextBox.Text);

            run_cmd("C:/Users/joshu/Desktop/git/CapstoneRepo/CallFunctions.py", $"C:/Users/joshu/Desktop/{fileName.Text}.txt");
        }
    }
}



