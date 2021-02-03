class readCharonFood54():
    def __init__(self,filePosition):

        self.filePosition = filePosition #filePosition = file name
        self.rawTextData  = []       # woher kommt rawTextData? muss es nihct als attribut in der funktion (def init) angegeben werden?
        #self.readFile()

    def readFoodRecResult(self):
        file1 = open(self.filePosition, 'r')  # 'r': open for reading
        self.rawTextData = file1.readlines()  # reading row wise 
        print(self.rawTextData)               # and print it into the rawTextData List?

    def splitLineIntoImageObjects(self,line): 
        objectList = line.split('>')  # each object is encapsuilated in ><
        del(objectList[0]) # first entry is frameNumber
        return objectList

    def getFrameNumberFromLine(self,line):
        objectList = line.split('>')
        frameNumber = int(objectList[0][0:-3])
        return frameNumber

    def readImageObject(self,imageObjectString):
        objectValList=imageObjectString.split(',') # object Values are seperated by ','
        objectValList[5]= objectValList[5][0:-2] # 6 object Values (0-5)
        for i in range(1,6):
            objectValList[i]= float(objectValList[i]) # convert string into floating point number

        return objectValList

    def imObjectVal2imObjDict(self,objectValList): # putting objectValues into Dictionary
        imObjName = objectValList[0]
        quality   = objectValList[1]
        boundingBoxCoordinates = tuple(objectValList[2::])   # a Tupel is a finite ordered list of elements
        x,y = self.boundingBox2centerOfMass(boundingBoxCoordinates)
        return {'name':imObjName,'centerOfMass': (x,y), 'quality': quality, 'boundingBox': boundingBoxCoordinates} #dictionary{key:value pairs}

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

    def assingFly2Arena(self): #
        #imObjectVal2imObjDict.get('name')
        imObjName = objectValList[0]
        flyId=0
        for flyId in imObjectVal2imObjDict:
            if imObjName == 'fly':
                flyPosition = imObjectVal2imObjDict.get('centerOfMass')
            flyId += 1
            return flyPosition
            
        ArenaId=0
        for ArenaId in imObjectVal2imObjDict:
            if imObjName == 'Arena':
                ArenaPosition = imObjectVal2imObjDict.get('boundingBoxCoordinates')
            ArenaId += 1
            return ArenaPosition
        
        if flyPosition >= boundingBoxCoordinates[0,1] and flyPosition <= boundingBoxCoordinates[2,3]:
            return flyId, ArenaId 
    

paul= readCharonFood54('foodTestTra.tra') 
paul.readFile() 
