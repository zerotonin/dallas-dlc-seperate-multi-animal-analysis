import matplotlib.pyplot as plt
import numpy as np

def standardPlot(frame,traObj,traSteps):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = plt.get_cmap('tab20b')  
    ax.imshow(frame)
    plotSlots(traObj,ax)
    plotTraPix(traObj,ax,cmap,traSteps)
    plt.show()

def standardPlotTrajectory(tra,traSteps,animalColor):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plotLollipop(tra,ax,animalColor,traSteps)
    ax.axis('equal')
    plt.show()


def plotSlots(traObj,ax):
        for animalI in  range(traObj.animalNo):
            ax.fill(traObj.slotCoord[animalI][:,0],traObj.slotCoord[animalI][:,1],fill=None,edgecolor='salmon') 

def plotTraPix(traObj,ax,cmap,traSteps):

    for animalI in  range(traObj.animalNo):
        plotLollipop(traObj.tra[:,animalI,:,0:2],ax,cmap.colors[animalI],traSteps)
            
            
def plotLollipop(tra,ax,animalColor,traSteps):
    for frameI in np.linspace(0,tra.shape[0],traSteps, endpoint=False, dtype=int ):
        ax.plot(tra[frameI,:,0],tra[frameI,:,1],'-',color=animalColor)        
        ax.plot(tra[frameI,0,0],tra[frameI,0,1],'.',color=animalColor)


def plotErrorTra(traObj,ax,cmap):
    for frameI in np.linspace(0,traObj.frameNo,100, endpoint=False, dtype=int ):

        for animalI in  range(traObj.animalNo):

            if traObj.artifactCandidates[frameI,animalI]:
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'k-')        
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'kx')
            else:
                ax.plot(traObj.tra[frameI,animalI,:,0],traObj.tra[frameI,animalI,:,1],'-',color=cmap.colors[animalI])        
                ax.plot(traObj.tra[frameI,animalI,0,0],traObj.tra[frameI,animalI,0,1],'.',color=cmap.colors[animalI])


