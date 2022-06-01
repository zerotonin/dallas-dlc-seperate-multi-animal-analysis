# Using readlines() 
file1 = open('foodTestTra.tra', 'r') 
Lines = file1.readlines() 
  

# Zeilen bearbeiten
line = Lines[0]

# each object is encapsuilated in ><
objectList = line.split('>')
print(objectList)
# get frameNumber
frameNumber = int(objectList[0][0:-3])
del(objectList[0]) #deletes framenumber from line...wozu muss man das löschen?
print('FrameNumber:', frameNumber) 

#object splitting
objectValList=objectList[29].split(',') # number in [] is the object number in the objectlist in line (depending on (line7: line = Lines[0]))
objectValList[5]= objectValList[5][0:-2] #deletes space and < at the end of the object at position 6 (0-5)
print(objectValList)

#get object Name
objectName = objectValList[0]
print (objectName)

#get fly Position
x0 = float (objectValList[2])
y0 = float (objectValList[3])
x1 = float (objectValList[4])
y1 = float (objectValList[5])

#get arena Position
x0a = float (objectValList[2])
y0a = float (objectValList[3])
x1a = float (objectValList[4])
y1a = float (objectValList[5])

#get marker Position 
x0m = float (objectValList[2])
y0m = float (objectValList[3])
x1m = float (objectValList[4])
y1m = float (objectValList[5])

if objectName == 'fly':
    flyPosition = (x0+x1)/2
    print ('flyPosition:',flyPosition)
elif objectName == 'arena':
    arenaPosition = (x0a+x1a)/2
    print ('arenaPosition:',arenaPosition)
elif objectName == 'marker':
    markerPosition = (x0m+x1m)/2
    print ('markerPosition:',markerPosition)

#flyPositionInArena 
arenaCenter = arenaPosition/2
if flyPosition < arenaCenter:
    print ('flyPositionInArena: left')
elif flyPosition > arenaCenter:
    print ('flyPositionInArena: right')
elif flyPosition == arenaCenter:
    print ('flyPositionInArena: center')

#get quality from object
objectQuality = float (objectValList[1])
print (objectQuality)


#get arena number

#find marker

#mean of arena over time

#get fly position in arena
# if clause to check if there is no fly / 2 flies than skip the next steps and discard this arena? else next steps?
# for loop add up number of times righ / left of flyposition in one arena 
# densityPropability = (l-r)/(l+r)
# if densityPropability < 1 
 #   print ('fly preferes right')
  #  else if densityPropability == 0 
   #     print('no preferation')
    #    else print ('fly preferes left')

#(count = 0
# Strips the newline character 
#for line in Lines: 
#   print("Line{}: {}".format(count, line.strip())) )