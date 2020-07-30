import DLC_reader,tqdm, trajectory_correcter,copy,cv2,videoDataGUI,dallasPlots
from importlib import reload 
import numpy as np


flyPos    = '/media/dataSSD/Anka1/A_01_01DeepCut_resnet50_ParalellClimb2Aug22shuffle1_150000.h5'
movPos    = '/media/dataSSD/Anka1/A_01_01.avi'

vGUI = videoDataGUI.videoDataGUI(movPos,'movie')  
arenaCoords = vGUI.run()
reload(DLC_reader)
x = DLC_reader.DLC_H5_reader(flyPos,15)  
x.readH5()
x.multiAnimal2numpy()


y= DLC_reader.multiAnimalEval(x.tra,arenaCoords )
y.testForArtifacts()
y.interpOverArtifacts()

reload(dallasPlots)
dallasPlots.standardPlot(vGUI.frame,y)
