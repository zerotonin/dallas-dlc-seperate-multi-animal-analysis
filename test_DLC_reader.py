import DLC_reader,tqdm 
from importlib import reload 
import matplotlib.pyplot as plt


reload(DLC_reader)
fPos = '/media/dataSSD/Anka4/2019-09-25__10_23_32DeepCut_resnet50_darkClimbFliesSep27shuffle1_1030000.h5'
x = DLC_reader.DLC_H5_reader(fPos)  
x.readH5()
x.multiAnimal2numpy()


#fig, ax = plt.subplots()
#ax.hold(True)
cmap = plt.get_cmap('tab20')      
for frame in tqdm.tqdm(x.tra):
    rows,cols = frame.shape
    c = 0
    for rowI in range(rows):
        if rowI%2 == 0:
            plt.plot(frame[rowI,0],frame[rowI,1],'x',color=cmap.colors[c])
        else:
            plt.plot(frame[rowI,0],frame[rowI,1],'o',color=cmap.colors[c])
            c+=1
plt.hold(False)

plt.show()


    
    
