import os, getopt,sys
import charonFoodTra,splitCharonMultiAnimalTra
import numpy as np 
from tqdm import tqdm
import pandas as pd
import cv2 as cv

class readMultiAnimalCharonTra:
    def __init__(self,traFile,movFile,bboxFile,arenaHeightmm,arenaWidthmm,maxReads=-1):
        self.traFile   = traFile
        self.movFile   = movFile
        self.bboxFile  = bboxFile
        self.maxReads  = maxReads
        self.arenaHeightmm = arenaHeightmm
        self.arenaWidthmm = arenaWidthmm

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

    def cart2pol(self,x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, phi)

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
                obj['coord_mmArena_y'] = coord_relArena_y*self.arenaHeightmm
                obj['coord_mmArena_x'] = coord_relArena_x*self.arenaWidthmm
                rho,phi = self.cart2pol(obj['coord_mmArena_x']-(self.arenaWidthmm/2.0),obj['coord_mmArena_y']-(self.arenaHeightmm/2.0))
                obj['coord_rho'] = rho
                obj['coord_phi'] = phi

    def saveAna(self,arenaFilePos,traFilePos):
        np.savetxt(arenaFilePos,self.meanArenaCoords,delimiter=',')
        dfTrajectory = pd.DataFrame(self.trajectory)   
        dfTrajectory.to_hdf(traFilePos,key='data')
    
    def run(self):
        self.read()
        self.calculateMeanArenaCoords()
        self.coordinateTransform()

if __name__ == '__main__':
    
    # get input variables
    usageStr = 'usage: analyseSingleArenaTra.py -t <traFilePos> -a <arenaBoundingBoxFilePos> -m <movieFilePos> -x <arenaWidthMM> -y <arenaHeightMM> -o <outputDir>'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ht:a:m:x:y:o:",["traFilePos=","arenaBoundingBoxFilePos=",'movieFilePos=',"arenaWidthMM=","arenaHeightMM=",'outputDir='])
        #print(sys.argv)
    except getopt.GetoptError:
        print(usageStr)
        sys.exit(2)

    #parse Inputs
    traFilePos              = False
    arenaBoundingBoxFilePos = False
    movieFilePos            = False

    for o, a in opts:
        # if user asks for help 
        if o == '-h':
            print(usageStr)
        elif o == '-t':
            traFilePos = a
        elif o == '-a':
            arenaBoundingBoxFilePos = a
        elif o == '-m':
            movieFilePos = a
        elif o == '-x':
            arenaWidthMM = float(a)
        elif o == '-y':
            arenaHeightMM = float(a)
        elif o == '-o':
            outputDir = a
    if os.path.isfile(traFilePos) == False:
        raise ValueError(f'-i is not an existing file: {traFilePos} ')
    if os.path.isfile(arenaBoundingBoxFilePos) == False:
        raise ValueError(f'-i is not an existing file: {arenaBoundingBoxFilePos} ')
    if os.path.isfile(movieFilePos) == False:
        raise ValueError(f'-i is not an existing file: {movieFilePos} ')

    fileName     = os.path.basename(traFilePos)[0:-4]   
    cleanTraOut  = os.path.join(outputDir,fileName+'_trajectory.h5')
    meanArenaOut = os.path.join(outputDir,fileName+'_meanArena.csv')
    cmar = readMultiAnimalCharonTra(traFilePos,movieFilePos,arenaBoundingBoxFilePos,arenaHeightMM,arenaWidthMM)
    cmar.run()
    cmar.saveAna(meanArenaOut,cleanTraOut)