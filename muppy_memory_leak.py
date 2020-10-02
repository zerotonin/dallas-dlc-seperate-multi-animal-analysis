from pympler import muppy, summary
import pandas as pd

def checkMemory():
    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)# Prints out a summary of the large objects

    summary.print_(sum1)# Get references to certain types of objects such as dataframe

    dataframes = [ao for ao in all_objects if isinstance(ao, pd.DataFrame)]

    for d in dataframes:
        print(d.columns.values)
        print(len(d))

        #test for git