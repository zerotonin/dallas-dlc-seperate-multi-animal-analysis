import mediaHandler,os,tqdm,copy
import numpy as np
from pathlib import Path
from importlib import reload 
from cv2 import cv2

# transcoding example
reload(mediaHandler)

sourceDir ='/media/gwdg-backup/BackUp/VicHalim'
seq_Files = [f for f in os.listdir(sourceDir) if f.endswith('.seq')]
seq_Files.sort()
os.system('clear')

for seqFile in tqdm.tqdm(seq_Files,desc='files seq->avi: '):
    seqFile = os.path.join(sourceDir,seqFile)
    targetFile = seqFile[:-3] +'avi'    
    mhObj = mediaHandler.mediaHandler(seqFile,'norpix')
    mhObj.transcode_seq2avis(targetFile)
    os.system('clear')


# registration example
reload(mediaHandler)

sourceDir ='/media/dataSSD/SealVids'
unregMovies = [f for f in os.listdir(sourceDir) if f.endswith('.MTS')]
unregMovies.sort()

for seqFile in tqdm.tqdm(unregMovies,desc='files MTS->avi: '):
    seqFile = os.path.join(sourceDir,seqFile)
         
    targetFile = seqFile[:-4] +'_reg.avi'    
    mhObj = mediaHandler.mediaHandler(seqFile,'movie')
    mhObj.register_movie(seqFile,targetFile)


    os.system('clear')

# after registration
reload(mediaHandler)
mhObj = mediaHandler.mediaHandler('/media/gwdg-backup/AutoBenzerSwap/2020-07-03__13_35_41.avi','movie')
img = mhObj.getFrame(105)    
tmp = mhObj.getFrame(207)  
res = mhObj.registerImage(tmp,img)   