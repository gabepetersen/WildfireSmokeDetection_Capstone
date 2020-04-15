# model_gabe_test.py
# 14 Apr 2020
# Test the model that is trained seperately

##
##  TO RUN:
##  python3 keras_model_v2_test.py test_video.mp4
##

import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
# keras imports
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
from keras import backend as K 
from keras.models import load_model
from keras.utils.vis_utils import plot_model


# reads in a video using opencv's VideoCapture object
def read_video(filename):
    # Create a VideoCapture object and read from input file
    # ZB Edit: was getting exceptions when trying to open video so used full directory name
    string = os.getcwd()
    video = cv2.VideoCapture(string + '/' + filename)
    # End ZB Edits
    # Check if video opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")
        return None
    else:
        # return video
        return video

# ------ from model.py ---------
# iterate through frames of a video and call model.predict on each cell in a 16x9 grid
# if smoke is identified then draw a green box on the cell, else draw red box
# @params:
# model - trained CNN model used to predict smoke results of grids
# video - test video to run the network on
# @returns:
# nothing - displays results of grid calculation on local machine.
def grid_contour(model, video):
    done = False
    while not done:
        ret, curr_frame = video.read()
        if not ret:
            break
        else:
            # cv2.imshow("CurrentFrame", frame_copy)
            frame_copy = curr_frame.copy()
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                done = True
                break
            for x in range(0, 16):
                for y in range(0, 9):
                    xg = x * 120
                    yg = y * 120
                    grid_segment = curr_frame[yg:yg + 120, xg:xg + 120]
                    # resize and reshape the grid segment
                    grid_segment = cv2.resize(grid_segment,(120, 120))
                    grid_segment = np.reshape(grid_segment,[1,120,120,3])
                    # predict the class
                    classes = model.predict_classes(grid_segment)
                    # get the class number
                    max_index = classes[0][0]
                    # edit the squares to be a pixel in
                    start = (xg + 1, yg + 1)
                    end = (xg + 119, yg + 119)
                    if max_index == 1:
                        color = (0, 255, 0)
                        frame_copy = cv2.rectangle(frame_copy, start, end, color, 1)
                    else:
                        color = (0, 0, 255)
                        frame_copy = cv2.rectangle(frame_copy, start, end, color, 2)
            cv2.imshow("CurrentFrame", frame_copy)

if __name__ == '__main__':
  # get the model from training program
  model = load_model('model_saved.h5')

  model.compile(loss='binary_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])
  
  # print the model summary
  print(model.summary())

  # check that a video is passed in
  if(len(sys.argv) > 1):
    video = read_video(sys.argv[1])
    grid_contour(model, video)
    
  else:
    print("error: pass in the filepath of the video you want to test")

