import readMultiAnimalCharonTra
import explorationRateBasedonBB
import augmentYegiTra
import os, getopt,sys


if __name__ == '__main__':
    
    # get input variables
    usageStr = 'usage: runExpoAnaYegiData.py -t <traFilePos>  -m <metaDataFlag> -f <fps> -a <activityThreshold> -b <arenaBoundingBoxFilePos> -s <movieFilePos> -x <arenaWidthMM> -y <arenaHeightMM> -o <outputDir>'
    try:
         opts, args = getopt.getopt(sys.argv[1:],"ht:m:f:a:b:s:x:y:o:",["traFilePos=","metaDataFlag=",'fps=',"activityThreshold=", "arenaBoundingBoxFilePos=", "movieFilePos=", "arenaWidthMM=", "arenaHeightMM=", "outputDir="])
        #print(sys.argv)
    except getopt.GetoptError:
        print(usageStr)
        sys.exit(2)

    #parse Inputs
    traFilePos  = False
    print(opts)
    for o, a in opts:
  
        # if user asks for help 
        if o == '-h':
            print(usageStr)
            sys.exit(2)
        elif o == '-t':
            traFilePos = a
        elif o == '-a':
            activityThreshold = float(a)
        elif o == '-m':
            metaDataFlag = a
        elif o == '-f':
            fps = float(a)
        elif o == '-b':
            arenaBoundingBoxFilePos = a
        elif o == '-s':
            movieFilePos = a
        elif o == '-x':
            arenaWidthMM = float(a)
        elif o == '-y':
            arenaHeightMM = float(a)
        elif o == '-o':
            outputDir = a
    
    # make files
    if os.path.isfile(traFilePos) == False:
        raise ValueError(f'-i is not an existing file: {traFilePos} ')
    if os.path.isfile(arenaBoundingBoxFilePos) == False:
        raise ValueError(f'-i is not an existing file: {arenaBoundingBoxFilePos} ')
    if os.path.isfile(movieFilePos) == False:
        raise ValueError(f'-i is not an existing file: {movieFilePos} ')
    
    # get meta data right
    if metaDataFlag == '28':import readMultiAnimalCharonTra
import explorationRateBasedonBB
import augmentYegiTra
import os, getopt,sys


if __name__ == '__main__':
    
    # get input variables
    usageStr = 'usage: runExpoAnaYegiData.py -t <traFilePos>  -m <metaDataFlag> -f <fps> -a <activityThreshold> -b <arenaBoundingBoxFilePos> -s <movieFilePos> -x <arenaWidthMM> -y <arenaHeightMM> -o <outputDir>'
    try:
         opts, args = getopt.getopt(sys.argv[1:],"ht:m:f:a:b:s:x:y:o:",["traFilePos=","metaDataFlag=",'fps=',"activityThreshold=", "arenaBoundingBoxFilePos=", "movieFilePos=", "arenaWidthMM=", "arenaHeightMM=", "outputDir="])
        #print(sys.argv)
    except getopt.GetoptError:
        print(usageStr)
        sys.exit(2)

    #parse Inputs
    traFilePos  = False
    print(opts)
    for o, a in opts:
  
        # if user asks for help 
        if o == '-h':
            print(usageStr)
            sys.exit(2)
        elif o == '-t':
            traFilePos = a
        elif o == '-a':
            activityThreshold = float(a)
        elif o == '-m':
            metaDataFlag = a
        elif o == '-f':
            fps = float(a)
        elif o == '-b':
            arenaBoundingBoxFilePos = a
        elif o == '-s':
            movieFilePos = a
        elif o == '-x':
            arenaWidthMM = float(a)
        elif o == '-y':
            arenaHeightMM = float(a)
        elif o == '-o':
            outputDir = a
    
    # make files
    if os.path.isfile(traFilePos) == False:
        raise ValueError(f'-i is not an existing file: {traFilePos} ')
    if os.path.isfile(arenaBoundingBoxFilePos) == False:
        raise ValueError(f'-i is not an existing file: {arenaBoundingBoxFilePos} ')
    if os.path.isfile(movieFilePos) == False:
        raise ValueError(f'-i is not an existing file: {movieFilePos} ')
    
    # get meta data right
    if metaDataFlag == '28':
        metaDataFlag = '<29'    
    elif metaDataFlag== '29':
        metaDataFlag ='>29'

    # make filenames
    fileName     = os.path.basename(traFilePos)[0:-4]   
    cleanTraOut  = os.path.join(outputDir,fileName+'_trajectory.h5')
    meanArenaOut = os.path.join(outputDir,fileName+'_meanArena.csv')
   
    # read trajectory
    cmar = readMultiAnimalCharonTra.readMultiAnimalCharonTra(traFilePos,movieFilePos,arenaBoundingBoxFilePos,arenaHeightMM,arenaWidthMM)
    cmar.run()
    cmar.saveAna(meanArenaOut,cleanTraOut)
    del(cmar)

    #augement data
    ayt = augmentYegiTra.augmentYegiTra(cleanTraOut,metaDataFlag,fps,activityThreshold)
    ayt.run()
    
    #calculate exploration rate
    expo = explorationRateBasedonBB.explorationRateCalculator(ayt.savePos)
    del(ayt)
    expo.analyseAllAnimals()

