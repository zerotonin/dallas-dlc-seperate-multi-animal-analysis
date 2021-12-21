import os, readMultiAnimalCharonTra
from importlib import reload
import numpy as np 
from tqdm import tqdm
import pandas as pd
import cv2 as cv
import matplotlib.pyplot as plt


# read and transform bounding box of arena position

#cmar = readMultiAnimalCharonTra.readMultiAnimalCharonTra(traFile,movFile,bbFile,20.0,20.0)
#cmar.run()
#cmar.saveAna('/media/dataSSD/YegiTra/arena.csv','/media/dataSSD/YegiTra/tra.h5')


fps = 10
df = pd.read_hdf('/media/dataSSD/YegiTra/tra.h5','data')
for arenaNo in range(20):
    subset = df.loc[df['arenaNo']==arenaNo,:].copy()
    subset['coord_mmArena_y'] = subset['coord_mmArena_y'].interpolate()
    subset['coord_mmArena_x'] = subset['coord_mmArena_x'].interpolate()
    subset['coord_rho'] = subset['coord_rho'].interpolate()
    subset['coord_phi'] = subset['coord_phi'].interpolate()
    # need to low pass filter first!
    subset['absSpeed_mm/s'] = np.insert(np.sqrt(np.diff(subset['coord_mmArena_y'].values)**2+np.diff(subset['coord_mmArena_x'].values)**2)*fps,0,np.NaN)

plt.plot(subset['coord_mmArena_x'],subset['coord_mmArena_y'])     
plt.axis('equal')
plt.show()