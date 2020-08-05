import mediaHandler,os,tqdm
from importlib import reload 
from pathlib import Path

reload(mediaHandler)

sourceDir ='/media/bgeurten/Anka/Anka2/19_05_17'
seq_Files = [f for f in os.listdir(sourceDir) if f.endswith('.seq')]
seq_Files.sort()

for seqFile in tqdm.tqdm(seq_Files,desc='files seq->avi: '):
    seqFile = os.path.join(sourceDir,seqFile)
    targetFile = seqFile[:-3] +'avi'    
    mhObj = mediaHandler.mediaHandler(seqFile,'norpix')
    mhObj.transcode_seq2avis(targetFile)
    os.system('clear')