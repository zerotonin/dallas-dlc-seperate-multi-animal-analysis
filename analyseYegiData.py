import os, readMultiAnimalCharonTra
from importlib import reload
import numpy as np 
from tqdm import tqdm
import pandas as pd
import cv2 as cv

sourceDir = '/media/gwdg-backup/BackUp/Yegi'
traList = [os.path.join(sourceDir,x) for x in os.listdir(sourceDir) if x.endswith('.tra')]
traList = [x for x in traList if  os.path.isfile(x[0:-3]+'csv')]
traList.sort()
bbList  = [x[0:-3]+'csv' for x in traList]
movList = [x[0:-3]+'avi' for x in traList]

traFile = traList[0]
bbFile  = bbList[0]
movFile = movList[0]
# read and transform bounding box of arena position

cmar = readMultiAnimalCharonTra.readMultiAnimalCharonTra(traFile,movFile,bbFile)
cmar.run()
cmar.saveAna('/media/dataSSD/YegiTra/arena.csv','/media/dataSSD/YegiTra/tra.h5')

