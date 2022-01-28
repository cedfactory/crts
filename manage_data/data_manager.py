import datetime
import pandas as pd

from tools import read_CSL_file
from tools import save_CRTS_output
from tools import clean_up_df_symbol
from scrap_yahoo_api import get_yahoo_recommendation
from scrap_investing import get_investing_recommendation
from tools import split_list_into_list
from set_category import set_df_category
from scrap_tradingview_api import get_tradingview_recommendation

import config

def get_df(input_file):
    output_file = input_file.replace("CSL","CRTS")
    config.OUTPUT_FILENAME = config.OUTPUT_DIR + "/recom_df_" + output_file + ".csv"

    if (config.COLAB == True):
        config.COLAB_OUTPUT_FILENAME = config.COLAB_OUTPUT_DIR + "/recom_df_" + output_file + ".csv"

    df = read_CSL_file(input_file)
    return df

def save_df(df):
    df = clean_up_df_symbol(df)
    save_CRTS_output(df, config.OUTPUT_FILENAME)
    if (config.COLAB == True):
        save_CRTS_output(df, config.COLAB_OUTPUT_FILENAME)

def add_market_recom(df_entry):
    # DEBUG
    # df_entry = df_entry[:config.DEBUG_REDUCE_DF_SIZE]
    START_TIME = datetime.datetime.now().now()

    if (config.COLAB == True):
        list_split_df = split_list_into_list(df_entry, config.PERFO_SPLIT_ENTRY_DATAFRAME_COLAB)
    else:
        list_split_df = split_list_into_list(df_entry, config.PERFO_SPLIT_ENTRY_DATAFRAME)
    list_output_df = []
    for df in list_split_df:
        if(config.YAHOO_RECOM == True):
            df = get_yahoo_recommendation(df)

        if (config.INVESTING_RECOM == True):
            df = get_investing_recommendation(df)

        if (config.TRADINGVIEW_RECOM == True):
            df = get_tradingview_recommendation(df)

        list_output_df.append(df)

    df = pd.concat(list_output_df, axis=0, ignore_index=True)
    df = clean_up_df_symbol(df)

    config.DEBUG_FILENAME = config.OUTPUT_DIR + "/recom_df_CRTS_ALL_colab.csv"
    df = pd.read_csv(config.DEBUG_FILENAME)

    df = set_df_category(df)

    save_df(df)

    print("OVERALL RUNTIME: ", datetime.datetime.now().now() - START_TIME)

    return df