from charonFoodTra import readCharonFood54
import numpy as np
#from importlib import reload 



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

for fly in f2a_assignment:
    for fly in a2f_assignment:
        if 'center'
def assignFlies2Arenas(flyList,arenaList):
    '''
    This function creates two lists one with the assignment fly to arena and
    the inverse arena to fly.
    '''
    #initialize fly counter
    flyC = 0
    # initialize return values as lists of empty lists with the respective length
    a2f_assignment = [[] for a in arenaList]
    f2a_assignment = [[] for a in   flyList]
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
                a2f_assignment[arenaC].append(flyC)
                # append the arena indice to the fly list
                f2a_assignment[flyC].append(arenaC)
                
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

# arenaList,flyList,markerList = splitImgObjectTypes(paul.imObjData[1][0::])
# a2f_assignment,f2a_assignment = assignFlies2Arenas(flyList,arenaList)