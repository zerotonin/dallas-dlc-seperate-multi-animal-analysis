import os, augmentYegiTra
from importlib import reload
import numpy as np 
from tqdm import tqdm
import pandas as pd
import cv2 as cv
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import matplotlib

#%% plotting

df = pd.read_hdf('/media/dataSSD/YegiTra/allAnaComb.h5','data')
def plotShade(ax,x,y,l,u,colorStr,labelStr):
    ax.plot(x, y, color=colorStr,label=labelStr)
    ax.fill_between(x, l, u,
        alpha=0.15, edgecolor=colorStr, facecolor=colorStr)

figHandles = list()

fig = plt.figure()
figHandles.append(fig)
sns.boxplot(x="status", y="activity", hue='sex', data=df)
fig = plt.figure()
figHandles.append(fig)
sns.boxplot(x="status", y="speed_max_mm/s", hue='sex', data=df)
fig = plt.figure()
figHandles.append(fig)
sns.boxplot(x="status", y="speed_median_mm/s", hue='sex', data=df)
fig = plt.figure()
figHandles.append(fig)
sns.boxplot(x="status", y="radius_median_mm", hue='sex', data=df)

xlabelList = ['hours','radius, mm','radius, mm']
ylabelList = ['probability density','probability density','norm. probability density']
titleList = ['activity pattern','centrophobism - histogram','centrophobism norm. surface area']
cmap = np.array([[0, 18, 25],[0, 95, 115],[10, 147, 150],[238, 155, 0],[187, 62, 3],[155, 34, 38]])/255
for histType in range(3):
    fig = plt.figure()
    figHandles.append(fig)
    ax = fig.subplots(1)
    c= 0
    for group in histList:
        labelStr,hists = group
        hData = hists[histType]
        plotShade(ax,hData[0,:],hData[1,:],hData[2,:],hData[3,:],cmap[c,:],labelStr)
        c+=1
    ax.legend()
    ax.set_xlabel(xlabelList[histType])
    ax.set_ylabel(ylabelList[histType])
    ax.set_title(titleList[histType])

for group in histList:
    labelStr,hists = group
    hdata = hists[3]
    hdata += 0.0000001
    fig = plt.figure()
    figHandles.append(fig)
    plt.pcolormesh(hdata.T, cmap='plasma', shading='gouraud',norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.title('mean histogram of positions for '+labelStr)


figFileNames = ['boxP_activity','boxP_speedMax','boxP_speedMedian','boxP_radiusMedian','histActivity',
                'histRadius','histRadiusNorm','position_femaleInfected','position_maleInfected',
                'position_femaleHealthy','position_maleHealthy','position_femaleTreated','position_maleTreated']
saveDir = '/media/dataSSD/YegiTra/figures'
c= 0
for fig in figHandles:
    fig.savefig(os.path.join(saveDir,figFileNames[c]+'.png'))
    fig.savefig(os.path.join(saveDir,figFileNames[c]+'.svg'))
    c+=1
plt.show()
#%%

def medianHistAna(bins,data):
    
    med_act = np.mean(data,axis=0)
    med_act = normBySum(med_act)
    low_act,up_act = get95CI4twoD(data)
    print(bins.shape,med_act.shape,low_act.shape,up_act.shape)
    return np.vstack([bins,med_act,low_act,up_act])   

def get95CI4twoD(data2d):
    lowList =list()
    upList =list()
    for i in range(data2d.shape[1]):
        lower, upper = get95Confint(data2d[:,i])
        lowList.append(lower)
        upList.append(upper)
    return np.array(lowList),np.array(upList)

def normBySum(data): 
    normVal = np.sum(data) 
    return data/normVal 

def get95Confint(data):
    return st.t.interval(alpha=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) 
 

keys =  df['key'].unique()  
histList = list()
for key in keys:
    subset = df.loc[df['key'] == key,:]
    actHistList = list()
    posHistList = list()
    radHistList = list()
    radNormList = list()
    for index,row in subset.iterrows():
        actBin,actHist = row['activityHourHist']
        posHistX,posHistY,posHistData = row['positionHist_x-y-2D']
        radBin,radHist,radHistNorm= row['radiusHist_bins_probD_probDNorm']
        actHistList.append(actHist)
        posHistList.append(posHistData)
        radHistList.append(radHist)
        radNormList.append(radHistNorm)
    #1d histograms
    actHistList = np.vstack(actHistList) 
    radHistList = np.vstack(radHistList) 
    radNormList = np.vstack(radNormList) 
    actHist = medianHistAna(actBin[0:-1],actHistList)
    radHist = medianHistAna(radBin[0:-1],radHistList)
    radNorm = medianHistAna(radBin[0:-1],radNormList)

    #2d histograms
    meanPosHist = normBySum( np.mean(np.dstack(posHistList),axis=2))
    hists = (actHist,radHist,radNorm,meanPosHist)
    histList.append((key,hists))

#%% collect all traces
import triboliumAna
      

sourceDir = '/media/dataSSD/YegiTra'
augmentedFPos = [os.path.join(sourceDir,x) for x in os.listdir(sourceDir) if x.endswith('Ana.h5')]
augmentedFPos.sort()
allTra = list()
for traPos in tqdm(augmentedFPos,desc='analyse individual trajectory'):
    df = pd.read_hdf(traPos,'data')
    for arenaNo in range(20):
        subset = df.loc[df['arenaNo']==arenaNo,:].copy()       
        tA = triboliumAna.triboliumAna(subset)
        results = tA.analyseIndividual()     
        results['sex'] = subset['sex'].values[0]
        results['infection'] = subset['infection'].values[0]
        results['treatment'] = subset['treatment'].values[0]
        results['time_epoch'] = subset['time_epoch'].values[0]
        allTra.append(results)


allTraDF = pd.DataFrame(allTra) 

# shortkeys f = female m = male i = infected h = healty t = treated
shortkey = [x[0] for x in allTraDF.sex.values]
allTraDF['key'] = shortkey
allTraDF.loc[df['infection'] == True,'key'] += 'i'
allTraDF.loc[df['infection'] == False,'key'] += 'h'
allTraDF.loc[df['treatment'] == True,'key'] += 't'

allTraDF['status'] = ['healthy' for x in allTraDF.sex.values]
allTraDF.loc[df['infection'] == True,'status'] = 'infected'
allTraDF.loc[df['treatment'] == True,'status'] = 'treated'

allTraDF.to_hdf('/media/dataSSD/YegiTra/allAnaComb.h5',key='data')
#%% read All traces
traData = [('/media/dataSSD/YegiTra/2021-02-24__13_46_29_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2021-02-23__08_53_57_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2020-11-27__13_59_15_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2020-11-19__14_34_03_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2021-04-21__14_30_38_trajectory.h5','>29'),
           ('/media/dataSSD/YegiTra/2021-04-07__18_06_45_trajectory.h5','>29'),
           ('/media/dataSSD/YegiTra/2020-11-25__13_13_36_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2020-12-02__14_12_22_trajectory.h5','<29'),
           ('/media/dataSSD/YegiTra/2021-03-29__17_34_06_trajectory.h5','>29'),
           ('/media/dataSSD/YegiTra/2021-04-06__17_28_29_trajectory.h5','>29'),
           ('/media/dataSSD/YegiTra/2020-11-24__14_15_16_trajectory.h5','<29')]

reload(augmentYegiTra)
for tra in tqdm(traData,desc='augmenting data'):
    aug =augmentYegiTra.augmentYegiTra(tra[0],tra[1])
    aug.run()

