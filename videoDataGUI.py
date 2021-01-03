import mediaHandler,time
import matplotlib.pyplot as plt
import numpy as np



class videoDataGUI():

    def __init__(self,videoPos,vidType='movie'):
        self.media     = mediaHandler.mediaHandler(videoPos,vidType)

    
    def tellme(self,s):
        print(s)
        plt.title(s, fontsize=16)
        plt.draw()

    
    def getArenaData(self,frame):
        imgplot = plt.imshow(frame)

        plt.setp(plt.gca(), autoscale_on=False)
        plt.get_current_fig_manager().full_screen_toggle() 
     

        self.tellme('You will define a box, click to begin')

        plt.waitforbuttonpress()

        while True:
            pts = []
            while len(pts) < 4:
                self.tellme('Select 4 corners with mouse')
                pts = np.asarray(plt.ginput(4, timeout=-1))
                if len(pts) < 4:
                    self.tellme('Too few points, starting over')
                    time.sleep(1)  # Wait a second

            ph = plt.fill(pts[:, 0], pts[:, 1], 'y', lw=2,alpha=0.5)

            self.tellme('Happy? Key click for yes, mouse click for no')

            if plt.waitforbuttonpress():
                break

            # Get rid of fill
            for p in ph:
                p.remove()
        #clear overlay
        plt.close('all')
        return pts

    def run(self):
        self.frame = self.media.getFrame(int(self.media.length/2))
        self.arenaCoordinates = self.getArenaData(self.frame)
        return self.arenaCoordinates