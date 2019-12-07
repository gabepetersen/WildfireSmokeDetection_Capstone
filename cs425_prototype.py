import cv2
import os
import re
import numpy as np


def load_data(input_dir):
    folder = os.fsencode(input_dir)
    return [os.fsdecode(file) for file in os.listdir(folder)]


def getTimeStamps(fileNames):
    first_name = fileNames[0]
    #m = re.search('(\d|\s)+(?=(PM|AM|pm|am))', first_name)
    timeStamps = []
    me = []
    for name in file_names:
        m = re.search('(\d|\s)+(?=(PM|AM|pm|am))', name)
        if m is not None:
            timeStamps.append(m.group(0) + m.group(2))
        else:
            timeStamps.append(0)
        me.append(name)
    return me, timeStamps

def output_data(result):
    ## Check if Output directory exists

    with open('output.txt', 'w') as f:
        for line in result:
            lines = [line[0] + '/ ' + line[1]]
            np.savetxt(f, lines, fmt='%s')


if __name__ == "__main__":
    file_names = load_data('Data/')
    names, timeStamps = getTimeStamps(file_names)
    result = np.column_stack((names, timeStamps))
    output_data(result)
