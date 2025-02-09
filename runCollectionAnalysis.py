import DLC_reader,trajectory_correcter,videoDataGUI,dallasPlots,trajectoryAna,dallasData
import tqdm,datetime,os
from importlib import reload 
reload(DLC_reader)
reload(dallasPlots)
reload(trajectory_correcter)
reload(videoDataGUI)
#user data
collection = 'Anka3'
saveDir    = '/media/dataSSD/AnkaArchive'
sourceDir  = '/media/bgeurten/Anka/Anka3'
sourceMode = 'csv' # h5
artifactFactorThreshold = .8

AI_pattern = 'DLC_resnet50_ParalellClimb2Aug22shuffle1_800000.' + sourceMode
startFile  = 0

#get all files that were analysed by this AI in source directory
flyPos_files = [f for f in os.listdir(sourceDir) if f.endswith(AI_pattern)]
flyPos_files.sort()

for movieI in tqdm.tqdm(range(startFile,len(flyPos_files)),desc='detection files '):

    # get movie position
    movPos = flyPos_files[movieI].split(AI_pattern)   
    movPos = os.path.join(sourceDir,movPos[0]+'.avi') 
    #get result position
    flyPos = os.path.join(sourceDir, flyPos_files[movieI]  )

    #check if movie exists and go
    if os.path.exists(movPos):  
        # get modification time from movie
        modTime    = datetime.datetime.strftime(datetime.datetime.fromtimestamp(os.path.getmtime(movPos)),'%Y-%m-%d %H:%M:%S' )   

        # get arena size
        vGUI = videoDataGUI.videoDataGUI(movPos,'movie')  
        arenaCoords = vGUI.run()

        # Read trajectory file
        if sourceMode == 'h5':
            #read in dlc H5 file
            readObj = DLC_reader.DLC_H5_reader(flyPos,15)  
            readObj.readH5()
            # split to 4D trajectory
            readObj.multiAnimal2numpy()
        elif sourceMode == 'csv':
            #read in dlc CSV file
            readObj = DLC_reader.DLC_CSV_reader(flyPos,15,2)
            readObj.readCSV()
        else:
            raise ValueError("Unkown Source Mode: " +str(sourceMode))

        # optimize trajectory
        optTraObj= DLC_reader.multiAnimalEval(readObj.tra,arenaCoords )
        optTraObj.sortByXCoordinate()
        optTraObj.testForArtifacts()
        optTraObj.interpOverArtifacts()
        optTraObj.calculateArtifactFactor()

        # create pix2mm object
        p2m = trajectoryAna.pix2mm(optTraObj.arenaCoords,'smallBenzer') 
        p2m.getMM_Standard()

        #now to ethology analysis
        traObjList = list()
        for animalI in tqdm.tqdm(range(optTraObj.animalNo),desc='speed,statistics,writing'):
            if animalI == optTraObj.animalNo-1:
                dallasPlots.plotForDataArchive(vGUI.frame,optTraObj,200,dataObj.exampelPictureFileName,artifactFactorThreshold)                  
            if optTraObj.artifactFactor[animalI] < artifactFactorThreshold:
                traObj = trajectoryAna.trajectoryAna(optTraObj.tra[:,animalI,:,0:2],vGUI.media.fps,p2m)
                traObj.runStandardAnalysis()
                traObjList.append(traObj)
                # write to dallas dataObj
                dataObj = dallasData.dallasData(traObj,animalI,movPos,flyPos,saveDir,collection=collection,
                                                recordDate=modTime)

                dataObj.runStandardOut()
                os.system('clear')
    print('Done!')


# old plots

#reload(dallasPlots)
#dallasPlots.plotSingleFeature(np.rad2deg(traObj.yaw),traObj.fps,'yaw [deg]')
#dallasPlots.plotSingleFeature(traObj.speeds,traObj.fps,'yaw [deg]')
#dallasPlots.plotFilterTraTest(traObj.mmTra,traObj.mmTraSmooth)     
#dallasPlots.standardPlotTrajectory(traObj.mmTra,200,(0.5,0.5,0.5))
