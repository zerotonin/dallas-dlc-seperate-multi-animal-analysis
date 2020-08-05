import DLC_reader,trajectory_correcter,videoDataGUI,dallasPlots,trajectoryAna,dallasData
import tqdm,datetime,os
from importlib import reload 

# get movie position
movPos = '/media/dataSSD/Anka6/2019-10-01__11_08_49.avi'
#get result position
flyPos = '/media/dataSSD/Anka6/2019-10-01__11_08_49DLC_resnet50_AnkaClimbJul29shuffle1_200000_bx.h5'
#get all files that were analysed by this AI in source directory


#check if movie exists and go
if os.path.exists(movPos):  
# get modification time from movie
    modTime  = datetime.datetime.strftime(datetime.datetime.fromtimestamp(os.path.getmtime(movPos)),'%Y-%m-%d %H:%M:%S' )   

# get arena size
vGUI = videoDataGUI.videoDataGUI(movPos,'movie')  
arenaCoords = vGUI.run()
#read in dlc file
readObj = DLC_reader.DLC_H5_reader(flyPos,15)  
readObj.readH5()
# split to 4D trajectory
readObj.multiAnimal2numpy()

# optimize trajectory
optTraObj= DLC_reader.multiAnimalEval(readObj.tra,arenaCoords )
optTraObj.testForArtifacts()
optTraObj.interpOverArtifacts()

# create pix2mm object
p2m = trajectoryAna.pix2mm(optTraObj.arenaCoords,'smallBenzer') 
p2m.getMM_Standard()

#now to ethology analysis
traObjList = list()
for animalI in tqdm.tqdm(range(optTraObj.animalNo),desc='speed,statistics,writing'):
    traObj = trajectoryAna.trajectoryAna(optTraObj.tra[:,animalI,:,0:2],vGUI.media.fps,p2m)
    traObj.runStandardAnalysis()
    traObjList.append(traObj)
    # write to dallas dataObj
    dataObj = dallasData.dallasData(traObj,animalI,movPos,flyPos,saveDir,collection=collection,
                                    recordDate=modTime)
    if animalI == 0:
        dallasPlots.plotForDataArchive(vGUI.frame,optTraObj,200,dataObj.exampelPictureFileName)                  
    dataObj.runStandardOut()
    os.system('clear')
print('Done!')


# old plots

#reload(dallasPlots)
#dallasPlots.plotSingleFeature(np.rad2deg(traObj.yaw),traObj.fps,'yaw [deg]')
#dallasPlots.plotSingleFeature(traObj.speeds,traObj.fps,'yaw [deg]')
#dallasPlots.plotFilterTraTest(traObj.mmTra,traObj.mmTraSmooth)     
#dallasPlots.standardPlotTrajectory(traObj.mmTra,200,(0.5,0.5,0.5))
