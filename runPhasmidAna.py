
import DLC_reader,trajectory_correcter,dallasPlots,trajectoryAna, phasmidAnalysis
import tqdm,datetime,os,glob
import numpy as np
from importlib import reload
from os import walk
import matplotlib.pyplot as plt
from scipy import signal
 
def list_files(directory, extension): 
    fileList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.'+extension]
    fileList.sort()
    return fileList

strainName              = 'Neohirasea maerens'
strainDir               = '/media/dataSSD/AlexVids/Neohirasea_videos'#/media/dataSSD/AlexVids/Sungaya_videos/'
qualityThreshold        = 0.25
minimalTrajectoryLength = 10


#get file positions
fPos = list_files(strainDir,'h5')
 
reload(phasmidAnalysis)
for fileI in tqdm.tqdm(range(len(fPos)),desc='detection files '):
    #reload(phasmidAnalysis)
    #fileI = 0

    #read dlc file
    readObj = DLC_reader.DLC_H5_reader(fPos[fileI],1)  
    readObj.readH5()
    readObj.singleAnimal2numpy() 
    # get phasmid axis data
    # mmTra
    pAna = phasmidAnalysis.phasmidAnalysis(fPos[fileI],strainName,qualityThreshold,readObj,minimalTrajectoryLength)

    if pAna.subTras != {}:
        sig=list()
        for key in pAna.subTras.keys():
            for data in pAna.subTras[key]:
                data = np.diff(data[1][:,0:2],axis=0)
                sig.append(np.sum(abs(data),axis=1))
        sig = np.concatenate(np.array(sig))
        freqs, psd = signal.welch(sig,fs=30)
        psdData = np.transpose(np.vstack((freqs,psd)))   
        np.savetxt(fPos[fileI][:-3]+'_PSD.csv' , psdData, header="freq,power spectral density", delimiter=",")




psdDir         = '/media/dataSSD/AlexVids/Neohirasea_videos/PSD'
stimTypeList   = ['15Hz','10Hz','5Hz','3Hz','2Hz','1Hz','0.5Hz','fast','slow','downward', 'upward']  
genderList     = ['female','male']
expTypList     = ['lights_movement','lights_only','movement_only']

for gender in genderList:
    genderDir =os.path.join(psdDir,gender)
    for expTyp in expTypList:
        expDir =os.path.join(genderDir,expTyp)
        fPos = list_files(expDir,'csv')
        expDict = {}
        for stimType in stimTypeList:
            res = [i for i in fPos if stimType in i] 
            psdDataList =list()
            for f in res:
                temp = np.loadtxt(f,delimiter=",")
                temp[:,1] = temp[:,1]/np.sum(temp[:,1])
                if temp.shape[0] == 129:
                    psdDataList.append(temp)
                fPos.remove(f)
            if psdDataList != []:
                expDict[stimType] = np.mean(np.dstack(psdDataList),axis=2)
        plt.figure(figsize=(5, 4))
        for key in expDict.keys():
            line, = plt.semilogx(expDict[key][:,0], expDict[key][:,1],'.-')
            line.set_label(key)
        plt.title('PSD: power spectral density ' + gender + ' ' + expTyp)
        plt.xlabel('Frequency')
        plt.ylabel('Power')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(expDir,'psd.svg'))
        plt.show()

