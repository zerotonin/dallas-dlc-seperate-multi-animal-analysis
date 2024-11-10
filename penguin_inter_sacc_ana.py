import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Set frames per second
fps = 25

# Read CSV files into DataFrames
df_dataset2_body = pd.read_csv('/home/geuba03p/Penguin_Rostock/pengu_head_movies/saccade_data/saccades_body.csv' )
df_dataset2_combi = pd.read_csv('/home/geuba03p/Penguin_Rostock/pengu_head_movies/saccade_data/saccades_combi.csv' )
df_dataset2_head = pd.read_csv('/home/geuba03p/Penguin_Rostock/pengu_head_movies/saccade_data/saccades_head.csv')
df_dataset1_inter_sacc = pd.read_csv('/home/geuba03p/Penguin_Rostock/penguins/body_inter_saccade_dur.csv')
df_dataset1_sacc = pd.read_csv('/home/geuba03p/Penguin_Rostock/penguins/body_saccade_dur.csv')

# Initialize lists to collect data
species          = list()
dataset          = list()
saccade_type     = list() # 'saccade' or 'intersaccade'
saccade_duration = list() # 'free', 'associated', 'intersaccade'
saccade_duration = list()
bodypart         = list()


for name,df in [('body',df_dataset2_body),('head',df_dataset2_head),('associated',df_dataset2_combi)]:  
    temp_sacc_dur = df.saccade_duration_ms.to_list()
    temp_sacc_type = ['saccade' for i in temp_sacc_dur]
    temp_intersacc_dur = np.diff(np.vstack((df.saccade_start_idx.to_numpy()[1::],df.saccade_stop_idx.to_numpy()[0:-1])).T,axis=1)
    temp_intersacc_dur = temp_intersacc_dur[temp_intersacc_dur>0]/fps*1000
    temp_sacc_type += ['intersaccade' for i in temp_intersacc_dur]
    
    saccade_duration += temp_sacc_dur + temp_intersacc_dur.flatten().tolist()
    saccade_type += temp_sacc_type
    species += ['gentoo' for i in temp_sacc_type]
    dataset += ['confined' for i in temp_sacc_type] 
    bodypart += [name for i in temp_sacc_type] 


temp_dur = list(df_dataset1_sacc.sacc_dur_sec.to_numpy()*1000)
saccade_duration += temp_dur
saccade_type +=['saccade' for i in temp_dur] 
species += df_dataset1_sacc.species.to_list()
dataset += ['open' for i in temp_dur] 
bodypart += ['body' for i in temp_dur] 

temp_dur = list(df_dataset1_inter_sacc.inter_sacc_dur_sec.to_numpy()*1000)
saccade_duration += temp_dur
saccade_type +=['intersaccade' for i in temp_dur] 
species += df_dataset1_inter_sacc.species.to_list()
dataset += ['open' for i in temp_dur] 
bodypart += ['body' for i in temp_dur] 


for x in (saccade_duration, saccade_type, species, dataset, bodypart):
    print(len(x))

df_durations = pd.DataFrame()
df_durations['saccade_duration_msec'] = saccade_duration
df_durations['saccade_type'] = saccade_type
df_durations['species'] = species
df_durations['dataset'] = dataset
df_durations['bodypart'] = bodypart
df_durations['id'] = [f'{ds} {bp} {s}' for ds,bp,s in list(zip(dataset,bodypart,species))]
df_durations.to_csv('/home/geuba03p/Penguin_Rostock/comb_durations.csv',index=False)

sns.boxplot(data=df_durations, x="id", y="saccade_duration_msec",hue='saccade_type')
plt.yscale('log')
plt.show()

print('done')

