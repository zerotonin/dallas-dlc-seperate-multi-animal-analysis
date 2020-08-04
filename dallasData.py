import numpy as np
import yaml,json,os

class dallasData():
    def __init__(self,traAnaObj,flyID,moVFpos,dlcFPos,saveDir,collection='Experiment',
                 recordDate='XX-XX-XX__XX-XX-XX'):
        self.flyID                = flyID # lane No
        self.trajectory           = []     # trajectory of this fly
        self.frameNo              = np.nan # number of frames in movies
        self.animalNo             = np.nan # number of animals in movies
        self.bodyPartsNo          = np.nan # number of traced body parts
        self.coordNo              = np.nan # number of coords 
        self.framesPerSecond      = np.nan # sample rate of recording
        self.speedClimb           = (np.nan,np.nan,np.nan,np.nan) # min,mean,median,max [mm/s]
        self.speedSumABS          = (np.nan,np.nan,np.nan,np.nan) # min,mean,median,max [mm/s]
        self.speedThrust          = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [mm/s]
        self.speedSlip            = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [mm/s]
        self.speedYaw             = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [deg/s]
        self.predominantBodyAngle = np.nan # mean [deg]
        self.dropNo               = np.nan # number of times the animal fell
        self.activity             = np.nan # percentage the animal was active during movie
        self.crossedMidLine       = (False,None)  # did the fly cross the midline -> classic Benzer 
        self.reachedTop           = (False,None)  # did the fly reach the 90% height line
        self.pix2mmFactor         = np.nan # pixel 2 mm convertion factor
        self.movieFileName        = moVFpos # file location of the movie
        self.collection           = collection # collection tag e.g. Anka1
        self.recordingDate        = recordDate # date and time of recording
        self.dlcFileName          = dlcFPos
        self.anaObjFileName       = '' # file location of the pickle object 
        self.traCSVFileName       = '' # file location of the flies tra file
        self.traAnaObj            = traAnaObj
        self.saveDir              = saveDir
        self.autoMakeSavePositions()
    

    def traAnaObj2DataObj(self):

        self.frameNo              = self.traAnaObj.frameNo
        self.bodyPartsNo          = self.traAnaObj.bodyPartNo
        self.coordNo              = self.traAnaObj.coordNo
        self.framesPerSecond      = self.traAnaObj.fps
        self.speedClimb           = self.traAnaObj.speedStatClimb
        self.speedSumABS          = self.traAnaObj.speedStatAbs
        self.speedThrust          = self.traAnaObj.speedStatThrust 
        self.speedSlip            = self.traAnaObj.speedStatSlip   
        self.speedYaw             = self.traAnaObj.speedStatYaw
        self.predominantBodyAngle = self.traAnaObj.bodyOrient
        self.dropNo               = self.traAnaObj.dropScore
        self.activity             = self.traAnaObj.activityScore
        self.crossedMidLine       = self.traAnaObj.crossedMidLine
        self.reachedTop           = self.traAnaObj.crossedTopLine
        self.pix2mmFactor         = self.traAnaObj.pix2mmObj.pix2mmFactor
    
    def writeCSVtra(self):
        tra    = self.traAnaObj.mmTraSmooth[:,0,:]
        for bodyI in range(1,self.traAnaObj.bodyPartNo):
            tra = np.hstack((tra,self.traAnaObj.mmTraSmooth[:,bodyI,:]))
        yaw    = self.traAnaObj.yaw
        speeds = np.vstack([self.traAnaObj.speeds,self.traAnaObj.speeds[-1,:]])  
        self.trajectory = np.hstack((np.column_stack((tra,yaw)),speeds))
        headerStr = "X pos Head [mm],Y pos Head [mm],X pos Abdomen [mm],Y pos Abdomen [mm],Yaw [rad],Thrust [mm/s],Slip [mm/s],Yaw [deg/s],Horiz. Vel. [mm/s],Vert. Vel. [mm/s],Abs. Vel. [mm/s]"
        np.savetxt(self.traCSVFileName, self.trajectory, delimiter=",",header=headerStr)

    def writeFly2JSON(self,):
        # dict that shit
        out_dict = { 'movieFileName'       : self.movieFileName       ,
                     'collection'          : self.collection          ,
                     'recordingDate'       : self.recordingDate       ,
                     'flyID'               : self.flyID               ,
                     'frameNo'             : self.frameNo             ,
                     'animalNo'            : self.animalNo            ,
                     'coordNo'             : self.coordNo             ,
                     'framesPerSecond'     : self.framesPerSecond     ,
                     'speedSumABS'         : self.speedSumABS         ,
                     'speedThrust'         : self.speedThrust         ,
                     'speedSlip'           : self.speedSlip           ,
                     'speedClimb'          : self.speedClimb          ,
                     'speedYaw'            : self.speedYaw            ,
                     'predominantBodyAngle': self.predominantBodyAngle,
                     'dropScore'           : self.dropNo              ,
                     'activityScore'       : self.activity            ,
                     'crossedMidLine'      : self.crossedMidLine      ,
                     'reachedTop'          : self.reachedTop          ,
                     'pix2mmFactor'        : self.pix2mmFactor        ,
                     'anaObjFileName'      : self.anaObjFileName      ,
                     'traCSVFileName'      : self.traCSVFileName      ,
                     'exampelPictureFN'    : self.exampelPictureFileName,
                     'yamlFile'            : self.yamlFileName,
                     'jsonFile'            : self.jsonFileName}

        with open(self.jsonFileName, 'w') as outfile:
            json.dump(out_dict, outfile)
    
    def writeFly2YAML(self,):
        # dict that shit
        out_dict = { 'movieFileName'       : self.movieFileName       ,
                     'collection'          : self.collection          ,
                     'recordingDate'       : self.recordingDate       ,
                     'flyID'               : self.flyID               ,
                     'frameNo'             : self.frameNo             ,
                     'animalNo'            : self.animalNo            ,
                     'coordNo'             : self.coordNo             ,
                     'framesPerSecond'     : self.framesPerSecond     ,
                     'speedSumABS_Min_MMperSec'         : float(self.speedSumABS[0])         ,
                     'speedSumABS_Mean_MMperSec'        : float(self.speedSumABS[1])         ,
                     'speedSumABS_Median_MMperSec'      : float(self.speedSumABS[2])         ,
                     'speedSumABS_Max_MMperSec'         : float(self.speedSumABS[3])         ,
                     'speedThrust_Min_MMperSec'         : float(self.speedThrust[0])         ,
                     'speedThrust_Mean_MMperSec'         : float(self.speedThrust[1])         ,
                     'speedThrust_Median_MMperSec'         : float(self.speedThrust[2])         ,
                     'speedThrust_Max_MMperSec'         : float(self.speedThrust[3])         ,
                     'speedSlip_Min_MMperSec'           : float(self.speedSlip[0])           ,
                     'speedSlip_Mean_MMperSec'           : float(self.speedSlip[1])           ,
                     'speedSlip_Median_MMperSec'           : float(self.speedSlip[2])           ,
                     'speedSlip_Max_MMperSec'           : float(self.speedSlip[3])           ,
                     'speedYaw_Min_MMperSec'            : float(self.speedYaw[0])            ,
                     'speedYaw_Mean_MMperSec'            : float(self.speedYaw[1])            ,
                     'speedYaw_Median_MMperSec'            : float(self.speedYaw[2])            ,
                     'speedYaw_Max_MMperSec'            : float(self.speedYaw[3])            ,
                     'speedClimb_Min_MMperSec'          : float(self.speedClimb[0])            ,
                     'speedClimb_Mean_MMperSec'          : float(self.speedClimb[1])            ,
                     'speedClimb_Median_MMperSec'          : float(self.speedClimb[2])            ,
                     'speedClimb_Max_MMperSec'          : float(self.speedClimb[3])            ,
                     'predominantBodyAngle': float(self.predominantBodyAngle),
                     'dropScore'           : float(self.dropNo)              ,
                     'activityScore'       : float(self.activity)            ,
                     'crossedMidLine'      : list(self.crossedMidLine),
                     'reachedTop'          : list(self.reachedTop)     ,
                     'pix2mmFactor'        : float(self.pix2mmFactor)        ,
                     'anaObjFileName'      : self.anaObjFileName      ,
                     'traCSVFileName'      : self.traCSVFileName      ,
                     'exampelPictureFN'    : self.exampelPictureFileName,
                     'yamlFile'            : self.yamlFileName,
                     'jsonFile'            : self.jsonFileName}

        with open(self.yamlFileName, 'w') as file:
            documents = yaml.dump(out_dict, file)
            

    def autoMakeSavePositions(self):
        saveFolders = {'jsonsFolder' : os.path.join(self.saveDir,'jsons'),
                       'traFolder'   : os.path.join(self.saveDir,'traCSV'),
                       'objectFolder': os.path.join(self.saveDir,'anaObj'),
                       'yamlFolder'  : os.path.join(self.saveDir,'yamls'),
                       'examplePic'  : os.path.join(self.saveDir,'overViewPics')} 
        
        for key,val in saveFolders.items(): 
            newFolder =os.path.join(val,self.collection)
            saveFolders[key] = newFolder
            os.makedirs(newFolder, exist_ok=True)
        self.saveFolders = saveFolders
        self.baseName = os.path.splitext(os.path.basename(self.movieFileName))[0]  

        self.traCSVFileName         = os.path.join(self.saveFolders['traFolder'],self.baseName+'_tra.csv')
        self.exampelPictureFileName = os.path.join(self.saveFolders['examplePic'],self.baseName+'_traOverview.png')
        self.anaObjFileName         = os.path.join(self.saveFolders['traFolder'],self.baseName+'_dallas.obj')
        self.jsonFileName           = os.path.join(self.saveFolders['jsonsFolder'],self.baseName+'.json')
        self.yamlFileName           = os.path.join(self.saveFolders['yamlFolder'],self.baseName+'.yaml')
    
