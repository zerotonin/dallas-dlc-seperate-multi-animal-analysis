import pandas as pd
import numpy as np 
df_AllColors = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0, skipfooter=3,index_col="State")
df_DCyellow = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DCyellow1","DCyellow2","DCyellow3","DCyellow4","DCyellow5"], skipfooter=3,index_col="State")
df_DCgreen = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DCgreen1","DCgreen2","DCgreen3","DCgreen4","DCgreen5"], skipfooter=3,index_col="State")
df_DCblue = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DCblue1","DCblue2","DCblue3","DCblue4","DCblue5"], skipfooter=3,index_col="State")
#DCYellow_Mean = df_DCyellow.mean(axis=1)
#DCBlue_Mean = df_DCblue.mean(axis=1)
#DCGreen_Mean = df_DCgreen.mean(axis=1)
df_DOyellow = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DOyellow1","DOyellow2","DOyellow3","DOyellow4","DOyellow5"], skipfooter=3,index_col="State")
df_DOgreen = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DOgreen1","DOgreen2","DOgreen3","DOgreen4","DOgreen5"], skipfooter=3,index_col="State")
df_DOblue = pd.read_excel("/Users/test/Documents/Master/Masterthesis/DevelopmentalTime2.xlsx", sheet_name=0,usecols=["State","DOblue1","DOblue2","DOblue3","DOblue4","DOblue5"], skipfooter=3,index_col="State")
#DOYellow_Mean = df_DOyellow.mean(axis=1)
#DOBlue_Mean = df_DOblue.mean(axis=1)
#DOGreen_Mean = df_DOgreen.mean(axis=1)
Descr_DC_Yellow = df_DCyellow.apply(pd.DataFrame.describe, axis=1) 
Descr_DC_Blue = df_DCblue.apply(pd.DataFrame.describe, axis=1)
Descr_DC_Green = df_DCgreen.apply(pd.DataFrame.describe, axis=1)
Descr_DO_Yellow = df_DOyellow.apply(pd.DataFrame.describe, axis=1)
Descr_DO_Blue = df_DOblue.apply(pd.DataFrame.describe, axis=1)
Descr_DO_Green = df_DOgreen.apply(pd.DataFrame.describe, axis=1)

#add columns with the means to the table
df_AllColors["MeanDCyellow"]= df_DCyellow.mean(axis=1)
df_AllColors["MeanDCblue"]= df_DCblue.mean(axis=1)
df_AllColors["MeanDCgreen"]= df_DCgreen.mean(axis=1)
df_AllColors["MeanDOyellow"]= df_DOyellow.mean(axis=1)
df_AllColors["MeanDOblue"]= df_DOblue.mean(axis=1)
df_AllColors["MeanDOgreen"]= df_DOgreen.mean(axis=1)

# select the last 6 columns with the averages
df_Averages = df_AllColors.iloc[:,-6:]

# identify the day where hatched eggs >= 50% laied eggs
# 50% of laied eggs
LE_50 =list()
a=df_Averages.iloc[0]
for LE in a:
    b = LE/2
    LE_50.append(b)
print (LE_50)

LE_50_DCyellow = LE_50[0]
LE_50_DCblue = LE_50[1]
LE_50_DCgreen = LE_50[2]
LE_50_DOyellow = LE_50[3]
LE_50_DOblue = LE_50[4]
LE_50_DOgreen = LE_50[5]


# find the day where 50% eggs have hatched
a = list()
HE_DCyellow = df_Averages.iloc[1:9,0]
for HE_50 in HE_DCyellow:
    if HE_50 >= LE_50_DCyellow:
        b = df_Averages.iloc(HE_50)[0]
        a.append(b)
        break
print (a)

# maximum number of hatched eggs
HE_Max = df_Averages.loc["HE-192h"]

'''


#HE_50 =list()
# find the index in th elist where 50% of the max number of laied eggs have hatched
HE_hours=df.iloc[1:9,1:]
for HE in HE_hours:
    for LE in LE_50:
        if HE >= LE:
         print (HE)

#for HE in HE-hours:#[1::]:
 #   b = HE/2
  #  HE_50.append(b)
#print (HE_50)
# maximal number of Pupae
Pupae_Max = df.loc[df["Color"] == "Pupae-264h"]
# maximal number of adults
Adult_Max = df.loc[df["Color"] == "adult-384h"]
#df.isnull().sum()
#df.describe()
'''