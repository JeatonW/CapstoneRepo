using ModernDesign.Core;
using System;
using System.IO; // For reading files
using Microsoft.Win32; // For OpenFileDialog
using System.ComponentModel; // This is usually part of your ObservableObject base class

namespace ModernDesign.MVVM.ViewModel
{
    class MainViewModel : ObservableObject
    {
        private object _currentView;
        private string _scriptContent; // Property to store the loaded script

        public RelayCommand HomeViewCommand { get; set; }
        public RelayCommand CreateScripCommand { get; set; }
        public RelayCommand LoadScriptCommand { get; set; } // Command to load a script

        public string ScriptContent
        {
            get => _scriptContent;
            set
            {
                _scriptContent = value;
                OnPropertyChanged();
            }
        }

        public HomeViewModel HomeVm { get; set; }
        public CreateScripViewModel CreateScripView { get; set; }

        public object CurrentView
        {
            get => _currentView;
            set
            {
                _currentView = value;
                OnPropertyChanged();
            }
        }

        public MainViewModel()
        {
            HomeVm = new HomeViewModel();
            CreateScripView = new CreateScripViewModel();
            CurrentView = HomeVm;

            HomeViewCommand = new RelayCommand(o => CurrentView = HomeVm, o => true);
            CreateScripCommand = new RelayCommand(o => CurrentView = CreateScripView, o => true);
            LoadScriptCommand = new RelayCommand(o => LoadScript(), o => true);

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
