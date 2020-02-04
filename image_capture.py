import numpy as np
import cv2
import grid_label as gl
import cs425_prototype as csp
import os
import random

random.seed(0)


def open_frame_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Directory ", directory, " created.")
    else:
        print("Directory ", directory, " exists.")


def frame_extractor(cap, video_number):
    total_frames = cap.get(7) - 1
    for i in range(5):
        frame_index = int(random.uniform(1, 1000000) % total_frames)
        cap.set(1, frame_index)
        ret, frame = cap.read()
        frame_name = "video" + str(video_number) + "_FC" + str(frame_index) + ".jpeg"
        cv2.imwrite(frame_name, frame)



def frame_extract_iterator(files):
    os.chdir("Extracted_Frames/")
    for i in range(len(files)):
        video = gl.read_video(files[i])
        frame_extractor(video, i)
        print("Frames from video " + str(i) + " extracted.")


if __name__ == "__main__":
    path = '/home/zach/workspace/cs425/Data/'
    files = csp.load_data(path)
    for i in range(len(files)):
        files[i] = path + files[i]
    open_frame_directory("Extracted_Frames")
    frame_extract_iterator(files)
