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
    public partial class TestingWindow : Window
    {
		public string newReportName;

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
			MainWindow mainWindow = (MainWindow)System.Windows.Application.Current.MainWindow;

			ReportFile newReport = new ReportFile(System.IO.Path.GetFileName(mainWindow._testVideoPath));

			GetReportName reportNameWindow = new GetReportName(newReport.ReportName);
			reportNameWindow.ShowDialog();

			newReport.ReportName = reportNameWindow.NewReportName;

			newReport.writeTextFileHeader(System.IO.Path.GetFileName(mainWindow._testVideoPath));
			mainWindow.addListItem(newReport.ReportName);
			mainWindow.reportManager.addReport(newReport);
		}


	}
}
