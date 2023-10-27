import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gmean
import glob

# Script Overview:
# This script demonstrates a proof of concept for quantifying c-starts in animals.
# Utilising the posture data tracked by TRex (Tristan Walter Iain D Couzin (2021)
# TRex, a fast multi-animal tracking system with markerless identification, and 2D
# estimation of posture and visual fields eLife 10:e64000), we can measure c-starts
# by dividing the Euclidean distance between the head and tail by the body length.
# If the animal forms a perfect circle, the result should be close to zero; if it
# is completely stretched out, the result should be 1.

#  ┌──────────────────────────────────────────────────────────────┐
#  │██████     FILE I/O     ██████████████████████████████████████│
#  └──────────────────────────────────────────────────────────────┘

# Constants
folder_path = "/home/bgeurten/Videos/data/P100025/"
pattern_without_posture = folder_path + "P1000255.MP4_fish*.npz"
pattern_with_posture = folder_path + "P1000255.MP4_posture_fish*.npz"

# Creating the lists of trajectory and posture files using glob
trajectory_files = sorted(glob.glob(pattern_without_posture))
posture_files = sorted(glob.glob(pattern_with_posture))

# Zipping the lists to iterate together
file_list = list(zip(trajectory_files, posture_files))

#  ┌──────────────────────────────────────────────────────────────┐
#  │██████      READING     ██████████████████████████████████████│
#  └──────────────────────────────────────────────────────────────┘

all_speeds = list()
all_curvs = list()

# Iterating over the trajectory and posture files
for (traj_file, post_file) in file_list:
    posture = np.load(post_file)
    trajectory = np.load(traj_file)
    
    # Calculating the curvature by considering the Euclidean distance
    # between the head and tail of the animal and dividing it by the body length.
    mdl_points = posture['midline_points']
    time = trajectory['time']
    speed = trajectory['SPEED']

    vector_diffs = np.diff(mdl_points, axis=1)
    vector_norms_along_vertices = np.linalg.norm(vector_diffs, axis=2)
    sum_vector_norms = np.sum(vector_norms_along_vertices, axis=1)
    vector_between_first_last = mdl_points[:, -1, :] - mdl_points[:, 0, :]
    norm_first_last = np.linalg.norm(vector_between_first_last, axis=1)

    curvature = norm_first_last/sum_vector_norms

    # Handling missing elements
    missing_elements = len(curvature) - 45000
    if missing_elements < 0:
        curvature = np.append(curvature, curvature[missing_elements])

    # Saving the data
    all_speeds.append(speed)
    all_curvs.append(curvature)

#  ┌──────────────────────────────────────────────────────────────┐
#  │██████    STATISTICS    ██████████████████████████████████████│
#  └──────────────────────────────────────────────────────────────┘

# Convert the lists to NumPy arrays
all_speeds = np.array(all_speeds).T
all_curvs = np.array(all_curvs).T

# Ensure the shape is (45000, 24) by trimming or padding as needed
all_speeds = all_speeds[:45000, :24]
all_curvs = all_curvs[:45000, :24]

# Calculate the median over axis 1 (24)
geom_mean_speeds = gmean(all_speeds, axis=1)
geom_mean_curvs = gmean(all_curvs, axis=1)

# Calculate the 95% confidence interval over axis 1 (24)
confidence_level = 0.95
degrees_freedom = all_speeds.shape[1] - 1
conf_interval_speeds = stats.t.interval(confidence_level, degrees_freedom, loc=geom_mean_speeds, scale=stats.sem(all_speeds, axis=1))
conf_interval_curvs = stats.t.interval(confidence_level, degrees_freedom, loc=geom_mean_curvs, scale=stats.sem(all_curvs, axis=1))

# Extract lower and upper bounds of the confidence intervals
lower_speed, upper_speed = conf_interval_speeds
lower_curv, upper_curv = conf_interval_curvs

# Stimulus time points
time_points = [60, 300, 540, 780, 1020, 1260]

#  ┌──────────────────────────────────────────────────────────────┐
#  │██████      PLOTTING    ██████████████████████████████████████│
#  └──────────────────────────────────────────────────────────────┘


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=False)

# Top Plot (Speed)
for i in range(all_speeds.shape[1]):
    ax1.plot(time, all_speeds[:,i], 'b-', alpha=0.1)
ax1.plot(time, geom_mean_speeds, 'b-', linewidth=2)
ax1.fill_between(time, lower_speed, upper_speed, facecolor='blue', alpha=0.2)
ax1.scatter(time_points, [-0.2 for t in time_points], marker='^', color='black') # Upward triangle
ax1.set_ylabel('Speed, cm*s^-^1', color='b')
ax1.set_xlabel('Time, s')
ax1.yaxis.label.set_color('b')
ax1.spines['left'].set_color('b')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

# Lower Plot (Curvature)
for i in range(all_curvs.shape[1]):
    ax2.plot(time, all_curvs[:,i], 'g-', alpha=0.1)
ax2.plot(time, geom_mean_curvs, 'g-', linewidth=2)
ax2.fill_between(time, lower_curv, upper_curv, facecolor='green', alpha=0.2)
ax2.scatter(time_points, [1.01 for t in time_points], marker='v', color='black') # Downward triangle
ax2.set_ylabel('Curvature, ratio', color='g')
ax2.yaxis.label.set_color('g')
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.xaxis.tick_top()
ax2.xaxis.set_ticklabels([])

plt.suptitle('Proof of concept - Cstart detectable after mechanic stimulus')
plt.show()
