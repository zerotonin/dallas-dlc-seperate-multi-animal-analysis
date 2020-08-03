import pandas,tqdm,copy,trajectory_correcter
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class DLC_H5_reader:
    def __init__(self,filePosition,animalNo):
        self.fPos = filePosition
        self.animalNo = animalNo
        self.pandasDF = None
        self.frameNo  = None  
        self.columns  = None
        self.areaNo   = None  
        self.tra      = None
    
    def readH5(self):
        self.pandasDF = pandas.read_hdf(self.fPos)
        self.frameNo  = self.pandasDF.shape[0]  
        self.columns  = self.pandasDF.shape[1]
        self.areaNo   = int(self.columns/3)  
    
    def multiAnimal2numpy(self):
        self.tra = list()
        for frameI in tqdm.tqdm(range(self.frameNo),desc ='reading '+self.fPos):
            frameRes = self.pandasDF.iloc[frameI].iloc[:] 
            frameRes = frameRes.to_numpy()  
            frameRes = np.reshape(frameRes,(self.areaNo,-1))  
            frameRes = np.reshape(frameRes,[self.animalNo,int(self.areaNo/self.animalNo),3])   
            self.tra.append(frameRes)
        self.tra = np.array(self.tra)
        
    
class multiAnimalEval:
    def __init__(self,tra3,arenaCoords,slotNo = 15):
        self.tra = tra3
        self.slotNo = 15
        self.arenaCoords = arenaCoords
        self.sortBoxCoordsClockWise()
        self.frameNo,self.animalNo,self.bodyPartNo,self.coordNo = tra3.shape[:]
        self.coordNo -=1
        self.posSorted= list()
        self.accuracyThreshold = 0.95

    def thresholdAcc(self,areaCoords):
        idx = np.nonzero(areaCoords[:,2]>=self.accuracyThreshold)
        return idx[0]  

    def calcBodyLen(self):
        self.bodyLength = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in tqdm.tqdm(range(self.frameNo),desc = 'body length test'):
            for animalI in range(self.animalNo):
                animal = self.tra[frameI,animalI,:,0:self.coordNo]
                self.bodyLength[frameI,animalI] = np.linalg.norm(np.diff(animal,axis=0)) 

    def testBodyLen(self, lenThreshold):
        self.calcBodyLen()
        lengthDiff = self.bodyLength/np.median(self.bodyLength.flatten())
        return lengthDiff > lenThreshold
        #self.lengthDiff = np.abs(normBL -1)    
    
    def calcMaxStepSize(self):
        self.step = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in tqdm.tqdm(range(1,self.frameNo),desc='step size test'):
            for animalI in range(self.animalNo):
                tempSteps = []
                for bodyPartI in range(self.bodyPartNo):
                        bpCoord = self.tra[frameI-1:frameI+1,animalI,bodyPartI,0:self.coordNo]   
                        tempSteps.append(np.linalg.norm(np.diff(bpCoord,axis=0)))
                self.step[frameI,animalI] = max(tempSteps)

    def testStepSize(self,percentile):
        self.calcMaxStepSize()
        stepThreshold = np.percentile(self.step.flatten(),percentile)
        return self.step > stepThreshold
    
    def testForArtifacts(self, stepThreshPerc = 99, bodyThresh= 2):
        stepSizeCandidates = self.testStepSize(stepThreshPerc)
        positionCandidates = self.positionTest()
        bodyLenCandidates  = self.testBodyLen(bodyThresh)

        self.artifactCandidates = bodyLenCandidates | stepSizeCandidates | positionCandidates

 


    def interpOverArtifacts(self):
        for animalI in tqdm.tqdm(range(self.animalNo),desc='trajectory correction'):
            if self.artifactCandidates[:,animalI].any() == True:
                for bodyPartI in range(self.bodyPartNo):
                    z = trajectory_correcter.trajectory_corrector(self.tra[:,animalI,bodyPartI,0:self.coordNo],self.artifactCandidates[:,animalI])
                    z.interpolateOverArtifacts()
                    self.tra[:,animalI,bodyPartI,0:self.coordNo] = z.tra

    def pointInPolygon(self,bodyCoord,slotCoord):
        bodyCoord = Point(bodyCoord[0],bodyCoord[1])
        slotCoord = Polygon([(slotCoord[0,0],slotCoord[0,1]),(slotCoord[1,0],slotCoord[1,1]),
                            (slotCoord[2,0],slotCoord[2,1]),(slotCoord[3,0],slotCoord[3,1])])
        return slotCoord.contains(bodyCoord)
    
    def calculateSlotCoords(self):
        arenaC = self.arenaCoords[self.arenaCoords[:,1].argsort()]

        upperXCoords = np.linspace(arenaC[0,0],arenaC[1,0],self.slotNo+1,endpoint=True)   
        upperYCoords = np.linspace(arenaC[0,1],arenaC[1,1],self.slotNo+1,endpoint=True) 
        lowerXCoords = np.linspace(arenaC[2,0],arenaC[3,0],self.slotNo+1,endpoint=True)   
        lowerYCoords = np.linspace(arenaC[2,1],arenaC[3,1],self.slotNo+1,endpoint=True)
        self.slotCoord = list() 
        for animalI in range(self.animalNo):
            xPts = [lowerXCoords[animalI],lowerXCoords[animalI+1],upperXCoords[animalI+1],upperXCoords[animalI]]
            yPts = [lowerYCoords[animalI],lowerYCoords[animalI+1],upperYCoords[animalI+1],upperYCoords[animalI]]
            self.slotCoord.append(np.array(list(zip(xPts,yPts))))

    def positionTest(self):
        self.calculateSlotCoords()
        posCandidates = np.zeros(shape=(self.frameNo,self.animalNo),dtype=bool)   
        for frameI in tqdm.tqdm(range(self.frameNo),desc='position test'):
            for animalI in range(self.animalNo):
                allInPolygon = list()
                for bodyPartI in range(self.bodyPartNo):
                    allInPolygon.append(self.pointInPolygon(self.tra[frameI,animalI,bodyPartI,0:self.coordNo],self.slotCoord[animalI]))
                if not all(allInPolygon):
                    posCandidates[frameI,animalI] = True 
        return posCandidates

    def sortBoxCoordsClockWise(self):
        arenaC = self.arenaCoords[self.arenaCoords[:, 0].argsort()]   
        sortedCoordinates = np.zeros(shape = arenaC.shape)
        if arenaC[0,1] < arenaC[1,1]:
            sortedCoordinates[0,:] = arenaC[0,:]
            sortedCoordinates[3,:] = arenaC[1,:]
        else:
            sortedCoordinates[0,:] = arenaC[1,:]
            sortedCoordinates[3,:] = arenaC[0,:]

        if arenaC[2,1] < arenaC[3,1]:
            sortedCoordinates[1,:] = arenaC[2,:]
            sortedCoordinates[2,:] = arenaC[3,:]
        else:
            sortedCoordinates[1,:] = arenaC[3,:]
            sortedCoordinates[2,:] = arenaC[2,:]
        self.arenaCoords = sortedCoordinates


    def Hungarian(self,ptsA,ptsB):
            C = cdist(ptsA,ptsB, 'euclidean')
            assignmentOld, assigmentNew = linear_sum_assignment(C)
            return assignmentOld, assigmentNew


