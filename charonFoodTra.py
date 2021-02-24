class readCharonFood54():
    def __init__(self,filePosition):

        self.filePosition = filePosition # filePosition = file name
        self.rawTextData  = []           # preallocation with empty list

    def readFoodRecResult(self):
        file1 = open(self.filePosition, 'r')  # 'r': open for reading
        self.rawTextData = file1.readlines()  # reading row wise 
        #print(self.rawTextData)               # and print it into the rawTextData List?

    def splitLineIntoImageObjects(self,line): 
        '''
        This function splits all objects in a line of raw text data. 
        The strings are split by the > symbol
        Function returns a list of string containing all found objects in this line, but ignores the framenumber.
        '''
        objectList = line.split('>')  # each object is encapsuilated in ><
        del(objectList[0]) # first entry is frameNumber
        return objectList

    def getFrameNumberFromLine(self,line):
        '''
        This function returns the frame number as int from a given text data line.
        '''
        objectList = line.split('>')
        frameNumber = int(objectList[0][0:-3])
        return frameNumber

    def readImageObject(self,imageObjectString):
        '''
        Each object consist out of one string (the object name) and 5 numbers: quality ,x0,y0,x1,y1
        The last for are the minimum and maximum of the bounding box of the object given
        in coordinates normalised to the picture size.
        The string containing this data is seperated by commata and is now split at these and the 
        numerical data are converted into floats. The return value is a list consistent of a string
        and five floats. 
        '''
        objectValList=imageObjectString.split(',') # object Values are seperated by ','
        objectValList[5]= objectValList[5][0:-2] # delete the last two characters of the string ' <'
        # convert all values into float except of the first which is the name of the object already given as a string
        for i in range(1,6):
            objectValList[i]= float(objectValList[i]) # convert string into floating point number
        # return object values in list
        return objectValList

    def imObjectVal2imObjDict(self,objectValList): # putting objectValues into Dictionary
        '''
        This function transforms the list of object values returned by self.readImageObject
        into a dictionary with the following keys and values

        keys         : values
        =============:======================================================================
        name         : a string with the identifier of the object, e.g. 'fly','arena','marker'
        centerOfMass : a tuple holding two floats the x and y coordinate normalised to the 
                       image size 
        quality      : a float with the normalized quality of detection 0->1
        boundingBox  : a tuple of four float with the minimum and maximum coordinates of the 
                       bounding box in the succession (x0,y0,x1,y1)
        '''
        # shorthands for name and quality
        imObjName = objectValList[0]
        quality   = objectValList[1]
        # combine coordinates into a tuple to avoid permutation of coordinates
        boundingBoxCoordinates = tuple(objectValList[2::])   # a Tupel is a finite ordered list of elements
        # caclulate center of mass
        x,y = self.boundingBox2centerOfMass(boundingBoxCoordinates)
        centerOfMass = (x,y) # make tuple to avoid permutation

        # define a dictionary with the data and return it
        return {'name':imObjName,'centerOfMass': centerOfMass, 'quality': quality, 'boundingBox': boundingBoxCoordinates} #dictionary{key:value pairs}

    def boundingBox2centerOfMass(self,boundingBoxCoordinates):
        '''
        To get the middle or center of mass of a bounding box you need to
        calculate the mean of the x-coordinates and y-coordinates respectively.
        '''
        x = (boundingBoxCoordinates[0]+boundingBoxCoordinates[2])/2.0
        y = (boundingBoxCoordinates[1]+boundingBoxCoordinates[3])/2.0
        return x,y
    
    def readImObjPerLine(self,line): 
        # get image objects as list of strings from line
        imageObjects  = self.splitLineIntoImageObjects(line)  
        # get frame number as integer from line
        frameNumber   = self.getFrameNumberFromLine(line)
        # initialize return list with frame number
        imgObjList = [frameNumber]
        # this for loop transverses through the list of string img Obj
        for imgObj in imageObjects:
            # object string is split in different values and numericals are converted to floats
            objectValList = self.readImageObject(imgObj)
            # converts list of data into a structer dict
            imObjDict     = self.imObjectVal2imObjDict(objectValList)
            # add dict to return list
            imgObjList.append(imObjDict)       
        return imgObjList

    def convertRecordingtoListDict(self):
        '''
        Convert the raw text data into a list in which each element is the data of a frame.
        Each frame consists of a list, which first element is the frame number as an integer. All following
        elements are dictionaries in the following format:

        keys         : values
        =============:======================================================================
        name         : a string with the identifier of the object, e.g. 'fly','arena','marker'
        centerOfMass : a tuple holding two floats the x and y coordinate normalised to the 
                       image size 
        quality      : a float with the normalized quality of detection 0->1
        boundingBox  : a tuple of four float with the minimum and maximum coordinates of the 
                       bounding box in the succession (ymin,xmin,ymax,ymin)

        '''
        # preallocation of an empty list
        self.imObjData = list()
        # for loop transverses each line of the file
        for line in self.rawTextData:
            # each line is read and converted into an image object dictionary list and appended to self.imgObjData
            self.imObjData.append(self.readImObjPerLine(line))

    def readFile(self):
        '''
        Main reader class.
        Reads the file at the position stored in self.filePosition.
        The raw text data is stored in a list of strings in self.rawTextData.
        The output list of image object dictionaries is stored in self.imObjData.
        '''
        # read text data from file
        self.readFoodRecResult()
        # convert text data 2 img object dictionaries
        self.convertRecordingtoListDict()

    #def assingFly2Arena(self): #
        #imObjectVal2imObjDict.get('name')
     #   imObjName = objectValList[0]
      #  flyId=0
       # for flyId in imObjectVal2imObjDict:
        #    if imObjName == 'fly':
         #       flyPosition = imObjectVal2imObjDict.get('centerOfMass')
          #  flyId += 1
           # return flyPosition
            
        #ArenaId=0
        #for ArenaId in imObjectVal2imObjDict:
        #    if imObjName == 'Arena':
         #       ArenaPosition = imObjectVal2imObjDict.get('boundingBoxCoordinates')
          #  ArenaId += 1
           # return ArenaPosition
        
       # if flyPosition >= boundingBoxCoordinates[0,1] and flyPosition <= boundingBoxCoordinates[2,3]:
        #    return flyId, ArenaId 
    
