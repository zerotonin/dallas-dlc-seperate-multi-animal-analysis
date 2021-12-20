import os
import pandas as pd
import seaborn as sns
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

fileDir = '/media/dataSSD/LennartSplitMovies'
fileList = [os.path.join(fileDir,x) for x in os.listdir(fileDir) if x.endswith('.h5')]
fileList.sort()
data = pd.read_hdf(fileList[0],key='fly')
for i in range(1,len(fileList)):
    temp = pd.read_hdf(fileList[i],key='fly')
    data = pd.concat([data,temp],axis=0)
data = data.reset_index()
data['activity'] = data['absSpeed_mmPsec']> 2.0 
data['time_epoch']=pd.to_datetime(data['time_epoch'])
data["time"] = pd.to_datetime(data["time_epoch"], format = "%H:%M:%S").dt.hour
activeSet = data.loc[data['activity'],:]

sns.boxplot(x="arenaNo", y="absSpeed_mmPsec",
            data=activeSet)
sns.despine(offset=5, trim=True)

# activity
sns.displot(activeSet, x="time", hue="arenaNo", stat="probability",kde=True, common_norm=False, multiple="dodge" )

sns.displot(subset, x="X_mmArena", y="Y_mmArena", binwidth=(.5, .5), cbar=True)

for arena in range(1,12):
    f = plt.figure()
    ax = plt.subplot(1,1,1)
    subset = data.loc[data['arenaNo']==arena,:]
    ax.plot(subset['X_mmArena'],subset['Y_mmArena'])
    ax.axis('equal')
    ax.x_label('x coordinate, mm')
    ax.y_label('y coordinate, mm')
    ax.title(f'arena {arena}')
plt.show()
