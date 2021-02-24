# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])
import numpy as np
from scipy.optimize import linear_sum_assignment
from operator import attrgetter
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
# sort Arena list by its x coordinates
def sortArenaListByXcoordinates (arenaList):
    func = lambda x:(x['centerOfMass'][1])
    sortedList = sorted (arenaList, key =func)
    return sortedList

# sort Arena list by its y coordinates
def sortArenaListByYcoordinates (sortedList):
        func = lambda x:(x['centerOfMass'][0])
        newList = sorted (sortedList, key=func)
        return newList

# for the 6 similar x values sort after y coordinate
def sortList (sortedList):
    newList2 = list()
    s = sortedList[0:6]
    func = lambda x:(x['centerOfMass'][1])
    s2 = sorted (s, key=func)
    newList2.append(s2)
    return newList2








# The Distances between Arenas in Frame 1 and Arenas in Frame 2 will be calculated using the euclidian distance

def getArenaAdjMat (sortedArenaList1, arenaList2):
    # pre-allocation of a 54 by 54 matrix
    adjMat = np.zeros(shape=(54,54))
    Frame1ArenaC = 0
    for arena in sortedArenaList1:
        CMx1,CMy1 = arena['centerOfMass']
        Frame2ArenaC = 0
        for arena in arenaList2:
            CMx2, CMy2 = arena['centerOfMass']
        
            vectorNorm = np.sqrt((CMx1-CMx2)**2+(CMy1-CMy2)**2)
            # returns a List of Distances between Arenas in Frame 1 and each Arena in Frame 2
            adjMat[Frame1ArenaC, Frame2ArenaC] = vectorNorm
            Frame2ArenaC += 1
        Frame1ArenaC += 1
    return adjMat

adjMat = getArenaAdjMat(arenaList1,arenaList2)
print(adjMat)
row_ind, col_ind = linear_sum_assignment(adjMat)
print(row_ind,col_ind)



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
