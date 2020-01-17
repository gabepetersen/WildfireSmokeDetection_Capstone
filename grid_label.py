# grid_label.py
# Gabe Petersen
# 13 Jan 2020
# To go thru a frame of a video and label each section as having smoke or not

# for a image of 480x270, 16 boxes in width and 9 in height will result in grid squares of 30 pixels each

import cv2
import keyboard
import argparse
import sys
import numpy as np

# declare a 2d array and initialize all entries to 0
smoke_regions = [[0 for x in range(9)] for y in range(16)]

# reads in a video using opencv's VideoCapture object
def read_video(filename):
    # Create a VideoCapture object and read from input file
    video = cv2.VideoCapture(filename)

    # Check if video opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")
    else:
        # return video
        return video

# redraws the data structure onto the image for visual clarification
def redrawBoxes(curr_frame):
    frame_copy = curr_frame.copy()
    # go thru the smoke_regions and draw rectangles on the frame copy
    for x in range(0, 16):
        for y in range(0, 9):
            if smoke_regions[x][y] == 255:
                xcord = x * 120
                ycord = y * 120
                frame_copy = cv2.rectangle(frame_copy, (xcord, ycord), (xcord+120, ycord+120), (0,255,0), 2)

    return frame_copy


# event handler for mouseclicking
def click_box(event, x, y, flags, param):
    # mouse was clicked and region is selected
    if event == cv2.EVENT_LBUTTONDOWN:
        # see what box in the data structure
        gridX = int(x / 120)
        gridY = int(y / 120)
        #print("Here is the coordinates you chose yo!  " + str(gridX) + ", " + str(gridY))

        # change between 0 and 255 depending on previous state
        if(smoke_regions[gridX][gridY] == 0):
            smoke_regions[gridX][gridY] = 255
        else:
            smoke_regions[gridX][gridY] = 0

# main function responsible for displaying frames and saving user inputted data
def grid_label(dataInputPath, videoCount):
    # create a VideoCapture object
    video = read_video(dataInputPath)
    # create a video writer for smoke_regions
    dataPath = 'GridDataResults/' + str(videoCount) + '.mov'
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    videoWrite = cv2.VideoWriter(dataPath, fourcc, 10, (16, 9), False)

    # start the frame sequence
    frame_sequence(video, videoWrite)

    # release the video read and write
    video.release()
    videoWrite.release()
    cv2.destroyAllWindows()

# goes thru video sequence and displays frames
def frame_sequence(video, videoWrite):
    # go through each of the frames
    frame_count = 0
    done = False
    while not done:
        frame_count += 1
        ret, curr_frame = video.read()
        frame_copy = redrawBoxes(curr_frame)

        # set event handler for mouseclick
        cv2.namedWindow("Current Frame")
        cv2.setMouseCallback("Current Frame", click_box)

        # displays the image and waits for clicks, next frame, or quit
        while True:
            # display the image
            cv2.imshow("Current Frame", frame_copy)
            key = cv2.waitKey(1) & 0xFF

            frame_copy = curr_frame.copy()
            # go thru the smoke_regions and redraw smoke_regions from previous frame
            for x in range(0, 16):
                for y in range(0, 9):
                    if smoke_regions[x][y] == 255:
                        xcord = x * 120
                        ycord = y * 120
                        frame_copy = cv2.rectangle(frame_copy, (xcord, ycord), (xcord+120, ycord+120), (0,255,0), 2)

            if key == ord("n"):
                # write the current data structure to the output video
                region_data = np.uint8(smoke_regions)
                # rotate and flip bc my code sucks haha
                region_data = cv2.flip(region_data, 1)
                region_data = cv2.rotate(region_data, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # resize for video sanity check
                region_data = cv2.resize(region_data, (16, 9))
                # write frame to movie
                videoWrite.write(region_data)
                break
            if key == ord("q"):
                # exit the program
                done = True
                break

if __name__ == "__main__":
    # get the video count from command line
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--number", required=True, help="Video Number in Data Folder")
    args = vars(ap.parse_args())

    videoCount = args["number"]

    dataInputPath = "Data/" + videoCount + ".mp4"
    print("From video file: " + dataInputPath)
    # start grid label sequence
    print("Instructions:")
    print("   - while on the image feed, click to select and unselect sections of smoke")
    print("   - after selection is made, hit n to write to file and go to next frame")
    print("   - hit q any time to quit while on the video")
    grid_label(dataInputPath, videoCount)
