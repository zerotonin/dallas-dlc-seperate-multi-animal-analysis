import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt  
## Data 

source_dir = '/media/dataSSD/YegiTra'
file_list = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.endswith('Ana.h5')]

df_list = list()

for file_pos in tqdm(file_list,desc='read data'):
    df = pd.read_hdf(file_pos)
    df['filename'] = file_pos
    try:
        df_list.append(df[['frameNo','arenaNo','time','sex','infection', 'treatment','exploredArea__mm2','filename']])
    except:
        print(file_pos)
    del df 

all_movie_df = pd.concat(df_list)
del df_list
all_movie_df.to_hdf(os.path.join(source_dir,'all_expo_data.h5'),key='data')


def get_id(row):
    if row.infection == True and row.treatment == True:
        strainID = 'antibiotics'
    elif row.infection == True and row.treatment == False:
        strainID = 'infected'

    elif  row.infection == False and row.treatment == False:
        strainID = 'healthy'
    else:
        strainID = 'control'

    animalID = strainID + '_'+str(row.filenum)+ '_'+str(row.arenaNo)

    return strainID,animalID
df  = pd.read_hdf('/home/bgeurten/all_expo_data.h5')
arena_chg = df.arenaNo.diff()         

starts,  = np.where(arena_chg != 0.0)   
stops  = starts[1::] -1
stops  = np.append(stops,len(df)-1)
df_stops = df.iloc[stops,:]

id_list = list()
for i,row in df_stops.iterrows():
    strainID, _ = get_id(row)
    id_list.append(strainID)

df_stops['status'] = id_list

sns.boxplot(x='sex',y='exploredArea__mm2',hue='status',data=df_stops,
                notch=True)     
plt.show()