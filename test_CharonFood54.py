from charonFoodTra import readCharonFood54
from charonFoodTra import plotCharonFood
from foodArenaAnalysis import flyAnalysis
from importlib import reload 
from tqdm import tqdm
import numpy as np 


paul= readCharonFood54('2020-10-27__14_52_10_blueCS8g6d_greenblue_Light.tra') # init of reader object with file position
plotObj = plotCharonFood()
paul.readFile()  # read data from file into memory

#reload(flyAnalysis)
fA = flyAnalysis(paul.imObjData)
fA.run()

sortedFlyList = fA.sortedFlyList
medArenaList  = fA.medArenaList


def getRelativePos(pos,arenaBox):
    posY = (pos[0]-arenaBox[0]) / (arenaBox[2]-arenaBox[0]) 
    posX = (pos[1]-arenaBox[1]) / (arenaBox[3]-arenaBox[1])
    return np.array((posY,posX)) 

frameNo = len(sortedFlyList)
trajectories = list()
sides  = list()
for flyI in range(54):
    flyTraj  = np.ones(shape=(frameNo,2))
    flySides =  np.ones(shape=(frameNo,1))
    arenaBox = np.array(medArenaList[flyI]['boundingBox'])
    arenaCenter = np.array(medArenaList[flyI]['centerOfMass'])
    for frameI in tqdm(range(frameNo),desc='analyse descisions'):
        if sortedFlyList[frameI][flyI] != None:
            pos    = np.array(sortedFlyList[frameI][flyI]['centerOfMass'])
            relPos = getRelativePos(pos,arenaBox)
            flyTraj[frameI,:] = relPos
            if relPos[1] > 0.55:
                flySides[frameI] = 1
            elif relPos[1] < 0.45:
                flySides[frameI] = -1
            else:
                flySides[frameI] = 0
        else:
            flyTraj[frameI,:] = np.array((np.nan,np.nan))
            flySides[frameI]  = np.nan

    trajectories.append(flyTraj)
    sides.append(flySides)

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
plt.set<_
plotObj.plotFlyAssignmentControll(fA.medArenaList,fA.sortedFlyList,1000)

