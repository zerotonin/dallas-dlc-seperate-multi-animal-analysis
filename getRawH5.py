import deeplabcut,os
 
def list_files(directory, extension): 
    fileList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.'+extension]
    fileList.sort()
    return fileList

fPos = list_files("/media/dataSSD/Vic_Bx/","pickle")

for pFile in fPos:
    deeplabcut.convert_raw_tracks_to_h5("/media/dataSSD/deepLabCut/FoodColourChoice-Victoria-2020-09-08/config.yaml",pFile) 


