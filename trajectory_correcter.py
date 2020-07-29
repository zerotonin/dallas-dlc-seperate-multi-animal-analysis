import indexTools
import numpy as np
class trajectory_corrector:
    
    def __init__(self,trajectory,artifactList):

        self.tra     = trajectory
        self.traLen,self.coordNo  = trajectory.shape[:]


        self.artSequences = indexTools.boolSequence2startEndIndices(artifactList)
        self.artSequences = indexTools.bracket_StartsEndOfSequence(self.artSequences,self.traLen)
        self.artSeqLen = self.artSequences.shape[0]



    def interpolateOverArtifacts(self):

        for i in range(self.artSeqLen):

            if self.artSequences[i,0] == 0:
                self.interpolateAtStart(self.artSequences[i,1])
            elif self.artSequence[i,1] == self.traLen:
                self.interpolateAtEnd(self.artSequences[i,0])
            else:
                self.interpolateTra(self.artSequences[i,0],self.artSequences[i,1])



    def interpolateAtStart(self, endOfSequence):
        steps = endOfSequence+1
        self.tra[0:endOfSequence,:] = np.kron(np.ones((steps,1)),self.tra[endOfSequence,:]) 

    def interpolateAtEnd(self, startOfSequence):
        steps = self.traLen-startOfSequence+1
        self.tra[startOfSequence:self.traLen,:] = np.kron(np.ones((steps,1)),self.tra[startOfSequence,:]) 
               

    def interpolateTra(self, startOfSequence, endOfSequence):
        startCoords = self.tra[startOfSequence,:]
        endCoords   = self.tra[endOfSequence,:]
        steps       = endOfSequence-startOfSequence +1

        for coordI in range(self.coordNo):
            self.tra[startOfSequence:endOfSequence,coordI] = np.linspace(startCoords[coordI],endCoords[coordI],steps)
