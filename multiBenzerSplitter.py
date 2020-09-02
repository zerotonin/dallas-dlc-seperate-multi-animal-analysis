import mediaHandler,os,tqdm,copy
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import signal
from cv2 import cv2
from vidstab import VidStab

class multiBenzerSplitter():
    def __init__(self,movPos,mediaMode,targetDir='automatic',testFrameNo =10):
        self.movPos    = movPos
        self.patternFrame = False
        self.mediaMode   = mediaMode
        self.targetDir   = targetDir
        self.testFrameNo = testFrameNo
        self.mhObj       = mediaHandler.mediaHandler(self.movPos,self.mediaMode)
        self.unwarpApproxList = list()
        self.monitorList = list()
        self.frameList   = list()

        #stabilizer
        self.patternFrame = self.mhObj.getFrame(self.mhObj.length-1)
        self.orb_detector = cv2.ORB_create(5000) 
        # Find keypoints and descriptors in pattern image
        self.kp2, self.d2 = self.orb_detector.detectAndCompute(self.patternFrame , None) 
        # Hamming distance as measurement mode. 
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 

        #blobdetector
        self.flyDetectorParams = cv2.SimpleBlobDetector_Params()
        # Filter by Area.
        self.flyDetectorParams.filterByArea = True
        #self.flyDetectorParams.minArea = 40
        self.flyDetectorParams.maxArea = 800
        self.flyDetectorParams.filterByColor = True
        self.flyDetectorParams.blobColor = 0
        #self.flyDetectorParams.maxThreshold = 50
        #self.flyDetectorParams.minThreshold = 0
        self.flyDetector = cv2.SimpleBlobDetector_create(self.flyDetectorParams)
        self.flyDetector.empty()
        self.flyDetectionMode = 'simple' # simple or backDiff

        for i in tqdm.tqdm(np.linspace(0,self.mhObj.length-1,self.testFrameNo),desc='loading frames'):
            temp = self.mhObj.getFrame(i)
            self.frameList.append(self.stabiliseFrame(temp))      

        # Constants
        self.MON_NUM          = 4
        self.MON_WIDTH        = 1480
        self.MON_HEIGHT       = 790
        self.TARGET_MON_SIZE  = np.array([ [0,0],[self.MON_WIDTH,0],[self.MON_WIDTH,self.MON_HEIGHT],[0,self.MON_HEIGHT] ],np.float32)
        self.MON_LIMITS       = (95,1430)

        self.LANE_HALF_WIDTH  = 23 
        self.LANE_NUM         = 26


    def rectifyMonitor(self,h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2),dtype = np.float32)
        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]
        hnew[2] = h[np.argmax(add)]
        diff = np.diff(h,axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
        return hnew

    def splitSlideMonitors(self,src):
        return (src[0:512,0:1024],src[0:512,1024:],src[512:,0:1024],src[512:,1024:])

    def undistortFrame(self,src):
        width  = src.shape[1]
        height = src.shape[0]  
        distCoeff = np.zeros((4,1),np.float64)
        distCoeff[0,0] =  0.0000000008 # k1
        distCoeff[1,0] =  0.0000000002 # k2
        distCoeff[2,0] =  0.000001     # p1
        distCoeff[3,0] = -0.00005      # p2

        # assume unit matrix for camera
        cam = np.eye(3,dtype=np.float32)

        cam[0,2] = width/2.0  # define center x
        cam[1,2] = height/2.0 # define center y
        cam[0,0] = 10.        # define focal length x
        cam[1,1] = 10.        # define focal length y

        # here the undistortion will be computed

        UdistImg = cv2.undistort(src,cam,distCoeff)
        return UdistImg

    def approxAndUnwarpMonitor(self,src):
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        # GaussianBlur(src, ksize, sigma1[, dst[, sigma2[, borderType]]]) -> dst
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]) -> dst
        #thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
        ret,thresh = cv2.threshold(gray,30,255,cv2.THRESH_BINARY)


        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Biggest blob is the square we are looking for. Results in 4x1x2 array.
        # First row is the TOP-RIGHT corner. Second row is the TOP-LEFT corner. Third row is the BOTTOM-LEFT corner. Finally, fourth one is the BOTTOM-RIGHT corner. 
        # The problem is that, there is no guarantee that for next image, the corners found out will be in this same order.
        # Change to uniform order with rectify. [TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM-LEFT]
        biggest = None
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 100:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area

        approx = self.rectifyMonitor(biggest)

        

        retval = cv2.getPerspectiveTransform(approx,self.TARGET_MON_SIZE)
        self.unwarpApproxList.append(retval) 
        warp = cv2.warpPerspective(gray,retval,(self.MON_WIDTH,self.MON_HEIGHT))

        return warp


    def extractMonitorsFromFrames(self):
        self.monitorList  = []
        for frameI in range(self.testFrameNo):
            testFrame    = self.frameList[frameI]
            testFrame    = self.undistortFrame(testFrame)
            rawMonitors  = self.splitSlideMonitors(testFrame)
            rectMonitors = list()
            for monitor in rawMonitors:
                rectMonitors.append(self.approxAndUnwarpMonitor(monitor))
            self.monitorList.append(copy.deepcopy(rectMonitors))

    def calculateMonitorXprofile(self):
        self.xProfileList = list()
        for monitorList in self.monitorList:
            profileTemp = list()
            for monitor in monitorList:
                profileTemp.append(np.sum(monitor,axis=0))
            self.xProfileList.append(copy.deepcopy(profileTemp))

    def calculateMeanProfile(self):
        self.meanProfile = np.zeros(shape=(self.MON_WIDTH))
        n = 0
        for xProfileList in self.xProfileList:
            n+=4
            self.meanProfile = self.meanProfile + xProfileList[0]+np.flip(xProfileList[1])+xProfileList[2]+np.flip(xProfileList[3])
        
        self.meanProfile = self.meanProfile/n
        

    def findLaneCenters(self):
        test = self.meanProfile[self.MON_LIMITS[0]:self.MON_LIMITS[1]]
        #sos = signal.butter(1, 2, 'hp', fs=100, output='sos')
        #self.test = signal.sosfilt(sos, test)
        peaks, properties = signal.find_peaks(test,width=10)
        self.laneCentersLeft = peaks + self.MON_LIMITS[0]
        self.laneCentersRight = np.sort(self.laneCentersLeft*-1 +(self.MON_WIDTH-1))
        self.laneCenterProps = properties

    def laneCenters2Borders(self,laneCenterList):
        
        borderList = list()
        for center in laneCenterList:
            borderList.append((center-self.LANE_HALF_WIDTH,center+self.LANE_HALF_WIDTH))

        return borderList


    def findLaneBorders(self):
        self.calculateMonitorXprofile()
        self.calculateMeanProfile()
        self.findLaneCenters()
        if len(self.laneCentersLeft) != self.LANE_NUM:
            if len(self.laneCentersLeft) == 27:
                self.laneCentersLeft  = np.delete(self.laneCentersLeft, 13, None)
                self.laneCentersRight  = np.delete(self.laneCentersRight,13, None)
                self.laneBordersLeft  = self.laneCenters2Borders(self.laneCentersLeft)
                self.laneBordersRight = self.laneCenters2Borders(self.laneCentersRight)
                print('Found 27, delted central center.')
            else:
                print('Found ' +str(len(self.laneCentersLeft) ) + ' expected: ' +str(self.LANE_NUM))
        else: 
            self.laneBordersLeft  = self.laneCenters2Borders(self.laneCentersLeft)
            self.laneBordersRight = self.laneCenters2Borders(self.laneCentersRight)
    
    def splitFileName(self,fPos):
        path, file  = os.path.split(fPos)    
        fName,ext = os.path.splitext(file)  
        return path,fName,ext

    def createTargetNames(self):

        if self.targetDir == 'automatic':
            path,fName,ext = self.splitFileName(self.movPos)
            newFolder = os.path.join(path,fName)
            
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)

            self.targetFileList = list()
            for laneI in  range(self.MON_NUM*self.LANE_NUM):
                newFileName = 'L'+ str(laneI).zfill(3)+'_' + fName+'.avi'
                self.targetFileList.append(os.path.join(newFolder,newFileName))
            self.csvPos = os.path.join(newFolder,'flyTra_' + fName+'.csv')

    def stabiliseFrame(self,frame):

        # Find keypoints and descriptors. 
        # The first arg is the image, second arg is the mask 
        #  (which is not reqiured in this case). 
        kp1, d1 = self.orb_detector.detectAndCompute(frame, None) 

        # Match the two sets of descriptors. 
        matches = self.matcher.match(d1, self.d2) 

        # Take the top 90 % matches forward. 
        matches = matches[:int(len(matches)*90)] 
        no_of_matches = len(matches) 

        # Define empty matrices of shape no_of_matches * 2. 
        p1 = np.zeros((no_of_matches, 2)) 
        p2 = np.zeros((no_of_matches, 2)) 
        
        for i in range(len(matches)): 
            p1[i, :] = kp1[matches[i].queryIdx].pt 
            p2[i, :] = self.kp2[matches[i].trainIdx].pt 
        
        # Find the homography matrix. 
        homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC) 
        
        # Use this matrix to transform the 
        # colored image wrt the reference image. 
        transformed_img = cv2.warpPerspective(frame,homography, (self.mhObj.width, self.mhObj.height)) 
        
        return transformed_img

    def getMeanUnwarping(self):
        self.meanUnwarpFactors = list()
        for i in range(self.MON_NUM):
            self.meanUnwarpFactors.append(np.mean(np.array(self.unwarpApproxList[i::self.MON_NUM]),axis=0))  

    def unwarpAndSplitBasedOnMeanApprox(self,monitors):
        # pre allocate empty list
        lanes = list()

        # unwarp and then split each monitor into lanes
        for monitorI  in range(self.MON_NUM):
            #get correct lane borders
            if (monitorI%2 == 0):
                laneBorders = self.laneBordersLeft
            else:
                laneBorders = self.laneBordersRight
            
            # unwarp monitor
            
            monitor = cv2.cvtColor(monitors[monitorI], cv2.COLOR_BGR2GRAY)
            monitor = cv2.warpPerspective(monitors[monitorI],self.meanUnwarpFactors[monitorI],(self.MON_WIDTH,self.MON_HEIGHT))


            #split lanes
            for laneI in range(self.LANE_NUM):
                lanes.append(monitor[:,laneBorders[laneI][0]:laneBorders[laneI][1]])
        return lanes


    def caclulateLaneBackgrounds(self):
        #calculate brightest background
        frameBG = np.array(self.frameList)    
        self.frameBG = np.max(frameBG,axis = 0) 
        # undistort frame
        self.frameBG    = self.undistortFrame(self.frameBG)
        # split into monitor sub frames
        monitors  = self.splitSlideMonitors(self.frameBG)
        #split monitor into lanes
        self.laneBG = self.unwarpAndSplitBasedOnMeanApprox(monitors)

    def detectFly(self,lane,background, plotFlag):
        if self.flyDetectionMode == 'backDiff':
                
            #make diff image
            diffImage = background-cv2.blur(lane,(5,5))
            #make grayscale and equalize
            gray_3c = cv2.equalizeHist(cv2.cvtColor(diffImage, cv2.COLOR_BGR2GRAY))
            
        if self.flyDetectionMode == 'simple':
            #make grayscale and equalize
            gray_3c = cv2.equalizeHist(cv2.cvtColor(cv2.blur(lane,(5,5)), cv2.COLOR_BGR2GRAY))
        #detect blobs
        #gray_3c = cv2.adaptiveThreshold(gray_3c,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        keypoints = self.flyDetector.detect(gray_3c)
        if plotFlag == True:
            cv2.imshow('image',lane)
            cv2.imshow('detectImage',gray_3c)

        #get largest blob
        if len(keypoints) !=0:
            largestKeyPoint = keypoints[0]
            for keypoint in keypoints:
                if keypoint.size > largestKeyPoint.size:
                    largestKeyPoint = keypoint
        
            markedLane = cv2.drawKeypoints(lane, [largestKeyPoint], np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            return [largestKeyPoint.pt[0],largestKeyPoint.pt[1],largestKeyPoint.size,largestKeyPoint.angle] , markedLane
        else:
            return  [-1,-1,-1,-1] , lane

    def splitMovie(self):
        # Getting Split Info
        self.extractMonitorsFromFrames()
        self.findLaneBorders()
        self.getMeanUnwarping()
        #calculating the backgrounds of the lanes
        self.caclulateLaneBackgrounds()

        # Defining movieParameters for split movies
        self.createTargetNames() # get fileNames
        sourceFPS = round(self.mhObj.fps) # frames per second
        frameShape = (self.LANE_HALF_WIDTH*2+1,self.MON_HEIGHT) #image size
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G') # Define the codec

        # open file dialogues
        writeOutObjectList = list()
        for laneI in  range(self.MON_NUM*self.LANE_NUM):
            writeOutObjectList.append(cv2.VideoWriter(self.targetFileList[laneI],fourcc, sourceFPS,frameShape))

        self.allFlies = list()
        for frameI in tqdm.tqdm(range(self.mhObj.length),desc ='splitting,detecting, trancoding'):  #transformed_img
            frame = self.mhObj.getFrame(frameI)
            # stabilise frame
            frame = self.stabiliseFrame(frame)
            # undistort frame
            frame    = self.undistortFrame(frame)
            # split into monitor sub frames
            monitors  = self.splitSlideMonitors(frame)
            #split monitors into lanes
            lanes = self.unwarpAndSplitBasedOnMeanApprox(monitors)

            fliesPerFrame = list()
            #write frames and detect flies
            for laneI in  range(self.MON_NUM*self.LANE_NUM):
                #detectflies
                fly, markedLane = self.detectFly(lanes[laneI],self.laneBG[laneI],False)
                fliesPerFrame.append(fly)
                #write to movie object
                writeOutObjectList[laneI].write(markedLane)

            self.allFlies.append(copy.deepcopy(fliesPerFrame))

        #release write out object
        for laneI in  range(self.MON_NUM*self.LANE_NUM):
                writeOutObjectList[laneI].release()
        
        #writeOut trajectories
        out = np.array(self.allFlies)  
        out = out.reshape(100,416)
        np.savetxt(self.csvPos, out, delimiter=",")

        

            


            


    def plotStandardAna(self,frameNo):
        monitors = self.monitorList[frameNo]
        profiles = self.xProfileList[frameNo]
        frame    = self.frameList[frameNo]
            

        fig = plt.figure() 
        ax = fig.add_subplot(321)
        ax.imshow(frame)
        ax = fig.add_subplot(322)    
        ax.plot(profiles[0])       
        ax.plot(np.flip(profiles[1]))
        ax.plot(profiles[2])       
        ax.plot(np.flip(profiles[3]))
        ax.plot(self.meanProfile,'k')
        ax.plot(self.laneCentersLeft, self.meanProfile[self.laneCentersLeft], "kx")
        for i in range(4):
            ax = fig.add_subplot(323+i) 
            ax.imshow(monitors[i],cmap='gray')   
            if (i%2 == 0):
                ax.plot(self.laneBordersLeft,np.ones(shape=self.LANE_NUM)*self.MON_HEIGHT/2,'gx')
            else:
                ax.plot(self.laneBordersRight,np.ones(shape=self.LANE_NUM)*self.MON_HEIGHT/2,'gx')

        #fig2 = plt.figure() 
        #ax = fig2.add_subplot(111)
        #ax.plot(self.test)
        
        plt.show()   

                

            