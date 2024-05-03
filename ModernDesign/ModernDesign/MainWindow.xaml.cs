using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;
using System.Windows.Input;

namespace ModernDesign{
    public partial class MainWindow : Window{
        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        //key modifiers
        private const int MOD_NONE = 0x0000;
        private const int MOD_ALT = 0x0001;
        private const int MOD_CONTROL = 0x0002;
        private const int MOD_SHIFT = 0x0004;
        private const int MOD_WIN = 0x0008;

        private const int WM_HOTKEY = 0x0312;

        private CancellationTokenSource cancellationTokenSource;
        private List<int> hotkeyIds = new List<int>();
        private NotifyIcon _notifyIcon;

        public MainWindow(){
            InitializeComponent();
            _notifyIcon = new NotifyIcon();
        }
       
            
            //this function will take the file of hotkeys that are on each line, 
            private void getkeys(){
            //change this to the location you decide in the WriteForC#
            string[] file = File.ReadAllLines("C:/Users/joshu/Desktop/cSharp.txt");
            List<string> lines = new List<string>();
            List<List<int>> keys = new List<List<int>>();
            foreach (string line in file){
                List<int> key = new List<int>();
                string[] parts = line.Split('+');
                foreach (string part in parts){
                    if (part == "left ctrl" || part =="right ctrl" ){key.Add(MOD_CONTROL);}
                    else if (part == "left shift" || part == "right shift"){key.Add(MOD_SHIFT);}
                    else if (part =="left alt" || part == "right alt"){key.Add(MOD_ALT);}
                    else{char character = part.ToCharArray()[0]; key.Add(((byte)character));}
                }
                keys.Add(key);
                lines.AddRange(parts);
            }
            int i = 1;
            foreach(List<int> hotkey in keys){
                bool success;
                if (hotkey.Count > 2){
                    success = RegisterHotKey(IntPtr.Zero, i, hotkey[0] | hotkey[1], hotkey[2]-32);
                }
                else{
                    success = RegisterHotKey(IntPtr.Zero, i, hotkey[0], hotkey[1]-32);
                }
                
                if (success){
                    hotkeyIds.Add(i);
                }
                else{
                    System.Windows.MessageBox.Show("failed to regiseter keys");
                }
                i++;
            }
        }

        protected override void OnClosed(EventArgs e)
        {
            base.OnClosed(e);
            UnregisterHotKeys();
            _notifyIcon.Dispose();
            _notifyIcon = null;
            
            
        }

        private void UnregisterHotKeys(){
            foreach (var id in hotkeyIds){
                UnregisterHotKey(IntPtr.Zero, id);
            }
            hotkeyIds.Clear();
        }


        //controls the top bar of the frame
        private void DragWithHeader(object sender, MouseButtonEventArgs e){
            if (e.ChangedButton == System.Windows.Input.MouseButton.Left)
                DragMove();
        }

        //controls the close button
        private void CloseButton_Click(object sender, RoutedEventArgs e){
            Close();
            
        }

        //controls the minimize button
        private void Minimize_Click(object sender, RoutedEventArgs e){
            this.WindowState = WindowState.Minimized;
        }

        //will open the file dialog window and let you select the file and it will be then sent to our program,
        //it will then be launched with out hotkey program.
        private async void loadScript(object sender, RoutedEventArgs e){
            Microsoft.Win32.OpenFileDialog openFileDialog = new Microsoft.Win32.OpenFileDialog
            {
                Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*",
                DefaultExt = "txt",
                Title = "Open Script File"
            };




            if (openFileDialog.ShowDialog() == true){
                try{
                    string filePath = openFileDialog.FileName;
                    string fileContent = File.ReadAllText(filePath);



                    _notifyIcon = new NotifyIcon();
                    _notifyIcon.Icon = new System.Drawing.Icon("C:/Users/joshu/Documents/GitHub/CapstoneRepo/ModernDesign/ModernDesign/Resources/Logo.ico");
                    _notifyIcon.Text = "IDE Hotkeys";
                    _notifyIcon.Visible = true;

                    _notifyIcon.ContextMenuStrip = new ContextMenuStrip();
                    _notifyIcon.ContextMenuStrip.Items.Add("Stop Lisiner",null,CancelProcessButton);

                    cancellationTokenSource = new CancellationTokenSource();
                    await run_cmd("C:/Users/joshu/Documents/GitHub/CapstoneRepo/WriteForC#.py", filePath, cancellationTokenSource.Token); //use the path to your local py file is 
                    getkeys();


                    await run_cmd("C:/Users/joshu/Documents/GitHub/CapstoneRepo/WindowKeyBlocker.py", filePath, cancellationTokenSource.Token); //use the path to local py file
                    UnregisterHotKeys();//MessageBox.Show("keys unregistered");
                }
                catch (Exception ex){
                    System.Windows.MessageBox.Show("Error reading file: " + ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }


        private void CancelProcessButton(object sender, EventArgs e)
        {
            System.Windows.MessageBox.Show("in cancelation fucntion");
            cancellationTokenSource?.Cancel();
            
        }

        //this function will take in a program and any arguemtns to run on the cmd line
        //we run it through python and throuh the shell, we also capture the stout and hide the cmd window
        private async Task run_cmd(string cmd, string args, CancellationToken cancellationToken){  
            try{
                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = "python";
                start.Arguments = string.Format("{0} {1}", cmd, args);
                start.UseShellExecute = false;
                start.RedirectStandardOutput = true;
                start.CreateNoWindow = false;
                using (Process process = Process.Start(start))
                {
                    using (StreamReader reader = process.StandardOutput)
                    {
                        string result = await reader.ReadToEndAsync();
         
                        //await reader.ReadToEndAsync();
                    }
                }
                
            } 
            catch (OperationCanceledException){
                System.Windows.MessageBox.Show("HotKeys have stopped");
            }
        }

    }
}
