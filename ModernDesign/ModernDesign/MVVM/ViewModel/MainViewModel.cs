using ModernDesign.Core;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModernDesign.MVVM.ViewModel
{
    class MainViewModel : ObservableObject
    {
        public RelayCommand HomeViewCommand { get; set; }
        public RelayCommand CreateScripCommand { get; set; }

        public HomeViewModel HomeVm { get; set; }
        public CreateScripViewModel CreateScripView { get; set; }
        private object _CurrentView;

        public object CurrentView
        {
            get { return _CurrentView; }
            set {
                _CurrentView = value;
                OnPropertyChanged();
            }
        }

        public MainViewModel() { 
        
            HomeVm = new HomeViewModel();
            CreateScripView = new CreateScripViewModel();
            CurrentView = HomeVm;

            HomeViewCommand = new RelayCommand(o => CurrentView = HomeVm, o => true);


            CreateScripCommand = new RelayCommand(o => CurrentView = CreateScripView, o => true);

        }
    }
}
