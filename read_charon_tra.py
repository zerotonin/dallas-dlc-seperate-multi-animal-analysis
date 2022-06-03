from tqdm import tqdm
import os
class read_charon_tra():
    def __init__(self,file_position):

        self.file_position = file_position # filePosition = file name
        self.rawTextData  = []           # preallocation with empty list

    def read_raw_text_entire_file(self):
        temporay_file_dialog = open(self.file_position, 'r')  # 'r': open for reading
        self.rawTextData = temporay_file_dialog.readlines()  # reading row wise 
        temporay_file_dialog.close()
        #print(self.rawTextData)               # and print it into the rawTextData List?

    def split_line_into_image_objects(self,line): 
        '''
        This function splits all objects in a line of raw text data. 
        The strings are split by the > symbol
        Function returns a list of string containing all found objects in this line, but ignores the framenumber.
        '''
        object_list = line.split('>')  # each object is encapsuilated in ><
        del(object_list[0]) # first entry is frameNumber
        return object_list

    def get_frame_number_from_line(self,line):
        '''
        This function returns the frame number as int from a given text data line.
        '''
        object_list = line.split('>')
        frame_number = int(object_list[0][0:-3])
        return frame_number

    def split_image_object_to_list(self,image_object_string):
        '''
        Each object consist out of one string (the object name) and 5 numbers: quality ,y0,x0,y1,x1
        The last for are the minimum and maximum of the bounding box of the object given
        in coordinates normalised to the picture size.
        The string containing this data is seperated by commata and is now split at these and the 
        numerical data are converted into floats. The return value is a list consistent of a string
        and five floats. 
        '''
        object_value_list=image_object_string.split(',') # object Values are seperated by ','
        object_value_list[5]= object_value_list[5][0:-2] # delete the last two characters of the string ' <'
        # convert all values into float except of the first which is the name of the object already given as a string
        for i in range(1,6):
            object_value_list[i]= float(object_value_list[i]) # convert string into floating point number
        # return object values in list
        return object_value_list

    def image_object_list_to_dict(self,object_value_list): # putting objectValues into Dictionary
        '''
        This function transforms the list of object values returned by self.readImageObject
        into a dictionary with the following keys and values

        keys         : values
        =============:======================================================================
        name         : a string with the identifier of the object, e.g. 'fly','arena','marker'
        centerOfMass : a tuple holding two floats the x and y coordinate normalised to the 
                       image size 
        quality      : a float with the normalized quality of detection 0->1
        boundingBox  : a tuple of four float with the minimum and maximum coordinates of the 
                       bounding box in the succession (y0,x0,y1,x1)
        '''
        # shorthands for name and quality
        image_objec_name = object_value_list#[0]
        quality   = object_value_list#[1]
        # combine coordinates into a tuple to avoid permutation of coordinates
        bounding_box_coordinates = tuple(object_value_list[2::])   # a Tupel is a finite ordered list of elements
        # caclulate center of mass
        y,x = self.calculate_center_of_mass_from_BB(bounding_box_coordinates)
        center_of_mass = (y,x) # make tuple to avoid permutation

        # define a dictionary with the data and return it
        return {'name':image_objec_name,'centerOfMass': center_of_mass, 'quality': quality, 'boundingBox': bounding_box_coordinates} #dictionary{key:value pairs}

    def calculate_center_of_mass_from_BB(self,bounding_box_coordinates):
        '''
        To get the middle or center of mass of a bounding box you need to
        calculate the mean of the x-coordinates and y-coordinates respectively.
        '''
        y = (bounding_box_coordinates[0]+bounding_box_coordinates[2])/2.0
        x = (bounding_box_coordinates[1]+bounding_box_coordinates[3])/2.0
        return y,x
    
    def read_image_object_per_line(self,line): 
        # get image objects as list of strings from line
        image_objects  = self.split_line_into_image_objects(line)  
        # get frame number as integer from line
        frame_number   = self.get_frame_number_from_line(line)
        # initialize return list with frame number
        image_object_dict_list = [frame_number]
        # this for loop transverses through the list of string img Obj
        for image_object in image_objects:
            # object string is split in different values and numericals are converted to floats
            object_value_list = self.split_image_object_to_list(image_object)
            # converts list of data into a structer dict
            image_object_dictionary = self.image_object_list_to_dict(object_value_list)
            # add dict to return list
            image_object_dict_list.append(image_object_dictionary)       
        return image_object_dict_list

    def convert_entire_raw_file_to_dicts(self):
        '''
        Convert the raw text data into a list in which each element is the data of a frame.
        Each frame consists of a list, which first element is the frame number as an integer. All following
        elements are dictionaries in the following format:

        keys         : values
        =============:======================================================================
        name         : a string with the identifier of the object, e.g. 'fly','arena','marker'
        centerOfMass : a tuple holding two floats the x and y coordinate normalised to the 
                       image size 
        quality      : a float with the normalized quality of detection 0->1
        boundingBox  : a tuple of four float with the minimum and maximum coordinates of the 
                       bounding box in the succession (ymin,xmin,ymax,ymin)

        '''
        # preallocation of an empty list
        self.image_object_data = list()
        # for loop transverses each line of the file
        for line in tqdm(self.rawTextData,desc = 'converting text to dict'):
            # each line is read and converted into an image object dictionary list and appended to self.imgObjData
            self.image_object_data.append(self.read_image_object_per_line(line))

    def read_entire_small_file(self):
        '''
        Main reader class.
        Reads the file at the position stored in self.filePosition.
        The raw text data is stored in a list of strings in self.rawTextData.
        The output list of image object dictionaries is stored in self.imObjData.
        '''
        # read text data from file
        self.read_raw_text_entire_file()
        # convert text data 2 img object dictionaries
        self.convert_entire_raw_file_to_dicts()

    def read_file(self,maximum_lines = -1):
        self.image_object_data = list()
        file_dialog = open(self.file_position, 'r')
        line_count = 0
        progress_bar_str='-\|/' 
        while True and (line_count <= maximum_lines):
            line_count += 1
            os.system("printf '\033c'")
            print(f'{progress_bar_str[line_count%4]} reading line {line_count}', flush=True)
    
            # Get next line from file
            line = file_dialog.readline()
            # if line is empty end of file is reached
            if not line:
                break
            self.image_object_data.append(self.read_image_object_per_line(line))
 
        file_dialog.close()
        


        

