import os

def expoAnalysisWithTPS(fileList,metaData,fps,activityThresh,arenaBoundingBoxFilePos,movieFilePos,arenaWidthMM,arenaHeightMM,outputDir,cueStr='',
                        pythonPos='/home/bgeurten/anaconda3/envs/dallas/bin/python',
                        scriptDir = '/home/bgeurten/PyProjects/dallas-dlc-seperate-multi-animal-analysis'):
    #set tsp socket
    if cueStr == '' or cueStr == None:
        tspStr = 'tsp'
    else:
        tspStr = f'TS_SOCKET=/tmp/{cueStr} tsp'
    #position of the script
    scriptPos = os.path.join(scriptDir,'runExpoAnalysisYegi.py')
    # send to tsp
    for fileI in range(len(fileList)):
        os.system(f'{tspStr} {pythonPos} {scriptPos} -t {fileList[fileI]} -m {metaData[fileI]} -f {fps} -a {activityThresh} -b {arenaBoundingBoxFilePos[fileI]} -s {movieFilePos[fileI]} -x {arenaWidthMM} -y {arenaHeightMM} -o {outputDir}')
# -
# USER INPUT
sourceDir = '/media/gwdg-backup/BackUp/Yegi'
outDir = '/media/dataSSD/YegiTra'
arenaHeightMM  = 20.0
arenaWidthMM   = 20.0
fps            = 10
activity_tresh = 0.3

traList = [os.path.join(sourceDir,x) for x in os.listdir(sourceDir) if x.endswith('.tra')]
traList = [x for x in traList if  os.path.isfile(x[0:-3]+'csv')]
traList.sort()
bbList  = [x[0:-3]+'csv' for x in traList]
movList = [x[0:-3]+'avi' for x in traList]
#meta tags
metaData = ['28' for i in range(9)]+['29' for i in range(4)]
#send to tsp


expoAnalysisWithTPS(traList,metaData,fps,activity_tresh,bbList,movList,arenaWidthMM,arenaHeightMM,outDir,None)