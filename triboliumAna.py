import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


class triboliumAna:


    def __init__(self,singleAnimalDataFrame):
        self.df = singleAnimalDataFrame
        

    def calcSurfaceAreaConcentricRings(self,rMin,rMax,rNum):
        ringRadius = np.linspace(rMin,rMax,rNum-1)

        ringAreaList = [np.pi*rMin**2]

        for i in range(1,rNum-1):
            circleArea = np.pi*ringRadius[i]**2
            ringArea = circleArea-ringAreaList[i-1]
            ringAreaList.append(ringArea)
        return np.array(ringAreaList)    

    def normBySum(self,data):
        normVal = np.sum(data)
        return data/normVal

    def radiusAna(self,radius,maxR):
        counts,bins = np.histogram(radius,np.linspace(0,maxR-1,maxR))   
        surfaceList = self.calcSurfaceAreaConcentricRings(1,maxR,maxR)
        probDense = self.normBySum(counts)
        probDenseNorm = probDense/surfaceList 
        probDenseNorm = self.normBySum(probDenseNorm)
        return bins,probDense,probDenseNorm

    def activityAna(self):
        self.df['time_epoch']=pd.to_datetime(self.df['time'])
        self.df["time"] = pd.to_datetime(self.df["time_epoch"], format = "%H:%M:%S").dt.hour
        activityHist,bins = np.histogram(self.df.loc[self.df['active'],'time'],np.linspace(0,24,25))    
        activityHist = self.normBySum(activityHist)
        return bins,activityHist

    def analyseIndividual(self):

        # activity
        activityFrac = np.sum(self.df.active)/self.df.shape[0]
        binsHour,activeHist = self.activityAna()
        # speed
        speed_max = self.df.loc[self.df['active'],'absSpeed_mm/s'].max()
        speed_median = self.df.loc[self.df['active'],'absSpeed_mm/s'].median()
        #position
        binsRadius,radProbDense,radProbDenseNorm = self.radiusAna(self.df.coord_rho,10)
        rho_median = self.df.coord_rho.median()
        data2D,x,y,handle = plt.hist2d(self.df['coord_mmArena_x'],self.df['coord_mmArena_y'],(np.linspace(0,20,60),np.linspace(0,20,60)))
        del handle

        # collectData
        self.result = {'activity': activityFrac, 'activityHourHist' : (binsHour,activeHist), 'speed_max_mm/s': speed_max, 'speed_median_mm/s': speed_median,
                       'radius_median_mm': rho_median, 'positionHist_x-y-2D': (x,y,data2D), 'radiusHist_bins_probD_probDNorm': (binsRadius,radProbDense,radProbDenseNorm) }     
        return self.result