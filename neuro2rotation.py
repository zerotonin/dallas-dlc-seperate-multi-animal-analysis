import pandas as pd
import math
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import numpy as np


# converts the .tra file to .csv for handling with pandas
def tra2csv(tra_file):
    csv_file_content = ''
    with open(tra_file, 'rt') as reading_file:
        for line in reading_file:
            # replace (multiple) space(s) with comma
            new_line = ','.join(line.split())
            # add modified line to new_file_content + line break
            csv_file_content += new_line + '\n'
    reading_file.close()
    # create csv file
    csv_file = tra_file[:-4] + '.csv'
    with open(csv_file, 'wt') as writing_file:
        writing_file.write(csv_file_content)
    writing_file.close()
    return csv_file


def tracing_cor(df, fly_num):
    # detects and corrects auto tracing errors and returns modified df
    for i in range(len(df) - 1):
        # create arrays containing (x,y)-coordinates of every fly for current and next frame
        cur_pos = []
        next_pos = []
        for n in fly_num:
            cur_x, cur_y = df.loc[i, 'x' + str(n)], df.loc[i, 'y' + str(n)]
            next_x, next_y = df.loc[i + 1, 'x' + str(n)], df.loc[i + 1, 'y' + str(n)]
            if math.isnan(cur_x) or math.isnan(cur_y):
                continue
            cur_pos.append([cur_x, cur_y])
            next_pos.append([next_x, next_y])
        # create cost matrix and execute hungarian algorithm
        c = cdist(cur_pos, next_pos, 'euclidean')
        assignment_old, assignment_new = linear_sum_assignment(c)
        # correct detected auto tracing errors
        if not np.array_equal(assignment_old, assignment_new):
            corr_line = [i + 1]
            for x in assignment_new:
                corr_line = corr_line + [value for value in df.iloc[i + 1, 1 + 5 * x:6 + 5 * x]]
            while len(corr_line) < len(df.columns):
                corr_line.append(np.nan)
            df.loc[i + 1] = corr_line
    return df


# creates df from csv with pandas
def create_df(tra_file):
    file = tra2csv(tra_file)
    # Loop the data lines
    with open(file, 'r') as temp_f:
        # get No of columns in each line
        col_count = [len(x.split(',')) for x in temp_f.readlines()]
    # determine No of flies
    fly_num = [x for x in range((max(col_count) - 1) // 5)]
    header_list = ['Frame']
    # Generate column names  (x0, y0, rad0, size0, ecce0, ..., xn, yn, radn, sizen, eccen)
    for i in fly_num:
        header_list = header_list + ['x' + str(i), 'y' + str(i), 'rad' + str(i), 'size' + str(i), 'ecce' + str(i)]
    # Read in csv
    df = pd.read_csv(file, header=None, delimiter=',', names=header_list)
    df = tracing_cor(df, fly_num)
    return df


# 1. creates dict containing x- and y-coordinates and radian for each fly in df
def rel_pos(tra_file):
    df = create_df(tra_file)
    fly_dict = {}
    # loop for each fly in df
    for n in range(int((len(df.columns) - 1) / 5)):
        # creates dictionary for each fly containing x-coordinate, y-coordinate, and angle in radian
        temp_dict = {'x-coor': [x for x in df['x' + str(n)]],
                     'y-coor': [x for x in df['y' + str(n)]],
                     'rad': [x for x in df['rad' + str(n)]]}
        # adds previously created temp_dict to fly_dict
        fly_dict['fly' + str(n)] = temp_dict


rel_pos('/tra/file/path.tra')
