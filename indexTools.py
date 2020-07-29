import numpy as np


def bool2indice(boolList):
    return np.array([i for i, x in enumerate(boolList) if x])

def bracketBools(boolList):

    for i in range(1,len(boolList)-1):
        if boolList[i] == 1:
            boolList[i-1],boolList[i+1] = (True,True)
    return boolList

def indiceSeq2startEnd(indiceList):
    indDiff = np.diff(indiceList)
    starts = [indiceList[0]]
    ends = list()
    for i in range(1,len(indiceList)):
        if indDiff[i-1] !=1:
            ends.append(indiceList[i-1])
            starts.append(indiceList[i])
    ends.append(indiceList[i])
    return np.array(list(zip(starts,ends)))

def boolSequence2startEndIndices(boolList):
    indices = bool2indice(boolList)
    return indiceSeq2startEnd(indices)
