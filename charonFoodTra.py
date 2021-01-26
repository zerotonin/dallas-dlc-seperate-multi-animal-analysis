class readCharonFood54():
    def __init__(self,filePosition):

        self.filePosition = filePosition
        self.rawTextData  = []
        #self.readFile()

    def readFoodRecResult(self):
        file1 = open(self.filePosition, 'r') 
        self.rawTextData = file1.readlines() 


    def splitLineIntoImageObjects(self,line):
        objectList = line.split('>')
        del(objectList[0]) # first entry is frameNumber
        return objectList

    def getFrameNumberFromLine(self,line):
        objectList = line.split('>')
        frameNumber = int(objectList[0][0:-3])
        return frameNumber

    def readImageObject(self,imageObjectString):
        objectValList=imageObjectString.split(',')
        objectValList[5]= objectValList[5][0:-2]
        for i in range(1,6):
            objectValList[i]= float(objectValList[i])

        return objectValList

    def imObjectVal2imObjDict(self,objectValList):
        imObjName = objectValList[0]
        quality   = objectValList[1]
        boundingBoxCoordinates = tuple(objectValList[2::])   
        x,y = self.boundingBox2centerOfMass(boundingBoxCoordinates)
        return {'name':imObjName,'centerOfMass': (x,y), 'quality': quality, 'boundingBox': boundingBoxCoordinates}

    def boundingBox2centerOfMass(self,boundingBoxCoordinates):
        x = (boundingBoxCoordinates[0]+boundingBoxCoordinates[2])/2.0
        y = (boundingBoxCoordinates[1]+boundingBoxCoordinates[3])/2.0
        return x,y
    
    def readImObjPerLine(self,line): 
        imageObjects  = self.splitLineIntoImageObjects(line)  
        frameNumber   = self.getFrameNumberFromLine(line)
        imObjList = [frameNumber]
        for imObj in imageObjects:
            objectValList = self.readImageObject(imObj)
            imObjDict     = self.imObjectVal2imObjDict(objectValList)
            imObjList.append(imObjDict)       
        return imObjList

    def convertRecordingtoListDict(self):
        self.imObjData = list()
        for line in self.rawTextData:
            self.imObjData.append(self.readImObjPerLine(line))

    def readFile(self):
        self.readFoodRecResult()
        self.convertRecordingtoListDict()
    
paul= readCharonFood54('foodTestTra.tra') 
paul.readFile()