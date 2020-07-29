import pandas,tqdm,copy
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


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
        for frameI in tqdm.tqdm(range(self.frameNo)):
            frameRes = self.pandasDF.iloc[frameI].iloc[:] 
            frameRes = frameRes.to_numpy()  
            frameRes = np.reshape(frameRes,(self.areaNo,-1))  
            frameRes = np.reshape(frameRes,[self.animalNo,int(self.areaNo/self.animalNo),3])   
            self.tra.append(frameRes)
        self.tra = np.array(self.tra)
        
    
class multiAnimalEval:
    def __init__(self,tra3):
        self.tra = tra3
        self.traLen,self.animalNo,self.bodyPartNo,self.coordNo = tra3.shape[:]
        self.posSorted= list()
        self.accuracyThreshold = 0.95

    def thresholdAcc(self,areaCoords):
        idx = np.nonzero(areaCoords[:,2]>=self.accuracyThreshold)
        return idx[0]  

    def calcBodyLen(self):
        self.bodyLength = np.zeros(shape=(self.traLen,self.animalNo))
        for frameI in range(self.traLen):
            for animalI in range(self.animalNo):
                animal = self.tra[frameI,animalI,:,0:2]
                self.bodyLength[frameI,animalI] = np.linalg.norm(np.diff(animal,axis=0)) 

    def testBodyLen(self, lenThreshold):
        self.calcBodyLen()
        lengthDiff = self.bodyLength/np.median(self.bodyLength,axis=0)
        return lengthDiff > lenThreshold
        #self.lengthDiff = np.abs(normBL -1)    
    
    def calcMaxStepSize(self):
        self.step = np.zeros(shape=(self.traLen,self.animalNo))
        for frameI in range(1,self.traLen):
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
    
    def testForArtifacts(self, stepThreshPerc = 99, bodyThresh= 2):
        bodyLenCandidates  = self.testBodyLen(bodyThresh)
        stepSizeCandidates = self.testStepSize(stepThreshPerc)

        self.artifactCandidates = bodyLenCandidates | stepSizeCandidates
 
    def sortOnPos(self):

        self.posSorted= list()
        ptsOld = self.tra[0,:,:]
        self.posSorted.append(ptsOld)
        
        for frameI in tqdm.tqdm(range(1,self.traLen)):
            ptsNew = copy.deepcopy(self.tra[frameI,:,:])
            IDX = self.thresholdAcc(ptsNew)
            C = cdist(ptsOld[:,0:2], ptsNew[IDX,0:2], 'euclidean')
            assignmentOld, assigmentNew = linear_sum_assignment(C)

            ptsOld[assignmentOld,:] = ptsNew[assigmentNew,:]


            self.posSorted.append(copy.deepcopy(ptsOld))




        


            


