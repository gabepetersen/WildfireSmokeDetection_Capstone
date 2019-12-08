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
    with open('output.txt', 'w') as f:
        for line in result:
            lines = [line[0] + '/ ' + line[1]]
            np.savetxt(f, lines, fmt='%s')


def trim_timestamps(time):
    #time = [time[i].strip() for i in range(len(time))]
    arr = ['']*len(time)
    index_a = 0
    for i in range(len(time)) :
        temp = time[i].upper().strip()

        if len(temp) > 8:
            temp = temp[-4:]
        integer = find_integer(temp)
        if integer-1 != -2 and not temp[integer-1].isspace():
            temp = insert_space(temp, integer)
        middle_start = temp.find(' ')
        middle_end = integer
        temp = temp[:middle_start] + temp[middle_end:]
        integer = find_integer(temp)
        if integer-1 != -2 and not temp[integer-1].isspace():
            temp = insert_space(temp, integer)
        temp = convert24(temp)
        arr[i] = temp
    return arr

def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]

def find_integer(string):
    integer = string.find('P')
    if integer == -1:
        integer = string.find('A')
    return integer

def convert24(str1):
    if not str1 == '0' and str1[1].isspace():
        str1 = '0' + str1
    if str1 == '0':
        return '0000'
    elif str1.find('P') == -1:
        str1 = str1.replace(" ", "")
        return str1[:-2] + '00'
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    space = str1.find(' ')
    return str(int(str1[:space]) + 12) + '00'

if __name__ == "__main__":
    file_names = load_data('Data/')
    names, timeStamps = getTimeStamps(file_names)
    result = np.column_stack((names, timeStamps))
    result[:, 1] = trim_timestamps(result[:, 1])
    output_data(result)
