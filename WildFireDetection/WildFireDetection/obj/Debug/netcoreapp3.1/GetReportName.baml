   M S B A M L   `   `   `  ����L  HWildFireDetection, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null5clr-namespace:WildFireDetectionWildFireDetection  5   	   %    WildFireDetection.GetReportName   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   1localclr-namespace:WildFireDetection     5   	     � Title$   ��5   	    � Topmost$
 True��5	   	    � WindowStyle$
 None=�5
   	   $	��150��5   	   $	��300��5   	    � 
ResizeMode$ NoResize=�5   	    � ShowInTaskbar$ False��5   	    � WindowStartupLocation$ CenterOwner=�5   	    � SizeToContent$ Manual=�5   	   $��4q�5   	   
����  �
�������.��5      �  � RowDefinitions 5   
   �� 5      6   �� 5      6   �� 5      6   �� 5      6   .+�5   
   � $��0��6   $��2 2 2 0q�6   .+�5      �� $��Center=�6   $��18(�65   �� 5      .�6   Test Successful6(   5      5       � 5!   
   $��1��6   $��
 10 2 10 2q�6   .+�5"      �� *(Please enter a name for the report file:5$      5%      � 5&   
   $��2��6   $��
 10 2 10 2q�6   .+�5'      �� -   5         ��Name$ reportTextBox��5'      
���   �.��6�   5(      5)      � 5*   
   $��3��6   $��
 50 2 50 2q�6   .+�5+      �� -   5        	 ��Name$	 reportSubmit��5+      $��Submit��6+   
�������
���   �$
{�True��6g   5,      5-      5.      5/      