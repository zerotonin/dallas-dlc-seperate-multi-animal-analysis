import indexTools
import numpy as np
class trajectory_corrector:
    
    def __init__(self,trajectory,artifactList):

        self.tra     = trajectory
        self.traLen,self.coordNo  = trajectory.shape[:]
        self.artifactList = artifactList

        self.artSequences = indexTools.bracket_Bools(artifactList)
        self.artSequences = indexTools.boolSequence2startEndIndices(self.artSequences)
        self.artSequences = indexTools.bracket_StartsEndOfSequence(self.artSequences,self.traLen)
        self.artSeqLen = self.artSequences.shape[0]



    def interpolateOverArtifacts(self):

        for i in range(self.artSeqLen):

            start = self.checkStart4Artifact(self.artSequences[i,0])
            end = self.checkStart4Artifact(self.artSequences[i,1])

            if start == 0:
                self.interpolateAtStart(end)
            elif end == self.traLen:
                self.interpolateAtEnd(start)
            else:
                self.interpolateTra(start,end)

    def checkEnd4Artifact(self,index):
        while self.artifactList[index] == True and index < self.traLen:
            index += 1
        return index

    def checkStart4Artifact(self,index):
        while self.artifactList[index] == True and index > 0:
            index -= 1
        return index
 

    def interpolateAtStart(self, endOfSequence):
        steps = endOfSequence+1
        self.tra[0:endOfSequence+1,:] = np.kron(np.ones((steps,1)),self.tra[endOfSequence,:]) 

    def interpolateAtEnd(self, startOfSequence):
        steps = self.traLen-startOfSequence
        self.tra[startOfSequence:self.traLen,:] = np.kron(np.ones((steps,1)),self.tra[startOfSequence,:]) 
               

    def interpolateTra(self, startOfSequence, endOfSequence):
        startCoords = self.tra[startOfSequence,:]
        endCoords   = self.tra[endOfSequence,:]
        steps       = endOfSequence-startOfSequence +1

        for coordI in range(self.coordNo):
            self.tra[startOfSequence:endOfSequence+1,coordI] = np.linspace(startCoords[coordI],endCoords[coordI],steps)
