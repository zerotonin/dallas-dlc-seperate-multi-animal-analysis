from charonFoodTra import readCharonFood54
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from scipy.optimize import linear_sum_assignment
#from importlib import reload 


def boundingBox2MPLrect(boundingBox,edgeColor, labelStr = ""):
    # Bounding box of an image object is xmin,ymin,xmax,ymax
    # also the y axis is inverse
    # matplotlib patches expects xmin and ymin plus width and height of the box

    # add a rectangle
    rect = mpatches.Rectangle((boundingBox[0],boundingBox[1]),boundingBox[2]-boundingBox[0],boundingBox[3]-boundingBox[1],
                              ec = edgeColor, fc = 'None',label=labelStr)
    return rect

def mplRects4ImgObjList(imgObjList, edgeColor='g', labelTag='imgObj'):
    imgObjRects = list()
    imgObjC = 0
    for imgObj in imgObjList:
        imgObjRects.append(boundingBox2MPLrect(imgObj['boundingBox'],edgeColor, labelTag +'_'+str(imgObjC)))
        imgObjC += 1
    return imgObjRects

def plotRecognisedImgObjBoundBoxes(flyList,arenaList):
    flyRects = []#mplRects4ImgObjList(flyList,edgeColor='b',labelTag ='fly')
    arenaRects = mplRects4ImgObjList(arenaList,edgeColor='g', labelTag ='arena')
    
    fig, ax = plt.subplots()

    collection = PatchCollection(flyRects+arenaRects)
    ax.add_collection(collection)
    
    plt.axis('equal')
   # plt.axis('off')
    #plt.tight_layout()

    plt.show()



def splitImgObjectTypes(frameListWOframeNumber):
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

def assignFlies2Arenas(flyList,arenaList):
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
            fly_x    = fly['centerOfMass'][0]
            fly_y    = fly['centerOfMass'][1]
            arena_x0 = arena['boundingBox'][0]
            arena_x1 = arena['boundingBox'][2]
            arena_y0 = arena['boundingBox'][1]
            arena_y1 = arena['boundingBox'][3]
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




def getArenaAdjMat(sortedArenaList1, arenaList2):
    # pre-allocation of a 54 by 54 matrix
    adjMat = np.zeros(shape=(54,54))
    Frame1ArenaC = 0
    for arena in sortedArenaList1:
        CMx1,CMy1 = arena['centerOfMass']
        

        Frame2ArenaC = 0
        for arena in arenaList2:
            CMx2 = arena['centerOfMass'][0]
            CMy2 = arena['centerOfMass'][1]
            vectorNorm = np.sqrt((CMx1-CMx2)**2+(CMy1-CMy2)**2)
            # returns a List of Distances between Arenas in Frame 1 and each Arena in Frame 2
            adjMat[Frame1ArenaC, Frame2ArenaC] = vectorNorm
            Frame2ArenaC += 1
        Frame1ArenaC += 1
    return adjMat

paul= readCharonFood54('foodTestTra.tra') # init of reader object with file position
paul.readFile()  # read data from file into memory

arenaList1,flyList1,markerList1 = splitImgObjectTypes(paul.imObjData[0][1::])
arenaList2,flyList2,markerList2 = splitImgObjectTypes(paul.imObjData[1][1::])
a2f_assignment1,f2a_assignment1 = assignFlies2Arenas(flyList1,arenaList1)
a2f_assignment2,f2a_assignment2 = assignFlies2Arenas(flyList2,arenaList2)# vectorNorm = getVectorNorm(ar

adjMat = getArenaAdjMat(arenaList1,arenaList2)
print(adjMat)
row_ind, col_ind = linear_sum_assignment(adjMat)
print(row_ind,col_ind)

