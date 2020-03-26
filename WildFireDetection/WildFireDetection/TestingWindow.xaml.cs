using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.ComponentModel;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace WildFireDetection
{
    /// <summary>
    /// Interaction logic for TestingWindow.xaml
    /// </summary>
    public partial class TestingWindow : Window
    {
        public TestingWindow()
        {
            InitializeComponent();

            BackgroundWorker workerProgress = new BackgroundWorker();
            workerProgress.WorkerReportsProgress = true;
            workerProgress.DoWork += workerProgress_DoWork;
            workerProgress.ProgressChanged += workerProgress_ProgressChanged;
            workerProgress.RunWorkerCompleted += workerProgress_RunWorkerCompleted;
            workerProgress.RunWorkerAsync(100);
        }

		void workerProgress_DoWork(object sender, DoWorkEventArgs e)
		{
			int max = (int)e.Argument;
			int result = 0;
			for (int i = 0; i < (max + 1); i++)
			{
				(sender as BackgroundWorker).ReportProgress(i);
				System.Threading.Thread.Sleep(100);
			}
			e.Result = result;
		}

		void workerProgress_ProgressChanged(object sender, ProgressChangedEventArgs e)
		{
			testProgressBar.Value = e.ProgressPercentage;
		}

		void workerProgress_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
		{
			this.Close();

			DateTime reportDate = DateTime.Now;
			TextBlock newItem = new TextBlock();
			string dateTime = reportDate.ToString() + ".txt";
			string reportName = dateTime.Replace(" ", "_");
			reportName = reportName.Replace(":", "-");
			reportName = reportName.Replace("/", "-");
			newItem.Text = reportName;
			Thickness listMargin = new Thickness(5, 5, 5, 0);
			newItem.Margin = listMargin;
			newItem.FontSize = 14;

			MessageBox.Show("Test Ran Succesfully...Report File Created " + reportName);

			MainWindow mainWindow = (MainWindow)System.Windows.Application.Current.MainWindow;
			mainWindow.addListItem(newItem);

			string currentDirectory = Directory.GetCurrentDirectory();

			System.IO.File.WriteAllText((currentDirectory + "\\" + reportName), System.IO.Path.GetFullPath(mainWindow._testVideoPath));
		}


	}
}
