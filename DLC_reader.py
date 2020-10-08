import pandas,tqdm,copy,trajectory_correcter
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class DLC_H5_reader:
    def __init__(self,filePosition,animalNo):
        self.fPos = filePosition
        self.animalNo = animalNo
        self.pandasDF = None
        self.frameNo  = None  
        self.columns  = None
        self.areaNo   = None  
        self.tra      = None
    
    def readH5(self):
        self.pandasDF = pandas.read_hdf(self.fPos)
        self.frameNo  = self.pandasDF.shape[0]  
        self.columns  = self.pandasDF.shape[1]
        self.areaNo   = int(self.columns/3)  
    
    def multiAnimal2numpy(self):
        self.tra = list()
        for frameI in tqdm.tqdm(range(self.frameNo),desc ='reading '+self.fPos):
            frameRes = self.pandasDF.iloc[frameI].iloc[:] 
            frameRes = frameRes.to_numpy()  
            frameRes = np.reshape(frameRes,(self.areaNo,-1))  
            frameRes = np.reshape(frameRes,[self.animalNo,int(self.areaNo/self.animalNo),3])   
            self.tra.append(frameRes)
        self.tra = np.array(self.tra)

    def singleAnimal2numpy(self):
        self.tra = list()
        for frameI in tqdm.tqdm(range(self.frameNo),desc ='reading '+self.fPos):
            frameRes = self.pandasDF.iloc[frameI].iloc[:] 
            frameRes = frameRes.to_numpy()  
            frameRes = np.reshape(frameRes,(self.areaNo,-1))  
            frameRes = np.reshape(frameRes,[self.areaNo,3])   
            self.tra.append(frameRes)
        self.tra = np.array(self.tra)

class DLC_CSV_reader:
    def __init__(self,filePosition,animalNo,bodyPartNo):
        self.fPos = filePosition
        self.animalNo = animalNo
        self.bodyPartNo = bodyPartNo
        self.csvData  = None
        self.frameNo  = None  
        self.columns  = None
        self.areaNo   = None  
        self.tra      = None

    def readCSV(self):
        #reads in csv trajectory
        self.csvData = np.genfromtxt(self.fPos,dtype=float,delimiter=',')
        self.csvData = self.csvData[3:,:] # gets rid off DLC names
        self.csvData = self.csvData[:,1:] # gets rid off frame counter

        # now this has to be arranged into a tra structure. A tra numpy matrix has 
        # in its first dimension the frames, 2nd animals, 3rd bodyparts, 4th x,y-coordinates and quality

        # First built up bodyparts than animals than frames

        self.frameNo  = self.csvData.shape[0]  
        self.columns  = self.csvData.shape[1]
        # test if the data is in accordance with the predicted number of animals and bodyparts
        if self.animalNo != self.columns/(self.bodyPartNo*3): # 3 coordinates per bodyPart
            raise ValueError('The DLC CSV file has a different number of columns than was predicted by animalNo and bodyPartNo!')
        else:
            self.tra = np.reshape(self.csvData,(self.frameNo,self.animalNo,self.bodyPartNo,3))
            self.areaNo   = self.animalNo   # to have all fields that the h5 reader has
    

        
    
