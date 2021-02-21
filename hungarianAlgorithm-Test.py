# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])
# distMat = getAdjacencyMatrix(arenaList,arenaList2)

def getVectorNorm (arenaList):
    ArenaC = 0
    for arena in arenaList:
        CMx = arena['centerOfMass'][0]
        CMy = arena['centerOfMass'][1]
        vectorNorm= vectorNorm = np.sqrt(np.square(CMx)+np.square(CMy))
        ArenaC+=1
        print (ArenaC, ':', vectorNorm)
    