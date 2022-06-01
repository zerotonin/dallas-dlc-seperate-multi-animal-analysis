import readMultiAnimalCharonTra
import explorationRateBasedonBB
import augmentYegiTra
import os


traFilePos              =  '/media/gwdg-backup/BackUp/Yegi/2021-03-29__17_34_06.tra' 
fps                     = 10 
activityThreshold       = 0.3
arenaBoundingBoxFilePos =  '/media/gwdg-backup/BackUp/Yegi/2021-03-29__17_34_06.csv'
movieFilePos            =  '/media/gwdg-backup/BackUp/Yegi/2021-03-29__17_34_06.avi'
arenaWidthMM            = 20.0 
arenaHeightMM           = 20.0 
outputDir               = '/media/dataSSD/YegiTra'
metaDataFlag            = '>29'
fileName     = os.path.basename(traFilePos)[0:-4]   
cleanTraOut  = os.path.join(outputDir,fileName+'_trajectory.h5')
meanArenaOut = os.path.join(outputDir,fileName+'_meanArena.csv')

# read trajectory
cmar = readMultiAnimalCharonTra.readMultiAnimalCharonTra(traFilePos,movieFilePos,arenaBoundingBoxFilePos,arenaHeightMM,arenaWidthMM)
cmar.run()
cmar.saveAna(meanArenaOut,cleanTraOut)
del(cmar)
#augement data
ayt = augmentYegiTra.augmentYegiTra(cleanTraOut,metaDataFlag,fps,activityThreshold)
ayt.run()

#calculate exploration rate
expo = explorationRateBasedonBB.explorationRateCalculator(ayt.savePos)
del(ayt)
expo.analyseAllAnimals()

