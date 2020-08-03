import DLC_reader,tqdm, trajectory_correcter,copy,cv2,videoDataGUI,dallasPlots,trajectoryAna
from importlib import reload 
import numpy as np


flyPos    = '/media/dataSSD/Anka1/B_05_03DeepCut_resnet50_ParalellClimb2Aug22shuffle1_800000.h5'
movPos    = '/media/dataSSD/Anka1/B_05_03.avi'

# get arena size
vGUI = videoDataGUI.videoDataGUI(movPos,'movie')  
arenaCoords = vGUI.run()
#read in dlc file
reload(DLC_reader)
readObj = DLC_reader.DLC_H5_reader(flyPos,15)  
readObj.readH5()
# split to 4D trajectory
readObj.multiAnimal2numpy()


# optimize trajectory
optTraObj= DLC_reader.multiAnimalEval(readObj.tra,arenaCoords )
optTraObj.testForArtifacts()
optTraObj.interpOverArtifacts()

#now to ethology analysis
reload(trajectoryAna)
# create pix2mm object
p2m = trajectoryAna.pix2mm(optTraObj.arenaCoords,'smallBenzer') 
p2m.getMM_Standard()
animalI = 3

traObj = trajectoryAna.trajectoryAna(optTraObj.tra[:,animalI,:,0:2],vGUI.media.fps,p2m)
traObj.convert2mm()
traObj.smoothTraGauss()
traObj.calculateYaw()


reload(dallasPlots)
dallasPlots.plotFilterTraTest(traObj.mmTra,traObj.mmTraSmooth)     
dallasPlots.standardPlotTrajectory(traObj.mmTra,200,(0.5,0.5,0.5))
#dallasPlots.standardPlot(vGUI.frame,optTraObj,200)
