using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Windows;

namespace WildFireDetection
{
    public class ReportManager
    {
        // List of all the active reports in the system.
        private List<ReportFile> activeReports;

        // Constant for the name of the report folder.
        private const string reportFolder = "ActiveReports";
        // Constant for test file containing all report names.
        private const string reportFileName = "active_reports.txt";
        // Constant for directory that the reports are stored in.
        private string reportsDirectory;
        private string reportListDirectory;

        public ReportManager()
        {
            reportsDirectory = Directory.GetCurrentDirectory() + "\\" + reportFolder;
            reportListDirectory = reportsDirectory + "\\" + reportFileName;
            activeReports = new List<ReportFile>();
            loadAllReports();
        }

        public void addReport(ReportFile newReport)
        {
            activeReports.Add(newReport);

            using (StreamWriter fileStream = File.AppendText(reportListDirectory))
            {
                fileStream.WriteLine(newReport.FileName);
            }
        }

        public int NumberofReports
        {
            get { return activeReports.Count; }
        }

        public void openReport(string openRep)
        {
            foreach (var rep in activeReports)
            {
                if (openRep == rep.ReportName)
                {
                    rep.open();
                }
            }
        }

        public void deleteReport(string delRep)
        {
            MainWindow mainWindow = (MainWindow)System.Windows.Application.Current.MainWindow;
            File.Delete(reportListDirectory);
            mainWindow.reportList.Items.Clear();

            for (int i = 0; i < activeReports.Count; i++)
            {
                if (activeReports[i].ReportName == delRep)
                {
                    File.Delete(activeReports[i].FileDirectory);
                    activeReports.RemoveAt(i);
                }
            }


            using (StreamWriter fileStream = File.AppendText(reportListDirectory))
            {
                for (int i = 0; i < activeReports.Count; i++)
                {
                    fileStream.WriteLine(activeReports[i].FileName);
                    mainWindow.addListItem(activeReports[i].ReportName);
                }
            }
        }

        private void loadAllReports()
        {
            List<string> active = new List<string>();

            if(File.Exists(reportListDirectory))
            {
                string nextReport;
                System.IO.StreamReader reportList = new System.IO.StreamReader(reportListDirectory);

                while ((nextReport = reportList.ReadLine()) != null)
                {
                    active.Add(nextReport);
                }

                reportList.Close();

                System.IO.StreamReader currentReport;
                MainWindow mainWindow = (MainWindow)System.Windows.Application.Current.MainWindow;

                foreach (var report in active)
                {
                    currentReport = new System.IO.StreamReader(reportsDirectory + "\\" + report);

                    string[] headerInfo = new string[3];
                    for(int i = 0; i < 3; i++)
                    {
                        headerInfo[i] = currentReport.ReadLine();
                    }

                    currentReport.Close();

                    headerInfo[0] = headerInfo[0].Substring(12);
                    headerInfo[1] = headerInfo[1].Substring(6);
                    headerInfo[2] = headerInfo[2].Substring(6);

                    ReportFile newReport = new ReportFile(report, headerInfo);

                    if (!newReport.expiredReport())
                    {
                        activeReports.Add(newReport);
                        mainWindow.addListItem(newReport.ReportName);
                    }
                    else
                    {
                        File.Delete(newReport.FileDirectory);
                    }
                }

                File.Delete(reportListDirectory);

                using (StreamWriter fileStream = File.AppendText(reportListDirectory))
                {
                    for (int i = 0; i < activeReports.Count; i++)
                    {
                        fileStream.WriteLine(activeReports[i].FileName);
                    }
                }

            }
            else
            {
                System.IO.File.WriteAllText(reportListDirectory, "");
            }
        }

    }
}
