
import DLC_reader,trajectory_correcter,dallasPlots,trajectoryAna, phasmidAnalysis
import tqdm,datetime,os,glob
import numpy as np
from importlib import reload
from os import walk
 
def list_files(directory, extension): 
    fileList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.'+extension]
    fileList.sort()
    return fileList

strainName              = 'Sungaya inexpectata'
strainDir               = '/media/dataSSD/AlexVids/Sungaya_videos'
qualityThreshold        = 0.5
minimalTrajectoryLength = 100


#get file positions
fPos = list_files(strainDir,'h5')
 
reload(phasmidAnalysis)
for fileI in tqdm.tqdm(range(len(fPos)),desc='detection files '):

reload(phasmidAnalysis)
fileI = 55
#read dlc file
readObj = DLC_reader.DLC_H5_reader(fPos[fileI],1)  
readObj.readH5()
readObj.singleAnimal2numpy() 
# get phasmid axis data
# mmTra
pAna = phasmidAnalysis.phasmidAnalysis(fPos[fileI],strainName,qualityThreshold,readObj,minimalTrajectoryLength)
mmTra = pAna.mmTra
