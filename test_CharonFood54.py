from charonFoodTra import readCharonFood54
from charonFoodTra import plotCharonFood
import foodArenaAnalysis
from importlib import reload 
from tqdm import tqdm
import numpy as np 
import matplotlib.pyplot as plt             

paul= readCharonFood54('2020-10-27__14_52_10_blueCS8g6d_greenblue_Light.tra') # init of reader object with file position
plotObj = plotCharonFood()
paul.readFile()  # read data from file into memory

#reload(flyAnalysis)
fA = foodArenaAnalysis.flyAnalysis(paul.imObjData)
fA.run()
reload(foodArenaAnalysis)
dA = foodArenaAnalysis.decisionAnalysis(fA.sortedFlyList,fA.medArenaList)
dA.flyWiseAna()

trajectories = dA.relTrajectories
sides        = dA.sides 

fig = plt.figure()
plt.scatter(trajectories[23][:,1],trajectories[23][:,0],c= np.arange(36002))   
plt.plot([0.45,0.45],[0,1],'k--')    
plt.plot([0.55,0.55],[0,1],'k--')  
plt.colorbar() 

fig = plt.figure()
plt.plot(sides[23])
plt.scatter(np.arange(36002),sides[23],c= np.arange(36002)) 
ax = plt.gca()
ax.set_yticks([-1,0,1])
ax.set_yticklabels(['left','middle','right'])
plt.colorbar() 

plt.show() 
plt.set
plotObj.plotFlyAssignmentControll(fA.medArenaList,fA.sortedFlyList,1000)

