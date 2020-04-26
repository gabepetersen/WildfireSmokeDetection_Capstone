# grid_label.py
# Gabe Petersen
# 21 Jan 2020
# version 1.5
# Go thru a frame-by-frame of a video and label regions of the frame as having smoke or not

# for an image of 480x270, 16 boxes in width and 9 in height will result in grid squares of 30x30 pixels
# for an image of 1920x1080, 16 boxes in width and 9 in height will result in grid squares of 120x120 pixels

import cv2
import keyboard
import argparse
import sys
import os
import numpy as np

# declare a 2d array and initialize all entries to 0
smoke_regions = [[0 for x in range(9)] for y in range(16)]


# reads in a video using opencv's VideoCapture object
def read_video(filename):
    # Create a VideoCapture object and read from input file
    # ZB Edit: was getting exceptions when trying to open video so used full directory name
    string = os.getcwd()
    video = cv2.VideoCapture(string + filename)
    # End ZB Edits
    # Check if video opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")
        return None
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
                frame_copy = cv2.rectangle(frame_copy, (xcord, ycord), (xcord + 120, ycord + 120), (0, 255, 0), 2)

    return frame_copy


# event handler for mouseclicking
def click_box(event, x, y, flags, param):
    # mouse was clicked and region is selected
    if event == cv2.EVENT_LBUTTONDOWN:
        # see what box in the data structure
        gridX = int(x / 120)
        gridY = int(y / 120)
        # print("Here is the coordinates you chose yo!  " + str(gridX) + ", " + str(gridY))

        # change between 0 and 255 depending on previous state
        if (smoke_regions[gridX][gridY] == 0):
            smoke_regions[gridX][gridY] = 255
        else:
            smoke_regions[gridX][gridY] = 0


# main function responsible for displaying frames and saving user inputted data
def grid_label(dataInputPath, videoCount):
    # create a VideoCapture object
    video = read_video(dataInputPath)
    vidName = dataInputPath[32:]
    if video is not None:
        # create a video writer for smoke_regions
        dataPath = 'GridDataResults/' + vidName + '.mov'

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        videoWrite = cv2.VideoWriter(dataPath, fourcc, 10, (16, 9), False)

        # start the frame sequence
        frame_sequence(video, videoWrite, videoCount, vidName)

        # release the video read and write
        video.release()
        videoWrite.release()
        cv2.destroyAllWindows()


# ZB EDIT to place individual grids in videos
def create_smoke_video(vidName):
    # ZB EDIT to place individual grids in videos
    fc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = 120
    frame_height = 120
    frame_name = 'FrameExtractor/ImageSegments/Smoke/' + vidName
    size = (int(frame_width), int(frame_height))
    smokeVideo = cv2.VideoWriter(frame_name, fc, 10, size)
    return smokeVideo
# ZB End edits


# ZB EDIT to place individual grids in videos
def create_nonsmoke_video(vidName):
    fc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = 120
    frame_height = 120
    nframe_name = 'FrameExtractor/ImageSegments/NoSmoke/' + vidName
    size = (int(frame_width), int(frame_height))
    noSmokeVideo = cv2.VideoWriter(nframe_name, fc, 10, size)
    return noSmokeVideo
# ZB End edits


