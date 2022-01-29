import sys

from manage_data import data_manager,tools
from init import config
import pandas as pd

"""
    CRTS module: Compute Recommendation Trend Signals
    python3 main.py --COLAB ./CSL_ALL
"""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if (str(sys.argv[1]) == "--COLAB"):
        config.COLAB = True
    else:
        config.COLAB = False

    tools.mk_directories()

    input_file = str(sys.argv[2])
    input_file = input_file[2:]

    df = data_manager.get_df(input_file)
    if isinstance(df, pd.DataFrame):
        df = data_manager.add_market_recom(df)
