import charonFoodTra,splitCharonMultiAnimalTra
import numpy as np 
from tqdm import tqdm
import pandas as pd
import cv2 as cv

class readMultiAnimalCharonTra:
    def __init__(self,traFile,movFile,bboxFile,maxReads=-1):
        self.traFile  = traFile
        self.movFile  = movFile
        self.bboxFile = bboxFile
        self.maxReads = maxReads

        self.getFrameParameters()
        self.getRelPos4ArenaPosBBox()
        self.sumArenaCoords = np.zeros(shape=(self.arenaNumber,4))
        self.arenaCoordsOcc = np.zeros(shape=(self.arenaNumber,1),dtype=int)
        
        self.objNameList = ['TC','arena']
        self.trajectory = list()
    
    def getFrameParameters(self):
        self.vidcap = cv.VideoCapture(self.movFile)
        self.totalFrames = int(self.vidcap.get(cv.CAP_PROP_FRAME_COUNT))
        self.frameWidth  = int(self.vidcap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.frameHeight = int(self.vidcap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.vidcap.release()
    
    def getRelPos4ArenaPosBBox(self):
        temp = np.genfromtxt(self.bboxFile,delimiter=',')
        self.arenaPosBbox = temp.copy()
        self.arenaPosBbox[:,1] = temp[:,0]/self.frameWidth
        self.arenaPosBbox[:,3] = temp[:,2]/self.frameWidth
        self.arenaPosBbox[:,0] = temp[:,1]/self.frameHeight
        self.arenaPosBbox[:,2] = temp[:,3]/self.frameHeight

        self.arenaNumber = self.arenaPosBbox.shape[0] 
    
    def read(self):
        reader = charonFoodTra.readCharonFood54(self.traFile)
        
        if self.maxReads == -1:
            readFrames = self.totalFrames
        else:
            readFrames = self.maxReads

        file1 = open(self.traFile, 'r')
        for i in tqdm(range(readFrames)):
            # Get next line from file
            line = file1.readline()
            imgObjList = reader.readImObjPerLine(line)
            scmat = splitCharonMultiAnimalTra.splitCharonMultiAnimalTra(imgObjList,self.arenaNumber,
                    self.objNameList,self.arenaPosBbox,self.sumArenaCoords,self.arenaCoordsOcc) 
            imgObjListClean,self.sumArenaCoords,self.arenaCoordsOcc = scmat.run()
            self.trajectory+=imgObjListClean
        file1.close()


    #get mean Arena Coords
    def getRelativePos(self,posYimg,posXimg,arenaPos):
        posYarena = (posYimg-arenaPos[0]) / (arenaPos[2]-arenaPos[0]) 
        posXarena = (posXimg-arenaPos[1]) / (arenaPos[3]-arenaPos[1])
        return posYarena,posXarena

    def calculateMeanArenaCoords(self):
        self.meanArenaCoords = self.sumArenaCoords/self.arenaCoordsOcc  

    def coordinateTransform(self):
        for obj in tqdm(self.trajectory,desc='coordinate transformation'):
            if obj['coord_relImg_y'] == None:
                obj['coord_relArena_y'] = None
                obj['coord_relArena_x'] = None
            else:
                arenaCoords = self.meanArenaCoords[obj['arenaNo'],:]
                coord_relArena_y,coord_relArena_x = self.getRelativePos(obj['coord_relImg_y'],obj['coord_relImg_x'],arenaCoords)
                obj['coord_relArena_y'] = coord_relArena_y
                obj['coord_relArena_x'] = coord_relArena_x

    def saveAna(self,arenaFilePos,traFilePos):
        np.savetxt(arenaFilePos,self.meanArenaCoords,delimiter=',')
        dfTrajectory = pd.DataFrame(self.trajectory)   
        dfTrajectory.to_hdf(traFilePos,key='data')
    
    def run(self):
        self.read()
        self.calculateMeanArenaCoords()
        self.coordinateTransform()