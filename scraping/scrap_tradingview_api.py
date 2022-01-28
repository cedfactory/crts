# Imports
import time
import pandas as pd
import numpy as np
import datetime
import uuid

import config
import concurrent.futures

from tools import split_list_into_list
from merge import merge_csv_to_df

from tradingview_ta import TA_Handler, Interval, Exchange

def insert_tradingview_df_column(df):
    columns = ["TV_symbol", "TV_country", "TV_exchange",
               "TV_recom", "TV_buy", "TV_sell", "TV_neutral"]
    for column in columns:
        df.insert(len(df.columns), column, "")
    return df

def set_tradingview_data(df, symbol, data_handler, summary):
    #df['TV_exchange'] = np.where(df['TV_symbol'] == symbol, exchange, df['TV_exchange'])

    df.loc[symbol, 'TV_exchange'] = data_handler.exchange
    df.loc[symbol, 'TV_recom'] = summary['RECOMMENDATION']
    sum = summary['BUY'] + summary['SELL'] + summary['NEUTRAL']
    df.loc[symbol, 'TV_buy'] = int(summary['BUY'] / sum * 100)
    df.loc[symbol, 'TV_sell'] = int(summary['SELL'] / sum * 100)
    df.loc[symbol, 'TV_neutral'] = int(summary['NEUTRAL'] / sum * 100)

    return df


def set_tradingview_columns(df):

    # for idx_yahoo in config.INDEX:
    #    index_match = config.DF_MATCH_INDEX_FULLNAME.loc[idx_yahoo, 'index_tradingview']
    #    df['TV_exchange'] = np.where(df['idx'] == idx_yahoo, index_match, df['TV_exchange'])

    df['TV_exchange'] = df['exchange'].copy()
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'GER', 'XETR', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NCM', 'NASDAQ', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NGM', 'NASDAQ', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NMS', 'NASDAQ', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NYQ', 'NYSE', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'PAR', 'EURONEXT', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'PNK', 'OTC', df['TV_exchange'])


    """
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'XETRA', 'XETR', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NasdaqGS', 'NASDQ', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'NasdaqCM', 'NASDQ', df['TV_exchange'])
    df['TV_exchange'] = np.where(df['TV_exchange'] == 'Paris', 'EURONEXT', df['TV_exchange'])
    """

    df['TV_symbol'] = df['symbol'].copy()

    list_split_symbol = df['TV_symbol'].str.split("\\.", n=1, expand=True)
    df['TV_symbol'] = list_split_symbol[0]

    df['TV_country'] = df['country'].copy()
    df['TV_country'] = df['TV_country'].str.lower()


    df['TV_country'] = np.where(df['TV_country'] == 'united states', 'america', df['TV_country'])
    df['TV_country'] = np.where(df['TV_exchange'] == 'NYSE', 'america', df['TV_country'])
    df['TV_country'] = np.where(df['TV_exchange'] == 'NASDAQ', 'america', df['TV_country'])
    df['TV_country'] = np.where(df['TV_symbol'] == 'AIR', 'france', df['TV_country'])

    # df['TV_country'] = np.where(df['TV_exchange'] == 'NASDAQ', 'america', df['TV_country'])

    return df

