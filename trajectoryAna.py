class trajectoryAna():
    
    def __init__(self,trajectory,fps,pix2mmObj):
        self.trajectory = trajectory 
        self.fps        = fps        
        self.pix2mmObj  = pix2mmObj  


class pix2mm():

    def __init__(self,mmArray,pixArray,mode):
        self.mmArray  = mmArray  
        self.pixArray = pixArray 
        self.mode     = mode     