# goes thru video sequence and displays frames
# Warning: This function is dreadfully long, sorry y'all
def frame_sequence(video, videoWrite, videoCount, vidName):
    # declare boolean pause/play conditi
    vidPlay = False
    # go through each of the frames
    frame_count = 0
    done = False
    noSmokeVideo = create_nonsmoke_video(vidName)
    smokeVideo = create_smoke_video(vidName)
    while not done:
        frame_count += 1
        ret, curr_frame = video.read()
        if not ret:
            done = True
            break
        frame_copy = redrawBoxes(curr_frame)
        # set event handler for mouseclick
        cv2.namedWindow("Current Frame")
        cv2.setMouseCallback("Current Frame", click_box)
        # displays the image and waits for clicks, next frame, or quit
        while True and ret:
            # display the image
            cv2.imshow("Current Frame", frame_copy)
            key = cv2.waitKey(1) & 0xFF

            # make copy of current frame
            frame_copy = curr_frame.copy()
            # go thru the smoke_regions and redraw smoke_regions onto copy
            for x in range(0, 16):
                for y in range(0, 9):
                    if smoke_regions[x][y] == 255:
                        xcord = x * 120
                        ycord = y * 120
                        frame_copy = cv2.rectangle(frame_copy, (xcord, ycord), (xcord + 120, ycord + 120), (0, 255, 0),
                                                   2)

            # next frame function
            if key == ord("n"):
                # write the current data structure to the output video
                region_data = np.uint8(smoke_regions)
                # rotate and flip 2d array bc I dont want to redo the code because I am lazy ok
                region_data = cv2.flip(region_data, 1)
                region_data = cv2.rotate(region_data, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # resize for video compatibility sanity check
                region_data = cv2.resize(region_data, (16, 9))
                break
            # clear the squares function
            if key == ord("c"):
                frame_copy = curr_frame.copy()
                for x in range(0, 16):
                    for y in range(0, 9):
                        smoke_regions[x][y] = 0
            # pause/play functionality
            if key == ord("p"):
                if vidPlay:
                    vidPlay = False
                else:
                    vidPlay = True
            # quit the program function
            if key == ord("q"):
                # exit the program
                done = True
                break
            # break loop if vidPlay is True
            if vidPlay:
                break
        # if the program isnt done, write data
        if not done:
            # write frame to movie
            videoWrite.write(region_data)
            imageDataPath = 'FrameExtractor/ImageSegments/'
            # write image frames for convolutions
            for x in range(0, 16):
                for y in range(0, 9):
                    # edit file names based on whether there is smoke or not in the frame
                    if smoke_regions[x][y] == 255:
                        imageDataPath = 'FrameExtractor/ImageSegments/Smoke/' + str(videoCount) + '_' + str(
                            frame_count) + '_' + str(x) + '_' + str(y) + '_' + str(1) + '.jpg'
                    else:
                        imageDataPath = 'FrameExtractor/ImageSegments/NoSmoke/' + str(videoCount) + '_' + str(
                            frame_count) + '_' + str(x) + '_' + str(y) + '_' + str(0) + '.jpg'
                    # crop all the grid squares and save them as images
                    xg = x * 120
                    yg = y * 120
                    grid_segment = curr_frame[yg:yg + 120, xg:xg + 120]
                    if imageDataPath.find('/NoSmoke/') != -1:
                        noSmokeVideo.write(grid_segment)
                    elif imageDataPath.find('/Smoke/') != -1:
                        smokeVideo.write(grid_segment)
                    # ZB EDIT: commented out statement to write images to smoke / nonsmoke directories
                    #cv2.imwrite(imageDataPath, grid_segment)
    smokeVideo.release()
    noSmokeVideo.release()


if __name__ == "__main__":
    # get the folder containing all the videos from the user
    # Enter the filepath relative to this dir where videos + HashedVideoNames.txt is stored below
    ######
    ###### Adjust input directory as needed
    ######
    filepath = "/FrameExtractor/ProcessedVideos/"
    cwd = os.getcwd()
    ######
    ###### Adjust input directory as needed
    ######
    # Test if the directory path is valid by trying to open a HashedVideoNames.txt within it
    try:
        videoNames = open((cwd + filepath + 'HashedVideoNames.txt'), encoding='utf-8')

    except IOError as e:
        print('Error opening the HashedVideoNames.txt at that file path: ' + str(e))
    else:
        # start grid label sequence
        print("Instructions:")
        print("   - while on the image feed, click to select and unselect sections of smoke")
        print("   - c - clear selection of squares")
        print("   - n - write to file frame by frame")
        print("   - p - write to file continuously until p is presssed again to 'pause'")
        print("   - q - any time to quit while on the video")

        # read the lines from HashedVideoNames.txt
        videoNameList = videoNames.read().splitlines()
        print(len(videoNameList))

        # ZB EDIT: altering videoCount to process middle 300 videos
        videoCount = 50
        files = []
        for i in range(300):
            files.append(videoNameList[videoCount])
            videoCount += 1
        videoCount = 50

        # label all those videos from the user specified directory
        for vidname in files:
            dataInputPath = filepath + vidname
            vidnameSplit = vidname.split('.')
            videoCount += 1
            print("From video file: " + dataInputPath)
            # call the label sequence for that video
            grid_label(dataInputPath, videoCount)
    finally:
        videoNames.close()
