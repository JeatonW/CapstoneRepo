using System.Windows;
using System.Windows.Media;
using Microsoft.Win32;

namespace HOTKEYS2
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            UpdateTheme(true); 
        }

        private void CreateScript_Click(object sender, RoutedEventArgs e)
        {
            var scriptEditorWindow = new Window
            {
                Content = new ScriptEditor(),
                SizeToContent = SizeToContent.WidthAndHeight,
                WindowStartupLocation = WindowStartupLocation.CenterScreen
            };
            scriptEditorWindow.ShowDialog();
        }

        private void LoadScript_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Script files (*.ps1)|*.ps1|All files (*.*)|*.*"
            };
            if (openFileDialog.ShowDialog() == true)
            {
                string fileContent = System.IO.File.ReadAllText(openFileDialog.FileName);
                MessageBox.Show("Script loaded.", "Info", MessageBoxButton.OK);
            }
        }

        private void LightMode_Checked(object sender, RoutedEventArgs e)
        {
            UpdateTheme(false);
        }

        private void LightMode_Unchecked(object sender, RoutedEventArgs e)
        {
            UpdateTheme(true);
        }

        private void UpdateTheme(bool isDarkMode)
        {
            Resources["AppBackground"] = new SolidColorBrush(isDarkMode ? Color.FromRgb(45, 45, 48) : Colors.White);
            Resources["AppForeground"] = new SolidColorBrush(isDarkMode ? Colors.White : Colors.Black);
        }
    }
}
