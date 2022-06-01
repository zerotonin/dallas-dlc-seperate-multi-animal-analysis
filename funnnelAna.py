import cv2,os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from houghDetector import houghDetector 

def getBaseName(filePos):
    fileName = os.path.basename(filePos)
    fileName = os.path.splitext(fileName)[0]
    return fileName


def getMetaDataDF(fileList):
    metaData = [ [fileName,  *getBaseName(fileName).split('__')] for fileName in fileList]
    for mdSet in metaData:
        subSet = mdSet[4].split('_')
        mdSet[4] = int(subSet[0])
        mdSet.append(subSet[1])
        if len(subSet)>2:
            if subSet[2] == 'BH':
                mdSet.append('light')
        else:
            mdSet.append('dark')
  
    return pd.DataFrame(metaData,columns=['FilePosition','Date','Time_h','Genotype','Orientation_int','Orientation_str','light'])  

# data Path
path2data = '/media/gwdg-backup/BackUp/Paul_Funnel'
newData = False
if newData:

    # get all image files
    fileList = list() 
    for (dirpath, dirnames, filenames) in os. walk(path2data):
        fileList += [os.path. join(dirpath, file) for file in filenames]
    # derive meta data from file name
    df = getMetaDataDF(fileList)
    df.to_csv(f'{path2data}/imgData.csv',index=False)
else:
    df = pd.read_csv(f'{path2data}/imgData.csv')


img = cv2.imread(df.iloc[0,0])
img_blurred= cv2.medianBlur(img,27)
# color filtering
darkBlue = (np.array([0,0,70]),np.array([70,70,200]))
mask = cv2.inRange(img_blurred,darkBlue[0],darkBlue[1])
# image erosion-dialation
kernel = np.ones((10,10), np.uint8)
maskE = cv2.erode(mask, kernel, iterations=2)
maskD = cv2.dilate(maskE, kernel, iterations=2)

fig, axList = plt.subplots(2, 2)
axList = axList.flatten()
axList[3].imshow(maskD,cmap='gray')
axList[0].imshow(img)
axList[1].imshow(img_blurred)
axList[2].imshow(mask,cmap='gray')
plt.show()