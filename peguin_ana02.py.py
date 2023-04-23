import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from peguin_ana01 import TrajectoryProcessor
import glob
import os


pix2m      = np.array([0.97/124.6,0.3/66,0.4/76.2]).mean()
im_height  = 788
im_width   = 1402
frame_rate = 30

path_to_penguins = "/home/bgeurten/penguins/sorted_and_filtered/"
file_extension = 'h5'

file_list = glob.glob(os.path.join(path_to_penguins, f'**/*{file_extension}'), recursive=True)

saccade_list = list()
angle_list = list()
angle_vel_list = list()

for file_path in file_list:
df = pd.read_hdf(f'{path_to_penguins}Gentoo_02-03-2021_Dato1.h5','trace')

tp = TrajectoryProcessor(df,im_width,im_height,pix2m,frame_rate)
df_interp,df_saccades = tp.main()

angle,angle_vel =tp.extract_one_sec_saccades(df_interp,df_saccades)
df_temp = df_interp.loc[df_interp.segment == 10,:]


