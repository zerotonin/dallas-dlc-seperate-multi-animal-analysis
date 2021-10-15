import DLC_reader
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from scipy import signal
import scipy.spatial

class BjornAnaGUI():

    def __init__(self,traPos):
        self.traPos = traPos
        self.metaDict = metaData(traPos).main()
        self.pix2mm = 350.0/715.0
        self.fps    = 250
        self.filter_cutoff = 20
        self.filter_order  = 5
        self.keys = ['head', 'left procoxa', 'left mesocoxa', 'left metacoxa', 'right procoxa', 'right mesocoxa', 'right metacoxa', 'left protibia joint', 'left mesotibia joint', 'left metatibia joint', 'right protibia joint', 'right mesotibia joint', 'right metatibia joint', 'left protarsus', 'left mesotarsus', 'left metatarsus', 'right protarsus', 'right mesotarsus', 'right metatarsus', 'abdomen', 'mesothorax']
        self.stableKeys =  ['head', 'left procoxa', 'left mesocoxa', 'left metacoxa', 'abdomen', 'mesothorax']
        self.timeBorders = [9.5,10.5,12.0]


    def readTra(self):
        readObj = DLC_reader.DLC_H5_reader(self.traPos,1)  
        readObj.readH5()
        readObj.singleAnimal2numpy()
        tra = dict()
        for i in range(readObj.tra.shape[1]):
            test = readObj.tra[:,i,:].copy()
            tra[self.keys[i]] = test 

        return tra

    

    def butter_lowpass(self):
        nyq = 0.5 * self.fps
        normal_cutoff = self.filter_cutoff / nyq
        b, a = signal.butter(self.filter_order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self,data):
        b, a = self.butter_lowpass()
        y = signal.filtfilt(b, a, data)
        return y
    
    def get_mmTRA(self):
        self.tra_mm = dict()
        for key in self.mostStableKeys:
            temp        = self.tra_pix[key].copy()
            temp[:,0:2] = temp[:,0:2]*self.pix2mm
            self.tra_mm[key] = temp

    def filter_mmTRA(self):
        self.tra_mm_filt = dict()
        for key in self.tra_mm:
            temp        = self.tra_mm[key].copy()
            temp[:,0] = self.butter_lowpass_filter(temp[:,0])
            temp[:,1] = self.butter_lowpass_filter(temp[:,1])
            self.tra_mm_filt[key] = temp

    def normalise2FirstSecond(self,vals):
        set2zero = vals.copy()
        set2zeroFirst = np.mean(vals[0:self.fps,0:2],axis=0)
        set2zero[:,0:2] = set2zero[:,0:2]-set2zeroFirst
        return set2zero

    def meanOfMostStable(self):
        traList = list()
        for key,vals in self.tra_mm_filt.items():
            set2zero = self.normalise2FirstSecond(vals)
            traList.append(set2zero)
        self.tra_mean = np.dstack(traList)
        self.tra_mean = np.mean(self.tra_mean,axis=2)

    def main(self):
        self.tra_pix = self.readTra()
        self.scGUI = StableChoiceGUI({key: self.tra_pix[key] for key in self.stableKeys})
        self.scGUI.prepareData()
        self.scGUI.plotStableChoice()
        self.mostStableKeys = self.scGUI.chosenList
        self.get_mmTRA()
        self.filter_mmTRA()
        self.meanOfMostStable()
        self.tsGUI =TimeSeriesGUI(self)
        self.calculatePSD()
        self.plotPSDs()
        dataDict = self.compileOutPut()
        return dataDict

    def compileOutPut(self):
        dataDict                      = self.metaDict
        dataDict['fps']               = self.fps
        dataDict['pix2mm']            = self.pix2mm
        dataDict['tra_mean']          = self.tra_mean
        dataDict['mostStableMarkers'] = self.mostStableKeys
        dataDict['psd_H_preStim']     = self.psdHorizDict['preStim']
        dataDict['psd_H_stim']        = self.psdHorizDict['stim']
        dataDict['psd_H_resp']        = self.psdHorizDict['resp']
        dataDict['psd_H_postStim']    = self.psdHorizDict['postStim']
        dataDict['psd_V_preStim']     = self.psdVertDict['preStim']
        dataDict['psd_V_stim']        = self.psdVertDict['stim']
        dataDict['psd_V_resp']        = self.psdVertDict['resp']
        dataDict['psd_V_postStim']    = self.psdVertDict['postStim']
        dataDict['traPos']            = self.traPos
        return dataDict


    def getIntBorders(self):
        self.timeBordersInt = np.array(self.timeBorders)
        self.timeBordersInt = np.round(self.timeBordersInt*self.fps)
        self.timeBordersInt = self.timeBordersInt.astype(int)
        self.timeBordersInt = np.insert(self.timeBordersInt,0,0)
        self.timeBordersInt = np.append(self.timeBordersInt,self.tra_mean.shape[0])

    def calculatePSD(self):
        self.getIntBorders()
        self.psdHorizDict = dict()
        self.psdVertDict = dict()
        keys = ['preStim','stim','resp','postStim']
        for i in range(4):
            freqs, psd = signal.welch(self.tra_mean[self.timeBordersInt[i]:self.timeBordersInt[i+1],0],fs=self.fps)
            self.psdHorizDict[keys[i]] = np.column_stack((freqs,psd))         
            freqs, psd = signal.welch(self.tra_mean[self.timeBordersInt[i]:self.timeBordersInt[i+1],1],fs=self.fps)
            self.psdVertDict[keys[i]] = np.column_stack((freqs,psd))         
    def plotPSDs(self):
        fig,axL = plt.subplots(2,2)
        keys = list(self.psdVertDict.keys())
        axL = axL.reshape(-1)
        for i in range(4):
            ax = axL[i]
            line, = ax.semilogx( self.psdHorizDict[keys[i]][:,0],  self.psdHorizDict[keys[i]][:,1])
            line.set_label(keys[i]+' horizontal')
            line2, = ax.semilogx( self.psdVertDict[keys[i]][:,0],  self.psdVertDict[keys[i]][:,1])
            line2.set_label(keys[i]+' vertical')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Power')
            ax.legend()
        plt.tight_layout()
        plt.show()



