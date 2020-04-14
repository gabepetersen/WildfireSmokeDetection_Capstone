using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
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
    /// Interaction logic for OpenReportFile.xaml
    /// </summary>
    public partial class OpenReportFile : Window
    {
        public OpenReportFile(ReportFile rf)
        {
            InitializeComponent();
            this.Title = rf.ReportName;

            Paragraph paragraph = new Paragraph();
            paragraph.Inlines.Add(System.IO.File.ReadAllText(rf.FileDirectory));
            FlowDocument document = new FlowDocument(paragraph);
            reportReader.Document = document;
        }
    }
}
