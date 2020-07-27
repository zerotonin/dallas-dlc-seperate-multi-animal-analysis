import DLC_reader,tqdm 
from importlib import reload 
import matplotlib.pyplot as plt
import numpy as np


reload(DLC_reader)
fPos = '/media/dataSSD/Anka5/2019-09-26__12_59_21DeepCut_resnet50_darkClimbFliesSep27shuffle1_1030000.h5'
x = DLC_reader.DLC_H5_reader(fPos)  
x.readH5()
x.multiAnimal2numpy()

y= DLC_reader.multiAreaEval(x.tra)
y.sortOnPos()





tra3 = np.array(y.posSorted) 
cmap = plt.get_cmap('tab20')      
c = 0
for areaI in tqdm.tqdm(range(tra3.shape[1])):
    if areaI%2 == 0:
        plt.plot(tra3[:,areaI,0],tra3[:,areaI,1],'.',color=cmap.colors[c])
    else:
        plt.plot(tra3[:,areaI,0],tra3[:,areaI,1],'<',color=cmap.colors[c])
        c+=1

plt.show()


    
    
