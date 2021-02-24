# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])
import numpy as np
from scipy.optimize import linear_sum_assignment
from operator import attrgetter

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
def sortArenaList (list2sort):
    # this delivers 9 groups with 6 members as we have 6 rows and 9 columns
    sortedY    = sortArenaListByYcoordinates(list2sort)
    # pre allocate
    sortedList = list()
    # run through each of the 9 groups ....
    for i in range(0,54,6):
        # ...sort them and add them to the sorted list
        sortedList += sortArenaListByXcoordinates(sortedY[i:i+6])

    return sortedList


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

def hungarianSort(templateList,list2sort):
    #get adjency matrix
    adjMat = getArenaAdjMat(templateList,list2sort)
    # run min cost perfect matching -> Hungarian
    row_ind, col_ind = linear_sum_assignment(adjMat)
    # return  sorted list2 sort
    return [list2sort[int(x)] for x in list(col_ind)]

def hungarianSort4Arenas(templateArenaList, list2sort):
    # This function sorts the arenas in western reading direction
    sortedTemplate = sortArenaList(templateArenaList)
    # now sort candidate list
    return hungarianSort(sortedTemplate,list2sort)   

def find54ArenaFrame(allFrames):
    for frame in allFrames:
        a=splitImgObjectTypes(allFrames[frame][1::])
        return arenaList
        for arenas in arenaList:
            if len(arenaList) == 54:
                arenaList = template
    return template


    
def sortAllArenas(allFramers,template):
    '''
    if len(currentArenaList) < 54:
        (np.inf,np.inf)

        sortedArenas = hungarianSort4Arenas(template,currentArenaList)
    return sortedList
    '''

    pass


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
