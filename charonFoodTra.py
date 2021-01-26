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
    pass


data = readFoodRecResult('foodTestTra.tra') 
imageObjects = splitLineIntoImageObjects(data[5])  
frameNumber  = getFrameNumberFromLine(data[5])       