# import cv2
import os
import re
import numpy as np

# Pass in input data folder path
def load_data(input_dir):
    # return all file names in folder
    folder = os.fsencode(input_dir)
    return [os.fsdecode(file) for file in os.listdir(folder)]


def getTimeStamps(fileNames):
    first_name = fileNames[0]
    # declare arrays
    timeStamps = []
    me = []
    # for all the names in file names
    for name in file_names:
        m = re.search('(\d|\s)+(?=(PM|AM|pm|am))', name)
        # if an entry m is not null
        if m is not None:
            # split group 0 by spaces
            times = m.group(0).split(' ')
            # remove empty strings
            while('' in times):
                times.remove('')
            # turn each into ints
            times = [int(i) for i in times]
            # remove any number that is not a valid time (years)
            if len(times) > 1:
                for i in times:
                    if i > 59:
                        times.remove(i)

            # if there are hours and minutes specified
            if len(times) == 2:
                # convert into one int
                timesStr = [str(i) for i in times]
            elif len(times) == 1:
                # append 00 if minutes are not specified
                timesStr = [str(i) for i in times]
                timesStr.append("00")
            # if PM, then add 1200 to convert to military time
            times = int("".join(timesStr))
            if m.group(2) in ("PM", "pm"):
                times += 1200

            # append to the times array
            timeStamps.append(times)
        # append 0 to timestamp if it doesnt have a valid number
        else:
            timeStamps.append(0)
        me.append(name)
    return me, timeStamps

def output_data(result):
    ## Check if Output directory exists

    with open('output.txt', 'w') as f:
        for line in result:
            lines = [line[0] + " / " + line[1]]
            np.savetxt(f, lines, fmt='%s')
    print("Preprocessed headers written to output.txt")


if __name__ == "__main__":
    file_names = load_data('Data/')
    names, timeStamps = getTimeStamps(file_names)
    result = np.column_stack((names, timeStamps))
    output_data(result)
