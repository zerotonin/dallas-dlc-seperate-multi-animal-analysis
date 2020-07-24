import pandas,glob,cv2,os,re,time,tqdm,pickle
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

def cliInput(questStr,answerList):
    answer = input(questStr)
    while answer not in answerList:
        answer = input(questStr)
    return answer

def getVideoFPos(h5Fpos):
    x= re.search("DLC",h5Fpos.name)  
    a = x.span()  
    return os.path.join(parentDir,h5Fpos.name[0:a[0]]+'.mp4')

def getArenaData(frame):
    imgplot = plt.imshow(frame)

    plt.setp(plt.gca(), autoscale_on=False)

    tellme('You will define a box, click to begin')

    plt.waitforbuttonpress()

    while True:
        pts = []
        while len(pts) < 4:
            tellme('Select 4 corners with mouse')
            pts = np.asarray(plt.ginput(4, timeout=-1))
            if len(pts) < 4:
                tellme('Too few points, starting over')
                time.sleep(1)  # Wait a second

        ph = plt.fill(pts[:, 0], pts[:, 1], 'y', lw=2,alpha=0.5)

        tellme('Happy? Key click for yes, mouse click for no')

        if plt.waitforbuttonpress():
            break

        # Get rid of fill
        for p in ph:
            p.remove()
    #clear overlay
    for p in ph:
        p.remove()
    return pts


def getFlyAndColourdata(modus):
    if modus == '3': 
        #Get arena colours
        arenaColours = cliInput('Colours from left to right e.g. yb or bg: ',['yb','by','yg','gy','bg','gb','r1b','br1','r1y','yr1','r5b','br5','r5y','yr5'])
        fly          = cliInput('On what was the fly raised e.g. y,b,g: ',['y','b','g'])
    elif modus == '1':
        arenaColours = ['by','by','gb',
                        'yg','yb','yg',
                        'bg','gb','gb',
                        'yg','yb','yg']
        fly = ['b','b','b','y','y','g','g','b','g','y','y','g']
    elif modus == '2':
        arenaColours = ['br1','br1','br1',
                        'r1y','r1y','r1y',
                        'r5b','r5b','r5b',
                        'yr5','yr5','yr5']
        fly = ['g','g','g','g','g','g','g','g','g','g','g','g']
    else:
        print('mode unknown',modus)
    return arenaColours, fly

def readFirstFrame(path):
    videoPos = getVideoFPos(path)
    f = cv2.VideoCapture(videoPos)
    rval, frame = f.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def getMetaData(RGB_frame):
    coordList = list()

    clear = lambda: os.system('clear')
    for i in range(12):
        clear()
        print('Arena No '+str(i+1))
        print('============')
        arenaCoordinates = getArenaData(RGB_frame)
        metaQuest = 'no'
        coordList.append(arenaCoordinates)
    # ask for colours
    while metaQuest == 'no':
        mode = cliInput('What is the area type (colour = 1,rosemary =2 or verbose =3):',['1','2', '3'])
        arenaColours, fly= getFlyAndColourdata(mode)
        print('Arena Colours:', arenaColours)
        print('Flies: ',fly)
        metaQuest = cliInput('Is this correct (yes | no)?',['yes','no'])
    
    
    return list(zip(coordList,arenaColours,fly))

def pointInRect(point,rect):
    x1,y1,x2,y2 =rect    
    
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False


def arenaSideTest(arenaCoordinates,flyCoord):
    x1,y1 =np.min(arenaCoordinates,axis=0)
    x2,y2 =np.max(arenaCoordinates,axis=0)

    xM = (x1+x2)/2.0
    leftRec = np.array([x1,y1,xM,y2])
    rightRec = np.array([xM,y1,x2,y2])
    isInLeft = pointInRect(flyCoord,leftRec)
    isInRight = pointInRect(flyCoord,rightRec)
    return isInLeft,isInRight

def testWhereflyIs(arenaData,flyPos,decisionMat):
    c = 0
    for arena in arenaData:
        arenaC = arena[0]
        left,right = arenaSideTest(arenaC,flyPos)
        if left:
            decisionMat[c][0] += 1
        if right:
            decisionMat[c][1] += 1
        c += 1
    return decisionMat

def testFlies(arenaData,meanCoords,decisionMat):
    for i in range(12):
        decisionMat = testWhereflyIs(arenaData,meanCoords[i][0:2],decisionMat)  
    return decisionMat

def splitArenaAnalysis(df_tra,arena_data):
    decisionMat = np.zeros(shape=(12,2))
    for frameI in tqdm.tqdm(range(df_tra.shape[0])):
        frameRes = df_tra.iloc[frameI].iloc[:]    
        frameRes = frameRes.to_numpy() 
        frameRes = np.reshape(frameRes,(36,-1))  
        meanCoords = list()
        for i in np.linspace(0,33,12):
            meanCoords.append(np.mean(frameRes[int(i):int(i)+3][:],axis=0))
        decisionMat = testFlies(arenaData,meanCoords,decisionMat)
    return decisionMat

def writeResult(h5Fpos,resultList):
    x= re.search("DLC",h5Fpos.name)  
    a = x.span()  
    csvPos = os.path.join(parentDir,h5Fpos.name[0:a[0]]+'_result.csv')
    with open(csvPos, 'w') as f: 
        for item in resultList: 
            f.write("%s, " % item[0])
            f.write("%s, " % item[1]) 
            f.write("%1.8f, " % item[2]) 
            f.write("%5d, " % item[3]) 
            f.write("%5d\n" % item[4]) 


parentDir = '/media/gwdg-backup/foodMovSwap'
fileList  = Path(parentDir).rglob('*filtered.h5')

for path in fileList:
    #read first image
    firstFrame = readFirstFrame(path)
    #verbose user arena data
    arenaData  = getMetaData(firstFrame)
    #read dlc stuff
    df_tra = pandas.read_hdf(path)
    #split to decision data
    descisionMat = splitArenaAnalysis(df_tra,arena_data)
    resultList = list()
    for i in range(12):
        MC = (decisionMat[i][0]-decisionMat[i][1]) / (decisionMat[i][0]+decisionMat[i][1])
        resultList.append([arenaData[i][2],arenaData[i][1],MC,decisionMat[i][0],decisionMat[i][1]])
    #write result
    writeResult(path,resultList)