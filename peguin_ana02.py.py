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
c = 0 
d = 0

for file_path in file_list:
    df = pd.read_hdf(file_path)

    c +=1

    tp = TrajectoryProcessor(df,im_width,im_height,pix2m,frame_rate)
    df_interp,df_saccades = tp.main()

    if df_saccades is not None:
        d +=1
        angle,angle_vel =tp.extract_one_sec_saccades(df_interp,df_saccades)
        saccade_list.append(df_saccades)
        angle_list.append(angle)
        angle_vel_list.append(angle_vel)
        print(c,d,angle.shape)

angle = np.vstack(angle_list)
angle_vel = np.vstack(angle_vel_list)
df_saccades = pd.concat(saccade_list)



plt.plot(np.mean(angle, axis=0))


plt.plot(np.mean(angle_vel, axis=0))
plt.show()
df_saccades.saccade_duration_s.hist()
df_saccades.amplitude_degPsec.hist()
