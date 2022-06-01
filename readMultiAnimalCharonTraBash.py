import os


def analyseTRAwithTSP(traList,movList,bbList,arenaHeightMM,arenaWidthMM,outDir,cueStr,pythonPos='/home/bgeurten/anaconda3/envs/dallas/bin/python',scriptDir = '/home/bgeurten/PyProjects/dallas-dlc-seperate-multi-animal-analysis'):
    #set tsp socket
    if cueStr == '' or cueStr == None:
        tspStr = 'tsp'
    else:
        tspStr = f'TS_SOCKET=/tmp/{cueStr} tsp'

    #position of the script
    scriptPos = os.path.join(scriptDir,'readMultiAnimalCharonTra.py')
    # send to tsp
    for fileI in range(len(traList)):
        os.system(f'{tspStr} {pythonPos} {scriptPos} -t {traList[fileI]} -a {bbList[fileI]} -m {movList[fileI]} -x {arenaWidthMM} -y {arenaHeightMM} -o {outDir}')

#analyseSingleArenaTra.py -t <traFilePos> -a <arenaBoundingBoxFilePos> -m <movieFilePos> -x <arenaWidthMM> -y <arenaHeightMM> -o <outputDir>'

sourceDir = '/media/gwdg-backup/BackUp/Yegi'
outDir = '/media/dataSSD/YegiTra'
arenaHeightMM = 20.0
arenaWidthMM  = 20.0

traList = [os.path.join(sourceDir,x) for x in os.listdir(sourceDir) if x.endswith('.tra')]
traList = [x for x in traList if  os.path.isfile(x[0:-3]+'csv')]
traList.sort()
bbList  = [x[0:-3]+'csv' for x in traList]
movList = [x[0:-3]+'avi' for x in traList]

analyseTRAwithTSP(traList,movList,bbList,arenaHeightMM,arenaWidthMM,outDir,None)