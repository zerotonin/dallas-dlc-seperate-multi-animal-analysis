import cv2,os
from matplotlib.image import BboxImage
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import markerExtractor as markE
from tqdm import tqdm
# data Path
path2data = '/media/gwdg-backup/BackUp/Paul_Funnel'
df = pd.read_csv(f'{path2data}/imgData.csv')



orientations = [1,4,5,6]

allOriMarkers= list()
for oriInt in orientations:
    orientSubSet = df[df.Orientation_int == oriInt ]
    markerList = list()
    for filePos in tqdm(orientSubSet['FilePosition'],desc=f'orientation: {oriInt}'):
        img = cv2.imread(filePos)

        mE = markE.markerExtractor(img)
        coords,markers = mE.extract()
        markerList.append(markers)
        topLeft = markerList[0::4]

markerList = np.concatenate(markerList)
m_all       = np.mean(markerList,axis=0,dtype=int)
m_topLeft   = np.mean(markerList[0::4],axis=0,dtype=int)
m_topRight  = np.mean(markerList[1::4],axis=0,dtype=int)
m_botLeft   = np.mean(markerList[2::4],axis=0,dtype=int)
m_botRight  = np.mean(markerList[3::4],axis=0,dtype=int)

f,a = plt.subplots(3,2)
a = a.flatten()
a[0].imshow(m_all)
a[1].imshow(m_topLeft)
a[2].imshow(m_topRight)
a[3].imshow(m_botLeft)
a[4].imshow(m_botRight) 
plt.show()