using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
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
    public partial class CreateScriptView : UserControl{
        
        public CreateScriptView(){
            InitializeComponent();
        }

        //A button Control that will open the file explorer and capture the text box and save it all in txt.
        private void SaveButton_Click(object sender, RoutedEventArgs e){
            {
                SaveFileDialog saveFileDialog = new SaveFileDialog{
                    Filter = "Script files (*.txt)|*.txt|All files (*.*)|*.*",
                    DefaultExt = "txt"
                };
                if (saveFileDialog.ShowDialog() == true){
                    try{
                        System.IO.File.WriteAllText(saveFileDialog.FileName, ScriptTextBox.Text);
                        MessageBox.Show($"Script '{saveFileDialog.FileName}' saved.", "Info", MessageBoxButton.OK);
                    }
                    catch (Exception ex){
                        MessageBox.Show($"Error saving script: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }

        //a helper function used to run python scripts
        private void run_cmd(string cmd, string args){
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.CreateNoWindow = true;
            using (Process process = Process.Start(start)){
                using (StreamReader reader = process.StandardOutput){
                    string result = reader.ReadToEnd();
                    MessageBox.Show(result);
                }
            }
        }

        //a helper function that temporarly saves the text box  and send it to a helper python script to verifiy correct compilation and then deletes the file 
        private void CheckBox(object sender, RoutedEventArgs e){
            string path = $"C:/Users/hager/temp.txt";
            File.WriteAllText(path, ScriptTextBox.Text);
            run_cmd("C:/Users/hager/Documents/GitHub/CapstoneRepo/CallFunctions.py", $"C:/Users/hager/Documents/temp.txt");
            File.Delete(path);

        }
    }
}



