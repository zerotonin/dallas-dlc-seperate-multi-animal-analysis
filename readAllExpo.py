import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt  
## Data 

def get_status(row):
    if row.infection == True and row.treatment == True:
        strainID = 'antibiotics'
    elif row.infection == True and row.treatment == False:
        strainID = 'infected'

    elif  row.infection == False and row.treatment == False:
        strainID = 'healthy'
    else:
        strainID = 'control'
    return strainID

def recombineDF(df):
    df = df.drop(columns=['coord_relImg_y', 'coord_relImg_x',
        'BB_relImg_ymin', 'BB_relImg_xmin', 'BB_relImg_ymax', 'BB_relImg_xmax',
        'coord_relArena_y', 'coord_relArena_x', 'coord_mmArena_y',
        'coord_mmArena_x', 'coord_rho', 'coord_phi', 'BB_mm_ymin', 'BB_mm_xmin',
        'BB_mm_ymax', 'BB_mm_xmax', 'absSpeed_mm/s', 'active' ])
    df['totalDur'] = df['frameNo'].iloc[-1]
    max_expo_list = list()
    for arena_no in df['arenaNo'].unique():
        temp = df[df['arenaNo']==arena_no]
        max_expo_row = temp.loc[temp['exploredArea__mm2'].idxmax()]
        max_expo_row['status'] = get_status(max_expo_row)
        max_expo_list.append(max_expo_row)

    return pd.DataFrame(max_expo_list)



source_dir = '/media/dataSSD/YegiTra'
file_list = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.endswith('Ana.h5')]

df_list = list()

for file_pos in tqdm(file_list,desc='read data'):
    df = pd.read_hdf(file_pos)
    dfg = recombineDF(df)
    del df 
    dfg['filename'] = file_pos
    df_list.append(dfg)
    del dfg

all_expo_df = pd.concat(df_list)
del df_list

all_expo_df['rel. expo rate, mm2/h'] = all_expo_df['exploredArea__mm2']/all_expo_df['frameNo']*10*3600
all_expo_df['abs. expo rate, mm2/h'] = all_expo_df['exploredArea__mm2']/all_expo_df['totalDur']*10*3600

all_expo_df.to_hdf('./all_expo_data.h5',key='data')



all_expo_df = pd.read_hdf('./all_expo_data.h5',key='data')
plt.figure()
sns.boxplot(x='status',y='exploredArea__mm2',hue='sex',data=all_expo_df,
                notch=False)     
plt.figure()
sns.boxplot(x='status',y='rel. expo rate, mm2/h',hue='sex',data=all_expo_df,
                notch=False)     
ax = plt.gca()
ax.set_yscale('log')

plt.figure()
sns.boxplot(x='status',y='abs. expo rate, mm2/h',hue='sex',data=all_expo_df,
                notch=False)     
ax = plt.gca()
ax.set_yscale('log')

plt.show()