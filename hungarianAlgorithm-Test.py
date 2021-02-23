# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])

'''
def getVectorNorm (arenaList):
    VN = list()
    ArenaC = 0
    for arena in arenaList:
        CMx = arena['centerOfMass'][0]
        CMy = arena['centerOfMass'][1]
        vectorNorm = np.sqrt(np.square(CMx)+np.square(CMy))
        ArenaC += 1
        #VN.append('The Vector Norm for ' + str (ArenaC) + 'is: ' + str(vectorNorm))
        VN.append(vectorNorm)
    return (sorted(VN))
'''
# Step 1: sort Frame 1 by its x and y coordinates ...
# The Distances between Arenas in Frame 1 and Arenas in Frame 2 will be calculated using the euclidian distance

def VN_multipleFrames (sortedArenaList1, arenaList2):
    VN_List = list()
    Frame1ArenaC = 1
    for arena in sortedArenaList1:
        CMx1 = arena['centerOfMass'][0]
        CMy1 = arena['centerOfMass'][1]

        Frame2ArenaC = 1
        for arena in arenaList2:
            CMx2 = arena['centerOfMass'][0]
            CMy2 = arena['centerOfMass'][1]
            vectorNorm = np.sqrt(np.square(CMx1-CMx2)+np.square(CMy1-CMy2))
            # returns a List of Distances between Arenas in Frame 1 and each Arena in Frame 2
            VN_List.append((Frame1ArenaC, Frame2ArenaC, vectorNorm))
            Frame2ArenaC += 1
        Frame1ArenaC += 1
    return (VN_List)

# distMat = getAdjacencyMatrix(arenaList1,arenaList2)
def ConvertList2AdjacencyMatrix (VN_List):
    Matrix = np.array(VN_List)
    shape = (54, 54) 
    Matrix.reshape(shape)
    return Matrix  


'''
# Row Reduction
def RowReduction (VN_List):
    minVal=list()
    for VN in VN_List:
        F1AN = VN [0] # Frame1ArenaNumber
        F2AN = VN [1] # Frame2ArenaNumber
        VeNo = VN [2] # Distance
        if F1AN == 1:
            a = min(VN[2])
            minVal.append(a)
        return minVal
        
'''   

#VN_ArenaList1 = getVectorNorm(arenaList1)
#VN_ArenaList1 = getVectorNorm(arenaList2)
#FirstFrameSorted = sorted(VN_ArenaList1)

#print(FirstFrameSorted)

'''
VN_ArenaList1 = getVectorNorm(arenaList1)   #warum wird hier nach dem letzten attribut gesorted und bei dem oberen nach dem ersten?
VN_ArenaList1 = getVectorNorm(arenaList2)
sorted(VN_ArenaList1)
 
VN_ArenaList1
'''