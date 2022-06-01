from tqdm import tqdm
import os
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
        Each object consist out of one string (the object name) and 5 numbers: quality ,y0,x0,y1,x1
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
        y,x = self.boundingBox2centerOfMass(boundingBoxCoordinates)
        centerOfMass = (y,x) # make tuple to avoid permutation

        # define a dictionary with the data and return it
        return {'name':imObjName,'centerOfMass': centerOfMass, 'quality': quality, 'boundingBox': boundingBoxCoordinates} #dictionary{key:value pairs}

    def boundingBox2centerOfMass(self,boundingBoxCoordinates):
        '''
        To get the middle or center of mass of a bounding box you need to
        calculate the mean of the x-coordinates and y-coordinates respectively.
        '''
        y = (boundingBoxCoordinates[0]+boundingBoxCoordinates[2])/2.0
        x = (boundingBoxCoordinates[1]+boundingBoxCoordinates[3])/2.0
        return y,x
    
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
        for line in tqdm(self.rawTextData,desc = 'converting text to dict'):
            # each line is read and converted into an image object dictionary list and appended to self.imgObjData
            self.imObjData.append(self.readImObjPerLine(line))

    def readFile_old(self):
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

    def readFile(self,maxReads = -1):
        self.imObjData = list()
        file1 = open(self.filePosition, 'r')
        count = 0
        progressStr='-\|/' 
        while True and (count <= maxReads):
            count += 1
            os.system("printf '\033c'")
            print(f'{progressStr[count%4]} reading line {count}', flush=True)
    
            # Get next line from file
            line = file1.readline()
            # if line is empty end of file is reached
            if not line:
                break
            self.imObjData.append(self.readImObjPerLine(line))
 
        file1.close()
        


        

import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib import cm
import itertools
class plotCharonFood:
    def __init__(self):
        pass

    def boundingBox2MPLrect(self,boundingBox,edgeColor, labelStr = ""):
        # Bounding box of an image object is ymin,xmin,ymax,xmax
        # also the y axis is inverse
        # matplotlib patches expects xmin and ymin plus width and height of the box

        # add a rectangle
        rect = mpatches.Rectangle((boundingBox[1],boundingBox[0]),boundingBox[3]-boundingBox[1],boundingBox[2]-boundingBox[0],
                                edgecolor = edgeColor, fill=False,label=labelStr,linewidth=1)
        return rect

    def mplRects4ImgObjList(self,imgObjList, edgeColor='g', labelTag='imgObj'):
        imgObjRects = list()
        imgObjC = 0
        for imgObj in imgObjList:
            imgObjRects.append(self.boundingBox2MPLrect(imgObj['boundingBox'],edgeColor, labelTag +'_'+str(imgObjC)))
            imgObjC += 1
        return imgObjRects

    def plotRecognisedImgObjBoundBoxes(self,arenaList,flyList):
        objectRects  = self.mplRects4ImgObjList(flyList,edgeColor=[0, 0, 1],labelTag ='fly')
        objectRects += self.mplRects4ImgObjList(arenaList,edgeColor= [1,0,0], labelTag ='arena')
        
        fig, ax = plt.subplots()

        for patch in objectRects:
            ax.add_patch(patch)
        plt.axis('equal')
        plt.show()

    def plotFlyAssignmentControll(self,arenaList,videoFly,step =1):
        # colormap
        plasmaCM  = cm.get_cmap('plasma', 54)
        plasmaCol = plasmaCM.colors
        # make arenas
        objectRects = self.mplRects4ImgObjList(arenaList,edgeColor= [0.5,0.5,0.5], labelTag ='arena')
        # figure window
        fig, ax = plt.subplots()
        # add arena patches
        for patch in objectRects:
            ax.add_patch(patch)
        # add flies
        for flyList in itertools.islice(videoFly,0,None,step):
            for i in range(54):
                if flyList[i] is not None:
                    ax.add_patch(self.boundingBox2MPLrect(flyList[i]['boundingBox'],edgeColor=plasmaCol[i], labelStr = "fly"))

        plt.axis('equal')
        #plt.show()
