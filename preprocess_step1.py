# preprocess_step1.py
# Gabe Petersen
# detect image blur, resize images, remove noise

import cv2
import os
import re
from vidstab import VidStab
#import matplotlib.pyplot as plt

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

# preprocesses the video frames to remove blurry frames and resize them
def preproc(vidcap, fps, width, height, videoCount):
    # create a videowriter object to store the preprocessed video
    #
    # NOTE: This codecs format with mp4v and .mov PROBABLY WONT WORK on other machines besides mac
    #
    dataPath = 'PreProc1/' + str(videoCount) + '.mov'
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    videoWrite = cv2.VideoWriter(dataPath, fourcc, fps, (480, 270) )
    # set previous frame
    ret, prev_frame = vidcap.read()
    prev_frame = cv2.resize(prev_frame, (480, 270))
    videoWrite.write(prev_frame)
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
                #

                # shrink video
                frame_v3 = cv2.resize(frame, (480, 270))
                videoWrite.write(frame_v3)
                # cv2.imshow('Resized Video', frame_v3)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
    videoWrite.release()
    # stabilize video
    stabilizer = VidStab()
    dataFinalPath = 'PreProc2/' + str(videoCount) + '.avi'
    stabilizer.stabilize(input_path=dataPath, output_path=dataFinalPath, border_type='black')

    #stabilizer.plot_trajectory()
    #plt.show()

    #stabilizer.plot_transforms()
    #plt.show()


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
    for x in range(1, 76):
        dataInputPath = 'Data/' + str(x) + '.mp4'
        video = read_video(dataInputPath)

        print("preprocessing video " + str(x))

        # get information about the video stream
        framerate = video.get(cv2.CAP_PROP_FPS)
        vid_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        vid_h = video.get(cv2.CAP_PROP_FRAME_WIDTH)

        # set capture sizes
        video.set(3, vid_w)
        video.set(4, vid_h)

        # get rid of blurry frames and resize the video frame by half
        preproc(video, framerate, vid_w, vid_h, x)

        # release the VideoCapture
        video.release()
        cv2.destroyAllWindows()
