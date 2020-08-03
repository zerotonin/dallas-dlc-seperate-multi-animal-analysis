import copy
import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
class trajectoryAna():
    
    def __init__(self,trajectory,fps,pix2mmObj):
        self.pixTra     = trajectory 
        self.frameNo,self.bodyPartNo, self.coordNo = self.pixTra.shape
        self.fps        = fps        
        self.pix2mmObj  = pix2mmObj 
        self.bodyTurner = bodyDirectionCorrector(self)
        self.bodyTurner.sortBodyPartsByProximity()
    
    def convert2mm(self): 
        self.mmTra = np.zeros(shape = self.pixTra.shape)
        for i in range(self.bodyPartNo):
            self.mmTra[:,i,:] = self.pix2mmObj.convertPix2mm(self.pixTra[:,i,:])
    
    
    def smoothTraGauss(self):
        self.mmTraSmooth= np.zeros(shape=self.mmTra.shape)
        for bodyI in range(self.bodyPartNo):
            for coordI in range(self.coordNo):
                self.mmTraSmooth[:,bodyI,coordI] = gaussian_filter1d(self.mmTra[:,bodyI,coordI], 5)
    
    def calculateYaw(self):
        self.yaw = np.zeros(shape=(self.frameNo,))
        directionVector = self.mmTraSmooth[:,0,:] - self.mmTraSmooth[:,-1,:]
        for i in range(self.frameNo):
            self.yaw[i] = np.math.atan2(directionVector[i,1],directionVector[i,0])
        self.yaw = np.unwrap(self.yaw)




class bodyDirectionCorrector():
    def __init__(self,traObj):
        self.tra = traObj.pixTra
        self.swapCounter = 0
        self.swapIDX = list()

    def sortBodyPartsByProximity(self):
        self.swapCounter = 0
        frameNo = self.tra.shape[0]
        for frameI in range(1,frameNo):
            ptsNew = self.tra[frameI,:,:]
            ptsOld = self.tra[frameI-1,:,:]
            assignmentOld, assignmentNew = self.Hungarian(ptsOld,ptsNew)
            if assignmentNew[0] == 1:
                self.tra[frameI,:,:] = self.tra[frameI,assignmentNew,:]
                self.swapCounter += 1
                self.swapIDX.append(frameI)
        
        if self.swapCounter > frameNo/2:
            self.tra = self.tra[:,[1,0],:]
            


    
    def Hungarian(self,ptsA,ptsB):
            C = cdist(ptsA,ptsB, 'euclidean')
            assignmentOld, assignmentNew = linear_sum_assignment(C)
            return assignmentOld, assignmentNew



class pix2mm():

    def __init__(self,pixArray,arenaType,mode = 'box',mmArray = np.nan):
        self.mmArray      = mmArray  
        self.pixArray     = pixArray 
        self.mode         = mode 
        self.arenaType    = arenaType
        self.pix2mmFactor = None

    
    def convertPix2mm(self, pixTra):

        if np.isnan(self.mmArray).any():
            print('You have to first define a mmArray')
            mmTra =  None
        else:
                
            if self.mode == 'box':
                mmTra = self.pix2mm_box(pixTra)
            elif self.mode == 'line':
                mmTra = self.pix2mm_line(pixTra)
            elif self.mode == 'circle':
                mmTra = self.pix2mm_circle(pixTra)
            else:
                self.raiseExceptionFlag('conversion type',self.mode)
                mmTra = None

        return mmTra
        
    def pix2mm_box(self,pixTra):
        pixLen = np.linalg.norm(np.diff(self.pixArray[0:2,:],axis =0))  
        mmLen = np.linalg.norm(np.diff(self.mmArray[0:2,:],axis =0))  
        self.pix2mmFactor = mmLen/pixLen

        points = np.array( (self.pixArray[:,0].flatten(), self.pixArray[:,1].flatten()) ).T
        mmXvalues = self.mmArray[:,0].flatten()
        mmYvalues = self.mmArray[:,1].flatten()

        mmX = griddata( points, mmXvalues, (pixTra[:,0],pixTra[:,1]) )
        mmY = griddata( points, mmYvalues, (pixTra[:,0],pixTra[:,1]) )

     
            
        return np.vstack((mmX,mmY)).T  


    def pix2mm_circle(self,pixTra):
        print('Not Implemented YET')
        return None

    def pix2mm_line(self,pixTra):
        pixLen = np.linalg.norm(np.diff(pixTra,axis =0))  
        mmLen = np.linalg.norm(np.diff(self.mmArray,axis =0))  
        self.pix2mmFactor = mmLen/pixLen

        return pixTra*self.pix2mmFactor
        
    def getMM_Standard(self):
        if self.mode == 'box':
            self.get_mmBox_standardArenas(self.arenaType)
        elif self.mode == 'line':
            self.get_mmLine_standardArenas(self.arenaType)
        elif self.mode == 'circle':
            self.get_mmCirc_standardArenas(self.arenaType)
        else:
            self.raiseExceptionFlag('arena type',self.arenaType)
    
    def get_mmBox_standardArenas(self,arena):

        if arena == 'smallBenzer':
            self.mmArray = np.array(((0,73),(90,73),(90,0),(0,0)))
        else:
            self.raiseExceptionFlag('arena',arena)

    def get_mmCirc_standardArenas(self,arena):
        print('Not Implemented YET')
    def get_mmLine_standardArenas(self,arena):
        print('Not Implemented YET')


    def raiseExceptionFlag(self,flag,flagVar):
            raise Exception('Unknown '+ flag +' type: ' + flagVar)


        