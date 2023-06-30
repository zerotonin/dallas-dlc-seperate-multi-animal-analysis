import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from peguin_ana01 import TrajectoryProcessor
import glob
import os
import json

pix2m      = np.array([0.97/124.6,0.3/66,0.4/76.2]).mean()
im_height  = 788
im_width   = 1402
frame_rate = 30

path_to_penguins = "/home/bgeurten/penguins/sorted_and_filtered/"
file_extension = 'h5'

file_list = glob.glob(os.path.join(path_to_penguins, f'**/*{file_extension}'), recursive=True)


saccade_list = {'gentoo': [], 'rockhopper': [], 'pooled': []}
angle_list = {'gentoo': [], 'rockhopper': [], 'pooled': []}
angle_vel_list = {'gentoo': [], 'rockhopper': [], 'pooled': []}
c = 0 
d = 0

for file_path in file_list:
    df = pd.read_hdf(file_path)

    c +=1

    tp = TrajectoryProcessor(df,im_width,im_height,pix2m,frame_rate)
    df_interp,df_saccades = tp.main()

    if df_saccades is not None:
        d +=1
        angle,angle_vel =tp.extract_saccades(df_interp,df_saccades,5)

        if 'Gentoo' in file_path:
            saccade_list['gentoo'].append(df_saccades)
            angle_list['gentoo'].append(angle)
            angle_vel_list['gentoo'].append(angle_vel)
        elif 'Rockhopper' in file_path:
            saccade_list['rockhopper'].append(df_saccades)
            angle_list['rockhopper'].append(angle)
            angle_vel_list['rockhopper'].append(angle_vel)

        saccade_list['pooled'].append(df_saccades)
        angle_list['pooled'].append(angle)
        angle_vel_list['pooled'].append(angle_vel)
        
        print(c, d, angle.shape)

for key in saccade_list:
    angle_list[key] = np.vstack(angle_list[key])
    angle_vel_list[key] = np.vstack(angle_vel_list[key])
    saccade_list[key] = pd.concat(saccade_list[key])


fig, axes = plt.subplots(4, 1, figsize=(10, 10))

colors = {'gentoo': 'red', 'rockhopper': 'blue', 'pooled': 'purple'}

saccade_attrib = dict()

for key in saccade_list:
    #    Calculate mean and standard error
    angle_mean = np.nanmean(angle_list[key], axis=0)
    angle_sem = stats.sem(angle_list[key], axis=0, nan_policy='omit')
    angle_vel_mean = np.nanmean(angle_vel_list[key], axis=0)
    angle_vel_sem = stats.sem(angle_vel_list[key], axis=0, nan_policy='omit')

    saccade_attrib[f'{key}_max_amplitude_angle'] = np.nanmax(angle_list[key])
    saccade_attrib[f'{key}_mean_amplitude_angle'] = np.nanmax(angle_mean)
    indices = np.where(angle_mean == saccade_attrib[f'{key}_mean_amplitude_angle'])
    saccade_attrib[f'{key}_sem_amplitude_angle'] = np.nanmax(angle_sem[indices])

    saccade_attrib[f'{key}_max_amplitude_angle_vel'] = np.nanmax(angle_vel_list[key])
    saccade_attrib[f'{key}_mean_amplitude_angle_vel'] = np.nanmax(angle_vel_mean)
    indices = np.where(angle_vel_mean == saccade_attrib[f'{key}_mean_amplitude_angle_vel'])
    saccade_attrib[f'{key}_sem_amplitude_angle_vel'] = np.nanmax(angle_vel_sem[indices])

    # Time vector in milliseconds
    t = np.arange(len(angle_mean)) * (1000.0 / frame_rate)

    # Plot mean angle with standard error
    axes[0].plot(t,angle_mean, color=colors[key], label=key)
    axes[0].fill_between(t, angle_mean-angle_sem, angle_mean+angle_sem, color=colors[key], alpha=0.2)

    # Plot mean angle velocity with standard error
    axes[1].plot(t,angle_vel_mean, color=colors[key], label=key)
    axes[1].fill_between(t, angle_vel_mean-angle_vel_sem, angle_vel_mean+angle_vel_sem, color=colors[key], alpha=0.2)


bins = np.linspace(0, max(max(saccade_list[key].saccade_duration_s*1000) for key in saccade_list), 10)
ax2 = axes[2]

# Plot saccade duration histogram
for idx, key in enumerate(saccade_list):
    hist, _ = np.histogram(saccade_list[key].saccade_duration_s*1000, bins=bins, density=True)
    hist= hist/sum(hist)
    ax2.bar(bins[:-1] + idx*20, hist, width=20, color=colors[key], label=key, alpha=1)

bins = np.linspace(0, max(max(saccade_list[key].amplitude_deg) for key in saccade_list), 10)
ax3 = axes[3]

# Plot amplitude histogram
for idx, key in enumerate(saccade_list):
    hist, _ = np.histogram(saccade_list[key].amplitude_deg, bins=bins, density=True)
    hist= hist/sum(hist)
    ax3.bar(bins[:-1] + idx*0.8, hist, width=0.8, color=colors[key], label=key, alpha=1)


# Add legends to the plots
for ax in axes:
    ax.legend()
# Plot median angle
axes[0].set_title('Mean Angle')
axes[0].set_ylabel('Yaw, deg')

# Plot median angle velocity
axes[1].set_title('Median Angle Velocity')
axes[1].set_ylabel('Yaw velocity, deg*s^-^1')
axes[1].set_xlabel('Time (ms)')

# Plot saccade duration histogram
axes[2].set_title('Saccade Duration Histogram')
axes[2].set_ylabel('Probability Density')
axes[2].set_xlabel('Duration, ms')


# Plot amplitude histogram
axes[3].set_title('Amplitude Histogram')
axes[3].set_ylabel('Probability Density')
axes[3].set_xlabel('Amplitude, deg')

# Set x-labels to 'Time (ms)'
# Show the figure
plt.tight_layout()
plt.show()

# Specify the file path for writing
file_path = "/home/bgeurten/ownCloud/Pengu_Comp/saccade_attributes.txt"

# Open the file in write mode
with open(file_path, 'w') as file:
    # Convert the dictionary to JSON format and write it to the file
    json.dump(saccade_attrib, file, indent=4)
