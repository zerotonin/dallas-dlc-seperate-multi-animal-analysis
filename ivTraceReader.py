import numpy as np
import os,warnings
from tqdm import tqdm

class ivTraceReader:

    def __init__(self,filePosition):
        self.filePosition = filePosition
        self.frameNo      = None
        self.animalNo     = None
        self.traceRaw     = None
        self.trace        = None

    def read_trace(self):
        self.read_ivTraceFile()
        self.determineTraceNumbers()
        self.reshapeTrace()

    def read_ivTraceFile(self):
        self.traceRaw = np.loadtxt(self.filePosition)

    def determineTraceNumbers(self):
        self.frameNo, numCols = self.traceRaw.shape[:]
        self.animalNo  =  (numCols-1)/5
        if self.animalNo.is_integer():
            self.animalNo = int(self.animalNo)
        else:
            warnings.warn("ivTraceReader could not correctly determine the number of animals: " + str(self.animalNo))
    
    def reshapeTrace(self):
        self.trace = np.zeros(shape=(self.frameNo,5,self.animalNo))
        for frameI in tqdm(range(self.frameNo),'reshaping trace'):
            for animalI in range(self.animalNo):
                start = 1 + (animalI*5) # +1 because the first column is the frame No
                stop  = start + 5
                self.trace[frameI,:,animalI] = self.traceRaw[frameI,start:stop]


sourcePath = '/home/bgeurten/DrosoGroup4Frontiers/GroupBehavCorthals/CantonS2013-09-04/14_07_35'
filePos    = os.path.join(sourcePath,'list_script.tra')
ivT =  ivTraceReader(filePos)
ivT.read_trace()
