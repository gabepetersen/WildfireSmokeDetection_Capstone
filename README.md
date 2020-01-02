# WildfireSmokeDetection_Capstone
A capstone project for team 24 to develop a wildfire smoke detection algorithm that incorporates time-based learning and smoke density recognition.

# The Team
Zachary Black

Gabe Petersen

William Williams

# To Do List

- Revise image preprocessing code to get rid of blurry, camera shake, and unneccessary frames via optical flow

- Modify database to operate on a cloud based service like AWS

- Preprocess videos and put on database

- Design program to, frame-by-frame, identify and label regions containing smoke based on computer vision techniques (optical flow, image segmentation, etc...)
  - option 1: use optical flow to identify where the main motion is in the image (hopefully only smoke since blurry and camera shake frames are already thrown out).
  - option 2: use image color intensity to determine what portions of the image are the most greyish and out of place (probably wont work for night time photos)
  - option 3: try to segment out background by other factors (blurriness, noiseyness, etc...)

- Design program to verify with user if the previous program identified the regions correctly (no false positives or negatives for each region)

- After data is totally preprocessed and given correct labels, put into database under seperate table

- Divide into convolutions (possibly on regions, filtered frames, etc...)

- train network

# Ideas for Design

# Ideas for Engineering

