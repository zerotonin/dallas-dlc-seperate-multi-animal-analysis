import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import interpolate

dataFpos = ['/media/gwdg-backup/BackUp/Bjoern/constantDark_constantWind_waterAt10_20secDur.h5',
'/media/gwdg-backup/BackUp/Bjoern/constantDark_noWind_waterAt10_20secDur.h5',
'/media/gwdg-backup/BackUp/Bjoern/constantLight_constantWind_waterAt10_20secDur.h5',
'/media/gwdg-backup/BackUp/Bjoern/constantLight_noWind_waterAt10_20secDur.h5',
'/media/gwdg-backup/BackUp/Bjoern/constantDark_noWind.h5']

brokenMov = ['Adult/female/2021-09-07__18-47-57',
             'Adult/female/2021-09-08__17-08',
             'Adult/male/2021-09-07__19-23-38',
             'Subadult/male/2021-09-07__18-32-55',
             'Subadult/male/2021-09-08__17-29-32',
             'Adult/female/2021-09-01__18-55-12',
             'Adult/female/2021-08-31__19-42-16',
             'Adult/female/2021-08-31__18-03-55',
             'Adult/female/2021-08-31__18-32-14',
             'Adult/female/2021-08-31__19-44-39',
             'Adult/male/2021-09-02__18-28-28',
             'Adult/male/2021-08-31__20-30-05',
             'Subadult/female/2021-08-31__18-49-53',
             'Subadult/male/2021-09-01__14-02-16',
             'Subadult/male/2021-09-01__14-31-16',
             'Subadult/male/2021-09-01__17-21-21',
             'Subadult/male/2021-09-02__17-51-09',
             'Adult/female/2021-09-04__16-04-45',
             'Adult/male/2021-09-03__17-12-56',
             'Adult/male/2021-09-03__17-59-59',
             'Adult/male/2021-09-03__14-49-19',
             'Subadult/female/2021-09-04__16-49-32',
             'Subadult/male/2021-09-04__16-56-05',
             'Subadult/male/2021-09-04__16-19-55',
             'Subadult/male/2021-09-03__16-07-31',
             'Subadult/male/2021-09-03__17-23-28']

df = pd.DataFrame()

for fPos in dataFpos:
    temp = pd.read_hdf(fPos,key='df')
    df = pd.concat((df,temp))


df['traPos'].duplicated()
df = df.drop_duplicates(subset='traPos', keep="last")
df.reset_index(inplace=True)

delMeList= []
searchC = 0
for searchStr in brokenMov:
    rowC=0
    for i,row in df.iterrows(): 
        if searchStr in row['traPos']:
            delMeList.append((searchC,rowC))
        rowC +=1
    searchC +=1 
   
df = df.drop([x[1] for x in delMeList])
df.reset_index(inplace=True)

df.to_hdf('./allDataBjorn.h5',key='df')

#%%
df = pd.read_hdf('./allDataBjorn.h5',key='df')


def getSubSet(df,col,val):
    return df.loc[df[col] == val]

def getExpSubSet(df,metaDict):
    temp = getSubSet(df,'species',metaDict['species'])
    temp = getSubSet(temp,'adult',metaDict['adult'])
    temp = getSubSet(temp,'sex',metaDict['sex'])
    temp = getSubSet(temp,'light',metaDict['light'])
    temp = getSubSet(temp,'wind',metaDict['wind'])
    return getSubSet(temp,'water',metaDict['water'])

def extractData(subset,dataCol):
    temp = list()
    freq = np.geomspace(0.01,100,100)     
    for data in subset[dataCol]:
        if data.size >0:
            f = interpolate.interp1d(data[:,0], data[:,1])
            temp.append(np.column_stack((freq,f(freq))))
    
    if temp == []:
        return None
    else:
        return np.dstack(temp)

