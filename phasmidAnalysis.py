import phasmidAnatomy
import numpy as np


class phasmidAnalysis:

    def __init__(self,fileName,strain,qualThreshold,readObj):
        self.fileName = fileName
        self.gender   = self.determine_gender()
        self.strain   = strain
        self.pA       = phasmidAnatomy.phasmidAnatomy(self.strain,self.gender)
        if self.pA.ready == True:
            self.qualThreshold = qualThreshold
            self.readObj       = readObj  
            self.startAnalysis()
        else:
            raise ValueError("Gender or Strainname where not correct!")

    def startAnalysis(self):
            # threshold by quality
            self.qualIDX       = self.readObj.tra[:,:,2] >= self.qualThreshold
            self.bodyPartList  = self.getBodyPartList()
            self.mmTra         = self.pixTra2mmTra() 
            self.mmTra         = self.clearTra()  

    def determine_gender(self):
        if 'female' in self.fileName or 'SUfe' in self.fileName:
            gender = 'f'
        else:
            gender =  'm'
        return gender

    def getBodyPartList(self):
        pandasDFColList = self.readObj.pandasDF.columns.values.tolist()  
        bodyPartList = list()
        for i in range(len(pandasDFColList)):
            if i%3 == 0:
                bodyPartList.append(pandasDFColList[i][1])
        return bodyPartList

    def getPix2mmconverter(self,qualVec,bodyPartList,phasmidObj,coordinates):

        availAxis  = self.getAvailableAxis(qualVec,bodyPartList,phasmidObj.getAvailableAxis())
        factorList =  list()
        for testAxis in availAxis:
            coords     = self.getCoordinates4Axis(bodyPartList,coordinates,testAxis)
            pixelLen   = np.linalg.norm(np.diff(np.transpose(coords))) 
            mmLen      = self.pA.getAxisLength(testAxis) 
            factorList.append(mmLen/pixelLen)
        return factorList

    def getCoordinates4Axis(self,bodyPartList,traVec,axis):
        coords = list()
        for i in range(len(bodyPartList)):
            if bodyPartList[i] in axis:
                coords.append(traVec[i,0:2])   
        return np.array(coords)

    def getAvailableBodyParts(self,qualVec,bodyPartList):
        availableBP = list()
        for i in range(len(qualVec)):
            if qualVec[i] == True:
                availableBP.append(bodyPartList[i])
        return availableBP

    def allBPpermutations(self,availableBP):
        possibleAxis = list()
        for i in range(len(availableBP)-1):
            for j in range(i+1,len(availableBP)):
                possibleAxis.append(availableBP[i]+ ' -> ' + availableBP[j])
        return possibleAxis

    def getAvailableAxis(self,qualVec,bodyPartList,axisList):
        availableBP  = self.getAvailableBodyParts(qualVec,bodyPartList)  
        possibleAxis = self.allBPpermutations(availableBP)  
        trueAxis     = list()
        for testAxis in possibleAxis:
            if testAxis in axisList:
                trueAxis.append(testAxis)
        return trueAxis

    def pixTra2mmTra(self):
        mmTra = np.ones(shape=self.readObj.tra.shape)*-1
        for frameI in range(self.readObj.tra.shape[0]):
            factorList = self.getPix2mmconverter(self.qualIDX[frameI,:],self.bodyPartList,self.pA,self.readObj.tra[frameI,:,:])
            pix2mm = np.mean(np.array(factorList))
            for bodyP in range(len(self.bodyPartList)):
                if self.qualIDX[frameI,bodyP] == True:
                    mmTra[frameI,bodyP,0:2] = self.readObj.tra[frameI,bodyP,0:2]*pix2mm
                    mmTra[frameI,bodyP,2]   = self.readObj.tra[frameI,bodyP,2]
        return mmTra
    
    def clearTra(self):
        neverSeenValue = self.mmTra.shape[0]*-1
        sumOfQuality   = sum(self.mmTra[:,:,2])
        newBodyPartList = list()
        newMMtra = list()
        for i in range(len(sumOfQuality)):
            if sumOfQuality[i] != neverSeenValue:
                print(sumOfQuality[i])
                newBodyPartList.append(self.bodyPartList[i])
                newMMtra.append(self.mmTra[:,i,:])
        print(newMMtra)
        self.mmTraDetected        = np.dstack(newMMtra)
        self.bodyPartListDetected = newBodyPartList
