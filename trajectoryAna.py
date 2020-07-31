import numpy as np
from scipy import interpolate

class trajectoryAna():
    
    def __init__(self,trajectory,fps,pix2mmObj):
        self.trajectory = trajectory 
        self.fps        = fps        
        self.pix2mmObj  = pix2mmObj  


class pix2mm():

    def __init__(self,pixArray,mmArray = None,mode = 'box',arenaType = None):
        self.mmArray      = mmArray  
        self.pixArray     = pixArray 
        self.mode         = mode 
        self.arenaType    = arenaType
        self.pix2mmFactor = None

    
    def pix2mm(self, pixTra):
        if self.mmArray == None:
            print('You have to first define a mmArray')
            mmTra =  None
        else:
                
            if mode == 'box':
                mmTra = self.pix2mm_box(pixTra)
            elif mode == 'line':
                mmTra = self.pix2mm_line(pixTra)
            elif mode == 'circle':
                mmTra = self.pix2mm_circle(pixTra)
            else:
                self.raiseExceptionFlag('conversion type',self.mode)
                mmTra = None

        return mmTra
        
    def pix2mm_box(self,pixTra):
        pixLen = np.linalg.norm(np.diff(pixTra[0:2,:],axis =0))  
        mmLen = np.linalg.norm(np.diff(self.mmArray[0:2,:],axis =0))  
        self.pix2mmFactor = mmLen/pixLen

        xx, yy = np.meshgrid(self.pixArray[:,0],self.pixArray[:,1])
        intX_func = interpolate.interp2d(x, y, self.mmArray[:,0], kind='cubic')
        intY_func = interpolate.interp2d(x, y, self.mmArray[:,1], kind='cubic')

        mmX = intX_func(pixTra[:,0])
        mmY = intY_func(pixTra[:,1])
        return (mmX,mmY)


    def pix2mm_circle(self,pixTra):
        print('Not Implemented YET')
        return None

    def pix2mm_line(self,pixTra):
        pixLen = np.linalg.norm(np.diff(pixTra,axis =0))  
        mmLen = np.linalg.norm(np.diff(self.mmArray,axis =0))  
        self.pix2mmFactor = mmLen/pixLen

        return pixTra*self.pix2mmFactor
        
    def getMM_Standard(self,arena = self.arenaType):
        if mode == 'box':
            self.get_mmBox_standardArenas(arena)
        elif mode == 'line':
            self.get_mmLine_standardArenas(arena)
        elif mode == 'circle':
            self.get_mmCirc_standardArenas(arena)
        else:
            self.raiseExceptionFlag('arena type',arenaType)
    
    def get_mmBox_standardArenas(self,arena):

        if arena == 'smallBenzer':
            self.mmArray = ((0,0),(90,0),(90,73),(0,73))
        else:
            self.raiseExceptionFlag('arena',arena)

    def get_mmCirc_standardArenas(self,arena):
        print('Not Implemented YET')
    def get_mmLine_standardArenas(self,arena):
        print('Not Implemented YET')


    def raiseExceptionFlag(self,flag,flagVar):
            raise Exception('Unknown '+ flag +' type: ' + flagVar)


        