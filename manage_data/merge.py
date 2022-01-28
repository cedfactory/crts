import os, fnmatch
import pandas as pd

def merge_csv_to_df(path, pattern):
    current_dir = os.getcwd()
    os.chdir(path)

    listOfFilesToRemove = os.listdir('./')
    #pattern = "*.csv"
    li = []
    for entry in listOfFilesToRemove:
        if fnmatch.fnmatch(entry, pattern):
            print("csv file : ",entry)
            df = pd.read_csv(entry, index_col=None, header=0)
            li.append(df)
            os.remove(entry)

    df_frame = pd.concat(li, axis=0, ignore_index=True)

    # today = date.today()
    # df_frame.to_csv("stocks_movments_merged_" + str(today) + ".csv", index=True, sep='\t')

    os.chdir(current_dir)

    return df_frame