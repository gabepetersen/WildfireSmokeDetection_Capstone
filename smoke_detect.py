# smoke_detect.py
# Gabe Petersen
# Calculate optical flow between frames and try to segment out smoke from it

import cv2
import sys
import numpy as np

IMG_W = 480
IMG_H = 270

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

def smoke_segment(dataInputPath):
    # create a VideoCapture object
    video = read_video(dataInputPath)
    # calculate the optical flow of the video
    smoke_segment_helper(video)

    # release the video
    video.release()

# optical flow motion detection
# subtracts two frames and evaluates if entire frame is moving or not
def smoke_segment_helper(video):
    # read the first frame
    ret, prev_frame = video.read()
    # apply the low saturation filter on the first frame
    prev_frame = hsv_filter(prev_frame)

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    # go through each of the frames
    while True:
        ret, curr_frame = video.read()
        if ret:
            # show the current frame in the video before filtering
            cv2.imshow("before saturation filter", curr_frame)
            # apply the low saturation filter on the current frame
            curr_frame = hsv_filter(curr_frame)
            # show the saturation filtered frame
            cv2.imshow("filtered saturation frame", curr_frame)
            # convert the frame to one channel
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            # conduct some good ol optical flow
            opFlow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 7, 1.5, 0)

            # create images for x and y optical flow
            opFlowX = np.zeros((IMG_H, IMG_W, 1), dtype="uint8")
            opFlowY = np.zeros((IMG_H, IMG_W, 1), dtype="uint8")
            # initialize the opFlowX and opFlowY
            for x in range(IMG_W):
                for y in range(IMG_H):
                    opFlowX[y,x] = int(abs(100*opFlow[y,x][0]))
                    opFlowY[y,x] = int(abs(100*opFlow[y,x][1]))

            # show optical flow in x and y directions
            cv2.imshow("optical flow x", opFlowX)
            cv2.imshow("optical flow y", opFlowY)
            # return op_flow
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            # update previous frame
            #prev_frame = curr_frame
            #prev_gray = curr_gray

# filter out high saturation pixels
def hsv_filter(frame):
    # convert frames to HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # for each pixel in the frame
    for x in range(IMG_W):
        for y in range(IMG_H):
            # color 0 if too high in saturation
            if(frame_hsv[y,x][1] > 50):
                frame[y,x] = 0
    return frame

if __name__ == "__main__":
    # get the video count from command line
    videoCount = 1
    if(len(sys.argv) > 0):
        videoCount = sys.argv[1]
    else:
        # print out error if not specified
        print("Error: specify video number when executing")
        sys.exit()

    dataInputPath = "PreProc2/" + str(videoCount) + ".avi"
    print(dataInputPath)
    smoke_segment(dataInputPath)
