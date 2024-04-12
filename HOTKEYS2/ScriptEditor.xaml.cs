using System;
using System.Windows;
using System.Windows.Controls;
using Microsoft.Win32;

namespace HOTKEYS2
{
    public partial class ScriptEditor : UserControl
    {
        public ScriptEditor()
        {
            InitializeComponent();
        }

        private void SaveButton_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog
            {
                Filter = "Script files (*.ps1)|*.ps1|All files (*.*)|*.*",
                DefaultExt = "ps1"
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
}
