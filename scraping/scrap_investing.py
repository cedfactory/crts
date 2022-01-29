import investpy

# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time

import sys
import os, fnmatch
import shutil

# imports
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import uuid

from manage_data import tools,merge
from init import config

import datetime
import concurrent.futures
from datetime import date, timedelta
from .load_investing_data import investing_moving_averages,investing_data_from_tag,investing_validate_tag

def insert_df_column(df):
    columns = ["investing_symbol", "investing_country", "investing_company_name",
               "RSI(14)", "STOCH(9,6)", "STOCHRSI(14)", "MACD(12,26)", "ADX(14)",
               "W%R", "CCI(14)", "ATR(14)", "Highs/Lows(14)", "UltimateOscillator",
               "ROC", "Bull/BearPower(13)", "SMA_5", "SMA_10", "EMA_5", "EMA_10"]
    for column in columns:
        df.insert(len(df.columns), column, "-")
    return df

def get_investpy_data(ticker):
    country = ['united states']
    try:
        country = [config.DF_MATCH_YAHOO_INVESTING.loc[ticker, 'country']]
        ticker = config.DF_MATCH_YAHOO_INVESTING.loc[ticker, 'investing']
    except:
        if ticker.endswith('.DE'):
            country = ['germany']
            ticker = ticker[0:(len(ticker) - 3)]
        else:
            if ticker.endswith('.PA'):
                country = ['france']
                ticker = ticker[0:(len(ticker) - 3)]
            else:
                if ticker.endswith('.AS'):
                    country = ['netherlands']
                    ticker = ticker[0:(len(ticker) - 3)]

    return ticker, country

def get_investpy_symbol(ticker, df):
    if ticker == 'AACG':
        country = "united states"
    else:
        country = [df['country'][ticker]]


    if ticker.endswith('.DE'):
        country = ['germany']
        ticker = ticker[0:(len(ticker) - 3)]
    else:
        if ticker.endswith('.PA'):
            country = ['france']
            ticker = ticker[0:(len(ticker) - 3)]
        else:
            if ticker.endswith('.AS'):
                country = ['netherlands']
                ticker = ticker[0:(len(ticker) - 3)]
    return ticker, country

def use_investpy_api(df):
    # len_df = len(df)
    # df_screener = df_screener.drop(df_screener[(df_screener.idx == '-')].index)
    # df_screener.drop(df_screener[df_screener.symbol == 'CON.DE'].index, inplace=True)
    # print("remove tickers with no index: ", len_df - len(df_screener))

    tickers = df['symbol'].tolist()

    # insert_df_column(df)

    df = df.set_index('symbol')

    for ticker in tickers:
        # ticker = 'ADOCR'
        #print(ticker)
        symbol = ticker
        #ticker, country = get_investpy_data(ticker)
        ticker, country = get_investpy_symbol(ticker, df)
        df['I_symbol'][symbol] = ticker

        # search_result = investpy.search_quotes(text=ticker, countries=country, products=['stocks'], n_results=1)
        # search_result = investpy.search_quotes(text=ticker, products=['stocks'], n_results=1)

        try:
            if (symbol == 'AAP') or (symbol == 'AME') or (symbol == 'BA') or (symbol == 'CI') or (symbol == 'MA'):
                search_result_list = investpy.search_quotes(text=ticker, countries=country, products=['stocks'], n_results=3)
                search_result = search_result_list[1]
            else:
                try:
                    search_result = investpy.search_quotes(text=ticker, countries=country, products=['stocks'], n_results=1)
                except:
                    search_result = investpy.search_quotes(text=ticker, products=['stocks'], n_results=1)

            # information = search_result.retrieve_information()
            # technical_indicators = search_result.retrieve_technical_indicators(interval='daily')

            tag = investing_validate_tag(search_result.tag[10:])
            df['I_tag'][symbol] = tag
            try:
                recom_summary, recom_technical_ind, recom_moving_avg = investing_data_from_tag(df['I_tag'][symbol],
                                                                                               interval='daily')
                df['I_r_Key'][symbol] = recom_summary
                df['I_r_tch_ind'][symbol] = recom_technical_ind
                df['I_r_ema_sma'][symbol] = recom_moving_avg

                df['I_symbol'][symbol] = search_result.symbol
                df['I_country'][symbol] = search_result.country
                df['I_company_name'][symbol] = search_result.name

                # print("Investing.com symbol: ", symbol)
            except:
                print("No Investing.com data for ", symbol)
        except:
            print("No Investing.com data for ",symbol)

    #df_screener.to_csv(config.OUTPUT_DIR+'tmp.csv')
    df['symbol'] = df.index
    df.reset_index(drop=True, inplace=True)

    first_column = df.pop('symbol')
    df.insert(0, 'symbol', first_column)

    return df

def use_investpy_multi_api(df):
    df = use_investpy_api(df)
    filename = config.MULTITHREADING_POOL + str(uuid.uuid4()) + '_result.csv'
    df.to_csv(filename)


def get_investing_recommendation(df):
    df["I_symbol"] = ""
    df["I_r_Key"] = ""
    df["I_r_tch_ind"] = ""
    df["I_r_ema_sma"] = ""
    df["I_tag"] = ""
    df['I_country'] = ""
    df['I_company_name'] = ""

    df['country'] = df['country'].str.lower()

    START_TIME = datetime.datetime.now().now()

    print("GET INVESTING.COM RECOM:")
    if config.MULTITHREADING == True:
        global_split_list = tools.split_list_into_list(df, config.MULTITHREADING_NB_SPLIT_DF)

        with concurrent.futures.ThreadPoolExecutor(max_workers=config.MULTITHREADING_NUM_THREADS) as executor:
            executor.map(use_investpy_multi_api, global_split_list)

        df = merge.merge_csv_to_df(config.MULTITHREADING_POOL, "*_result.csv")

    else:
        df = use_investpy_api(df)

    print("INVESTING.COM RUNTIME: ", datetime.datetime.now().now() - START_TIME)

    return df