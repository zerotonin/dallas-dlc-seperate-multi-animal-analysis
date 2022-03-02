import explorationRateBasedonBB
import augmentYegiTra
import os, getopt,sys


if __name__ == '__main__':
    
    # get input variables
    usageStr = 'usage: runExpoAnaYegiData.py -t <traFilePos>  -m <metaDataFlag> -f <fps> -a <activityThreshold>'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ht:m:f:a:",["traFilePos=","metaDataFlag=",'fps=',"activityThreshold="])
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
    if os.path.isfile(traFilePos) == False:
        raise ValueError(f'-i is not an existing file: {traFilePos} ')
    if metaDataFlag == '28':
        metaDataFlag = '<29'
    elif metaDataFlag== '29':
        metaDataFlag ='>29'

    print(traFilePos,activityThreshold,metaDataFlag,fps)
    ayt = augmentYegiTra.augmentYegiTra(traFilePos,metaDataFlag,fps,activityThreshold)
    ayt.run()
    
    expo = explorationRateBasedonBB.explorationRateCalculator(ayt.traPos)
    expo.analyseAllAnimals()
