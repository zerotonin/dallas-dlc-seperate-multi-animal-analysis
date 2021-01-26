def readFoodTra(fileName):
    file1 = open(fileName, 'r') 
    lines = file1.readlines() 
    return lines
    
data = readFoodTra('foodTestTra.tra')          