def use_tradingview_api(df):
    df = insert_tradingview_df_column(df)
    df = set_tradingview_columns(df)

    # list_symbol = df['TV_symbol'].tolist()
    # df = df.set_index('TV_symbol')
    list_symbol = df['symbol'].tolist()
    df = df.set_index('symbol', drop=False)

    for symbol in list_symbol:

        # symbol = 'ACAN'

        ticker = symbol
        country = df.loc[symbol, 'TV_country']
        exchange = df.loc[symbol, 'TV_exchange']
        symbol = df.loc[symbol, 'TV_symbol']
        data_handler_found = True
        try:
            symbol_test = exchange + "-" + symbol
            data_handler = TA_Handler(
                symbol=symbol_test,
                interval=Interval.INTERVAL_1_DAY,
            )
            tradingview_summary = data_handler.get_analysis().summary
            print(symbol_test)
        except:
            if (country == 'america'):
                try:
                    exchange = 'NYSE'
                    data_handler = TA_Handler(
                        symbol=symbol,
                        screener=country,
                        exchange=exchange,
                        interval=Interval.INTERVAL_1_DAY,
                    )
                    tradingview_summary = data_handler.get_analysis().summary
                except:
                    try:
                        exchange = 'NASDAQ'
                        data_handler = TA_Handler(
                            symbol=symbol,
                            screener=country,
                            exchange=exchange,
                            interval=Interval.INTERVAL_1_DAY,
                        )
                        # print("ticker: ", symbol, " exchange: ", exchange, " ",data_handler.get_analysis().summary)
                        tradingview_summary = data_handler.get_analysis().summary
                    except:
                        try:
                            exchange = 'AMEX'
                            data_handler = TA_Handler(
                                symbol=symbol,
                                screener=country,
                                exchange=exchange,
                                interval=Interval.INTERVAL_1_DAY,
                            )
                            # print("ticker: ", symbol, " exchange: ", exchange, " ",data_handler.get_analysis().summary)
                            tradingview_summary = data_handler.get_analysis().summary
                        except:
                            try:
                                exchange = 'SPX'
                                data_handler = TA_Handler(
                                    symbol=symbol,
                                    screener=country,
                                    exchange=exchange,
                                    interval=Interval.INTERVAL_1_DAY,
                                )
                                #print("ticker: ", symbol, " exchange: ", exchange, " ", data_handler.get_analysis().summary)
                                tradingview_summary = data_handler.get_analysis().summary
                            except:
                                data_handler_found = False
                                print("tradingview error ticker: ", symbol," country: ", country)
            else:
                try:
                    data_handler = TA_Handler(
                        symbol=symbol,
                        screener=country,
                        exchange=exchange,
                        interval=Interval.INTERVAL_1_DAY,
                    )
                    # print("ticker: ", symbol, " exchange: ", exchange, " ",data_handler.get_analysis().summary)
                    tradingview_summary = data_handler.get_analysis().summary
                except:
                    try:
                        exchange = 'EURONEXT'
                        data_handler = TA_Handler(
                            symbol=symbol,
                            screener=country,
                            exchange=exchange,
                            interval=Interval.INTERVAL_1_DAY,
                        )
                        # print("ticker: ", symbol, " exchange: ", exchange, " ",data_handler.get_analysis().summary)
                        tradingview_summary = data_handler.get_analysis().summary
                    except:
                        data_handler_found = False
                        print("tradingview error ticker: ", symbol," country: ", country)

        if data_handler_found == True:
            set_tradingview_data(df, ticker, data_handler, tradingview_summary)

    df.reset_index(inplace=True, drop=True)
    return df

def use_tradingview_multi_api(df):
    df = use_tradingview_api(df)
    filename = config.MULTITHREADING_POOL + str(uuid.uuid4()) + '_result.csv'
    df.to_csv(filename)

def get_tradingview_recommendation(df):
    print("GET TRADINGVIEW RECOM")

    START_TIME = datetime.datetime.now().now()
    if config.MULTITHREADING == True:
        global_split_list = split_list_into_list(df, config.MULTITHREADING_NB_SPLIT_DF)

        with concurrent.futures.ThreadPoolExecutor(max_workers=config.MULTITHREADING_NUM_THREADS) as executor:
            executor.map(use_tradingview_multi_api, global_split_list)

        df = merge_csv_to_df(config.MULTITHREADING_POOL, "*_result.csv")
    else:
        df = use_tradingview_api(df)

    print("TRADINGVIEW RUNTIME: ", datetime.datetime.now().now() - START_TIME)

    return df