def medianCI(data, ci, p):
    '''
    data: pandas datafame/series or numpy array
    ci: confidence level
    p: percentile' percent, for median it is 0.5
    output: a list with two elements, [lowerBound, upperBound]
    '''
    if type(data) is pd.Series or type(data) is pd.DataFrame:
        #transfer data into np.array
        data = data.values

    #flat to one dimension array
    data = data.reshape(-1)
    data = np.sort(data)
    N = data.shape[0]

    lowCount, upCount = stats.binom.interval(ci, N, p, loc=0)
    #given this: https://onlinecourses.science.psu.edu/stat414/node/316
    #lowCount and upCount both refers to  W's value, W follows binomial Dis.
    #lowCount need to change to lowCount-1, upCount no need to change in python indexing
    #print(lowCount,upCount)
    lowCount -= 1
    return data[int(lowCount)], data[int(upCount)]
    

def getMedCI(data):
    lowerList = list()
    upperList = list()
    medData = np.median(data,axis=2)
    if data.shape[2] == 1:
        lowerList = data[:,1]
        upperList = data[:,1]
    elif data.shape[2] == 2:
        temp = data.copy()
        temp.sort(axis=2)
        lowerList= temp[:,1,0]
        upperList= temp[:,1,1]
    elif data.shape[2] == 3:
        temp = data.copy()
        temp.sort(axis=2)
        lowerList= temp[:,1,0]
        upperList= temp[:,1,2]
    else:
        for j in range(data.shape[0]):
            lower,upper = medianCI(data[j,1,:],0.95,0.5)
            lowerList.append(lower)
            upperList.append(upper)
    return np.column_stack((medData,np.array(lowerList),np.array(upperList)))
     

def analyse(df,metaDict):
    resultDict= metaDict
    dataStr = ['psd_H_preStim','psd_H_stim', 'psd_H_resp', 'psd_H_postStim', 
               'psd_V_preStim','psd_V_stim', 'psd_V_resp', 'psd_V_postStim']
    subset = getExpSubSet(df,metaDict)
    if subset.size >0:
        for dataType in dataStr:
            if(extractData(subset,dataType)) is not None:

                resultDict[f'{dataType}_rawData'] = extractData(subset,dataType)
                resultDict[f'{dataType}_medData'] = getMedCI(resultDict[f'{dataType}_rawData'])
                resultDict[f'{dataType}_n'] = resultDict[f'{dataType}_rawData'].shape[2]
            else:
                resultDict[f'{dataType}_rawData'] = None
                resultDict[f'{dataType}_medData'] = None
                resultDict[f'{dataType}_n'] = 0
        return resultDict
    else:
        return None


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
                        result = analyse(df,metaDict)
                        if result is not None:
                            dictList.append(result) 

df2 = pd.DataFrame(dictList)
df2.to_hdf('./BjoernDataMedianCI.h5',key = 'df')

#%% Long form table

df = pd.read_hdf('./BjoernDataMedianCI.h5',key = 'df')
dataStr = ['psd_H_preStim','psd_H_stim', 'psd_H_resp', 'psd_H_postStim', 
           'psd_V_preStim','psd_V_stim', 'psd_V_resp', 'psd_V_postStim']


speciesList = list() 
adultList = list()
sexList = list()
lightList = list()
windList = list()
waterList = list()
dataTypeList = list()
nList = list()
moveDirList = list()
frequencyList = np.array([])
psdMedianList = np.array([])
upperCIList = np.array([])
lowerCIList = np.array([])   
for ind,row in df.iterrows():
    for dataType in dataStr:
        dataShortF, direction,dataShortE = dataType.split('_')
        if direction == 'H':
            direction = 'horizontal'
        else:
            direction = 'vertcial'
        dataShort = dataShortF+' '+dataShortE
        if row[dataType+'_medData'] is not None:
            speciesList += [row['species'] for i in range(100)] 
            adultList += [row['adult'] for i in range(100)]
            sexList += [row['sex'] for i in range(100)]
            lightList += [row['light'] for i in range(100)]
            windList += [row['wind'] for i in range(100)]
            waterList += [row['water'] for i in range(100)]
            dataTypeList += [dataShort for i in range(100)]
            moveDirList += [direction for i in range(100)]
            nList += [row[dataType+'_n'] for i in range(100)]
            frequencyList = np.append(frequencyList,row[dataType+'_medData'][:,0],axis=0)
            psdMedianList = np.append(psdMedianList,row[dataType+'_medData'][:,1],axis=0)
            upperCIList = np.append(upperCIList,row[dataType+'_medData'][:,2],axis=0)
            lowerCIList = np.append(lowerCIList,row[dataType+'_medData'][:,3],axis=0)

