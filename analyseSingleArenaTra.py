from numpy.core.fromnumeric import shape
from charonFoodTra import readCharonFood54
from tqdm import tqdm
import numpy as np
import pandas as pd
import os


class analyseSingleArenaTra:

    def __init__(self,imgObjData,filePos,fps =10,objectNameList = ['arena','fly'],neutralZone=(0.45,.55)):
        self.imgObjData = imgObjData
        self.filePos = filePos
        self.objectNameList = objectNameList
        self.traLen  = len(self.imgObjData)
        self.fps = fps
        self.neutralZone     = neutralZone
        self.arenaHeightMM   = 8
        self.arenaWidthMM    = 18
    
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
        # staying : will result in a zero
        #  0 ->  1: -1 from neutral to right
        #  1 ->  0:  1 from right to neutral
        #  0 -> -2:  2 from neutral to left
        # -2 ->  0: -2 from left to neutral
        # -2 ->  1: -3 from left to right
        #  1 -> -2:  3 from right to left

        # 0 on neutral ground
        # 1 right of the neutral zone
        # -2 left of the neutral zone

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

    def calcSpeed(self):
        absSpeedPerFrame = np.sqrt(np.sum(np.square(np.diff(self.mm_arena,axis=0)),axis=1)) 
        absSpeedPerFrame = np.insert(absSpeedPerFrame,0,absSpeedPerFrame[0]) # to make this the same length as the coordinates
        self.absSpeedMMperSec = absSpeedPerFrame*self.fps
        
    def getMetaInfo(self):
        fileName = os.path.basename(self.filePos).split('.')[0]   
        dateTimeStr,arenaStr = fileName.split('__')
        
        #get arena number
        self.arenaNum = int(arenaStr.split('_')[1])
        #get absolute time vector
        self.timeVector = self.getTimeVector(dateTimeStr)


    def getTimeVector(self,dateTimeStr):
        # reformat to numpy date format
        dateStr,timeStr = dateTimeStr.split('_')
        timeStr = timeStr.replace('-',':')
        #get numpy time obkecet
        startDateTime = np.datetime64(f'{dateStr}T{timeStr}')
        # calculate the length of the trajectory in millisecods
        traLen_ms = int(np.round(self.traLen*1000/self.fps))
        # caclulate the end of the trajectory as date and time
        endDateTime   = startDateTime + np.timedelta64(traLen_ms,'ms') 
        # transfrom into pandas date time to get the time as Unix epochs
        startDateTime = pd.Timestamp(startDateTime)
        endDateTime   = pd.Timestamp(endDateTime)
        # return linspace vector
        return  np.linspace(startDateTime.value,endDateTime.value,self.traLen)
    
    def convert2pandas(self):
        data = np.column_stack((self.timeVector,self.rel_image,self.rel_arena,self.mm_arena,self.absSpeedMMperSec,self.sides,np.ones(shape=(self.traLen,))*self.arenaNum))
        self.data = pd.DataFrame(data,columns=['time_epoch','Y_relImage','X_relImage','Y_relArena','X_relArena','Y_mmArena','X_mmArena','absSpeed_mmPsec','sides','arenaNo'])

    def run(self):
        self.reduceToBestDetections()
        self.getOverallDetectionSuccess()
        self.calcAvgArena()
        self.calcFlyTrajectories()
        self.calcSpeed()
        self.getMetaInfo()
        self.convert2pandas()