'''
middle    = list()
leftSite  = list()
rightSite = list()
for fly in f2a_assignment:
    for arena in f2a_assignment:
        fly_x     = fly['centerOfMass'][0]
        arena_xCM = arena['centerOfMass'][0]
        if fly_x < (arena_xCM/2.0):
            leftSite.append(imObj)
        elif fly_x > (arena_xCM/2.0):
            rightSite.append(imObj)
        elif fly_x == (arena_xCM/2.0):
            middle.append(imObj)
'''
'''
def site(flyList, f2a_assignment):

    middle    = list()
    leftSide  = list()
    rightSide = list()
    fly_x        = fly['centerOfMass'][0]
    arena_x0     = arena['boundingBox'][0]
    arena_x1     = arena['boundingBox'][2]
    arena_xCM    = arena['centerOfMass'][0]
    arena_middle = (arena_xCM)/2.0
    
    for a in f2a_assignment:
        extracted_elements = [flyList[index] for index in f2a_assignment[0]] # extract info from flyList for the first fly in f2a_assignmentList
        a = [extracted_elements[fly_x], extracted_elements[arena_middle]]

        if a[0] < a[1]:
            leftSide.append(flyList[index])
        elif a[0] > a[1]:
            rightSide.append(flyList[index])
        elif a[0] == a[1]:
            middle.append(flyList[index])
    
    return middle,rightSite,leftSite
 


def site(flyList, f2a_assignment):

    middle    = list()
    leftSite  = list()
    rightSite = list()
    fly_x        = fly['centerOfMass'][0]
    arena_x0     = arena['boundingBox'][0]
    arena_x1     = arena['boundingBox'][2]
    arena_xCM    = arena['centerOfMass'][0]
    arena_middle = (arena_xCM)/2.0
    
    for a in f2a_assignment:
        if fly_x < arena_middle:
            leftSite.append(a)
        elif fly_x > arena_middle:
            rightSite.append(a)
        elif fly_x == arena_middle:
            middle.append(a)
    
    return middle,rightSite,leftSite
'''
'''
#collect center of Mass from Arenas for all Frames and sort the List by the Framenumber
def collectArenasFromAllFrames (imObjData):
    allArenas=list()
    ArenaC = 0 
    for imgObj in imObjData:
        if imgObj["name"] == 'arena':
            frameNumber = int(imObjData[0][0:-3])
            x_CM = arenaList[ArenaC]['centerOfMass'][0]
            y_CM = arenaList[ArenaC]['centerOfMass'][1]
            Arena_centerOfMass = ((x_CM, y_CM))
            allArenas.append(frameNumber + str (ArenaC) + Arena_centerOfMass)
        ArenaC += 1
    allArenas.sort(key = attrgetter(frameNumber), reverse = True)
    return allArenas
'''
'''
# 1. split 'allArenas' List in Lists of Arenas per Frame

ArenasInFrame_= [[] for a in allArenas]
i=0
for Frame in allArenas:
    if frameNumber==i:
        ArenasInFrame_[i].append(Frame)
    allArenas.remove(Frame) # remove entry from List after appending it to the new List
    i += 1
return ArenasInFrame_[i]



# 2. sort the first frame by x and y coordniates: 
# 2.1 select in each iteration of the for loop the smallest centerofMass from each List, put it in List and delet it from previous List




'''

# middle    = list()
# leftSite  = list()
# rightSite = list()



'''
arenaC    = 0
for assignedFlies in f2a_assignment:
    for fly in assignedFlies:
        fly_x     = flyList[fly]['centerOfMass'][0]
        arena_xCM = arenaList[arenaC]['centerOfMass'][0]
        outputStr = "Arena No " + str(arenaC) + " encompasses fly No " + str(fly) + '. The fly is @ x = ' + str(fly_x) + '. The arena mid line is @ x= ' + str(arena_xCM) +"."
        if fly_x < (arena_xCM/2.0):
            outputStr += "The fly is on the left side."
        elif fly_x > (arena_xCM/2.0):
            outputStr += "The fly is on the right side."
        elif fly_x == (arena_xCM/2.0):
            outputStr += "The fly is in the middle."
        
        print(outputStr)
        arenaC +=1

plotRecognisedImgObjBoundBoxes(flyList,arenaList)
'''

