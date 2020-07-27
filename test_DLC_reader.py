import DLC_reader 
from importlib import reload 


reload(DLC_reader)
fPos = '/media/dataSSD/Anka4/2019-09-25__10_23_32DeepCut_resnet50_darkClimbFliesSep27shuffle1_1030000.h5'
x = DLC_reader.DLC_H5_reader(fPos)  
x.readH5()
x.multiAnimal2numpy()