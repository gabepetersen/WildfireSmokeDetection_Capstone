   M S B A M L   `   `   `  ����L  HWildFireDetection, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null5clr-namespace:WildFireDetectionWildFireDetection  5   	   "    WildFireDetection.MainWindow   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   1localclr-namespace:WildFireDetection     5   	     � Title$  Wild Fire Smoke Detector��5   	    � WindowState$ Normal=�5	   	   $	��900��5
   	   $	��600��5   	   $	��900��5   	   $	��600��5   	    � 
ResizeMode$ CanResizeWithGrip=�5   	    � ShowInTaskbar$
 True��5   	    � SizeToContent$ Manual=�5   	   
���   �$��2q�5   	   .��5      �  � ShowGridLines$
 True��6    � ColumnDefinitions 5   
   �� 5      -   5         ��Name$ DisplayColumn��5      $��2* �66   6C   �� 5      -   5        $ ReportColumn��5      $	��300��66   $	��350��6F   6W   .+�5   
   � $��0��6   
�����w�.+�5      ]� .+�5      o� $	��Top=�6   
������ .@�5      m� $��Testing��6   $��16(�60   $��90��6>   
���   �$��1q�6]   $��5,5,5,5q�6q   
�������.@�5      m� -   5        $��Select Video��5   #   6X   m� 5      -   5        $��
Begin Test��5   #   6W   5      m� 5       $��Alert��6   $��16(�6.   $��90��6<   
���   �$��1q�6[   $��5,5,5,5q�6o   
�������.@�5!      m� $��Alerts Raised��6#   6<   m� 5"      $��Alert Options��6#   6<   5#      m� 5$      $��Options��6   $��16(�60   $��90��6>   
���   �$��1q�6]   $��5,5,5,5q�6q   
�������.@�5%      m� $��Search Training Data��6#   6C   m� 5&      $��Test Options��6#   6;   m� 5'      $��Report Options��6#   6=   5(      5)      (� 5*      -   5         (�Name$ 
previewBox��5*   2   	 (� Stretch$	 UniformToFill=�6   .��5+      r� -   5        
 r�Name$
 previewVideo��5+   #    r� Stretch$ UniformToFill=�69   5,      5-      5.      5/      � 50   
   $��1��6   
�������.+�51      ]� .+�52      �� $	��Top=�6   $��2q�6.   
���   �._�53      ��  �� TextAlignment$ Center=�6    $��Heavy"�67   $��30(�6J   B� 54      .�6(   	Reports61   55      56      �� 57      
���   �$��2 0 0 0q�6-   ._�58      �� -   5         ��Name$ 
reportList��58      
�������59      5:      5;      5<      5=      5>      