# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])
import numpy as np
from scipy.optimize import linear_sum_assignment
from operator import attrgetter

class foodArenaAnalysis:
    def __init__(self,videoFrameObjects):
        # This is a list of charonfood54  arena 
        # each mber is a list of  all arenas recognised
        # in that frame. 
        self.frameObjectList = videoFrameObjects
        # this is the preallocation for the template list
        # to which all other frames will be sorted to.
        self.templateArenaList = list()

    # Step 1: sort Frame 1 by its x and y coordinates ...
    # sort Arena list by its x coordinates
    def sortArenaListByXcoordinates(self,arenaList):
        func = lambda x:(x['centerOfMass'][1])
        sortedList = sorted(arenaList, key =func)
        return sortedList

    # sort Arena list by its y coordinates
    def sortArenaListByYcoordinates(self,sortedList):
            func = lambda x:(x['centerOfMass'][0])
            newList = sorted(sortedList, key=func)
            return newList

    # for the 6 similar x values sort after y coordinate
    def sortArenaList(self,list2sort):
        # this delivers 9 groups with 6 members as we have 6 rows and 9 columns
        sortedY    = self.sortArenaListByYcoordinates(list2sort)
        # pre allocate
        sortedList = list()
        # run through each of the 9 groups ....
        for i in range(0,54,6):
            # ...sort them and add them to the sorted list
            sortedList += self.sortArenaListByXcoordinates(sortedY[i:i+6])

        return sortedList


    # The Distances between Arenas in Frame 1 and Arenas in Frame 2 are calculated using the euclidian distance

    def getArenaAdjMat(self,sortedArenaList1, arenaList2):
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

    def hungarianSort(self,templateList,list2sort):
        #get adjency matrix
        adjMat = self.getArenaAdjMat(templateList,list2sort)
        # run min cost perfect matching -> Hungarian
        row_ind, col_ind = linear_sum_assignment(adjMat)
        # return  sorted list2 sort
        return [list2sort[int(x)] for x in list(col_ind)]

    def hungarianSort4Arenas(self,list2sort):
        # now sort candidate list
        return self.hungarianSort(self.templateArenaList,list2sort)   

    def createTemplate(self):

        for currentArenaList in self.frameObjectList:
            #return currentArenaList
            for arenas in currentArenaList:
                if len(currentArenaList) == 54:
                    template = currentArenaList
                    # This function sorts the arenas in western reading direction
                    self.templateArenaList = self.sortArenaList(template)
                    return

        
    def sortAllArenas(self):

        template = self.templateArenaList
        self.sortedArenasList = list()
        for frame in self.frameObjectList:
            self.sortedArenaList.append(hungarianSort(template, frame))
        return self.sortedArenaList

        #     #hungarianSort


        '''  
        frame = 0
        for frame in frameListWOframeNumber:
            currentArenaList,flyList,markerList = splitImgObjectTypes(frameListWOframeNumber[frame][1::])
            #return currentArenaList

            for arenas in currentArenaList:
                if len(currentArenaList) < 54:
                    newList = currentArenaList.append(np.inf,np.inf)
                    sortedList = self.hungarianSort4Arenas(template, newList)
                    return sortedList

                elif len(currentArenaList) == 54:
                    sortedList = hungarianSort4Arenas(template, currentArenaList)
                    return sortedList
        '''

    '''
    if len(currentArenaList) < 54:
        (np.inf,np.inf)

        sortedArenas = hungarianSort4Arenas(template,currentArenaList)
    return sortedList
    '''



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
