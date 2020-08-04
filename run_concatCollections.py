import yaml,xlsxwriter,os,fnmatch,datetime,math
from natsort import natsorted, ns

archiveDir    = '/media/dataSSD/AnkaArchive'


xlsxFN        = os.path.join(archiveDir,'archiveData_'+datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d__%H-%M-%S')+'.xlsx') 
yamlDir       = os.path.join(archiveDir,'yamls') 

#get all files that were analysed by this AI in source directory

yamlFiles = []
for root, dirnames, filenames in os.walk(yamlDir):
    for filename in fnmatch.filter(filenames, '*.yaml'):
        yamlFiles.append(os.path.join(root, filename))

natsorted(yamlFiles)
with xlsxwriter.Workbook(xlsxFN) as workbook:
    worksheet = workbook.add_worksheet()

    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'})
    worksheet.merge_range('A1:C1', 'Fly Identification', merge_format)
    worksheet.merge_range('D1:J1', 'Benzer Quantification', merge_format)
    worksheet.merge_range('K1:AD1', 'Speed Quantification', merge_format)
    worksheet.merge_range('AE1:AH1', 'Video Parameter', merge_format)
    worksheet.merge_range('AI1:AM1', 'external Data', merge_format)
    #writeHeaders
    worksheet.write(1, 0,'collection')    #A
    worksheet.write(1, 1,'movieFileName') #B
    worksheet.write(1, 2,'flyID')         #C
    worksheet.write(1, 3,'activityScore') #D
    worksheet.write(1, 4,'crossedMidLineBool')#E
    worksheet.write(1, 5,'crossedMidLineTimeSec')#F
    worksheet.write(1, 6,'dropScore')#G
    worksheet.write(1, 7,'predominantBodyAngleDeg') #H
    worksheet.write(1, 8,'reachedTopBool')#I
    worksheet.write(1, 9,'reachedTopTimeSec') #J
    worksheet.write(1,10,'speedClimb_Max_MMperSec') #K
    worksheet.write(1,11,'speedClimb_Mean_MMperSec')#L
    worksheet.write(1,12,'speedClimb_Median_MMperSec')#M
    worksheet.write(1,13,'speedClimb_Min_MMperSec')#N
    worksheet.write(1,14,'speedSlip_Max_MMperSec')#O
    worksheet.write(1,15,'speedSlip_Mean_MMperSec')#P
    worksheet.write(1,16,'speedSlip_Median_MMperSec')#Q
    worksheet.write(1,17,'speedSlip_Min_MMperSec')#R
    worksheet.write(1,18,'speedSumABS_Max_MMperSec')#S
    worksheet.write(1,19,'speedSumABS_Mean_MMperSec')#T
    worksheet.write(1,20,'speedSumABS_Median_MMperSec')#U
    worksheet.write(1,21,'speedSumABS_Min_MMperSec')#V
    worksheet.write(1,22,'speedThrust_Max_MMperSec')#W
    worksheet.write(1,23,'speedThrust_Mean_MMperSec')#X
    worksheet.write(1,24,'speedThrust_Median_MMperSec')#Y
    worksheet.write(1,25,'speedThrust_Min_MMperSec')#Z
    worksheet.write(1,26,'speedYaw_Max_MMperSec')#AA
    worksheet.write(1,27,'speedYaw_Mean_MMperSec')#AB
    worksheet.write(1,28,'speedYaw_Median_MMperSec')#AC
    worksheet.write(1,29,'speedYaw_Min_MMperSec')#AD
    worksheet.write(1,30,'frameNo')#AE
    worksheet.write(1,31,'framesPerSecond')#AF
    worksheet.write(1,32,'recordingDate')#AG
    worksheet.write(1,33,'pix2mmFactor')#AH
    worksheet.write(1,34,'anaObjFileName')#AI
    worksheet.write(1,35,'exampelPictureFN')#AJ
    worksheet.write(1,36,'jsonFile')#AK
    worksheet.write(1,37,'traCSVFileName')#AL
    worksheet.write(1,38,'yamlFile')#AM

    for fileI in range(len(yamlFiles)):
        rowIndex = fileI+2
        dataFile = yaml.load(open(yamlFiles[fileI]),Loader=yaml.FullLoader)
        for key,val in dataFile.items(): 
            if type(val) == float: 
                if math.isnan(val): 
                    val = 'NaN' 
                    dataFile[key] = val   

        worksheet.write(rowIndex, 0,dataFile['collection'])    #A
        worksheet.write(rowIndex, 1,dataFile['movieFileName']) #B
        worksheet.write(rowIndex, 2,dataFile['flyID'])         #C
        worksheet.write(rowIndex, 3,dataFile['activityScore']) #D
        worksheet.write(rowIndex, 4,dataFile['crossedMidLineBool'])#E
        worksheet.write(rowIndex, 5,dataFile['crossedMidLineTimeSec'])#F
        worksheet.write(rowIndex, 6,dataFile['dropScore'])#G
        worksheet.write(rowIndex, 7,dataFile['predominantBodyAngleDeg']) #H
        worksheet.write(rowIndex, 8,dataFile['reachedTopBool'])#I
        worksheet.write(rowIndex, 9,dataFile['reachedTopTimeSec']) #J
        worksheet.write(rowIndex,10,dataFile['speedClimb_Max_MMperSec']) #K
        worksheet.write(rowIndex,11,dataFile['speedClimb_Mean_MMperSec'])#L
        worksheet.write(rowIndex,12,dataFile['speedClimb_Median_MMperSec'])#M
        worksheet.write(rowIndex,13,dataFile['speedClimb_Min_MMperSec'])#N
        worksheet.write(rowIndex,14,dataFile['speedSlip_Max_MMperSec'])#O
        worksheet.write(rowIndex,15,dataFile['speedSlip_Mean_MMperSec'])#P
        worksheet.write(rowIndex,16,dataFile['speedSlip_Median_MMperSec'])#Q
        worksheet.write(rowIndex,17,dataFile['speedSlip_Min_MMperSec'])#R
        worksheet.write(rowIndex,18,dataFile['speedSumABS_Max_MMperSec'])#S
        worksheet.write(rowIndex,19,dataFile['speedSumABS_Mean_MMperSec'])#T
        worksheet.write(rowIndex,20,dataFile['speedSumABS_Median_MMperSec'])#U
        worksheet.write(rowIndex,21,dataFile['speedSumABS_Min_MMperSec'])#V
        worksheet.write(rowIndex,22,dataFile['speedThrust_Max_MMperSec'])#W
        worksheet.write(rowIndex,23,dataFile['speedThrust_Mean_MMperSec'])#X
        worksheet.write(rowIndex,24,dataFile['speedThrust_Median_MMperSec'])#Y
        worksheet.write(rowIndex,25,dataFile['speedThrust_Min_MMperSec'])#Z
        worksheet.write(rowIndex,26,dataFile['speedYaw_Max_MMperSec'])#AA
        worksheet.write(rowIndex,27,dataFile['speedYaw_Mean_MMperSec'])#AB
        worksheet.write(rowIndex,28,dataFile['speedYaw_Median_MMperSec'])#AC
        worksheet.write(rowIndex,29,dataFile['speedYaw_Min_MMperSec'])#AD
        worksheet.write(rowIndex,30,dataFile['frameNo'])#AE
        worksheet.write(rowIndex,31,dataFile['framesPerSecond'])#AF
        worksheet.write(rowIndex,32,dataFile['recordingDate'])#AG
        worksheet.write(rowIndex,33,dataFile['pix2mmFactor'])#AH
        worksheet.write(rowIndex,34,dataFile['anaObjFileName'])#AI
        worksheet.write(rowIndex,35,dataFile['exampelPictureFN'])#AJ
        worksheet.write(rowIndex,36,dataFile['jsonFile'])#AK
        worksheet.write(rowIndex,37,dataFile['traCSVFileName'])#AL
        worksheet.write(rowIndex,38,dataFile['yamlFile'])#AM


