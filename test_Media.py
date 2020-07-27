import mediaHandler,cv2,os,tqdm
from importlib import reload 
import matplotlib.pyplot as plt
from pathlib import Path


testFile = Path('/media/gwdg-backup/BackUp/Anka/2018-04-19__10_41_58.seq')
# Define the codec and create VideoWriter object 
fourcc = cv2.VideoWriter_fourcc('m','j','p','g')
targetFile = os.path.join(testFile.parent,testFile.name[:-3] +'mp4'    )
mhObj = mediaHandler.mediaHandler(testFile,'norpix')
sourceFPS = round(mhObj.fps)
frameShape = mhObj.media.frame_shape  
frameShape = (frameShape[1],frameShape[0])   
allocatedFrames = mhObj.media.header_dict['allocated_frames']    

out = cv2.VideoWriter(targetFile,fourcc, sourceFPS,frameShape) 

for frameNo in tqdm.tqdm(range(1000)):#allocatedFrames)):
#frameNo  = 23
    frame = mhObj.getFrame(frameNo)
    #gray = cv2.normalize(frame, None, 255, 0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    gray_3c = cv2.merge([frame, frame, frame])
    frame = cv2.flip(frame,0)
    out.write(gray_3c)
#cv2.imshow('frame',frame)

frameNo  = 23
frame = mhObj.getFrame(frameNo)
imgplot = plt.imshow(frame)
plt.show()