class multiAnimalEval:
    def __init__(self,tra3,arenaCoords,slotNo = 15):
        self.tra = tra3
        self.slotNo = slotNo
        self.arenaCoords = arenaCoords
        self.sortBoxCoordsClockWise()
        self.frameNo,self.animalNo,self.bodyPartNo,self.coordNo = tra3.shape[:]
        self.coordNo -=1
        self.posSorted= list()
        self.accuracyThreshold = 0.95

    def thresholdAcc(self,areaCoords):
        idx = np.nonzero(areaCoords[:,2]>=self.accuracyThreshold)
        return idx[0]  

    def calcBodyLen(self):
        self.bodyLength = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in tqdm.tqdm(range(self.frameNo),desc = 'body length test'):
            for animalI in range(self.animalNo):
                animal = self.tra[frameI,animalI,:,0:self.coordNo]
                self.bodyLength[frameI,animalI] = np.linalg.norm(np.diff(animal,axis=0)) 

    def testBodyLen(self, lenThreshold):
        self.calcBodyLen()
        lengthDiff = self.bodyLength/np.median(self.bodyLength.flatten())
        return lengthDiff > lenThreshold
        #self.lengthDiff = np.abs(normBL -1)    
    
    def calcMaxStepSize(self):
        self.step = np.zeros(shape=(self.frameNo,self.animalNo))
        for frameI in tqdm.tqdm(range(1,self.frameNo),desc='step size test'):
            for animalI in range(self.animalNo):
                tempSteps = []
                for bodyPartI in range(self.bodyPartNo):
                        bpCoord = self.tra[frameI-1:frameI+1,animalI,bodyPartI,0:self.coordNo]   
                        tempSteps.append(np.linalg.norm(np.diff(bpCoord,axis=0)))
                self.step[frameI,animalI] = max(tempSteps)

    def testStepSize(self,percentile):
        self.calcMaxStepSize()
        stepThreshold = np.percentile(self.step.flatten(),percentile)
        return self.step > stepThreshold
    
    def testForArtifacts(self, stepThreshPerc = 99, bodyThresh= 2):
        stepSizeCandidates = self.testStepSize(stepThreshPerc)
        positionCandidates = self.positionTest()
        bodyLenCandidates  = self.testBodyLen(bodyThresh)

        self.artifactCandidates = bodyLenCandidates | stepSizeCandidates | positionCandidates

 


    def interpOverArtifacts(self):
        for animalI in tqdm.tqdm(range(self.animalNo),desc='trajectory correction'):
            if self.artifactCandidates[:,animalI].any() == True:
                for bodyPartI in range(self.bodyPartNo):
                    z = trajectory_correcter.trajectory_corrector(self.tra[:,animalI,bodyPartI,0:self.coordNo],self.artifactCandidates[:,animalI])
                    z.interpolateOverArtifacts()
                    self.tra[:,animalI,bodyPartI,0:self.coordNo] = z.tra

    def pointInPolygon(self,bodyCoord,slotCoord):
        bodyCoord = Point(bodyCoord[0],bodyCoord[1])
        slotCoord = Polygon([(slotCoord[0,0],slotCoord[0,1]),(slotCoord[1,0],slotCoord[1,1]),
                            (slotCoord[2,0],slotCoord[2,1]),(slotCoord[3,0],slotCoord[3,1])])
        return slotCoord.contains(bodyCoord)
    
    def calculateSlotCoords(self):
        

        upperXCoords = np.linspace(self.arenaCoords[0,0],self.arenaCoords[1,0],self.slotNo+1,endpoint=True)   
        upperYCoords = np.linspace(self.arenaCoords[0,1],self.arenaCoords[1,1],self.slotNo+1,endpoint=True) 
        lowerXCoords = np.linspace(self.arenaCoords[3,0],self.arenaCoords[2,0],self.slotNo+1,endpoint=True)   
        lowerYCoords = np.linspace(self.arenaCoords[3,1],self.arenaCoords[2,1],self.slotNo+1,endpoint=True)
        self.slotCoord = list() 
        for animalI in range(self.animalNo):
            xPts = [lowerXCoords[animalI],lowerXCoords[animalI+1],upperXCoords[animalI+1],upperXCoords[animalI]]
            yPts = [lowerYCoords[animalI],lowerYCoords[animalI+1],upperYCoords[animalI+1],upperYCoords[animalI]]
            self.slotCoord.append(np.array(list(zip(xPts,yPts))))

    def positionTest(self):
        self.calculateSlotCoords()
        posCandidates = np.zeros(shape=(self.frameNo,self.animalNo),dtype=bool)   
        for frameI in tqdm.tqdm(range(self.frameNo),desc='position test'):
            for animalI in range(self.animalNo):
                allInPolygon = list()
                for bodyPartI in range(self.bodyPartNo):
                    allInPolygon.append(self.pointInPolygon(self.tra[frameI,animalI,bodyPartI,0:self.coordNo],self.slotCoord[animalI]))
                if not all(allInPolygon):
                    posCandidates[frameI,animalI] = True 
        return posCandidates
    
    def positionSorting(self):
        self.calculateSlotCoords()
        for frameI in tqdm.tqdm(range(self.frameNo),desc='position sorting'):
            headSlotList =  [ [] for _ in range(self.slotNo) ]
            abdoSlotList =  [ [] for _ in range(self.slotNo) ]
            pointList = list(self.tra[frameI,:,:,:])
            for slotPosI in range(self.slotNo):
                for point in pointList:
                     if self.pointInPolygon(point[0,0:2],slotCoord):
                         headSlotList[slotPosI].append(copy.deepcopy(point))
                         point[0] = -1

                     if self.pointInPolygon(point[1,0:2],slotCoord):
                         abdoSlotList[slotPosI].append(copy.deepcopy(point))
                         point[0] = -1
            
            pointList = list()
            for slotPosI in range(self.bodyPartNo,self.coordNo):
                point = np.zeros(shape=(self.bodyPartNo))
                if not headSlotList[slotPosI]:
                    point[0,:] = np.array([np.nan,np.nan,np.nan])
                else:
                    temp = np.array(headSlotList[slotPosI])
                    point[0,:] = temp[temp[:,-1].argmax(),:]      

                if not abdoSlotList[slotPosI]:
                    point[0,:] = np.array([np.nan,np.nan,np.nan])
                else:
                    temp = np.array(abdoSlotList[slotPosI])
                    point[0,:] = temp[temp[:,-1].argmax(),:]     





    def sortBoxCoordsClockWise(self):
        arenaC = self.arenaCoords[self.arenaCoords[:, 0].argsort()]   
        sortedCoordinates = np.zeros(shape = arenaC.shape)
        if arenaC[0,1] < arenaC[1,1]:
            sortedCoordinates[0,:] = arenaC[0,:]
            sortedCoordinates[3,:] = arenaC[1,:]
        else:
            sortedCoordinates[0,:] = arenaC[1,:]
            sortedCoordinates[3,:] = arenaC[0,:]

        if arenaC[2,1] < arenaC[3,1]:
            sortedCoordinates[1,:] = arenaC[2,:]
            sortedCoordinates[2,:] = arenaC[3,:]
        else:
            sortedCoordinates[1,:] = arenaC[3,:]
            sortedCoordinates[2,:] = arenaC[2,:]
        self.arenaCoords = sortedCoordinates