listOLists =[speciesList, adultList, sexList, lightList, windList, waterList, dataTypeList, 
             moveDirList, nList, frequencyList, psdMedianList, upperCIList, lowerCIList] 
columns=['species', 'adult', 'sex', 'light', 'wind', 'water', 'dataType','movement direction',
         'n', 'frequency','psd median','upper 0.95 CI','lower 0.95 CI']

dfLong = pd.DataFrame(dict(zip(columns,listOLists)))
dfLong.to_hdf('./BjoernDataMedianCILong.h5',key = 'df')

#%% Long form table for individual 

df = pd.read_hdf('./BjoernDataMedianCI.h5',key = 'df')
dataStr = ['psd_H_preStim','psd_H_stim', 'psd_H_resp', 'psd_H_postStim', 
           'psd_V_preStim','psd_V_stim', 'psd_V_resp', 'psd_V_postStim']


speciesList = list() 
adultList = list()
sexList = list()
lightList = list()
windList = list()
waterList = list()
idList = list()
dataTypeList = list()
nList = list()
moveDirList = list()
frequencyList = np.array([])
psdMedianList = np.array([])
upperCIList = np.array([])
lowerCIList = np.array([])   
for ind,row in df.iterrows():
    for dataType in dataStr:
        dataShortF, direction,dataShortE = dataType.split('_')
        if direction == 'H':
            direction = 'horizontal'
        else:
            direction = 'vertcial'
        dataShort = dataShortF+' '+dataShortE
        if row[dataType+'_medData'] is not None:
            indData =row[dataType+'_rawData'].transpose(2,0,1).reshape(-1,2)  
            rowN = indData.shape[0]
            speciesList += [row['species'] for i in range(rowN)] 
            adultList += [row['adult'] for i in range(rowN)]
            sexList += [row['sex'] for i in range(rowN)]
            lightList += [row['light'] for i in range(rowN)]
            windList += [row['wind'] for i in range(rowN)]
            waterList += [row['water'] for i in range(rowN)]
            idList  += [[i for x in range(100)] for i in range(row[dataType+'_n'])]
            dataTypeList += [dataShort for i in range(rowN)]
            moveDirList += [direction for i in range(rowN)]
            nList += [row[dataType+'_n'] for i in range(rowN)]
            frequencyList = np.append(frequencyList,indData[:,0],axis=0)
            psdMedianList = np.append(psdMedianList,indData[:,1],axis=0)


listOLists =[speciesList, adultList, sexList, lightList, windList, waterList, 'id',dataTypeList, 
             moveDirList, nList, frequencyList, psdMedianList] 
columns=['species', 'adult', 'sex', 'light', 'wind', 'water','id', 'dataType','movement direction',
         'n', 'frequency','power spectral density']

dfLong = pd.DataFrame(dict(zip(columns,listOLists)))
dfLong.to_hdf('./BjoernDataMedianCILongInd.h5',key = 'df')



#%%

plt.figure(figsize=(5, 4))
line, = plt.semilogx(mean[:,0],mean[:,1],'.-')
    #line.set_label(key)
#plt.title('PSD: power spectral density ' + gender + ' ' + expTyp)
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.legend()
plt.tight_layout()
#plt.savefig(os.path.join(expDir,'psd.svg'))
plt.show()


'''
const_dark-const_wind:
1. "1:24:55<05:41" (89/100) (hab filenamen nicht mehr gesehen)
2. 2021-09-15__13-13-04 (Med-male)
'''

