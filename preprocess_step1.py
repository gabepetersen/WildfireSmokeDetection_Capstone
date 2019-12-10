# preprocess_step1.py
# Gabe Petersen
# detect image blur, resize images, remove noise

import cv2
import os
import re
import numpy as np

# reads in a video using opencv's VideoCapture object
def read_video(filename):
    # Create a VideoCapture object and read from input file
    video = cv2.VideoCapture(filename)

    # Check if video opened successfully
    if (video.isOpened()== False):
        print("Error opening video stream or file")
    else:
        # return video
        return video

# preprocesses the video frames to remove blurry frames and resize them
def preproc(vidcap, fps, width, height):
    # create a videowriter object to store the preprocessed video
    #
    # NOTE: This codecs format with mp4v and .mov PROBABLY WONT WORK on other machines besides mac
    #
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    videoWrite = cv2.VideoWriter('preproc_1.mov', fourcc, fps, (int(vidcap.get(3)), int(vidcap.get(4))) )
    # get each frame and store into videowriter
    while True:
        ret, frame = vidcap.read()
        if ret:
            # convert frame to BGR
            cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # evaluate if frame is in focus (not too blurry)
            if(BlurEval(frame)):
                # elementary solution for image denoize - DOESNT WORK ATM
                # frame_v2 = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
                #
                # add the frame to the output video
                # THIS DOESNT WORK WHEN CAPTURE FRAME IS SHRUNK TO ANOTHER SIZE
                #
                videoWrite.write(frame)
                # shrink video
                frame_v3 = cv2.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
                cv2.imshow('Resized Video', frame_v3)
                if cv2.waitKey(24) & 0xFF == ord('q'):
                    break
        else:
            break
    videoWrite.release()

# evaluate if an image is too blurry or not
# returns true if not too blurry
def BlurEval(img):
    # really blurry images are around 100
    # sorta blurry images are 200
    threshold = 300.0

    # convery to greyscale
    greyscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_val = cv2.Laplacian(greyscaled, cv2.CV_64F).var()
    # if Laplacian value is under a threshold value, then the image is too blurry
    # print("Here is the laplacian value: " + str(lap_val))
    if lap_val < threshold:
        return False
    return True

if __name__ == "__main__":
    # import video
    video = read_video('Data/Yet another suspicious fire near the Heavenly Gondola is confirmed around 4 30 PM (2).mp4')

    print("The width of the video: " + str(video.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("The height of the video: " + str(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("The FPS of the video: " + str(video.get(cv2.CAP_PROP_FPS)))

    # get information about the video stream
    framerate = video.get(cv2.CAP_PROP_FPS)
    vid_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    vid_h = video.get(cv2.CAP_PROP_FRAME_WIDTH)

    # set capture sizes
    video.set(3, vid_w)
    video.set(4, vid_h)

    # get rid of blurry frames, de-noise the image, resize the video frame by half
    # store as preproc_1.mp4
    preproc(video, framerate, vid_w, vid_h)

    # release the VideoCapture
    # vidcap.release()
    cv2.destroyAllWindows()
