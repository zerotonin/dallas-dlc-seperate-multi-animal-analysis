import pims,cv2,tqdm
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

            self.fps    = self.media.get(cv2.CAP_PROP_FPS)   
            self.SR_makeIntParameters()
            
        elif(self.modus == 'norpix'):
            self.media = pims.NorpixSeq(filename)
            self.length = len(self.media)-1
            if len(self.media.frame_shape) ==2:
                self.height, self.width  = self.media.frame_shape
            else:
                self.height, self.width, self.colorDim = self.media.frame_shape
                    
            self.fps    = self.media.frame_rate
            self.SR_makeIntParameters()
        elif(self.modus == 'image'):
            # here the programs for image list should follow
            self.media =  pims.ImageSequence(filename)
            self.length = len(self.media)-1
            self.height, self.width, self.colorDim = self.media.frame_shape
            self.fps    = 25   
            self.SR_makeIntParameters()
        else:
            print('MediaHandler:unknown modus')
            
    def SR_makeIntParameters(self):

        self.length = int(self.length)
        self.height = int(self.height)
        self.width  = int(self.width)
        self.size   = (self.height,self.width)

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
    
  
    
    def transcode_seq2avis(self,targetFile):
        if self.modus == 'norpix':
            # Get information about the norpix file
            sourceFPS = round(self.fps)
            frameShape = self.size 
            allocatedFrames = self.media.header_dict['allocated_frames']    

            # Define the codec and create VideoWriter object 
            fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
            out = cv2.VideoWriter(targetFile,fourcc, sourceFPS,frameShape) 

            for frameNo in tqdm.tqdm(range(allocatedFrames),desc='trasconding '+self.fileName):
                frame = self.getFrame(frameNo)
                gray_3c = cv2.merge([frame, frame, frame])
                out.write(gray_3c)
                cv2.imshow('frame',gray_3c)

            out.release()
        else:
            print('This function only works with norpix movie files')
    
    def register_movie(self, targetFile):

        # Get information about the norpix file
        sourceFPS = round(self.fps)
        frameShape = self.size
        allocatedFrames = self.length

        # Define the codec and create VideoWriter object 
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        out = cv2.VideoWriter(targetFile,fourcc, sourceFPS,frameShape)   

        # we take the central frame of the movie as a registration template
        template = self.getFrame(round(allocatedFrames/2))

        for frameNo in tqdm.tqdm(range(allocatedFrames),desc='trasconding '+self.fileName):
            frame = self.getFrame(frameNo)
            regFrame = self.registerImage(template,frame)
            out.write(regFrame)

        out.release()

    def registerImage(self,template,image2match):
        '''
            Image registration based on opbject detection in open cv
            Taken and adapted from: 
            https://www.geeksforgeeks.org/image-registration-using-opencv-python/
        '''
        # Convert to grayscale. 
        img1 = cv2.cvtColor(image2match, cv2.COLOR_BGR2GRAY) 
        img2 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) 
        height, width = img2.shape 

        # Create ORB detector with 5000 features. 
        orb_detector = cv2.ORB_create(5000) 

        # Find keypoints and descriptors. 
        # The first arg is the image, second arg is the mask 
        # (which is not reqiured in this case). 
        kp1, d1 = orb_detector.detectAndCompute(img1, None) 
        kp2, d2 = orb_detector.detectAndCompute(img2, None) 

        # Match features between the two images. 
        # We create a Brute Force matcher with 
        # Hamming distance as measurement mode. 
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 

        # Match the two sets of descriptors. 
        matches = matcher.match(d1, d2) 

        # Sort matches on the basis of their Hamming distance. 
        matches.sort(key = lambda x: x.distance) 

        # Take the top 90 % matches forward. 
        matches = matches[:int(len(matches)*90)] 
        no_of_matches = len(matches) 

        # Define empty matrices of shape no_of_matches * 2. 
        p1 = np.zeros((no_of_matches, 2)) 
        p2 = np.zeros((no_of_matches, 2)) 

        for i in range(len(matches)): 
            p1[i, :] = kp1[matches[i].queryIdx].pt 
            p2[i, :] = kp2[matches[i].trainIdx].pt 

        # Find the homography matrix. 
        homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC) 

        # Use this matrix to transform the 
        # colored image wrt the reference image. 
        transformed_img = cv2.warpPerspective(image2match, homography, (width, height)) 

        # return the matched img
        return transformed_img