# Using readlines() 
file1 = open('foodTestTra.tra', 'r') 
Lines = file1.readlines() 
  

# Zeilen bearbeiten
line = Lines[0]
# each object is encapsuilated in ><
objectList = line.split('>')
# get frameNumber
frameNumber = int(objectList[0][0:-3])
del(objectList[0])

#object splitting
objectValList=objectList[2].split(',')
objectValList[5]= objectValList[5][0:-2]

count = 0
# Strips the newline character 
for line in Lines: 
    print("Line{}: {}".format(count, line.strip())) 