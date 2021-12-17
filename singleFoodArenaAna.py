from numpy.lib.function_base import average
from numpy.testing._private.nosetester import _numpy_tester
from charonFoodTra import readCharonFood54
from tqdm import tqdm
import numpy as np


class analyseSingleArena:

    def __init__(self,imgObjData,arenaNo,objectNameList = ['arena','fly']):
        self.imgObjData = imgObjData
        self.arenaNo = arenaNo
        self.objectNameList = objectNameList
        self.traLen  = len(self.imgObjData)
        self.arenaHeightMM   = 8
        self.arenaWidthMM    = 18
        self.neutralZone     = (0.45,.55)
    
    def reduceToBestDetections(self):
        
        for c in tqdm(range(self.traLen ),'reducing to best detections'):
            #shorthand
            temp = self.imgObjData[c]
            #preallocation
            cleaned = list()
            #keep frame number
            cleaned.append(temp[0])
            #pick best 
            for objName in self.objectNameList:
                # get all objects with either fly or arena
                tempObjList = [item for item in temp[1::] if item["name"] == objName]
                #pick best detection of that object
                if tempObjList:
                    tempQualList = [item['quality'] for item in tempObjList]
                    bestIndex = np.argmax(np.array(tempQualList)) 
                    cleaned.append(tempObjList[bestIndex])
            #save back
            self.imgObjData[c] = cleaned

    def getOverallDetectionSuccess(self):
        # check number of detections
        detectNum = np.array([len(x) for x in self.imgObjData ],dtype=int)-1
        self.detectionSuccess = np.sum(detectNum)/(2*self.traLen )
    
    def calcAvgArena(self):
        avgArenaList = list()
        for c in range(self.traLen ):
            arenaDict = self.imgObjData[c][1]
            avgArenaList.append(arenaDict['boundingBox'])
        avgArenaList = np.array(avgArenaList)
        self.avgArena = np.median(avgArenaList,axis=0)

    def getRelativePos(self,pos):
        posY = (pos[0]-self.avgArena[0]) / (self.avgArena[2]-self.avgArena[0]) 
        posX = (pos[1]-self.avgArena[1]) / (self.avgArena[3]-self.avgArena[1])
        return np.array((posY,posX))
    
    def getSide(self,flyX):
        #  0 ->  1: -1 from neutral to right
        #  1 ->  0:  1 from right to neutral
        #  0 -> -2:  2 from neutral to left
        # -2 ->  0: -2 from left to neutral
        # -2 ->  1: -3 from left to right
        #  1 -> -2:  3 from right to left

        if flyX < self.neutralZone[0]:
            return -2   
        elif flyX > self.neutralZone[1]:
            return 1
        else:
            return 0

    def calcFlyTrajectories(self):
        self.mm_arena  = np.ones(shape=(self.traLen,2))*-1 
        self.rel_arena = np.ones(shape=(self.traLen,2))*-1
        self.rel_image = np.ones(shape=(self.traLen,2))*-1
        self.sides     = np.ones(shape=(self.traLen, ))*-1
        for c in tqdm(range(self.traLen),'calculating trajectories'):
            detections = self.imgObjData[c]
            if len(detections) == 1 or (len(detections) == 2 and detections[1]['name'] != 'fly'):
                self.mm_arena[c,:]  = np.NaN
                self.rel_arena[c,:] = np.NaN
                self.rel_image[c,:] = np.NaN
            else:
                self.rel_image[c,:] = detections[-1]['centerOfMass'][:]
                self.rel_arena[c,:] = self.getRelativePos(self.rel_image[c,:])
                self.mm_arena[c,0]  = self.rel_arena[c,0]*self.arenaHeightMM
                self.mm_arena[c,1]  = self.rel_arena[c,1]*self.arenaWidthMM
                self.sides[c]          = self.getSide(self.rel_arena[c,1])

        




reader = readCharonFood54('/media/gwdg-backup/BackUp/Lennart/2021-10-03_10-19-27/2021-10-03_10-19-27__arena_02.tra')
reader.readFile()
imgObjData = reader.imObjData
asa = analyseSingleArena(imgObjData,2)
asa.reduceToBestDetections()
asa.calcAvgArena()
asa.calcFlyTrajectories()