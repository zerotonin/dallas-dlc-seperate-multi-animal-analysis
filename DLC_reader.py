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
        self.frameNo,self.animalNo,self.bodyPartNo,self.coordNo = tra3.shape[:]
        self.posSorted= list()
        self.accuracyThreshold = 0.95

    def thresholdAcc(self,areaCoords):
        idx = np.nonzero(areaCoords[:,2]>=self.accuracyThreshold)
        return idx[0]  

    def calcBodyLen(self, artifactCandidates):
        self.bodyLength = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in range(self.frameNo):
            for animalI in range(self.animalNo):
                if artifactCandidates[frameI,animalI] == False:
                    animal = self.tra[frameI,animalI,:,0:2]
                    self.bodyLength[frameI,animalI] = np.linalg.norm(np.diff(animal,axis=0)) 
                else:
                    self.bodyLength[frameI,animalI] = np.nan

    def testBodyLen(self, lenThreshold, artifactCandidates):
        self.calcBodyLen(artifactCandidates)
        lengthDiff = self.bodyLength/np.nanmedian(self.bodyLength.flatten())
        return np.nan_to_num(lengthDiff,copy=False) > lenThreshold
        #self.lengthDiff = np.abs(normBL -1)    
    
    def calcMaxStepSize(self):
        self.step = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in range(1,self.frameNo):
            for animalI in range(self.animalNo):
                tempSteps = []
                for bodyPartI in range(self.bodyPartNo):
                        bpCoord = self.tra[frameI-1:frameI+1,animalI,bodyPartI,0:2]   
                        tempSteps.append(np.linalg.norm(np.diff(bpCoord,axis=0)))
                self.step[frameI,animalI] = max(tempSteps)

    def testStepSize(self,percentile):
        self.calcMaxStepSize()
        stepThreshold = np.percentile(self.step.flatten(),percentile)
        return self.step > stepThreshold
    
    def testForArtifacts(self, stepThreshPerc = 99, bodyThresh= 2,sepCoord= 0):
        stepSizeCandidates = self.testStepSize(stepThreshPerc)
        positionCandidates = self.positionTest(sepCoord)
        bodyLenCandidates  = self.testBodyLen(bodyThresh,stepSizeCandidates | positionCandidates)

        self.artifactCandidates = bodyLenCandidates | stepSizeCandidates | positionCandidates

 


    def interpOverArtifacts(self):

        for animalI in range(self.animalNo):
            if self.artifactCandidates[:,animalI].any() == True:
                for bodyPartI in range(self.bodyPartNo):
                    z = trajectory_correcter.trajectory_corrector(self.tra[:,animalI,bodyPartI,0:2],self.artifactCandidates[:,animalI])
                    z.interpolateOverArtifacts
                    self.tra[:,animalI,bodyPartI,0:2] = z.tra

    def pointInPolygon(self,bodyCoord,slotCoord):
        bodyCoord = Point(bodyCoord[0],bodyCoord[1])
        slotCoord = Polygon((slotCoord[0:,0],slotCoord[0:,1]),(slotCoord[1:,0],slotCoord[1:,1]),
                            (slotCoord[2:,0],slotCoord[2:,1]),(slotCoord[3:,0],slotCoord[3:,1]))
        return slotCoord.contains(bodyCoord)
        
    def positionTest(self):
        pass
    def simplePositionTest(self,seperaterCoord):
        allSepCoords = self.tra[:,:,:,seperaterCoord].flatten()

        boundaries = np.linspace(np.percentile(allSepCoords,0.5),np.percentile(allSepCoords,99.5) ,self.animalNo+1,endpoint=True)   
        posCandidates = np.zeros(shape=(self.frameNo,self.animalNo),dtype=bool)   
        for frameI in range(self.frameNo):
            for animalI in range(self.animalNo):
                sep_coords = self.tra[frameI,animalI,:,seperaterCoord]
                for sep_coord in sep_coords:
                    if ((boundaries[animalI] < sep_coord)  &  (boundaries[animalI+1] >= sep_coord)) == False:
                        posCandidates[frameI,animalI] = True 
        return posCandidates
                    


    def Hungarian(ptsA,ptsB):
            C = cdist(ptsA,ptsB, 'euclidean')
            assignmentOld, assigmentNew = linear_sum_assignment(C)
            return assignmentOld, assigmentNew


