
import DLC_reader,trajectory_correcter,dallasPlots,trajectoryAna, phasmidAnatomy
import tqdm,datetime,os,glob
from importlib import reload
from os import walk
 
def list_files(directory, extension): 
    fileList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.'+extension]
    fileList.sort()
    return fileList

def determine_gender(fileName):
    if 'female' in fileName or 'SUfe' in fileName:
        gender = 'f'
    else:
        gender =  'm'
    return gender




strainName = 'Sungaya inexpectata'
strainDir  = '/media/dataSSD/AlexVids/Sungaya_videos'

fPos = list_files(strainDir,'h5')
 

fileI = 12
reload(DLC_reader)
#read in dlc file
readObj = DLC_reader.DLC_H5_reader(fPos[fileI],1)  
gender  = determine_gender(fPos[fileI])
pA = phasmidAnatomy.phasmidAnatomy(strainName,gender)   
readObj.readH5()
readObj.singleAnimal2numpy() 
readObj.tra.shape