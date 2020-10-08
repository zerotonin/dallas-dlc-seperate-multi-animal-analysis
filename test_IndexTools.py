import indexTools
import matplotlib.pyplot as plt 
from importlib import reload 
reload(indexTools)
fig = plt.figure() 
ax = fig.add_subplot(211) 
ax.plot(x[0:10])
ax2 = fig.add_subplot(212)
ax2.plot(indexTools.bracket_Bools(x[0:10]))    
plt.show() 