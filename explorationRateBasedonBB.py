from cmath import nan
from tqdm import tqdm
from shapely.geometry import box
from shapely.ops import unary_union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class explorationRateCalculator:

    def __init__(self,traAnaFilePos):
        self.traAnaFilePos = traAnaFilePos
        self.df = pd.read_hdf(self.traAnaFilePos)
        self.resultDFList = list()

    def boundingBoxInShapely(self,trajectoryEntry):
        tra_entry = np.array([trajectoryEntry['BB_mm_xmin'], trajectoryEntry['BB_mm_ymin'],trajectoryEntry['BB_mm_xmax'], trajectoryEntry['BB_mm_ymax']])
        if np.isnan(tra_entry).any():
            return box(0,0,0,0)
        else:
            return box(trajectoryEntry['BB_mm_xmin'], trajectoryEntry['BB_mm_ymin'],trajectoryEntry['BB_mm_xmax'], trajectoryEntry['BB_mm_ymax'])

    def calculateExplorationRate(self,subset):

        expoArea = list()
        tracePolygon = self.boundingBoxInShapely(subset.iloc[0])
        for i,traEntry in tqdm(subset.iterrows(),desc='additiveRun'):
                newBox =self.boundingBoxInShapely(traEntry)  
                tracePolygon = tracePolygon.union(newBox)
                expoArea.append(tracePolygon.area)

        subset['exploredArea__mm2'] = expoArea
        return subset    

    def analyseAllAnimals(self):
        for arenaNo in tqdm(range(20),desc='calculating for each arena'):
            subset = self.df.loc[self.df['arenaNo'] == arenaNo] 
            subset = subset.interpolate()
            self.resultDFList.append(self.calculateExplorationRate(subset))
        
        self.resultDF = pd.concat(self.resultDFList)
        self.resultDF.to_hdf(self.traAnaFilePos,key='data')
        

