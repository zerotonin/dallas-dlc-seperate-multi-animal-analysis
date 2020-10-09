import indexTools
import matplotlib.pyplot as plt 
from importlib import reload 
reload(indexTools)
for i in range(15):
    fig = plt.figure() 
    ax = fig.add_subplot(211) 
    ax.plot(optTraObj.artifactCandidates[:,i])
    ax2 = fig.add_subplot(212)
    ax2.plot(optTraObj.tra[:,i,0,0])
plt.show() 