import DLC_reader,tqdm 
from importlib import reload 
import matplotlib.pyplot as plt
import numpy as np


reload(DLC_reader)
flyPos    = '/media/dataSSD/Anka1/A_01_01DeepCut_resnet50_ParalellClimb2Aug22shuffle1_150000.h5'
cornerPos2= '/media/dataSSD/Anka1/A_01_01DeepCut_resnet50_darkClimbCornersSep13shuffle1_1030000.h5'

x = DLC_reader.DLC_H5_reader(flyPos)  
x.readH5()
x.multiAnimal2numpy()

y= DLC_reader.multiAreaEval(x.tra)
y.sortOnPos()





tra3Sorted = np.array(y.posSorted) 
tra3 = np.array(x.tra) 
cmap = plt.get_cmap('tab20')      
fig, axs = plt.subplots(2, 1)
c = 0
for areaI in range(tra3.shape[1]):
    if areaI%2 == 0:
        axs[0].plot(tra3[:,areaI,0],tra3[:,areaI,1],'.',color=cmap.colors[c])
    else:
        axs[0].plot(tra3[:,areaI,0],tra3[:,areaI,1],'<',color=cmap.colors[c])
        c+=1

c = 0
for areaI in range(tra3Sorted.shape[1]):
    if areaI%2 == 0:
        axs[1].plot(tra3Sorted[:,areaI,0],tra3Sorted[:,areaI,1],'.',color=cmap.colors[c])
    else:
        axs[1].plot(tra3Sorted[:,areaI,0],tra3Sorted[:,areaI,1],'<',color=cmap.colors[c])
        c+=1
axs[0].axis('equal')
axs[1].axis('equal')

plt.show()


    
