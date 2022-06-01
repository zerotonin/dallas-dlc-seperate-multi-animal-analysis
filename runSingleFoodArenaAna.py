import os, getopt,sys
from charonFoodTra import readCharonFood54
from analyseSingleArenaTra import analyseSingleArenaTra

if __name__ == '__main__':
    
    # get input variables
    usageStr = 'usage: analyseSingleArenaTra.py -i <FilePositionOfTrajectory> -f <framesPerSecond> -o <outputFilePos> \n output is an h5 file with key = fly'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:f:n:z:o:",["filePos=","fps=",'savePos='])
        #print(sys.argv)
    except getopt.GetoptError:
        print(usageStr)
        sys.exit(2)

    #parse Inputs
    filePos         = False
    savePos         = False
    neutralZone     = (0.5,0.5)
    fps             = 10
    objectNameList  = ['arena','fly']

    for o, a in opts:
        # if user asks for help 
        if o == '-h':
            print(usageStr)
        elif o == '-i':
            filePos = a
        elif o == '-f':
            fps = float(a)
        elif o == '-o':
            savePos = a

    if os.path.isfile(filePos) == False:
        raise ValueError(f'-i is not an existing file: {filePos} ')

    reader = readCharonFood54(filePos)
    reader.readFile()
    asa = analyseSingleArenaTra(reader.imObjData,filePos,neutralZone=neutralZone,fps=fps,objectNameList = objectNameList)
    asa.run()
    asa.data.to_hdf(savePos,key='fly')          
