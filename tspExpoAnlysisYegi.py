import os

def expoAnalysisWithTPS(fileList,metaData,fps,activityThresh =0.3,cueStr='',
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
        os.system(f'{tspStr} {pythonPos} {scriptPos} -t {fileList[fileI]} -m {metaData[fileI]} -f {fps} -a {activityThresh} ')



# USER INPUT
fileDir = '/media/dataSSD/YegiTra'
fps     = 10

#get input files
fileList = [os.path.join(fileDir,x) for x in os.listdir(fileDir) if x.endswith('.h5')]
fileList.sort()
#get output file positions
metaData = ['28' for i in range(8)]+['29' for i in range(3)]
#send to tsp
expoAnalysisWithTPS(fileList,metaData,fps,0.3)