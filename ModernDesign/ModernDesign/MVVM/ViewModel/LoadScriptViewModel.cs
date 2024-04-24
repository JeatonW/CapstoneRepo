using ModernDesign.Core;
using Microsoft.Win32;
using System.IO;

namespace ModernDesign.MVVM.ViewModel
{
    class LoadScriptViewModel : ObservableObject
    {
        private string _scriptContent;

        public string ScriptContent
        {
            get => _scriptContent;
            set
            {
                _scriptContent = value;
                OnPropertyChanged();
            }
        }

        public RelayCommand LoadScriptCommand { get; set; }

        public LoadScriptViewModel()
        {
            LoadScriptCommand = new RelayCommand(o => LoadScript());
        }

        private void LoadScript()
        {
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Script files (*.txt;*.cs;*.js)|*.txt;*.cs;*.js|All files (*.*)|*.*",
                DefaultExt = "txt"
            };

            if (openFileDialog.ShowDialog() == true)
            {
                ScriptContent = File.ReadAllText(openFileDialog.FileName);
            }
        }
    }
}
