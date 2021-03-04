# vectorNorm = getVectorNorm(arenaList1[0],arenaList2[2])
import numpy as np
from scipy.optimize import linear_sum_assignment
from operator import attrgetter
from tqdm import tqdm

class arenaAnalysis:
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
        if len(list2sort) != 54:
            costList = adjMat[row_ind, col_ind]
            # checking the arena that could not have been assigned as it was not detected in the first place
            ind = np.where(costList == 0.)
            dummy = {'name': 'arenaDummy', 'centerOfMass': (0., 0.), 'quality': 0.0, 'boundingBox': (np.nan,np.nan,np.nan,np.nan)}
            for index in ind[0]:
                list2sort.insert(index,dummy)
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

        self.sortedArenaList = list()
        for frame in tqdm(self.frameObjectList,desc='sorting arenas'):
            self.sortedArenaList.append(self.hungarianSort4Arenas(frame))
    
    def runSorter(self):
        self.createTemplate()
        self.sortAllArenas()
        
    def getMedianArenas(self):
        self.runSorter()
        self.medArenaList = list()
        for arenaNum in range(54):

            quality = list()
            centerOfMass = list()
            boundingBox  = list()
            arenaMedDict = dict()
            for frameList in self.sortedArenaList:
                quality.append(frameList[arenaNum]['quality'])
                centerOfMass.append(frameList[arenaNum]['centerOfMass'])
                boundingBox.append(frameList[arenaNum]['boundingBox'])

            arenaMedDict['name'] = 'arena'
            arenaMedDict['centerOfMass'] = np.nanmedian(np.array(centerOfMass),0)
            arenaMedDict['quality'] = np.nanmedian(np.array(quality),0)
            arenaMedDict['boundingBox'] = np.nanmedian(np.array(boundingBox),0)

            self.medArenaList.append(arenaMedDict)

class flyAnalysis:
    from foodArenaAnalysis import arenaAnalysis
    def __init__(self,imgObjData):
        self.imObjData    = imgObjData
        self.video_arena   = list()
        self.video_fly     = list()
        self.video_marker  = list()
        self.medArenaList  = list()
        self.sortedFlyList = list()

    def run(self):
        self.splitImgObjTypes4Video()
        self.arenaSorter  = arenaAnalysis(self.video_arena)
        self.arenaSorter.getMedianArenas()
        self.medArenaList = self.arenaSorter.medArenaList # shorthand
        self.sortFlies2Arena4Video()

    def splitImgObjectTypes(self,frameListWOframeNumber):
        '''
        This function splits the arena, markers, and flies into 3 different lists.

        !WARNING! The frameList must not include the frameNumber
        '''
        #preallocation
        flyList    = list()
        arenaList  = list()
        markerList = list()
        # transverse all image objects and append to according list
        for imgObj in frameListWOframeNumber:
            if imgObj["name"] == 'fly':
                flyList.append(imgObj)
            elif imgObj["name"] == 'arena':
                arenaList.append(imgObj)
            elif imgObj["name"] == 'marker':
                markerList.append(imgObj)
            else:
                raise ValueError("Found unexpected name in image object: " + str(imgObj["name"] ))
        
        return arenaList,flyList,markerList

    def assignFlies2Arenas(self,arenaList,flyList):
        '''
        This function creates two lists one with the assignment fly to arena and
        the inverse arena to fly.
        '''
        #initialize fly counter
        flyC = 0
        # initialize return values as lists of empty lists with the respective length
        a2f_assignment = [[] for a in flyList]
        f2a_assignment = [[] for a in arenaList]
        #transverse all flies
        for fly in flyList:
            #initialize arena counter
            arenaC = 0
            # transverse all arenas
            for arena in arenaList:
                # shorthands
                fly_y,fly_x = fly['centerOfMass']
                arena_y0, arena_x0, arena_y1, arena_x1 = arena['boundingBox']
                # check if flys center of mass is inside the arena bounding box
                if  fly_x >= arena_x0 and fly_x <= arena_x1 and fly_y >= arena_y0 and fly_y <= arena_y1:
                    # append the correct fly indice to the arena list
                    f2a_assignment[arenaC].append(flyC)
                    # append the arena indice to the fly list
                    a2f_assignment[flyC].append(arenaC)
                    
                    break
                #increase arena counter
                arenaC +=1
            #increase fly counter
            flyC+=1
        return a2f_assignment,f2a_assignment

    def sortFlies2Arena4Frame(self,flyList,f2a_assignment):
        temp = list()
        for assignment in f2a_assignment:
            if assignment == []:
                temp.append(None)
            else:
                temp.append(flyList[assignment[0]])
        return temp

    def sortFlies2Arena4Video(self):
        self.sortedFlyList = list()
        for flyList in tqdm(self.video_fly,desc='assign flies to arenas'):         
            a2f_assignment,f2a_assignment =self.assignFlies2Arenas(self.medArenaList,flyList)
            self.sortedFlyList.append(self.sortFlies2Arena4Frame(flyList,f2a_assignment))

            

    def splitImgObjTypes4Video(self):
        self.video_arena  = list()
        self.video_fly    = list()
        self.video_marker = list()
        for frame in self.imObjData:
            arenaList,flyList,markerList = self.splitImgObjectTypes(frame[1::])
            self.video_arena.append(arenaList)
            self.video_fly.append(flyList)
            self.video_marker.append(markerList)
        

