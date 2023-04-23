import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from peguin_ana01 import TrajectoryProcessor

pix2m      = np.array([0.97/124.6,0.3/66,0.4/76.2]).mean()
im_height  = 788
im_width   = 1402
frame_rate = 30

path_to_penguins = "/home/bgeurten/penguins/sorted_and_filtered/"

df = pd.read_hdf(f'{path_to_penguins}Gentoo_02-03-2021_Dato1.h5','trace')

tp = TrajectoryProcessor(df,im_width,im_height,pix2m,frame_rate)
df_interp,df_saccades = tp.main()

x =tp.save_saccade_data(df_interp,df_saccades)
df_temp = df_interp.loc[df_interp.segment == 10,:]



#######
# here is the code that can be ran in ipython that works already. the for loops still gives to many error since it cant find the saccade peaks
#######

row = 0
saccade_data = df_interp.loc[df_interp['segment'] == int(df_realSaccades.iloc[[row]].segment)] #take the data from df.interp for segment 
saccade_data = saccade_data.dropna()
saccadePeak  = saccade_data.loc[saccade_data['rot_speed_degPs'] == float(df_realSaccades.iloc[[row]].amplitude_degPsec)] #find the frame with the saccadic peak
oneSecSaccade = saccade_data.loc[np.arange(saccadePeak.index.values[0]-5,saccadePeak.index.values[0]+5)] # create a new dataframe sourrounding the saccadic peak (in total 30frames) currently using 5 as 15 is extending the Dataset
    
oneSecSaccade['yaw_rad'] = oneSecSaccade.yaw_rad - oneSecSaccade.iloc[[0,1]].yaw_rad.mean() #normalize yaw to basement yaw before start of saccade
oneSecSaccade.yaw_deg = np.rad2deg(oneSecSaccade.yaw_rad)
oneSecSaccade.to_csv("/media/anne/Samsung_T5/PHD/saccadicData.csv",index=False) # still needs to be automated for the for loop

oneSecSaccade.rot_speed_degPs.plot()
plt.show()
oneSecSaccade.yaw_deg.plot()
plt.show()