class TimeSeriesGUI():
    def __init__(self,bag):
        self.bag = bag
        self.fig, (self.ax1,self.ax2)= plt.subplots(2, 1)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.set_size_inches(18.5, 10.5)
        self.borderCounter = 1
        self.borderY = []
        self.refreshGUI()
        plt.show()

    def getTimeAx(self,traLen):
        return np.linspace(0,traLen/self.bag.fps,traLen)
        
    def updateBorderCounter(self):
        self.borderCounter +=1 
        self.borderCounter = self.borderCounter%3
    
    def plotMovement(self):
        lineStyleList = ['--','-.',':']
        lineNameList  = ['pre stim|stim','stim|response','response|post stim']
    
        for key in self.bag.tra_mm_filt:
            tra = self.bag.tra_mm_filt[key]
            tra = self.bag.normalise2FirstSecond(tra)
            tax = self.getTimeAx(tra.shape[0])
            self.ax1.plot(tax,tra[:,0]-tra[0,0],label=key)
            self.ax2.plot(tax,tra[:,1]-tra[0,1],label=key)
        for  i in range(3):
            tidx = self.bag.timeBorders[i]
            self.ax1.plot([tidx,tidx],self.ax1.get_ylim(),'k'+lineStyleList[i],label=lineNameList[i])
            self.ax2.plot([tidx,tidx] ,self.ax2.get_ylim(),'k'+lineStyleList[i],label=lineNameList[i])
        self.ax1.plot(tax,self.bag.tra_mean[:,0],label='mean',linewidth=2)
        self.ax2.plot(tax,self.bag.tra_mean[:,1],label='mean',linewidth=2)
        self.ax2.legend()
        self.ax2.set_xlabel('time, s')
        self.ax2.set_ylabel('vertical movement, mm')
        self.ax1.set_ylabel('horizontal movement, mm')
        self.ax1.set_title(f' Now setting border: {lineNameList[self.borderCounter-1]}')
        plt.draw()
    
    def refreshGUI(self):
        self.ax1.cla()
        self.ax2.cla()
        self.plotMovement()
            
    def onclick(self,event):
        if event.button is MouseButton.LEFT:
            self.bag.timeBorders[self.borderCounter-1] = event.xdata
            self.updateBorderCounter()
            self.refreshGUI()

        if event.button is MouseButton.RIGHT:
            plt.close(self.fig)



