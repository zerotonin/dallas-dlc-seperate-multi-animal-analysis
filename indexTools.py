import numpy as np
import copy

def bool2indice(boolList):
    return np.array([i for i, x in enumerate(boolList) if x])

def indiceSeq2startEnd(indiceList):
    indDiff = np.diff(indiceList)
    starts = [indiceList[0]]
    ends = list()
    for i in range(1,len(indiceList)):
        if indDiff[i-1] !=1:
            ends.append(indiceList[i-1])
            starts.append(indiceList[i])
    ends.append(indiceList[-1])
    return np.array(list(zip(starts,ends)))

def boolSequence2startEndIndices(boolList):
    indices = bool2indice(boolList)
    return indiceSeq2startEnd(indices)

def bracket_Bools(boolList):
    returnList = copy.deepcopy(boolList)
    for i in range(1,len(returnList)-1):
        if boolList[i] == 1:
            returnList[i-1],returnList[i+1] = (True,True)
    return returnList

def bracket_StartsEndOfSequence(startEndSequenceInd,seqLen):
    returnList = copy.deepcopy(startEndSequenceInd)
    for seqI in range(returnList.shape[0]):
        
        if returnList[seqI,0] != 0 and returnList[seqI,1] >= seqLen:
            returnList[seqI,0] = returnList[seqI,0]-1
            returnList[seqI,1] = returnList[seqI,1]+1
    return returnList
    
