import pandas as pd
from datetime import date
DATE = str(date.today())

COLAB = False
# COLAB = True

INPUT_DIR = "./DATA/INPUT/"
OUTPUT_DIR = "./DATA/OUTPUT/" + DATE

DRIVER_PATH = "./chromedriver.exe"

OUTPUT_FILENAME = ""

YAHOO_RECOM = True
INVESTING_RECOM = True
TRADINGVIEW_RECOM = True

#YAHOO_RECOM = False
#INVESTING_RECOM = False
#TRADINGVIEW_RECOM = False

MULTITHREADING = True
MULTITHREADING_POOL = OUTPUT_DIR + "/POOL/"
MULTITHREADING_NB_SPLIT_DF = 30
MULTITHREADING_NUM_THREADS = 20
MULTITHREADING_MIXED_COMPUTATION = True

PERFO_SPLIT_ENTRY_DATAFRAME = 20
PERFO_SPLIT_ENTRY_DATAFRAME_COLAB = 50

COLAB = False
COLAB_OUTPUT_CRTS = "../drive/MyDrive/colab_results/CRTS/"
COLAB_OUTPUT_DIR = COLAB_OUTPUT_CRTS + DATE
COLAB_OUTPUT_FILENAME = ""


data = ["Strong Buy", "Buy", "Hold", "Under-perform", "Sell"]
DF_YAHOO_RECOMENDATTION = pd.DataFrame(data, columns=['recom_key'])

DEBUG_REDUCE_DF_SIZE = 1000

INTERVAL_FILTERS = {
    "1min": 60,
    "5mins": 60 * 5,
    "15mins": 60 * 15,
    "30mins": 60 * 30,
    "1hour": 60 * 60,
    "5hours": 60 * 60 * 5,
    "daily": 60 * 60 * 24,
    "weekly": "week",
    "monthly": "month",
}
