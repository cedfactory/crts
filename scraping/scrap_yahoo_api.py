from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import concurrent.futures
import uuid
import pandas as pd

from bs4 import BeautifulSoup
import requests
import re

import config

from tools import my_random_user_agent
from tools import split_list_into_list
from merge import merge_csv_to_df

from yahooquery import Ticker

from scrap_yahoo_selenium import use_yfinance_scraping


def use_yfinance_mixed(df):
    list_stocks = df.symbol.tolist()
    df = df.set_index('symbol')

    for stock in list_stocks:
        try:
            yf_stock = yf.Ticker(stock)
            df["Y_r_Key"][stock] = yf_stock.info['recommendationKey']
            df["Y_r_Mean"][stock] = yf_stock.info['recommendationMean']

            # print("symbol Yfinance: ", stock)
        except:
            try:
                quote_data = si.get_quote_data(stock)
                yahoo_recommendation = quote_data['averageAnalystRating']
                yahoo_recommendation_split = yahoo_recommendation.split(" - ")
                df["Y_r_Mean"][stock] = yahoo_recommendation_split[0]
                df["Y_r_Key"][stock] = yahoo_recommendation_split[1]

                print("symbol Y_fin: ", stock)
            except:
                try:
                    yahoo_recommendation = Ticker(stock).quotes[stock]['averageAnalystRating']
                    yahoo_recommendation_split = yahoo_recommendation.split(" - ")
                    df["Y_r_Mean"][stock] = yahoo_recommendation_split[0]
                    df["Y_r_Key"][stock] = yahoo_recommendation_split[1]

                    print("symbol Y_querry: ", stock)
                except:
                    print("symbol failure: ", stock)

    df.reset_index(inplace=True)

    return df

def use_yfinance_api(df):
    list_stocks = df.symbol.tolist()
    df = df.set_index('symbol')

    for stock in list_stocks:
        try:
            yf_stock = yf.Ticker(stock)
            df["Y_r_Key"][stock] = yf_stock.info['recommendationKey']
            df["Y_r_Mean"][stock] = yf_stock.info['recommendationMean']

            if df['Y_r_Key'][stock] == 'none':
                df["Y_r_Key"][stock] = ''
                df["Y_r_Mean"][stock] = ''

            print("symbol: ", stock)
        except:
            print("no YahooF data symbol: ", stock)

    df.reset_index(inplace=True)

    return df

def use_yahoo_fin_api(df):
    list_stocks = df.symbol.tolist()
    df = df.set_index('symbol')

    for stock in list_stocks:
        try:
            quote_data = si.get_quote_data(stock)
            yahoo_recommendation = quote_data['averageAnalystRating']
            yahoo_recommendation_split = yahoo_recommendation.split(" - ")
            df["Y_r_Mean"][stock] = yahoo_recommendation_split[0]
            df["Y_r_Key"][stock] = yahoo_recommendation_split[1]

            print("symbol Y_fin: ", stock)
        except:
            print("no Y_finF data symbol: ", stock)

    df.reset_index(inplace=True)
    return df

def use_yahooquery_api(df):
    # use Yahooquery lib
    list_stocks = df.symbol.tolist()
    df = df.set_index('symbol')

    for stock in list_stocks:
        try:
            yahoo_recommendation = Ticker(stock).quotes[stock]['averageAnalystRating']
            yahoo_recommendation_split = yahoo_recommendation.split(" - ")
            df["Y_r_Mean"][stock] = yahoo_recommendation_split[0]
            df["Y_r_Key"][stock] = yahoo_recommendation_split[1]

            print("symbol Y_querry: ", stock)
        except:
            print("no Y_querry data symbol: ", stock)

    df.reset_index(inplace=True)
    return df

def use_yfinance_multi_api(df):
    if (config.MULTITHREADING_MIXED_COMPUTATION == True):
        df = use_yfinance_mixed(df)
    else:
        df = use_yahooquery_api(df)
        df_yfinance = df.loc[df['Y_r_Key'] != '', df.columns].copy()

        df = df.loc[df['Y_r_Key'] == '', df.columns].copy()
        # df = use_yfinance_scraping(df)
        df = use_yahoo_fin_api(df)
        df_yahoo_fin = df.loc[df['Y_r_Mean'] != '', df.columns].copy()

        df = df.loc[df['Y_r_Mean'] == '', df.columns].copy()
        df = use_yfinance_api(df)

        frame = [df_yfinance, df_yahoo_fin, df]
        df = pd.concat(frame)

    filename = config.MULTITHREADING_POOL + str(uuid.uuid4()) + '_result.csv'
    df.to_csv(filename)


def get_yahoo_recommendation(df):
    df["Y_r_Key"] = ""
    df["Y_r_Mean"] = ""
    START_TIME = datetime.datetime.now().now()
    print("GET YAHOO FINANCE RECOM:")
    if config.MULTITHREADING == True:
        global_split_list = split_list_into_list(df, config.MULTITHREADING_NB_SPLIT_DF)

        with concurrent.futures.ThreadPoolExecutor(max_workers=config.MULTITHREADING_NUM_THREADS) as executor:
            executor.map(use_yfinance_multi_api, global_split_list)

        df = merge_csv_to_df(config.MULTITHREADING_POOL, "*_result.csv")

    else:
        # df = use_yfinance_scraping(df)

        df = use_yahooquery_api(df)
        df_yfinance = df.loc[df['Y_r_Key'] != '', df.columns].copy()

        df = df.loc[df['Y_r_Key'] == '', df.columns].copy()
        # df = use_yfinance_scraping(df)
        df = use_yahoo_fin_api(df)
        df_yahoo_fin = df.loc[df['Y_r_Mean'] != '', df.columns].copy()

        df = df.loc[df['Y_r_Mean'] == '', df.columns].copy()
        df = use_yfinance_api(df)

        frame = [df_yfinance, df_yahoo_fin, df]
        df = pd.concat(frame)

    print("YAHOO FINANCE RUNTIME: ", datetime.datetime.now().now() - START_TIME)

    # df = use_yahoo_fin_api(df)

    return df




