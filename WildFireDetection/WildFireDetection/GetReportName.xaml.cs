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
    /// Interaction logic for GetReportName.xaml
    /// </summary>
    public partial class GetReportName : Window
    {
        private string newReportName;
        private bool textCorrect;

        public GetReportName(string fileName)
        {
            InitializeComponent();

            reportTextBox.Text = fileName;
            textCorrect = true;
        }

        private void reportSubmit_Click(object sender, RoutedEventArgs e)
        {
            if(textCorrect)
            {
                newReportName = reportTextBox.Text;
                this.Close();
            }
            else
            {
                MessageBox.Show("Invalid Charater in the report name. Cannot contain | * & / | ? \\ : ");
            }
        }

        public string NewReportName
        {
            get { return newReportName; }
        }

        private void reportTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            string newText = reportTextBox.Text;

            if(newText.Contains('<') || newText.Contains('>') || newText.Contains(':') ||
                newText.Contains('"') || newText.Contains('/') || newText.Contains('\\') ||
                newText.Contains('|') || newText.Contains('?') || newText.Contains('*'))
            {
                reportTextBox.Background = new SolidColorBrush(Colors.Red);
                textCorrect = false;
            }
            else
            {
                reportTextBox.Background = new SolidColorBrush(Colors.White);
                textCorrect = true;
            }
        }

        private void reportTextBox_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            reportTextBox.SelectAll();
        }

        private void reportTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.Key == Key.Enter)
            {
                reportSubmit_Click(sender, e);
            }
        }
    }
}
