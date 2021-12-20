
from tqdm import tqdm
import os

def analyseTRAwithTSP(fileList,saveList,fps,cueStr,pythonPos='/home/bgeurten/anaconda3/envs/dallas/bin/python',scriptDir = '/home/bgeurten/PyProjects/dallas-dlc-seperate-multi-animal-analysis'):
    #set tsp socket
    if cueStr == '' or cueStr == None:
        tspStr = 'tsp'
    else:
        tspStr = f'TS_SOCKET=/tmp/{cueStr} tsp'
    #position of the script
    scriptPos = os.path.join(scriptDir,'runSingleFoodArenaAna.py')
    # send to tsp
    for fileI in range(len(fileList)):
        os.system(f'{tspStr} {pythonPos} {scriptPos} -i {fileList[fileI]} -f {fps} -o {saveList[fileI]}')



# USER INPUT
fileDir = '/media/dataSSD/LennartSplitMovies'
fps     = 10
cueStr  = 'shorttasks' # set to None if you want it included in the main cue

#get input files
fileList = [os.path.join(fileDir,x) for x in os.listdir(fileDir) if x.endswith('.tra')]
fileList.sort()
#get output file positions
saveList = [x.split('.')[0]+'.h5' for x in fileList ]
#send to tsp
analyseTRAwithTSP(fileList[0:-1],saveList[0:-1],fps,cueStr)