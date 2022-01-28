import numpy as np

def set_df_category(df):
    df["category"] = ""

    df["yahoo"] = ""
    df["investing"] = ""
    df["trading"] = ""

    df['Y_r_Key'] = df['Y_r_Key'].str.upper()
    df['I_r_Key'] = df['I_r_Key'].str.upper()
    df['TV_recom'] = df['TV_recom'].str.upper()

    df['I_r_Key'].replace('STRONG BUY', 'STRONG_BUY', inplace=True)
    df['I_r_Key'].replace('STRONG BUY', 'STRONG_BUY', inplace=True)
    df['TV_recom'].replace('STRONG BUY', 'STRONG_BUY', inplace=True)

    # CATEGORY 3  BUY * 3
    df['yahoo'] = np.where((df['Y_r_Key'] == 'BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_3', df['category'])


    # CATEGORY 2  BUY * 2  STRONG BUY * 1
    df['yahoo'] = np.where((df['Y_r_Key'] == 'STRONG_BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_2', df['category'])

    df['yahoo'] = np.where((df['Y_r_Key'] == 'BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'STRONG_BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_2', df['category'])

    df['yahoo'] = np.where((df['Y_r_Key'] == 'BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'STRONG_BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_2', df['category'])


    # CATEGORY 1  BUY * 1  STRONG BUY * 2
    df['yahoo'] = np.where((df['Y_r_Key'] == 'STRONG_BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'STRONG_BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_1', df['category'])

    df['yahoo'] = np.where((df['Y_r_Key'] == 'BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'STRONG_BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'STRONG_BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_1', df['category'])

    df['yahoo'] = np.where((df['Y_r_Key'] == 'STRONG_BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'STRONG_BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_1', df['category'])



    # CATEGORY 0  BUY * 1  STRONG BUY * 2
    df['yahoo'] = np.where((df['Y_r_Key'] == 'STRONG_BUY'), True, False)
    df['investing'] = np.where((df['I_r_Key'] == 'STRONG_BUY'), True, False)
    df['trading'] = np.where((df['TV_recom'] == 'STRONG_BUY'), True, False)

    df['category'] = np.where( ((df['yahoo']) & (df['investing']) & (df['trading'])), 'CATEGORY_0', df['category'])

    df.drop(['yahoo'], axis=1, inplace=True)
    df.drop(['investing'], axis=1, inplace=True)
    df.drop(['trading'], axis=1, inplace=True)

    return df

