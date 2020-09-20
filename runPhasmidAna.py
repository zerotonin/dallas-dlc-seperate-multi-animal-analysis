
import DLC_reader,trajectory_correcter,dallasPlots,trajectoryAna, phasmidAnatomy
import tqdm,datetime,os,glob
import numpy as np
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

def getBodyPartList(pandasDF):

    pandasDFColList = pandasDF.columns.values.tolist()  
    bodyPartList = list()
    for i in range(len(pandasDFColList)):
        if i%3 == 0:
            bodyPartList.append(pandasDFColList[i][1])
    return bodyPartList

def getPix2mmconverter(qualVec,bodyPartList,phasmidObj,coordinates):

    availAxis  = getAvailableAxis(qualVec,bodyPartList,phasmidObj.getAvailableAxis())
    factorList =  list()
    for testAxis in availAxis:
        coords     = getCoordinates4Axis(bodyPartList,coordinates,testAxis)
        pixelLen   = np.linalg.norm(np.diff(np.transpose(coords))) 
        mmLen      = phasmidObj.getAxisLength(testAxis) 
        factorList.append(mmLen/pixelLen)
    return factorList




def getCoordinates4Axis(bodyPartList,traVec,axis):
    coords = list()
    for i in range(len(bodyPartList)):
        if bodyPartList[i] in axis:
            coords.append(traVec[i,0:2])   
    return np.array(coords)

def getAvailableBodyParts(qualVec,bodyPartList):
    availableBP = list()
    for i in range(len(qualVec)):
        if qualVec[i] == True:
            availableBP.append(bodyPartList[i])
    
    return availableBP

def allBPpermutations(availableBP):
    possibleAxis = list()
    for i in range(len(availableBP)-1):
        for j in range(i+1,len(availableBP)):
            possibleAxis.append(availableBP[i]+ ' -> ' + availableBP[j])
    return possibleAxis



def getAvailableAxis(qualVec,bodyPartList,axisList):
    availableBP  = getAvailableBodyParts(qualIDX[0,:],bodyPartList)  
    possibleAxis = allBPpermutations(availableBP)  
    trueAxis     = list()
    for testAxis in possibleAxis:
        if testAxis in axisList:
            trueAxis.append(testAxis)
    return trueAxis

def pixTra2mmTra(readObj,qualIDX,bodyPartList,pA):
    mmTra = np.ones(shape=readObj.tra.shape)*-1
    for frameI in range(readObj.tra.shape[0]):
        fList = getPix2mmconverter(qualIDX[frameI,:],bodyPartList,pA,readObj.tra[frameI,:,:])
        pix2mm = np.mean(np.array(fList))
        for bodyP in range(len(bodyPartList)):
            if qualIDX[frameI,bodyP] == True:
                mmTra[frameI,bodyP,0:2] = readObj.tra[frameI,bodyP,0:2]*pix2mm
                mmTra[frameI,bodyP,2]   = readObj.tra[frameI,bodyP,2]
    return mmTra





strainName = 'Sungaya inexpectata'
strainDir  = '/media/dataSSD/AlexVids/Sungaya_videos'
qualThresh = 0.5


#get file positions
fPos = list_files(strainDir,'h5')
 

fileI = 12

#read dlc file
readObj = DLC_reader.DLC_H5_reader(fPos[fileI],1)  
readObj.readH5()
readObj.singleAnimal2numpy() 
# get phasmid axis data
gender  = determine_gender(fPos[fileI])
pA = phasmidAnatomy.phasmidAnatomy(strainName,gender)
bodyPartList = getBodyPartList(readObj.pandasDF)     
#quality Index
qualIDX = readObj.tra[:,:,2] >= qualThresh
# mmTra

mmTra = pixTra2mmTra(readObj,qualIDX,bodyPartList,pA)