class StableChoiceGUI():
    def __init__(self,tra_pix):
        self.tra_pix = tra_pix
        self.ckdtree = None
        self.groupID = None
        self.chosenList = list()
    
    def prepareData(self):
        self.groupID = list()
        self.points = list()
        for key,vals in self.tra_pix.items():
            self.points.append(vals[:,0:2])
            self.groupID += [key for i in range(vals.shape[0])]
        self.points = np.vstack(tuple(self.points))
        self.ckdtree = scipy.spatial.cKDTree(self.points)

    def plotStableChoice(self):
        self.fig, self.ax= plt.subplots(1, 1)
        self.fig.set_size_inches(18.5, 10.5)
        for key in self.tra_pix:
            self.ax.scatter(self.tra_pix[key][:,0],self.tra_pix[key][:,1],label=key)
        self.ax.invert_yaxis()
        self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.ax.axis('equal')
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.updateTitle()
        plt.show()
    
    def onclick(self,event):
        if event.button is MouseButton.LEFT:
            choice = self.closest_groupID(event.xdata, event.ydata)
            if choice in self.chosenList:
                self.chosenList.remove(choice)
            else:
                self.chosenList.append(choice)
            self.updateTitle()
        if event.button is MouseButton.RIGHT:
            if self.chosenList != []:
                plt.close(self.fig)

            

    def updateTitle(self):
        titleStr = f'left mouse button to chose marker | currently chosen: f{self.chosenList}'
        self.ax.set_title(titleStr)
        plt.tight_layout()
        plt.draw()





    def closest_point_distance(self, x, y):
        #returns distance to closest point
        return self.ckdtree.query([x, y])[0]

    def closest_point_id(self, x, y):
        #returns index of closest point
        return self.ckdtree.query([x, y])[1]

    def closest_point_coords(self, x, y):
        # returns coordinates of closest point
        return self.ckdtree.data[self.closest_point_id(x, y)]
        # ckdtree.data is the same as points

    def closest_groupID(self,x,y):
        # returns coordinates of closest point
        return self.groupID[self.closest_point_id(x, y)]



class  metaData():
    def __init__(self,traPos):
        self.traPos = traPos
    
    def main(self):
        self.getMetaData()
        metaDict ={'species':self.species,'adult':self.adult,
                   'sex':self.sex,'light':self.light,
                   'wind':self.wind,'water':self.water}
        return metaDict


    def getMetaData(self):
        self.determineSex()
        self.determineWind()
        self.determineLightCondition()
        self.determineWaterStim()
        self.determineAge()
        self.determineSpecies()
    
    def determineSpecies(self):
        if 'Medauroidea' in self.traPos:
            self.species = 'Medauroidea extradentata'
        elif 'Sungaya' in self.traPos:
            self.species = 'Sungaya inexpectata'
        else:
            self.species = 'Unknown'

    
    def determineAge(self):
        if 'Subadult' in self.traPos:
            self.adult = False
        else:
            self.adult = True


    def determineWaterStim(self):
        if 'water' in self.traPos:
            self.water = True
        else:
            self.water = False

    def determineLightCondition(self):
        if 'Dark' in self.traPos:
            self.light = False
        else:
            self.light = True

    def determineWind(self):
        if 'noWind' in self.traPos:
            self.wind = False
        else:
            self.wind = True

    def determineSex(self):
        if 'female' in self.traPos:
            self.sex = 'female'
        else:
            self.sex ='male'

if __name__ == '__main__':
    traPos = '/media/gwdg-backup/BackUp/Bjoern/Experiments/constantLight_constantWind_waterAt10_20secDur/Medauroidea/Subadult/male/2021-08-31__18-17-16DLC_resnet152_MedauroideaMaleSep30shuffle1_750000.h5'
    #traPos = '/media/gwdg-backup/BackUp/Bjoern/Experiments/constantLight_noWind_waterAt10_20secDur/Medauroidea/Adult/male/2021-09-03__14-11-42DLC_resnet152_MedauroideaMaleSep30shuffle1_750000.h5'
    bag = BjornAnaGUI(traPos)
    data = bag.main()

  