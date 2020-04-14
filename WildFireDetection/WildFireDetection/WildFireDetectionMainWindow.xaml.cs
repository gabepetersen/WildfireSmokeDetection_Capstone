using System;
using System.Diagnostics;
using System.IO;
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
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;

namespace WildFireDetection
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    { 
        public string _testVideoPath = "";
        public ReportManager reportManager;

        public MainWindow()
        {
            InitializeComponent();

            reportManager = new ReportManager();
        }

        private void SelectDataMenu_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileSystem = new OpenFileDialog();
            openFileSystem.Multiselect = false;
            openFileSystem.InitialDirectory = @"C:\";
            openFileSystem.Filter = "Video Files (*.jpeg;*.mov;*.avi;*.mp4)|*.jpeg;*.mov;*.avi;*.mp4|All Files (*.*)|*.*";
            openFileSystem.Tag = "Video";
            openFileSystem.Title = "Select Video For Testing";

            Nullable<bool> fileSelected = openFileSystem.ShowDialog();

            if(fileSelected == true)
            {
                _testVideoPath = openFileSystem.FileName;
                Uri videoPath = new Uri(_testVideoPath);
                previewVideo.Source = videoPath;
            }
        }

        private void SelectBeginTest_Click(object sender, RoutedEventArgs e)
        {
            if(_testVideoPath != "")
            {
                TestingWindow openTestProgress = new TestingWindow();
                openTestProgress.ShowDialog();
            }
        }

        public void addListItem(string newReportName)
        {
            TextBlock newItem = new TextBlock();
            newItem.Text = newReportName;
            Thickness listMargin = new Thickness(5, 5, 5, 0);
            newItem.Margin = listMargin;
            newItem.FontSize = 16;

            ListBoxItem newListItem = new ListBoxItem();
            newListItem.Content = newItem;
            newListItem.AddHandler(ListBoxItem.MouseDoubleClickEvent, new MouseButtonEventHandler(openReportFile));
            newListItem.AddHandler(ListBoxItem.KeyDownEvent, new KeyEventHandler(deleteReportFile));
            reportList.Items.Add(newListItem);
        }

        private void deleteReportFile(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.D)
            {
                ListBoxItem reportListItem = reportList.SelectedItem as ListBoxItem;

                if (reportListItem != null)
                {
                    TextBlock listItem = reportListItem.Content as TextBlock;

                    reportManager.deleteReport(listItem.Text);
                }
            }
        }

        private void openReportFile(object sender, MouseButtonEventArgs e)
        {
            ListBoxItem reportListItem = e.Source as ListBoxItem;

            TextBlock listItem = reportListItem.Content as TextBlock;

            reportManager.openReport(listItem.Text);
        }
    }
}
