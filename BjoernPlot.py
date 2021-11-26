import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


dataStrList = ['psd preStim','psd stim', 'psd resp', 'psd postStim']

def getSubSet(df,col,val):
    if val is None:
        return df
    else:
        return df.loc[df[col] == val]

def getExpSubSet(df,metaDict):
    temp = getSubSet(df,'species',metaDict['species'])
    temp = getSubSet(temp,'adult',metaDict['adult'])
    temp = getSubSet(temp,'sex',metaDict['sex'])
    temp = getSubSet(temp,'light',metaDict['light'])
    temp = getSubSet(temp,'wind',metaDict['wind'])
    temp = getSubSet(temp,'dataType',metaDict['dataType'])
    return getSubSet(temp,'water',metaDict['water'])

def getTitleString(metaDict):
    titleStr = metaDict['species']
    if metaDict['adult'] is not None:
        if metaDict['adult'] == True:
            titleStr += ' adult'
        else:
            titleStr +=' sub-adult'

    if metaDict['sex'] is not None:
        titleStr += ' ' + metaDict['sex']+'\n'

    if metaDict['light'] is not None:
        if metaDict['light'] == True:
            titleStr += ' in light'
        else:
            titleStr += ' in darkness'
            
    if metaDict['wind'] is not None:
        if metaDict['wind'] == True:
            titleStr += ' with wind'
        else:
            titleStr += ' without wind'
        
    if metaDict['water'] is not None:
        if metaDict['water'] == True:
            titleStr += ' and a water stimulus'

    if metaDict['dataType'] is not None:
        titleStr += ' ' + metaDict['dataType'] + ' comparisson'
        
    return titleStr

def plotPSD(df,metaDict,savepath='./figures/psds/',hueStr='dataType',yLim=None):
    temp = getExpSubSet(df,metaDict)

    f = plt.figure()
    sns.set_theme(style="darkgrid")

    x =sns.lineplot(x="frequency", y='power spectral density',
                hue = hueStr, style='movement direction',
                data=temp)
    x.set_xscale('log')
    #x.set_yscale('log')
    if yLim is not None:
        x.set_ylim(yLim)
    x.legend(loc='upper left')
    titleStr = getTitleString(metaDict)
    x.set_title(titleStr)
    fName = titleStr.replace('\n', '')
    fName = fName.replace(' ', '_')
    f.savefig(savepath+fName+'.jpg')
    f.savefig(savepath+fName+'.svg')


def plotBox(df,metaDict,savepath='./figures/boxplots/',y = 'power spectral density'):
    subset = getExpSubSet(df, metaDict)
    windList = list(subset['wind'])
    lightList = list(subset['light'])
    
    combList = list()
    for i in range(len(lightList)):
        if windList[i] and lightList[i]:
            combList.append('light, wind')
        if not windList[i] and lightList[i]:
            combList.append('no light, wind')
        if not windList[i] and not lightList[i]:
            combList.append('no light, no wind')
        if windList[i] and not lightList[i]:
            combList.append('light, no wind')

    subset['conditions'] = combList
    
    f = plt.figure()
    ax = sns.boxplot(x="conditions", y=y, hue="movement direction", data=subset, linewidth=2,notch = True)
    ax.set_yscale('log')
    titleStr = getTitleString(metaDict)
    ax.set_title(titleStr)
    fName = titleStr.replace('\n', '')
    fName = fName.replace(' ', '_')
    f.savefig(savepath+fName+'.jpg')
    f.savefig(savepath+fName+'.svg')


#%% quantitative comparisons

df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')

for dtype in['psd preStim', 'psd postStim']:
    for sex in ['female','male']:
            metaDict = {'species' : 'Medauroidea extradentata',
                        'adult'   : True,
                        'sex'     : sex,
                        'light'   : None,
                        'wind'    : False,
                        'water'   : True,
                        'dataType': dtype}
            if sex == 'female':
                yLim = [0,0.05]
            else:
                yLim = [0,0.08]
            plotPSD(df,metaDict,savepath='./figures/comparisons/',hueStr='light',yLim=yLim)
plt.show()


#%% All

df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')

for species in ['Medauroidea extradentata', 'Sungaya inexpectata']:
    for adult in [False,True]:
        for sex in ['female','male']:
            for light in [False,True]:
                for wind in [False,True]:
                    for water in [False,True]:
                        metaDict = {'species' : species,
                                    'adult'   : adult,
                                    'sex'     : sex,
                                    'light'   : light,
                                    'wind'    : wind,
                                    'water'   : water,
                                    'dataType': None}
                        temp = getExpSubSet(df,metaDict)
                        if temp.size >0:
                            plotPSD(df,metaDict)
plt.show()

#%% movement

df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')

for species in ['Medauroidea extradentata', 'Sungaya inexpectata']:
    for adult in [False,True]:
        for sex in ['female','male']:
            for light in [False,True]:
                for wind in [False,True]:
                    for water in [False,True]:
                        metaDict = {'species' : species,
                                    'adult'   : adult,
                                    'sex'     : sex,
                                    'light'   : light,
                                    'wind'    : wind,
                                    'water'   : False,
                                    'dataType': 'psd preStim'}
                        temp = getExpSubSet(df,metaDict)
                        if temp.size >0:
                            plotPSD(df,metaDict,savepath='./figures/locomotion/')

plt.show()
#%%

df =  pd.read_hdf('./BjoernDataMedianCILongInd4BoxPlotBest.h5',key = 'df')
metaDict = {'species' : 'Medauroidea extradentata',
        'adult'   : True,
        'sex'     : 'female',
        'light'   : None,
        'wind'    : None,
        'water'   : True,
        'movement direction' :None,
        'dataType': 'psd preStim'}
plotBox(df,metaDict)
#plotBox(df,metaDict,y='best frequency')
plt.show()

#%% single test
df =  pd.read_hdf('./BjoernDataMedianCILongInd4BoxPlotBest.h5',key = 'df')
metaDict = {'species' : 'Medauroidea extradentata',
            'adult'   : True,
            'sex'     : 'female',
            'light'   : None,
            'wind'    : None,
            'water'   : True,
            'movement direction' :None,
            'dataType': 'psd preStim'}

plotBox(df,metaDict)
#plotPSD(df,metaDict)
plt.show()

#%%
df =  pd.read_hdf('./BjoernDataMedianCILongInd4BoxPlotBest.h5',key = 'df')
metaDict = {'species' : None,
            'adult'   : None,
            'sex'     : 'female',
            'light'   : None,
            'wind'    : None,
            'water'   : False,
            'movement direction' :None,
            'dataType': 'psd preStim'}

plotBox(df,metaDict)
#plotPSD(df,metaDict)
plt.show()
#%% check singles
df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')

metaDict = {'species' : 'Medauroidea extradentata',
            'adult'   : True,
            'sex'     : 'male',
            'light'   : True,
            'wind'    : True,
            'water'   : True,
            'dataType': 'psd preStim'}
temp = getExpSubSet(df,metaDict)
if temp.size >0:
    plotPSD(df,metaDict,savepath='./figures/locomotion/')

plt.show()