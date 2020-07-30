import pims,cv2
import numpy as np

class mediaHandler():
    def __init__(self,filename,modus,fps=0,bufferSize = 2000):
        self.activeFrame = []
        self.frameNo = 0
        self.modus = modus
        self.buffer = {}
        self.bufferLog = []
        self.bufferSize = bufferSize
        self.fileName = filename
        if (modus == 'movie'):
            self.media  =  cv2.VideoCapture(filename)
            self.length   = self.media.get(cv2.CAP_PROP_FRAME_COUNT) 
            self.height   = self.media.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.width    = self.media.get(cv2.CAP_PROP_FRAME_WIDTH)
            flag,testFrame = self.media.read()
            if len(testFrame.shape) == 3:
                self.colorDim = testFrame.shape[2]

            self.size   = (self.width, self.height)
            self.fps    = 25
            
        elif(self.modus == 'norpix'):
            self.media = pims.NorpixSeq(filename)
            self.length = len(self.media)-1
            if len(self.media.frame_shape) ==2:
                self.height, self.width  = self.media.frame_shape
            else:
                self.height, self.width, self.colorDim = self.media.frame_shape
                    
            self.size   = (self.width, self.height)
            self.fps    = self.media.frame_rate
        elif(self.modus == 'image'):
            # here the programs for image list should follow
            self.media =  pims.ImageSequence(filename)
            self.length = len(self.media)-1
            self.height, self.width, self.colorDim = self.media.frame_shape
            self.size   = (self.width, self.height)
            self.fps    = 25
        else:
            print('MediaHandler:unknown modus')
            
    
    def getFrame(self,frameNo):
        
        if (frameNo <0):
            frameNo = 0
            #print 'frame No was below zero, now set to zero'
            
        elif (frameNo > self.length):
            frameNo = self.length
            #print 'frame No was larger than media length, now set to media length'
            
        # check if frame can be read from buffer    
        if (frameNo in self.bufferLog): 
            self.activeFrame = np.array(self.buffer[frameNo], copy=True)
            self.frameNo     = frameNo
        else:
                
            if (self.modus == 'movie'):
                self.getFrameMov(frameNo)
            elif(self.modus == 'norpix'):
                self.getFrameNorpix(frameNo)
            elif(self.modus == 'image'):
                self.getFrameImage(frameNo)
            else:
                print('MediaHandler:unknown modus')
                
            #delete from buffer if to large
            if (len(self.bufferLog) > self.bufferSize):
                self.buffer.pop(self.bufferLog[0])
                self.bufferLog.pop(0)
                
            #update buffer
            self.buffer[frameNo] = np.array(self.activeFrame, copy=True)
            self.bufferLog.append(frameNo)
                            
        return self.activeFrame
            
    def get_frameNo(self):
        return self.frameNo
    def getFrameMov(self,frameNo):
        
        self.frameNo     = frameNo
        self.media.set(1,frameNo)
        flag,self.activeFrame = self.media.read(frameNo)   
        
    def getFrameNorpix(self,frameNo):
        self.frameNo     = frameNo
        self.activeFrame = self.media.get_frame(frameNo)   
            
    def getFrameImage(self,frameNo):
        self.frameNo     = frameNo
        self.activeFrame = self.media.get_frame(frameNo)   
        
    
    def get_time(self):
        return self.frameNo/self.fps
