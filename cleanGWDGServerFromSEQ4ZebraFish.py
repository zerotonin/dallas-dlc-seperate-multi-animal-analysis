import mediaHandler,os,tqdm,copy,shutil
import numpy as np
from pathlib import Path
from importlib import reload 
from cv2 import cv2

def transcodeSeqLocally(seqFile,sourceDir,localDir,expectedSize = 0):
    
    sourcePos = os.path.join(sourceDir,seqFile)
    localPos  = os.path.join(localDir,seqFile)
    targetPos = sourcePos[:-3] +'avi'    
    
    print('source position: ',sourcePos)    
    print('local position: ',localPos)
    print('target position: ',targetPos)
    if os.path.getsize(sourcePos) >= expectedSize:

        try:
            shutil.move(sourcePos,localPos)
            mhObj = mediaHandler.mediaHandler(localPos,'norpix')
            mhObj.transcode_seq2avis(targetPos)
            os.remove(localPos)
        except:
            print('Could not handle: ', sourcePos)
    else:
        print('File size too small: ', sourcePos) 
    os.system('clear')


sourceDir = '/media/gwdg-backup/BackUp/Bart/IR28bdBenzer/seqFiles'
localDir  = '/home/bgeurten/Videos'
expectedSize = 0 #80000000000 about 80GB
seq_Files = [f for f in os.listdir(sourceDir) if f.endswith('.seq')]
seq_Files.sort()
os.system('clear')
#print(os.listdir(sourceDir) )

for seqFile in tqdm.tqdm(seq_Files,desc='files seq->avi: '):
    transcodeSeqLocally(seqFile,sourceDir,localDir,expectedSize)