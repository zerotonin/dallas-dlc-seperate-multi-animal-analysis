import DLC_reader,tqdm, trajectory_correcter,copy,cv2,videoDataGUI,dallasPlots
from importlib import reload 
import numpy as np


flyPos    = '/media/dataSSD/Anka1/B_05_03DeepCut_resnet50_ParalellClimb2Aug22shuffle1_800000.h5'
movPos    = '/media/dataSSD/Anka1/B_05_03.avi'

# get arena size
vGUI = videoDataGUI.videoDataGUI(movPos,'movie')  
arenaCoords = vGUI.run()
#read in dlc file
reload(DLC_reader)
x = DLC_reader.DLC_H5_reader(flyPos,15)  
x.readH5()
# split to 4D trajectory
x.multiAnimal2numpy()

# optimize trajectory
y= DLC_reader.multiAnimalEval(x.tra,arenaCoords )
y.testForArtifacts()
y.interpOverArtifacts()

reload(dallasPlots)
dallasPlots.standardPlot(vGUI.frame,y,200)
