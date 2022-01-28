import os, fnmatch
import pandas as pd
import random
import config
import constant

def read_CSL_file(input_file):
    filename = config.INPUT_DIR + 'symbol_list_' + input_file + '.csv'
    if not os.path.exists(filename):
        print("no file: ", filename)
    else:
        df = pd.read_csv(filename)
        return df

def save_CRTS_output(df, filename):
    df.to_csv(filename)

def mk_directories():
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    if (config.MULTITHREADING == True):
        if not os.path.exists(config.MULTITHREADING_POOL):
            os.makedirs(config.MULTITHREADING_POOL)
        else:
            for f in os.listdir(config.MULTITHREADING_POOL):
                os.remove(os.path.join(config.MULTITHREADING_POOL, f))

    if (config.COLAB == True):
        if not os.path.exists(config.COLAB_OUTPUT_CRTS):
            os.makedirs(config.COLAB_OUTPUT_CRTS)
        if not os.path.exists(config.COLAB_OUTPUT_DIR):
            os.makedirs(config.COLAB_OUTPUT_DIR)

def split_df(df, size_split):
    return df[:size_split], df[size_split:]

def split_list_into_list(df, split_size):
    # split a df into a list of breakdown df
    len_df = len(df)
    len_split_df = int(len_df / split_size)

    rest_of_the_df = df.copy()
    global_split_list = []

    for i in range(split_size):
        splited_df, rest_of_the_df = split_df(rest_of_the_df, len_split_df)
        global_split_list.append(splited_df)

    if len(rest_of_the_df) > 1:
        global_split_list.append(rest_of_the_df)

    return global_split_list

def clean_up_df_symbol(df):
    for c in df.columns:
        if c.startswith("Unnamed"):
            df.drop(c, axis=1, inplace=True)

    return df

def my_random_user_agent():
    """
    This function selects a random User-Agent from the User-Agent list, which is a constant
    variable that can be found at `investpy.utils.constant.USER_AGENTS`. User-Agents are used in
    order to avoid the limitations of the requests to Investing.com. The User-Agent is
    specified on the headers of the requests and is different for every request.
    Note that Investing.com, via changing the User-Agent on the headers of every request, allows
    a lot of requests, since it has been tested with over 10k consecutive requests without getting
    any HTTP error code from Investing.com.
    Returns:
        :obj:`str` - user_agent:
            The returned :obj:`str` is the name of a random User-Agent, which will be passed on the
            headers of a request so to avoid restrictions due to the use of multiple requests from the
            same User-Agent.
    """

    return random.choice(constant.USER_AGENTS)






