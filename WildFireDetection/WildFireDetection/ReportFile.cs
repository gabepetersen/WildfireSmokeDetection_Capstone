/*
 * Class Name: ReportFile
 * Namespace: WildFireDetection
 * Author: William Williams
 * Date Created: 4/5/2020
 * 
 * Purpose: Keep Details for an Individual Report
 * 
 * Fields (get only):
 *      -FileName: The name of the report file in the file system (ReportName + ".txt")
 *      -FileDirectory: The directory that the report file is stored in.
 *      -ReportName: The name of the report file that appears in the application.
 */


using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace WildFireDetection
{
    public class ReportFile
    {
        // Variables to store the name of the file, report, and directory
        // the report is stored in.
        private string fileName;
        private string reportName;
        private string videoName;
        private string fileDirectory;

        // Number of days that the report shall be active before deleted.
        private double expiration;

        // Stores the date and time that the report was created on.
        private DateTime createdOnDate = new DateTime();
        // Stores the date and time that the report expires.
        private DateTime expirationDate = new DateTime();

        // Constant for the name of the report folder.
        private const string reportFolder = "ActiveReports";

        /* Funtion Name: ReportFile()
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Constructor for the class, will initialize the variables
         *          by determing the current working directory and the current
         *          date and time that the report was created for its name.
         * Arguments:
         *          - int exp : Number of days before report is deleted, default is 1.
         */
        public ReportFile(string vname, int exp = 1)
        {
            expiration = exp;
            videoName = vname;
            fileName = vname.Remove(vname.LastIndexOf(".")) + ".txt";
            reportName = fileName.Remove(fileName.LastIndexOf("."));
            fileDirectory = Directory.GetCurrentDirectory() + "\\" + reportFolder + "\\" + fileName;
            createdOnDate = DateTime.Now;
            expirationDate = createdOnDate.AddDays(expiration);
        }

        public ReportFile(string fName, string [] reportInfo, int exp = 1)
        {
            expiration = exp;
            fileName = fName;
            reportName = fileName.Remove(fileName.LastIndexOf(".txt"));
            videoName = reportInfo[0];
            createdOnDate = DateTime.Parse(reportInfo[1] + " " + reportInfo[2]);
            expirationDate = createdOnDate.AddDays(expiration);
            fileDirectory = Directory.GetCurrentDirectory() + "\\" + reportFolder + "\\" + fileName;
        }

        /* Funtion Name: ReportFile(ReportFile other)
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Copy constructor for the class, will initialize the variables
         *          by setting them to the variables of the 'other' report file
         *          sent in as an argument.
         */
        public ReportFile(ReportFile other)
        {
            fileName = other.FileName;
            fileDirectory = other.FileDirectory;
            reportName = other.ReportName;
            createdOnDate = other.createdOnDate;
            expirationDate = other.expirationDate;
        }

        /* Funtion Name: FileName
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Accessors function fileName variable.
         */
        public string FileName
        {
            get { return fileName; }
        }

        /* Funtion Name: FileDirectory
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Accessors function fileDirectory variable.
         */
        public string FileDirectory
        {
            get { return fileDirectory; }
        }

        /* Funtion Name: ReportName
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Accessor function reportName variable.
         */
        public string ReportName
        {
            get { return reportName; }
            set { reportName = value;
                fileName = reportName + ".txt";
                fileDirectory = Directory.GetCurrentDirectory() + "\\" + reportFolder + "\\" + fileName;
            }
        }

        public string VideoName
        {
            get { return videoName; }
        }

        /* Funtion Name: getDateTime()
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Accessors function for createdOnDate, returns the Date object
         *          as a string object in the format "Month/Day/Hour Hour:Minute:Seconds AM|PM".
         */
        public string getDateTime()
        {
            return createdOnDate.ToString();
        }

        /* Funtion Name: expiredReport()
         * Author: William Williams
         * Date: 4/5/2020
         * Purpose: Returns true if the report is expired, false if still active.
         */
        public bool expiredReport()
        {
            // Get current date and time.
            DateTime currentTime = DateTime.Now;

            // Compare current date/time to expiration date/time
            if(currentTime <= expirationDate)
            {
                // If not past expiration date, return false.
                return false;
            }
            else
            {
                // If past expiration date, return true.
                return true;
            }
        }

        /* Funtion Name: open()
         * Author: William Williams
         * Date: 4/8/2020
         * Purpose: Open the report file in a new window.
         */
        public void open()
        {
            // Prepare the report file window and show it to the user.
            OpenReportFile openReport = new OpenReportFile(this);
            openReport.Show();
        }

        public void writeTextFileHeader(string vidName)
        {
            string[] headerInfo = { "Video Name: " + vidName,
                                    "Date: " + createdOnDate.ToShortDateString(),
                                    "Time: " + createdOnDate.ToLongTimeString()};

            System.IO.File.WriteAllLines(fileDirectory, headerInfo);
        }

    }
}
