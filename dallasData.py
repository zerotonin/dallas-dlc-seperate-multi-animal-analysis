import numpy as np
import json,os

class dallasData():
    def __init__(self):
        self.flyID                = np.nan # lane No
        self.trajectory           = []     # trajectory of this fly
        self.frameNo              = np.nan # number of frames in movies
        self.animalNo             = np.nan # number of animals in movies
        self.coordNo              = np.nan # number of coords 
        self.framesPerSecond      = np.nan # sample rate of recording
        self.speedSumABS          = (np.nan,np.nan,np.nan,np.nan) # min,mean,median,max [mm/s]
        self.speedThrust          = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [mm/s]
        self.speedSlip            = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [mm/s]
        self.speedYaw             = (np.nan,np.nan,np.nan,np.nan)# min,mean,median,max [deg/s]
        self.predominantBodyAngle = (np.nan,np.nan)# mean,median[deg]
        self.dropNo               = np.nan # number of times the animal fell
        self.activity             = np.nan # percentage the animal was active during movie
        self.crossedMidLine       = False  # did the fly cross the midline -> classic Benzer 
        self.reachedTop           = False  # did the fly reach the 90% height line
        self.pix2mmFactor         = np.nan # pixel 2 mm convertion factor
        self.movieFileName        = ''     # file location of the movie
        self.anaObjFileName       = ''     # file location of the pickle object 
        self.traCSVFileName       = ''     # file location of the flies tra file
        self.exampePictureFN      = ''     # file location of the example Picture
    
    def writeFly2JSON(self,fileName,directory):
        # output filenames
        csvFPos  = os.path.join(directory,fileName+'.csv')
        jsonFPos = os.path.join(directory,fileName+'.json')
        # write trajectory_away
        np.savetxt(csvFPos, self.trajectory, delimiter=",")

        # dict that shit
        out_dict = {'movieFileName       ': self.movieFileName       ,
                     'flyID               ': self.flyID               ,
                     'frameNo             ': self.frameNo             ,
                     'animalNo            ': self.animalNo            ,
                     'coordNo             ': self.coordNo             ,
                     'framesPerSecond     ': self.framesPerSecond     ,
                     'speedSumABS         ': self.speedSumABS         ,
                     'speedThrust         ': self.speedThrust         ,
                     'speedSlip           ': self.speedSlip           ,
                     'speedYaw            ': self.speedYaw            ,
                     'predominantBodyAngle': self.predominantBodyAngle,
                     'dropNo              ': self.dropNo              ,
                     'activity            ': self.activity            ,
                     'crossedMidLine      ': self.crossedMidLine      ,
                     'reachedTop          ': self.reachedTop          ,
                     'pix2mmFactor        ': self.pix2mmFactor        ,
                     'movieFileName       ': self.movieFileName       ,
                     'anaObjFileName      ': self.anaObjFileName      ,
                     'traCSVFileName      ': self.traCSVFileName      ,
                     'exampePictureFN     ': self.exampePictureFN     }

        with open(jsonFPos, 'w') as outfile:
            json.dump(out_dict, outfile)

        
    
