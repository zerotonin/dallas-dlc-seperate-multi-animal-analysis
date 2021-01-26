def readFoodRecResult(fileName):
    file1 = open(fileName, 'r') 
    lines = file1.readlines() 
    return lines

def splitLineIntoImageObjects(line):
    objectList = line.split('>')
    del(objectList[0]) # first entry is frameNumber
    return objectList

def getFrameNumberFromLine(line):
    objectList = line.split('>')
    frameNumber = int(objectList[0][0:-3])
    return frameNumber

def readImageObject(imageObjectString):
    objectValList=imageObjectString.split(',')
    objectValList[5]= objectValList[5][0:-2]
    for i in range(1,6):
        objectValList[i]= float(objectValList[i])

    return objectValList

def imObjectVal2imObjDict(objectValList):
    imObjName = objectValList[0]
    quality   = objectValList[1]
    boundingBoxCoordinates = tuple(objectValList[2::])   
    x,y = boundingBox2centerOfMass(boundingBoxCoordinates)
    return {'name':imObjName,'centerOfMass': (x,y), 'quality': quality, 'boundingBox': boundingBoxCoordinates}

def boundingBox2centerOfMass(boundingBoxCoordinates):
    x = (boundingBoxCoordinates[0]+boundingBoxCoordinates[2])/2.0
    y = (boundingBoxCoordinates[1]+boundingBoxCoordinates[3])/2.0
    return x,y



data = readFoodRecResult('foodTestTra.tra') 
imageObjects  = splitLineIntoImageObjects(data[5])  
frameNumber   = getFrameNumberFromLine(data[5])

for imObj in imageObjects:
    objectValList = readImageObject(imObj)
    imObjDict  = imObjectVal2imObjDict(objectValList)       