import multiBenzerSplitter
from importlib import reload 
import matplotlib.pyplot as plt 
import numpy as np     
from cv2 import cv2


movPos = '/media/dataSSD/2020-07-03__13_43_56.avi'
mediaMode = 'movie'


reload(multiBenzerSplitter)
mbsObj = multiBenzerSplitter.multiBenzerSplitter(movPos,mediaMode)
mbsObj.splitMovie()

mbsObj.extractMonitorsFromFrames()
mbsObj.findLaneBorders()
mbsObj.plotStandardAna(1)


fig = plt.figure()
ax = fig.add_subplot(111) 
for i in range(4):
    ax.plot(xProfileList[i])  
    ax.plot(peakList[i], xProfileList[i][peakList[i]], "x")
plt.show()   