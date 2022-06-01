import numpy as np 

class splitCharonMultiAnimalTra:
    def __init__(self,imgObjList,arenaNumber,objNameList,arenaCoordsRel,sumArenaCoords,arenaCoordsOcc):
        self.arenaNumber    = arenaNumber
        self.objNameList    = objNameList
        self.imgObjList     = imgObjList
        self.sumArenaCoords = sumArenaCoords
        self.arenaCoordsOcc = arenaCoordsOcc
        self.arenaCoordsRel = arenaCoordsRel
        self.newImgObjList  = list()
    
    def splitFrameNumber(self):
        self.frameNumber = self.imgObjList[0]
        del self.imgObjList[0]


    def assignArenaPositions(self):
    
        # check which object belongs to which arena position
        self.arenaPosList= list()
        # arena PosList will show the arena position and -1 for unknown position -2 for the marker
        for detection in self.imgObjList:
            if detection['name'] == 'marker':
                arenaNo = np.array([-2])
            else:
                arenaNo = np.where((self.arenaCoordsRel[:,0]<=detection['centerOfMass'][0]) & (self.arenaCoordsRel[:,2]>=detection['centerOfMass'][0])&(self.arenaCoordsRel[:,1]<=detection['centerOfMass'][1]) & (self.arenaCoordsRel[:,3]>=detection['centerOfMass'][1]))
                if arenaNo[0].size == 0: 
                    arenaNo = np.array([-1])
            self.arenaPosList.append(arenaNo[0])
        self.arenaPosList = np.hstack(self.arenaPosList)

    def getBestDetections(self):
        self.newImgObjList = list()
        # now we check each arena position and devide it up into a beetle detection and the arena detection, sorting out lower detection qualities
        for i in range(self.arenaNumber):
            # get all detection for this arena position
            objIndex = np.where(self.arenaPosList == i)
            # check which detections are the best for this arena position
            bestArena = (-1,0)
            bestTC    = (-1,0)
            for objI in list(objIndex[0]):
                if self.imgObjList[objI]['name'] == 'TC':
                    if bestTC[1] <= self.imgObjList[objI]['quality']:
                        bestTC = (objI,self.imgObjList[objI]['quality'])
                elif self.imgObjList[objI]['name'] == 'arena':
                    if bestArena[1] <= self.imgObjList[objI]['quality']:
                        bestArena = (objI,self.imgObjList[objI]['quality'])
            
            self.analyseBestArena(bestArena,i)
            self.analyseBestTC(bestTC,i)

    def analyseBestArena(self,bestArena,i):
        # if a best arena could be found add the coordinates to the sum of coordinates and count the occasion
        if bestArena[0] != -1:
            self.sumArenaCoords[i,:] += np.array(self.imgObjList[bestArena[0]]['boundingBox'])
            self.arenaCoordsOcc[i]   += 1

    def analyseBestTC(self,bestTC,i):
        # if a beetle could be found reduce to the important data add frame and arena number
        if bestTC[0] != -1:
            TCdict = self.imgObjList[bestTC[0]]
            TCdictNew = dict()
            TCdictNew['frameNo'] = self.frameNumber
            TCdictNew['arenaNo'] = i
            TCdictNew['coord_relImg_y'] = TCdict['centerOfMass'][0]
            TCdictNew['coord_relImg_x'] = TCdict['centerOfMass'][1]
            TCdictNew['BB_relImg_ymin'] = TCdict['boundingBox'][0]
            TCdictNew['BB_relImg_xmin'] = TCdict['boundingBox'][1]
            TCdictNew['BB_relImg_ymax'] = TCdict['boundingBox'][2]
            TCdictNew['BB_relImg_xmax'] = TCdict['boundingBox'][3]
            self.newImgObjList.append(TCdictNew)
        # if no beetle could be found add empty dict
        else:
            self.newImgObjList.append({'frameNo':self.frameNumber, 'arenaNo':i, 'coord_relImg_y':None, 'coord_relImg_x':None, 'BB_relImg_ymin':None, 'BB_relImg_xmin':None, 'BB_relImg_ymax':None, 'BB_relImg_xmax':None})

    def run(self):
        self.splitFrameNumber()
        self.assignArenaPositions()
        self.getBestDetections()
        return self.newImgObjList,self.sumArenaCoords,self.arenaCoordsOcc

