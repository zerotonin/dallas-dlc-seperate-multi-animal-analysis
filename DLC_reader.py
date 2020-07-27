import pandas,tqdm
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class DLC_H5_reader:
    def __init__(self,filePosition):
        self.fPos = filePosition
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
            self.tra.append(frameRes)
    
class multiAreaEval:
    def __init__(self,tra3):
        self.tra = tra3
        self.traLen = len(tra3)
    
    def sortOnPos(self):

        self.posSorted= list()
        ptsOld = self.tra[0][:,0:2]
        self.posSorted.append(ptsOld)
        for frameI in tqdm.tqdm(range(1,self.traLen))):
            ptsNew = self.tra[frameI][:,0:2]
            C = cdist(ptsOld, ptsNew, 'euclidean')
            _, assigment = linear_sum_assignment(C)
            self.posSorted(self.tra[frameI][assigment,:])
            ptsOld = ptsNew


        


            


