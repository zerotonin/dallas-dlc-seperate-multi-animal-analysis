class phasmidAnatomy:
    def __init__(self,species,gender):

        self.knownSpecies = ['Sungaya inexpectata','Medauroidea extradentata','Neohirasea maerens']
        
        if gender!='f' and gender!='m':
            print('Unknown gender: ' + gender)
        else:
            self.gender = gender

        if species in self.knownSpecies:
            self.species = species
            self.getPhasmidAnatomy()
        else:
            print('Unknown species: ' +species)
        
    def getAxisLength(self,axisName):
        if axisName in self.anatomy.keys():
            return self.anatomy[axisName]
        else:
            return -1
    
    def getPhasmidAnatomy(self):
        if self.species  == 'Neohirasea maerens':
            self.getAnatomy_Neohirasea()
        elif self.species  == 'Medauroidea extradentata':
            self.getAnatomy_Medauroidea()
        elif self.species  == 'Sungaya inexpectata':
            self.getAnatomy_Sungaya()
        else:
            print('Unknown get-Axis function for species: ' +self.species )
    
    def getAnatomy_Neohirasea(self):
        if self.gender == 'f':
            self.anatomy = {'right metacoxa' + ' -> ' +'right metatibia joint'  : 17.08,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 17.08,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 22.81,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 22.81,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 12.43,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 12.43,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 16.18,
                            'left mesotbia joint'+ ' -> ' +'left mesotarsus'    : 16.18,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 15.77,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 15.77,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 20.05,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 20.05,
                            'head'+ ' -> ' +'mesothoracic spikes'               : 19.39,
                            'mesothoracic spikes'+ ' -> ' +'metathoracic spikes': 6.47,
                            'metathoracic spikes'+ ' -> ' +'abdomen'            : 16.27,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 13.78,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 6.44,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 15.7,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 6.44,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 15.7}
        else:
            self.anatomy = {'right metacoxa' + ' -> ' +'right metatibia joint'  : 15.59,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 15.59,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 23.35,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 23.35,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 12.3,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 12.3,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 17.06,
                            'left mesotibia joint'+ ' -> ' +'left mesotarsus'   : 17.06,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 15.48,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 15.48,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 20.16,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 20.16,
                            'head'+ ' -> ' +'mesothoracic spikes'               : 14.72,
                            'mesothoracic spikes'+ ' -> ' +'metathoracic spikes': 4.63,
                            'metathoracic spikes'+ ' -> ' +'abdomen'            : 13.49,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 15.08,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 6.58,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 11.7,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 6.58,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 11.7}
    
    def getAnatomy_Medauroidea(self):
        if self.gender == 'f':
            self.anatomy = {'right metacoxa' + ' -> ' +'right metatibia joint'  : 29.34,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 29.34,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 40.81,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 40.81,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 25.99,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 25.99,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 31.51,
                            'left mesotbia joint'+ ' -> ' +'left mesotarsus'    : 31.51,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 39.0,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 39.0,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 40.94,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 40.94,
                            'head'+ ' -> ' +'mesothorax'                        : 34.56,
                            'mesothorax'+ ' -> ' +'abdomen'                     : 36.16,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 23.45,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 16.34,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 23.1,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 16.34,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 23.1}
        else:
            self.anatomy= {'right metacoxa' + ' -> ' +'right metatibia joint'   : 26.77,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 26.77,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 41.08,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 41.08,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 22.18,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 22.18,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 31.89,
                            'left mesotbia joint'+ ' -> ' +'left mesotarsus'    : 31.89,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 33.53,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 33.53,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 49.74,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 49.74,
                            'head'+ ' -> ' +'mesothorax'                        : 25.89,
                            'mesothorax'+ ' -> ' +'abdomen'                     : 40.55,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 17.58,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 14.12,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 18.68,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 14.12,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 18.68}

    def getAnatomy_Sungaya(self):
        if self.gender == 'f':
            self.anatomy = {'right metacoxa' + ' -> ' +'right metatibia joint'  : 20.31,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 20.31,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 24.48,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 24.48,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 15.46,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 15.46,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 18.34,
                            'left mesotbia joint'+ ' -> ' +'left mesotarsus'    : 18.34,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 17.16,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 17.16,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 21.3,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 21.3,
                            'right antenna base'+ ' -> ' +'head'                : 5.54,
                            'left antenna base'+ ' -> ' +'head'                 : 5.54,
                            'head'+ ' -> ' +'mesonotum'                         : 16.44,
                            'mesonotum'+ ' -> ' +'metanotum'                    : 7.76,
                            'metanotum'+ ' -> ' +'abdomen'                      : 20.71,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 25.41,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 11.55,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 14.97,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 11.55,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 14.97}
        else:
            self.anatomy = {'right metacoxa' + ' -> ' +'right metatibia joint'  : 16.18,
                            'left metacoxa' + ' -> ' +'left metatibia joint'    : 16.18,
                            'right metatibia joint'+ ' -> ' +'right metatarsus' : 20.79,
                            'left metatibia joint'+ ' -> ' +'left metatarsus'   : 20.79,
                            'right mesocoxa' + ' -> ' +'right mesotibia joint'  : 12.76,
                            'left mesocoxa' + ' -> ' +'left mesotibia joint'    : 12.76,
                            'right mesotibia joint'+ ' -> ' +'right mesotarsus' : 14.08,
                            'left mesotbia joint'+ ' -> ' +'left mesotarsus'    : 14.08,
                            'right procoxa' + ' -> ' +'right protibia joint'    : 13.54,
                            'left procoxa' + ' -> ' +'left protibia joint'      : 13.54,
                            'right protibia joint'+ ' -> ' +'right protarsus'   : 17.18,
                            'left protibia joint'+ ' -> ' +'left protarsus'     : 17.18,
                            'right antenna base'+ ' -> ' +'head'                : 4.46,
                            'left antenna base'+ ' -> ' +'head'                 : 4.46,
                            'head'+ ' -> ' +'mesonotum'                         : 14.01,
                            'mesonotum'+ ' -> ' +'metanotum'                    : 6.81,
                            'metanotum'+ ' -> ' +'abdomen'                      : 19.71,
                            'abdomen'+ ' -> ' +'abdomen apex'                   : 13.84,
                            'right metacoxa'+ ' -> ' +'right mesocoxa'          : 6.8,
                            'right mesocoxa'+ ' -> ' +'right procoxa'           : 11.99,
                            'left metacoxa'+ ' -> ' +'left mesocoxa'            : 6.8,
                            'left mesocoxa'+ ' -> ' +'left procoxa'             : 11.99}
