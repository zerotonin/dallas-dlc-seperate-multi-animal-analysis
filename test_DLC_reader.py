import DLC_reader,trajectory_correcter,videoDataGUI,dallasPlots,trajectoryAna,dallasData
import tqdm,datetime,os
from importlib import reload 
import numpy as np

collection = 'Anka1'
flyPos     = '/media/dataSSD/Anka1/B_05_03DeepCut_resnet50_ParalellClimb2Aug22shuffle1_800000.h5'
movPos     = '/media/dataSSD/Anka1/B_05_03.avi'
modTime    = datetime.datetime.strftime(datetime.datetime.fromtimestamp(os.path.getmtime(movPos)),'%Y-%m-%d %H:%M:%S' )   

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

#now to ethology analysis
traObjList = list()
for animalI in tqdm.tqdm(range(optTraObj.animalNo),desc='speed,position,statistics'):
    traObj = trajectoryAna.trajectoryAna(optTraObj.tra[:,animalI,:,0:2],vGUI.media.fps,p2m)
    traObj.runStandardAnalysis()
    traObjList.append(traObj)

# write to dallas dataObj
reload(dallasData)
dataObj = dallasData.dallasData(traObj,14)
dataObj.traAnaObj2DataObj()   

dallasPlots.standardPlot(vGUI.frame,optTraObj,200)


# write to dallas dataObj
reload(dallasData)
dataObj = dallasData.dallasData(traObj,14,movPos,flyPos,collection=collection,
                                recordDate=modTime)
dataObj.traAnaObj2DataObj()   

reload(dallasPlots)
dallasPlots.plotSingleFeature(np.rad2deg(traObj.yaw),traObj.fps,'yaw [deg]')
dallasPlots.plotSingleFeature(traObj.speeds,traObj.fps,'yaw [deg]')
dallasPlots.plotFilterTraTest(traObj.mmTra,traObj.mmTraSmooth)     
dallasPlots.standardPlotTrajectory(traObj.mmTra,200,(0.5,0.5,0.5))