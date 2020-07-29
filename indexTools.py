import numpy as np

class indexTools:
    def __init__(self):
        pass

    def bool2indice(boolList):
       return np.array([i for i, x in enumerate(boolList) if x])

    def indiceSeq2startEnd(indiceList):
        indDiff = np.diff(indiceList)
        starts = [indiceList[0]]
        ends = list()
        for i in range(1,len(indiceList)):
            if indDiff[i] !=1:
                ends.append(indiceList[i-1])
                starts.append(indiceList[i])
        ends.append(indiceList[i])