import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib import cm
import itertools
class plotCharonFood:
    def __init__(self):
        pass

    def boundingBox2MPLrect(self,boundingBox,edgeColor, labelStr = ""):
        # Bounding box of an image object is ymin,xmin,ymax,xmax
        # also the y axis is inverse
        # matplotlib patches expects xmin and ymin plus width and height of the box

        # add a rectangle
        rect = mpatches.Rectangle((boundingBox[1],boundingBox[0]),boundingBox[3]-boundingBox[1],boundingBox[2]-boundingBox[0],
                                edgecolor = edgeColor, fill=False,label=labelStr,linewidth=1)
        return rect

    def mplRects4ImgObjList(self,imgObjList, edgeColor='g', labelTag='imgObj'):
        imgObjRects = list()
        imgObjC = 0
        for imgObj in imgObjList:
            imgObjRects.append(self.boundingBox2MPLrect(imgObj['boundingBox'],edgeColor, labelTag +'_'+str(imgObjC)))
            imgObjC += 1
        return imgObjRects

    def plotRecognisedImgObjBoundBoxes(self,arenaList,flyList):
        objectRects  = self.mplRects4ImgObjList(flyList,edgeColor=[0, 0, 1],labelTag ='fly')
        objectRects += self.mplRects4ImgObjList(arenaList,edgeColor= [1,0,0], labelTag ='arena')
        
        fig, ax = plt.subplots()

        for patch in objectRects:
            ax.add_patch(patch)
        plt.axis('equal')
        plt.show()

    def plotFlyAssignmentControll(self,arenaList,videoFly,step =1):
        # colormap
        plasmaCM  = cm.get_cmap('plasma', 54)
        plasmaCol = plasmaCM.colors
        # make arenas
        objectRects = self.mplRects4ImgObjList(arenaList,edgeColor= [0.5,0.5,0.5], labelTag ='arena')
        # figure window
        fig, ax = plt.subplots()
        # add arena patches
        for patch in objectRects:
            ax.add_patch(patch)
        # add flies
        for flyList in itertools.islice(videoFly,0,None,step):
            for i in range(54):
                if flyList[i] is not None:
                    ax.add_patch(self.boundingBox2MPLrect(flyList[i]['boundingBox'],edgeColor=plasmaCol[i], labelStr = "fly"))

        plt.axis('equal')
        #plt.show()
