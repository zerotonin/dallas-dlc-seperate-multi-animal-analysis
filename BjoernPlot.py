import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


dataStrList = ['psd preStim','psd stim', 'psd resp', 'psd postStim']

def getSubSet(df,col,val):
    return df.loc[df[col] == val]

def getExpSubSet(df,metaDict):
    temp = getSubSet(df,'species',metaDict['species'])
    temp = getSubSet(temp,'adult',metaDict['adult'])
    temp = getSubSet(temp,'sex',metaDict['sex'])
    temp = getSubSet(temp,'light',metaDict['light'])
    temp = getSubSet(temp,'wind',metaDict['wind'])
    return getSubSet(temp,'water',metaDict['water'])

def getTitleString(metaDict):
    titleStr = metaDict['species']
    if metaDict['adult'] == True:
        titleStr += ' adult'
    else:
        titleStr +=' sub-adult'

    titleStr += ' ' + metaDict['sex']+'\n'
    if metaDict['light'] == True:
        titleStr += ' in light'
    else:
        titleStr += ' in darkness'
        
    if metaDict['wind'] == True:
        titleStr += ' with wind'
    else:
        titleStr += ' without wind'
    
    if metaDict['water'] == True:
        titleStr += ' and a water stimulus'
    
    return titleStr

def plotPSD(df,metaDict,savepath='./figures/psds/'):
    temp = getExpSubSet(df,metaDict)

    f = plt.figure()
    sns.set_theme(style="darkgrid")

    x =sns.lineplot(x="frequency", y='power spectral density',
                hue = 'dataType', style='movement direction',
                data=temp)
    x.set_xscale('log')
    x.legend(loc='upper left')
    titleStr = getTitleString(metaDict)
    x.set_title(titleStr)
    fName = titleStr.replace('\n', '')
    fName = fName.replace(' ', '_')
    f.savefig(savepath+fName+'.jpg')
    f.savefig(savepath+fName+'.svg')


df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')




dictList = list()
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
                                    'water'   : water}
                        temp = getExpSubSet(df,metaDict)
                        if temp.size >0:
                            plotPSD(df,metaDict)

#%%
df =  pd.read_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')
metaDict = {'species' : 'Medauroidea extradentata',
            'adult'   : True,
            'sex'     : 'male',
            'light'   : True,
            'wind'    : True,
            'water'   : True}

plotPSD(df,metaDict)
plt.show()