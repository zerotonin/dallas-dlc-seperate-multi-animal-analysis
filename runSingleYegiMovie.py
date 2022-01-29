import os, readMultiAnimalCharonTra
import pandas as pd

traFilePos ='/media/gwdg-backup/BackUp/Yegi/2021-03-29__17_34_06.tra'
outputDir = '/media/dataSSD/YegiTra/withBoxes'
fileName     = os.path.basename(traFilePos)[0:-4]   
movieFilePos = traFilePos[0:-4]+'.avi'
arenaBoundingBoxFilePos = traFilePos[0:-4]+'.csv'
cleanTraOut  = os.path.join(outputDir,fileName+'_trajectory.h5')
meanArenaOut = os.path.join(outputDir,fileName+'_meanArena.csv')
cmar = readMultiAnimalCharonTra.readMultiAnimalCharonTra(traFilePos,movieFilePos,arenaBoundingBoxFilePos,20,20)
cmar.run()
cmar.saveAna(meanArenaOut,cleanTraOut)