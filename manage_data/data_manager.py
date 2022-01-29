import datetime
import os
import pandas as pd
from scraping import scrap_yahoo_api,scrap_investing,scrap_tradingview_api
from init import config
from manage_data import tools,set_category


def read_csl_file(input_file):
    output_file = input_file.replace("CSL","CRTS")
    config.OUTPUT_FILENAME = config.OUTPUT_DIR + "/recom_df_" + output_file + ".csv"

    if (config.COLAB == True):
        config.COLAB_OUTPUT_FILENAME = config.COLAB_OUTPUT_DIR + "/recom_df_" + output_file + ".csv"

    filename = input_file
    if not os.path.exists(filename):
        filename = config.INPUT_DIR + 'symbol_list_' + input_file + '.csv'
    if not os.path.exists(filename):
        print("no file: ", filename)
        return None

    df = pd.read_csv(filename)
    return df


def save_df(df):
    df = tools.clean_up_df_symbol(df)
    tools.save_CRTS_output(df, config.OUTPUT_FILENAME)
    if (config.COLAB == True):
        tools.save_CRTS_output(df, config.COLAB_OUTPUT_FILENAME)

def add_market_recom(df_entry):
    # DEBUG
    # df_entry = df_entry[:config.DEBUG_REDUCE_DF_SIZE]
    START_TIME = datetime.datetime.now().now()

    if (config.COLAB == True):
        list_split_df = tools.split_list_into_list(df_entry, config.PERFO_SPLIT_ENTRY_DATAFRAME_COLAB)
    else:
        list_split_df = tools.split_list_into_list(df_entry, config.PERFO_SPLIT_ENTRY_DATAFRAME)
    list_output_df = []
    for df in list_split_df:
        if(config.YAHOO_RECOM == True):
            df = scrap_yahoo_api.get_yahoo_recommendation(df)

        if (config.INVESTING_RECOM == True):
            df = scrap_investing.get_investing_recommendation(df)

        if (config.TRADINGVIEW_RECOM == True):
            df = scrap_tradingview_api.get_tradingview_recommendation(df)

        list_output_df.append(df)

    df = pd.concat(list_output_df, axis=0, ignore_index=True)
    df = tools.clean_up_df_symbol(df)

    config.DEBUG_FILENAME = config.OUTPUT_DIR + "/recom_df_CRTS_ALL_colab.csv"
    df = pd.read_csv(config.DEBUG_FILENAME)

    df = set_category.set_df_category(df)

    save_df(df)

    print("OVERALL RUNTIME: ", datetime.datetime.now().now() - START_TIME)

    return df