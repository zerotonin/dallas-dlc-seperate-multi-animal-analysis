import foodChoiceAna
import tqdm,datetime,os,csv
from importlib import reload 
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import chisquare

def list_files(directory, extension): 
    fileList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if os.path.splitext(f)[1] == '.'+extension]
    fileList.sort()
    return fileList

#user data

AI_pattern = 'DLC_resnet50_FoodColourChoiceSep8shuffle1_200000_bx.h5'
startFile  = 0

flyPos  = list_files("/media/gwdg-backup/BackUp/VicHalim/rawTraces","h5")
flyPos.sort()
metaPos = list_files("/media/gwdg-backup/BackUp/VicHalim/metaData","xml")
metaPos.sort()

reload(foodChoiceAna)
data= list()
for movieI in range(len(flyPos)):
    fCA = foodChoiceAna.foodChoiceAna(flyPos[movieI],metaPos[movieI],12,AI_pattern)
    data += fCA.runAnalysis()


with open("/media/gwdg-backup/BackUp/VicHalim/output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)



with open("/media/gwdg-backup/BackUp/VicHalim/output.csv", newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)


#Score
c   = 0
cs  = [list(),list(),list(),list()]
rut = [list(),list(),list(),list()]
dun = [list(),list(),list(),list()]
for exp in data:
    if exp[2] == 'blue':
        colorIDX = 1
    elif exp[2] == 'green':
        colorIDX = 2
    else:
        colorIDX = 3

    if float(exp[9])+float(exp[8])>100:
        if exp[0] == 'cs':
            cs[0].append(float(exp[6]))
            cs[colorIDX].append(float(exp[6]))           
        elif exp[0] == 'rut':
            rut[0].append(float(exp[6]))
            rut[colorIDX].append(float(exp[6]))
        else:
            dun[0].append(float(exp[6]))
            dun[colorIDX].append(float(exp[6]))

titleList = ['combined','blue','green','yellow' ]

for i in range(4):
    plotData = [cs[i],rut[i],dun[i]]
    fig,ax   = plt.subplots(nrows=1, ncols=1)
    ax.plot([0.5,3.5],[0,0],'k--')
    ax.boxplot(plotData,notch="on",labels=['Canton S', 'rutabaga','Dunce'])
    plt.title('Rearing colour: ' + titleList[i])
    plt.ylabel('score [-1 new color | 1 rearing color]')
    plt.ylim((-1.05,1.05))
    plt.savefig(os.path.join('/media/gwdg-backup/BackUp/VicHalim/','score_'+str(i)+'.svg'))


#Percentage
cs  = [list(),list(),list(),list()]
rut = [list(),list(),list(),list()]
dun = [list(),list(),list(),list()]
quantifier = 4
for exp in data:
    if exp[2] == 'blue':
        colorIDX = 1
    elif exp[2] == 'green':
        colorIDX = 2
    else:
        colorIDX = 3

    if float(exp[9])+float(exp[8])>100:
        if exp[0] == 'cs':
            cs[0].append(float(exp[quantifier])*100)
            cs[colorIDX].append(float(exp[quantifier])*100)           
        elif exp[0] == 'rut':
            rut[0].append(float(exp[quantifier])*100)
            rut[colorIDX].append(float(exp[quantifier])*100)
        else:
            dun[0].append(float(exp[quantifier])*100)
            dun[colorIDX].append(float(exp[quantifier])*100)

titleList = ['combined','blue','green','yellow' ]

for i in range(4):
    plotData = [cs[i],rut[i],dun[i]]
    fig,ax   = plt.subplots(nrows=1, ncols=1)
    ax.plot([0.5,3.5],[50,50],'k--')
    ax.boxplot(plotData,notch="on",labels=['Canton S', 'rutabaga','Dunce'])
    plt.title('Rearing colour: ' + titleList[i])
    plt.ylabel('Rearing color chosen, in %')
    plt.ylim((-1,101))
    plt.savefig(os.path.join('/media/gwdg-backup/BackUp/VicHalim/','percentage_'+str(i)+'.svg'))

#Coinestimate
cs  = [list(),list(),list(),list()]
rut = [list(),list(),list(),list()]
dun = [list(),list(),list(),list()]
quantifier = 7
for exp in data:
    if exp[2] == 'blue':
        colorIDX = 1
    elif exp[2] == 'green':
        colorIDX = 2
    else:
        colorIDX = 3

    if float(exp[9])+float(exp[8])>100:
        if exp[0] == 'cs':
            cs[0].append(float(exp[quantifier]))
            cs[colorIDX].append(float(exp[quantifier]))           
        elif exp[0] == 'rut':
            rut[0].append(float(exp[quantifier]))
            rut[colorIDX].append(float(exp[quantifier]))
        else:
            dun[0].append(float(exp[quantifier]))
            dun[colorIDX].append(float(exp[quantifier]))

titleList = ['combined','blue','green','yellow' ]

for i in range(4):
    freq = [np.sum(np.array(cs[i]),axis=0)/len(cs[i]),np.sum(np.array(rut[i]),axis=0)/len(rut[i]),np.sum(np.array(dun[i]),axis=0)/len(dun[i])]
    fig,ax   = plt.subplots(nrows=1, ncols=1)
    ax.plot([-0.5,2.5],[0.5,0.5],'k--')
    ax.bar(range(3),freq)
    plt.title('Rearing colour: ' + titleList[i])
    plt.ylabel('binonminal frequency')
    plt.xticks(range(3), ('Canton S', 'rutabaga','Dunce'))
    plt.ylim((0,1))
    plt.savefig(os.path.join('/media/gwdg-backup/BackUp/VicHalim/','binominal_'+str(i)+'.svg'))


plt.show() 


