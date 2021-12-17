from charonFoodTra import readCharonFood54
from charonFoodTra import plotCharonFood
import foodArenaAnalysis
from importlib import reload 
from tqdm import tqdm
import numpy as np 
import matplotlib.pyplot as plt             

paul= readCharonFood54('/media/gwdg-backup/BackUp/Yegi/2020-11-19__14_34_03.tra') # init of reader object with file position
plotObj = plotCharonFood()
paul.readFile()  # read data from file into memory

#reload(flyAnalysis)
fA = foodArenaAnalysis.flyAnalysis(paul.imObjData)
fA.run()
reload(foodArenaAnalysis)
dA = foodArenaAnalysis.decisionAnalysis(fA.sortedFlyList,fA.medArenaList)
dA.flyWiseAna()

trajectories = dA.relTrajectories
mmTra        = dA.mmTrajectories
sides        = dA.sides 
flyI         = 5


titleStr = 'fly #'+str(flyI)+": "
fig = plt.figure()

plt.scatter(trajectories[flyI][:,1],trajectories[flyI][:,0],c= np.arange(36002))   
plt.plot([dA.neutralZone[0],dA.neutralZone[0]],[0,1],'k--')    
plt.plot([dA.neutralZone[1],dA.neutralZone[1]],[0,1],'k--')  
ax = plt.gca()
ax.set_title(titleStr+'relative trajectory', fontsize=10)
plt.colorbar() 

fig = plt.figure()
plt.scatter(mmTra[flyI][:,0],mmTra[flyI][:,1],c= np.arange(36002))   
plt.plot([dA.neutralZone[0]*dA.arenaWidthMM,dA.neutralZone[0]*dA.arenaWidthMM],[0,dA.arenaHeightMM],'k--')    
plt.plot([dA.neutralZone[1]*dA.arenaWidthMM,dA.neutralZone[1]*dA.arenaWidthMM],[0,dA.arenaHeightMM],'k--')  
ax = plt.gca()
ax.set_aspect('equal', 'box')
ax.set_title(titleStr+'mm trajectory', fontsize=10)
plt.colorbar() 

fig = plt.figure()
plt.plot(sides[flyI])
plt.scatter(np.arange(36002),sides[flyI],c= np.arange(36002)) 
ax = plt.gca()
ax.set_yticks([-1,0,1])
ax.set_yticklabels(['left','middle','right'])
ax.set_title(titleStr+'decisions', fontsize=10)
plt.colorbar() 

plotObj.plotFlyAssignmentControll(fA.medArenaList,fA.sortedFlyList,2000)
ax = plt.gca()
ax.set_title('entire movie every 2000th frame', fontsize=10)

plt.show()