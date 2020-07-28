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
        
    
class multiAreaEval:
    def __init__(self,tra3):
        self.tra = tra3
        self.traLen,self.animalNo,self.bodyPartNo,self.coordNo = tra3.shape[:]
        self.posSorted= list()
        self.accuracyThreshold = 0.95

    def thresholdAcc(self,areaCoords):
        idx = np.nonzero(areaCoords[:,2]>=self.accuracyThreshold)
        return idx[0]  

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




        


            


