import matplotlib.pyplot as plt
import numpy as np

def standardPlot(frame,traObj):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = plt.get_cmap('tab20b')  
    ax.imshow(frame)
    plotSlots(traObj,ax)
    plotTra(traObj,ax,cmap)
    plt.show()

def plotSlots(traObj,ax):
        for animalI in  range(traObj.animalNo):
            ax.fill(traObj.slotCoord[animalI][:,0],traObj.slotCoord[animalI][:,1],fill=None,edgecolor='salmon') 

def plotTra(traObj,ax,cmap):
    for frameI in np.linspace(0,traObj.frameNo,100, endpoint=False, dtype=int ):

        for animalI in  range(traObj.animalNo):
            
            ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'-',color=cmap.colors[animalI])        
            ax.plot(traObj.tra[frameI,animalI,0,0],traObj.tra[frameI,animalI,0,1],'.',color=cmap.colors[animalI])



def plotErrorTra(traObj,ax,cmap):
    for frameI in np.linspace(0,traObj.frameNo,100, endpoint=False, dtype=int ):

        for animalI in  range(traObj.animalNo):

            if y.artifactCandidates[frameI,animalI]:
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'k-')        
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'kx')
            else:
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'-',color=cmap.colors[animalI])        
                ax.plot(traObj.tra[frameI,animalI,0,0],traObj.tra[frameI,animalI,0,1],'.',color=cmap.colors[animalI])


