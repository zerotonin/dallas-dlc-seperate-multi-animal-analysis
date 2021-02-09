from charonFoodTra import readCharonFood54
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
#from importlib import reload 


def boundingBox2MPLrect(boundingBox,edgeColor, labelStr = ""):
    # Bounding box of an image object is xmin,ymin,xmax,ymax
    # also the y axis is inverse
    # matplotlib patches expects xmin and ymin plus width and height of the box

    # add a rectangle
    rect = mpatches.Rectangle((boundingBox[0],boundingBox[1]),boundingBox[2]-boundingBox[0],boundingBox[3]-boundingBox[1],
                              ec = edgeColor, fc = None,label=labelStr)
    return rect

def mplRects4ImgObjList(imgObjList, edgeColor='g', labelTag='imgObj'):
    imgObjRects = list()
    imgObjC = 0
    for imgObj in imgObjList:
        imgObjRects.append(boundingBox2MPLrect(imgObj['boundingBox'],edgeColor, labelTag +'_'+str(imgObjC)))
        imgObjC += 1
    return imgObjRects

def plotRecognisedImgObjBoundBoxes(flyList,arenaList):
    flyRects = mplRects4ImgObjList(flyList,edgeColor='b',labelTag ='fly')
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

paul= readCharonFood54('foodTestTra.tra') # init of reader object with file position
paul.readFile()  # read data from file into memory
# how to adresse data in the imObjData
# readClass.resultList[frameNumber][objectNumber][objectParameter]
# paul.imObjData[3][22]['centerOfMass']

arenaList,flyList,markerList = splitImgObjectTypes(paul.imObjData[1][1::])
a2f_assignment,f2a_assignment = assignFlies2Arenas(flyList,arenaList)
# middle    = list()
# leftSite  = list()
# rightSite = list()
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
            outputStr += "The fly isin the middle side."
        
        print(outputStr)
        arenaC +=1

plotRecognisedImgObjBoundBoxes(flyList,arenaList)
