from charonFoodTra import readCharonFood54
from importlib import reload 

paul= readCharonFood54('foodTestTra.tra') # init of reader object with file position
paul.readFile()  # read data from file into memory
# how to adresse data in the imObjData

 readClass.resultList[frameNumber][objectNumber][objectParameter]
 paul.imObjData[3][22]['centerOfMass']

frameList = paul.imObjData[0][1::] # get objects in frame and ignore frame number
flyId=0
for imgObj in frameList:
    if imgObj["name"] == 'fly':
        flyId += 1
        print("Fly " + str(flyId) + ": " + "@ " + str(imgObj['centerOfMass'][0]) + ", " + str(imgObj['centerOfMass'][1]))

ArenaId=0
for imObj in frameList:
    if imObj ['name'] == 'arena':
        ArenaId += 1
        print("Arena " + str(ArenaId) + ": " + "@ " + str(imObj['boundingBox'][0])+ ", " + str(imObj['boundingBox'][1]) + ", " + str(imObj['boundingBox'][2])+ ", " + str(imObj['boundingBox'][3]))
    

if 'centerOfMass' >= ('boundingBox'[0,1]) and 'centerOfMass' <= ('boundingBox'[2,3]):
    print(flyId, ArenaId) 