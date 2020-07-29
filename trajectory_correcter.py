import indexTools
import numpy as np
class trajectory_corrector:
    
    def __init__(self,trajectory,artifactList):
        self.tra     = trajectory
        self.traLen  = trajectory.shape[0]
        self.artList = artifactList
        self.artSequences = indexTools.boolSequence2startEndIndices(artifactList)
        self.artSeqLen = self.artSequences.shape[0]

    def interpolateOverArtifacts(self):

        for i in range(self.artSeqLen):

            if self.artSequences[i,0] == 0:
                self.interpolateAtStart(self.artSequences[i,1])
            elif seöf.artSequence[i,1] == self.traLen:
                self.interpolateAtEnd(self.artSequences[i,0])
            else:
                self.interpolateTra(self.artSequences[i,0],self.artSequences[i,1])



    def interpolateAtStart(self, endOfSequence):
        pass

    def interpolateAtEnd(self, startOfSequence):
        pass            

    def interpolateAtEnd(self, startOfSequence,endOfSequence):
        pass            
