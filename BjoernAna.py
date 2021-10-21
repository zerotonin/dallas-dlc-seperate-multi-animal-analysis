#%% imports
import BjornAnaGUI
from tqdm import tqdm
import numpy as np
import pandas as pd
from importlib import reload
from pathlib import Path


def areYouDoneYet():
    inputCorrect = False
    while inputCorrect == False:
        answer = input('Do you want to repeat this file (y/n):' )
        if answer == 'y' or answer == 'n':
            inputCorrect = True
            return answer

#%% Read data
folderName = 'constantDark_noWind'
parentPath = '/media/gwdg-backup/BackUp/Bjoern/Experiments/'+folderName
saveFile   = './'+folderName+'.h5'
data = list()
fileList = [x for x in Path(parentPath).rglob('*.h5')]
for path in tqdm(fileList,desc='analysing...'):
    done = False
    while done == False:
        bag = BjornAnaGUI.BjornAnaGUI(str(path))
        answer = areYouDoneYet()
        if answer == 'n':
            done = True
        else:
            data.append(bag.main())


df = pd.DataFrame(data)
df.to_hdf(saveFile,key='df')