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
    cv2.destroyAllWindows()

# optical flow motion detection
# subtracts two frames and evaluates if entire frame is moving or not
def smoke_segment_helper(video):
    # read the first frame
    ret, prev_frame = video.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # go through each of the frames
    while True:
        ret, curr_frame = video.read()
        if ret:
            # blur this!
            # kernel = np.ones((3,3), np.float32) / 9
            # curr_frame = cv2.filter2D(curr_frame, -1, kernel)
            curr_frame = cv2.GaussianBlur(curr_frame, (3,3), 0)

            # morphological smoothing
            kernel = np.ones((15,15), np.uint8)
            #curr_frame = cv2.morphologyEx(curr_frame, cv2.MORPH_OPEN, kernel)

            # show the current frame in the video before filtering
            cv2.imshow("before saturation filter", curr_frame)

            # convert the frame to one channel
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

            # calculate the optical flow
            op_flow(curr_gray, prev_gray, curr_frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            # update previous frame
            prev_gray = curr_gray

def op_flow(curr_gray, prev_gray, curr_frame):
        # conduct some good ol optical flow
        opFlow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 7, 1.5, 0)

        # create images for x and y optical flow
        opFlowX, opFlowY = cv2.split(opFlow)
        # convert to CV_8U
        opFlowY *= 10
        opFlowY = np.uint8(opFlowY)
        # show the optical flow of y
        cv2.imshow("optical flow y", opFlowY)

        # canny edge detector
        frameEdges = cv2.Canny(curr_frame, 20, 60, 1)
        cv2.imshow("canny edge detect", frameEdges)

        # this line is almost unnecessary but its there - so there
        ret, smokeSegments = cv2.threshold(opFlowY, 200, 255, cv2.THRESH_BINARY)

        # thresh_frame = hsv_thresh(curr_frame)
        # cv2.imshow("thresh frame", thresh_frame)
        # hsv filter to further eliminate false positives
        smokeSegments = hsv_filter(curr_frame, smokeSegments, 10)

        # show final segmented optical flow
        cv2.imshow("smoke segments", smokeSegments)

# threshold a frame from median value of saturation
def hsv_thresh(iframe):
    min = 256
    max = 0
    frame_hsv = cv2.cvtColor(iframe, cv2.COLOR_BGR2HSV)
    for x in range(IMG_W):
        for y in range(IMG_H):
            # find min and max of saturation values in image
            if(frame_hsv[y,x][1] > max):
                max = frame_hsv[y,x][1]
            if(frame_hsv[y,x][1] < min):
                min = frame_hsv[y,x][1]
    median = (max + min) / 2
    for x in range(IMG_W):
        for y in range(IMG_H):
            # find min and max of saturation values in image
            if(frame_hsv[y,x][1] > median):
                frame_hsv[y,x][1] = 255
            else:
                frame_hsv[y,x][1] = 0
    return cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)

# filter out high saturation pixels
def hsv_filter(iframe, oframe, thresh):
    # convert frames to HSV
    frame_hsv = cv2.cvtColor(iframe, cv2.COLOR_BGR2HSV)
    # for each pixel in the frame
    for x in range(IMG_W):
        for y in range(IMG_H):
            # color 0 if too high in saturation
            if(frame_hsv[y,x][1] > thresh):
                oframe[y,x] = 0
    return oframe

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
