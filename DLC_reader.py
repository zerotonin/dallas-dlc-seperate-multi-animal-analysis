import pandas,tqdm

class DLC_H5_reader:
    def __init__(self,filePosition):
        self.fPos = filePosition
        self.pandasDF = None
        self.frameNo  = None  
        self.columns  = None
        self.areaNo   = None  
        self.tra      = None
    
    def readH5(self):
        self.pandasDF = pandas.read_hdf(self.fPos)
        self.frameNo  = self.pandasDF.pandasDF.shape[0]  
        self.columns  = self.pandasDF.pandasDF.shape[1]
        self.areaNo   = self.columns/4  
    
    def multiAnimal2numpy(self):
        for frameI in tqdm.tqdm(range(df_tra.shape[0])):
            frameRes = self.pandasDF.iloc[frameI].iloc[:]  
            


