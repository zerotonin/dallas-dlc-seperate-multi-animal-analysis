import re
import numpy as np
from pathlib import Path
import copy 
def readCSVList(fList):
    dataAll = list()
    for file in fileList:

        x= re.search("_result.csv",file.name)  
        a = x.span()  
        strain=file.name[0:a[0]-1]
        if strain =='w':
            strain ='wt'
        with open(file, 'r') as f:
            line =f.readline()
            while line !='':
                fly,arena,mc,left,right = line.split(', ')  
                dataAll.append([strain,fly,arena,float(mc),int(left),int(right)])
                line =f.readline()
    return dataAll

def unifyList(data):
    unifiedList = list()
    for row in data:
        strain = row[0]
        fly    = row[1]
        arena  = row[2]
        p = re.search(fly,arena) 
        if  p == None:
            p = re.search('r',arena) 
            p = p.span()
        else:
            p = p.span()


        if p == 1:
            score = row[3]
        else:
            score = row[3]*-1
        
        dataID = strain+'_'+fly+'_'+"".join(sorted(arena))    
        unifiedList.append([dataID, score])
    unifiedList.sort()
    return unifiedList

def splitIntoAllIDs(dataU):

    expName     = dataU[0][0]
    expNameList = list()
    expDataList = list()
    tempList    = list()
    expName     = dataU[0][0]
    expNameList.append(expName)
    for row in dataU:
        if row[0] == expName:
            tempList.append(row[1])
        else:
            #set new experiment name ....
            expName     = row[0]
            # ... and add it to the experiment List
            expNameList.append(expName)
            #add collected data
            expDataList.append(copy.deepcopy(tempList))
            #refresh templist
            tempList    = list()
            tempList.append(row[1])
    # add last collected data
    expDataList.append(copy.deepcopy(tempList))
        
def splitIntoExp(dataU):
    wtList    = list()
    wtR1List  = list()
    wtR5List  = list()
    rutList   = list()
    rutR1List = list()
    rutR5List = list()

    for row in dataU:
        flyID = row[0]
        if 'wt' in flyID:
            if 'ros' in flyID:
                if '5' in flyID:
                    wtR5List.append(row[1])
                else:
                    wtR1List.append(row[1])
            else:
                wtList.append(row[1])
        else:
            if 'ros' in flyID:
                if '5' in flyID:
                    rutR5List.append(row[1])
                else:
                    rutR1List.append(row[1])
            else:
                rutList.append(row[1])
    dataByType = [wtList   ,wtR1List ,wtR5List ,rutList  ,rutR1List,rutR5List]
    typeName = ['wt','wt_r1','wt_r5','rut','rut_r1','rut_r5']
    return dataByType,typeName

parentDir = '/media/gwdg-backup/foodMovSwap'
fileList  = Path(parentDir).rglob('*.csv')
#'%s, %s, %1.8f, %5d, %5d'
data  = readCSVList(fileList)
dataU = unifyList(data)

dataByType,typeName = splitIntoExp(dataU)



###plotting
labels = ['Known Color', 'KC + 0.1g rm', 'KC + 0.5g rm']
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
bplot1 = axes[0].boxplot(dataByType[0:3],
                         notch=True,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
axes[0].set_title('wildtype')

bplot2 = axes[1].boxplot(dataByType[3:7],
                         notch=True,  # notch shape
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
axes[1].set_title('rutabaga')
# fill with colors
colors = ['lightblue', 'lightgreen', 'darkgreen']
for bplot in (bplot1, bplot2):
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

#adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(False)
    ax.set_xlabel('choices')
    ax.set_ylabel("score [1= known color -1 new color]")
    ax.plot([0,7],[0,0],'--',color=[.5,.5 ,.5])

plt.show()


