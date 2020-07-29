import DLC_reader,tqdm, trajectory_correcter,copy
from importlib import reload 
import matplotlib.pyplot as plt
import numpy as np


reload(DLC_reader)
flyPos    = '/media/dataSSD/Anka1/A_01_01DeepCut_resnet50_ParalellClimb2Aug22shuffle1_150000.h5'
flyPos    = '/media/dataSSD/Anka4/2019-09-25__10_18_09DeepCut_resnet50_darkClimbFliesSep27shuffle1_1030000.h5'

cornerPos2= '/media/dataSSD/Anka1/A_01_01DeepCut_resnet50_darkClimbCornersSep13shuffle1_1030000.h5'

x = DLC_reader.DLC_H5_reader(flyPos,15)  
x.readH5()
x.multiAnimal2numpy()

y= DLC_reader.multiAnimalEval(copy.deepcopy(x.tra))
y.testForArtifacts()
y.interpOverArtifacts()


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
cmap = plt.get_cmap('tab20')  
ax.set_xlim(0,1000)
ax.set_ylim(0,800)
ax.axis('equal')
plt.gca().invert_yaxis()

for frameI in np.linspace(0,x.frameNo,100, endpoint=False, dtype=int ):
    
    for animalI in  range(x.animalNo):
    #animalI =5
        if y.artifactCandidates[frameI,animalI]:
            ax.plot(y.tra[frameI,animalI,:,0],y.tra[frameI,animalI,:,1],'k-')        
            ax.plot(y.tra[frameI,animalI,:,0],y.tra[frameI,animalI,:,1],'kx')
        else:
            ax.plot(y.tra[frameI,animalI,:,0],y.tra[frameI,animalI,:,1],'-',color=cmap.colors[animalI])        
            ax.plot(y.tra[frameI,animalI,0,0],y.tra[frameI,animalI,0,1],'.',color=cmap.colors[animalI])
        
        fig.canvas.draw()
#plt.show()

