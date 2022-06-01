import cv2,os
from matplotlib.image import BboxImage
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class markerExtractor():
    def __init__(self, image,bboxSize=270):
        #save inputs
        self.img      = image
        self.bboxSize = bboxSize 
        #initialise values
        self.coords     = list()
        self.markerList = list()
        self.ongoing    = True
        #start figure and events
        plt.ion()
        self.fig, self.ax = plt.subplots(1)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press) 
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
    
    def on_click(self,event):
        ix, iy = event.xdata, event.ydata
        self.coords.append((ix, iy))
        self.refreshImage()
    
    def on_press(self,event):
        if event.key == 'd':
            if self.coords:
                self.coords = self.coords[:-1]
                self.refreshImage()
        elif event.key == 'q' or event.key == 'Q':
            plt.close()
            self.ongoing = False
               
    def refreshImage(self):
        plt.cla()
        self.ax.imshow(self.img)
        # Create a Rectangle patch
        for coord in self.coords:
            coord = np.array(coord)
            coord = coord - self.bboxSize/2
            rect = patches.Rectangle(coord, self.bboxSize, self.bboxSize, linewidth=5, edgecolor='r', facecolor='none')
            # Add the patch to the Axes
            self.ax.add_patch(rect)
        self.ax.set_title(f'pick markers clockwise starting top left | bounding box size: {self.bboxSize} | q or Q = ends picking | d = deletes last pick' )
        self.fig.canvas.draw()
    
    def extract(self):
        self.refreshImage()
        while self.ongoing:
            plt.pause(0.1)

        self.coords = np.array(self.coords,dtype=int)
        self.bboxes = np.hstack((self.coords-self.bboxSize/2,self.coords+self.bboxSize/2))
        self.bboxes = np.array(self.bboxes,dtype=int)
        markers = list()
        for i in range(self.bboxes.shape[0]):
            markers.append(self.img[self.bboxes[i,1]:self.bboxes[i,3],self.bboxes[i,0]:self.bboxes[i,2]])


        return self.coords, np.array(markers)
