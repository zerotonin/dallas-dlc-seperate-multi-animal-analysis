import pandas as pd
import numpy as np 
from scipy.ndimage import gaussian_filter1d
from tqdm import tqdm
import os

class augmentYegiTra:
    def __init__(self,traPos,metaDataFlag='<29',fps=10,activityThreshHold=0.3):
        self.traPos = traPos
        self.metaDataFlag = metaDataFlag
        self.fps = fps
        self.activityThreshHold = activityThreshHold
        if metaDataFlag == '<29':
            self.animalStrainDict = {0:('female',True,False),5:('male',True,False),10:('female',False,False),15:('male',False,False)}
        elif metaDataFlag == '>29':
            self.animalStrainDict = {0:('female',True,True),5:('female',True,True),10:('male',True,True),15:('male',True,True)}
        else:
            raise ValueError(f'augmentTrajectory:init: The metaDataFlag is unknown: {metaDataFlag}')


    def smoothTraGauss(self,inputData,sigma = 5):
        return gaussian_filter1d(inputData, sigma)

    def readTra(self):
        self.df = pd.read_hdf(self.traPos,'data')
    
    def getTimeVector(self,traLen):
        dateStr,rest=os.path.basename(self.traPos).split('__')              
        timeStr = rest.split('_tr')[0]
        # reformat to numpy date format
        timeStr = timeStr.replace('_',':')
        timeStr += '.000000'
        #get numpy time obkecet
        startDateTime = np.datetime64(f'{dateStr}T{timeStr}')
        # calculate the length of the trajectory in millisecods (*1000 for milliseconds)
        traLen_ms = int(np.round(traLen*1000/self.fps))
        # caclulate the end of the trajectory as date and time
        endDateTime   = startDateTime + np.timedelta64(traLen_ms,'ms') 
        # transfrom into pandas date time to get the time as Unix epochs
        startDateTime = pd.Timestamp(startDateTime)
        endDateTime   = pd.Timestamp(endDateTime)
        # return linspace vector
        return  np.linspace(startDateTime.value,endDateTime.value,traLen)


    def augment(self):
        subsetList=list()
        for arenaNo in tqdm(range(20),desc='interpolation,filtering,calc...'):

            if arenaNo < 5:
                metaData = self.animalStrainDict[0]
            elif arenaNo < 10:
                metaData = self.animalStrainDict[5]
            elif arenaNo < 15:
                metaData = self.animalStrainDict[10]
            else:
                metaData = self.animalStrainDict[15]
            
            subset                    = self.df.loc[self.df['arenaNo']==arenaNo,:].copy()
            subset                    = subset.interpolate()
            subset['coord_mmArena_y'] = self.smoothTraGauss(subset['coord_mmArena_y'])
            subset['coord_mmArena_x'] = self.smoothTraGauss(subset['coord_mmArena_x'])
            subset['coord_rho']       = self.smoothTraGauss(subset['coord_rho'])
            subset['coord_phi']       = self.smoothTraGauss(subset['coord_phi'])
            subset['BB_mm_ymin']      = self.smoothTraGauss(subset['BB_mm_ymin'])
            subset['BB_mm_xmin']      = self.smoothTraGauss(subset['BB_mm_xmin'])
            subset['BB_mm_ymax']      = self.smoothTraGauss(subset['BB_mm_ymax'])
            subset['BB_mm_xmax']      = self.smoothTraGauss(subset['coord_phi'])
            subset['absSpeed_mm/s']   = np.insert(np.sqrt(np.diff(subset['coord_mmArena_y'].values)**2+np.diff(subset['coord_mmArena_x'].values)**2)*self.fps,0,np.NaN)
            subset['active']          = subset['absSpeed_mm/s'] > self.activityThreshHold
            subset['time']            = self.getTimeVector(subset.shape[0])
            subset['sex']             = metaData[0]
            subset['infection']       = metaData[1]
            subset['treatment']       = metaData[2]
                   
            subsetList.append(subset)

        self.dfAugmented = pd.concat(subsetList)     

    def writeTra(self):
        self.dfAugmented.to_hdf(self.traPos[0:-3]+'Ana.h5','data')

    def run(self):
        self.readTra()
        self.augment()
        self.writeTra()