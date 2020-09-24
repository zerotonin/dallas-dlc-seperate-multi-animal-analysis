import DLC_reader
import tqdm,datetime,os
import xml.etree.ElementTree as ET  
import numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class foodChoiceAna:
    def __init__(self,flyPos,metaPos,flyNo,AI_pattern):
        self.flyPos       = flyPos
        self.metaPos      = metaPos
        self.flyNo        = flyNo
        self.AI_pattern   = AI_pattern
        self.knownColours = ['blue','yellow','green']
        self.knownStrains = ['dunce','rut','cs']

    
    def readDLCflies(self):
        #read in dlc file
        readObj = DLC_reader.DLC_H5_reader(self.flyPos,self.flyNo)  
        readObj.readH5()
        # split to 4D trajectory
        readObj.multiAnimal2numpy()
        self.tra = readObj.tra
    
    def readXMLmetaData(self):
        tree = ET.parse(self.metaPos) 
        root = tree.getroot()
        self.foodArenaCoordinates = np.zeros(shape=(24,4))
        self.colNames = list()
        for i in range(24):
            self.colNames.append(root[6+i][0].text)
            for j in range(4):               
                self.foodArenaCoordinates[i,j] = root[6+i][4][j].text
        self.colorOptions = list(set(self.colNames)) 

    
    def getStrainCondition(self):
        self.movName = os.path.basename(self.flyPos).split(self.AI_pattern)  
        self.movName  = self.movName [0]
        expStr = self.movName[21::].split("_") 
        strainCondition = expStr[0].lower()
        for strain in self.knownStrains:
            if strain in strainCondition:
                self.strain = strain
        for colour in self.knownColours:
            if colour in strainCondition:
                self.rearingColour = colour

        # reared colour is always first
        if self.rearingColour == self.colorOptions[1]:
            self.rearingColIDX = 0
            self.colorOptions.reverse()
        else:
            self.rearingColIDX = 0
        


    def analyseFlyPositions(self):

        self.arenaChoices = np.zeros(shape=(24,))

        for frameI in tqdm.tqdm(range(self.tra.shape[0]),desc='analysing frames'):
            for flyI in range(self.flyNo):
                if np.mean(self.tra[frameI,flyI,:,1]) > 0.65:
                    x = np.mean(self.tra[frameI,flyI,:,0])
                    y = np.mean(self.tra[frameI,flyI,:,1])

                    for arenaI in range(24):
                        if self.foodArenaCoordinates[arenaI,0] <= x and self.foodArenaCoordinates[arenaI,2] >= x and self.foodArenaCoordinates[arenaI,1] <= y and self.foodArenaCoordinates[arenaI,3] >= y:
                            self.arenaChoices[arenaI] +=1


    def getArenaSpatialAssignment(self):
        xCoords = np.mean(np.transpose(np.vstack((self.foodArenaCoordinates[:,0],self.foodArenaCoordinates[:,2]))),axis=1)
        yCoords = np.mean(np.transpose(np.vstack((self.foodArenaCoordinates[:,1],self.foodArenaCoordinates[:,3]))),axis=1)*2 # this is done so that in row matching is preferred

        points1 = list()
        points2 = list()
        for i in range(24):
            if self.colNames[i] == self.colorOptions[0]:
                points1.append([xCoords[i],yCoords[i],i])
            else:
                points2.append([xCoords[i],yCoords[i],i])
        self.points1 = np.array(points1)
        self.points2 = np.array(points2)
        C = cdist(self.points1[:,0:2], self.points2[:,0:2])
        _, self.arenaAssignment = linear_sum_assignment(C)
        self.arenaIDX = np.transpose(np.vstack((self.points1[:,2],self.points2[self.arenaAssignment,2])))     

    def plotArenaSpatialAssignment(self):
        plt.plot(self.points1[:,0], self.points1[:,1],'bo', markersize = 10)
        plt.plot(self.points2[:,0], self.points2[:,1],'rs',  markersize = 7)
        for p in range(12):
            plt.plot([self.points1[p,0], self.points2[self.arenaAssignment[p],0]], [self.points1[p,1], self.points2[self.arenaAssignment[p],1]], 'k')

        plt.axes().set_aspect('equal')
        plt.show()

    def combineArenaData(self):
        self.countingData = np.zeros(shape=self.arenaIDX.shape)

        for i in range(12):
            for j in range(2):
                self.countingData[i,j] = self.arenaChoices[self.arenaIDX[i,j].astype(int)]
        

    def analysePreference(self):
        sumOfChoices = np.sum(self.countingData,axis=1)
        self.percentage   = np.zeros(shape=self.countingData.shape)
        self.score        = np.zeros(shape=(12,))
        self.choice        = np.zeros(shape=(12,))
        for i  in range(12):
            self.percentage[i,0] = self.countingData[i,0]/sumOfChoices[i]
            self.percentage[i,1] = self.countingData[i,1]/sumOfChoices[i]
            self.score[i]        = (self.countingData[i,0]-self.countingData[i,1])/(self.countingData[i,0]+self.countingData[i,1])
            self.choice[i]       = np.round(self.countingData[i,0]/sumOfChoices[i])
        
    def makeOutPutList(self):
        self.outPutList= list()

        for i  in range(12):
            self.outPutList.append([self.strain,i,self.rearingColour,self.colorOptions[1],self.percentage[i,0],self.percentage[i,1],self.score[i],self.choice[i],self.countingData[i,0],self.countingData[i,1],self.movName])
        

    def runAnalysis(self):
        self.readDLCflies()
        self.readXMLmetaData()
        self.getStrainCondition()
        self.getArenaSpatialAssignment()
        self.analyseFlyPositions()
        self.combineArenaData()
        self.analysePreference()
        self.makeOutPutList()
        return self.outPutList
        


            