import random

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring
from unidecode import unidecode
from bs4 import BeautifulSoup
import re

from init import config,constant
from manage_data import tools

def investing_moving_averages(name, country, id, product_type, interval="daily"):
    """
    This function retrieves the moving averages values calculated by Investing.com for every financial product
    available (stocks, funds, etfs, indices, currency crosses, bonds, certificates and commodities) for different
    time intervals. So on, the user must provide the product_type name and the name of the product (unless product_type
    is 'stock' which name value will be the stock's symbol) and the country if required (mandatory unless product_type
    is either 'currency_cross' or 'commodity', where it must be None). Additionally, the interval can be specified
    which defines the update frequency of the calculations of the moving averages (both simple and exponential). Note
    that the specified interval is not the moving average's interval, since all the available time frames used on
    the calculation of the moving averages are retrieved.

    Args:
        name (:obj:`str`):
            name of the product to retrieve the moving averages table from (if product_type is `stock`, its value
            must be the stock's symbol not the name).
        country (:obj:`str`):
            country name of the introduced product if applicable (if product_type is either `currency_cross` or `commodity`
            this parameter should be None, unless it can be specified just for `commodity` product_type).
        product_type (:obj:`str`):
            identifier of the introduced product, available ones are: `stock`, `fund`, `etf`, `index`, `currency_cross`,
            `bond`, `certificate` and `commodity`.
        interval (:obj:`str`):
            time interval of the resulting calculations, available values are: `5mins`, `15mins`, `30mins`, `1hour`,
            `5hours`, `daily`, `weekly` and `monthly`.

    Returns:
        :obj:`pandas.DataFrame` - moving_averages:
            The resulting :obj:`pandas.DataFrame` contains the table with the results of the calculation of the moving averages
            made by Investing.com for the introduced financial product. So on, if the retrieval process succeed
            its result will look like::

                 period | sma_value | sma_signal | ema_value | ema_signal
                --------|-----------|------------|-----------|------------
                 xxxxxx | xxxxxxxxx | xxxxxxxxxx | xxxxxxxxx | xxxxxxxxxx

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        ConnectionError: raised if the connection to Investing.com errored or could not be established.

    Examples:
        # >>> data = investpy.moving_averages(name='bbva', country='spain', product_type='stock', interval='daily')
        # >>> data.head()
          period  sma_value sma_signal  ema_value ema_signal
        0      5      4.615        buy      4.650        buy
        1     10      4.675       sell      4.693       sell
        2     20      4.817       sell      4.763       sell
        3     50      4.859       sell      4.825       sell
        4    100      4.809       sell      4.830       sell
        5    200      4.822       sell      4.867       sell

    """

    product_type = unidecode(product_type.lower().strip())

    if product_type == "stock":
        check = "symbol"
    else:
        check = "name"

    name = unidecode(name.lower().strip())


    product_id = id

    data_values = {
        "pairID": product_id,
        "period": constant.INTERVAL_FILTERS[interval],
        "viewType": "normal",
    }


    headers = {
        "User-Agent": tools.my_random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)
    # req = requests.post(url, headers={'User-Agent': 'Mozilla/5.0'} ,data=data_values)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'movingAvgsTbl')]/tbody/tr")

    moving_avgs = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get("class") is not None:
                if value.get("class").__contains__("symbol"):
                    ma_period = value.text_content().strip().replace("MA", "")
                    sma_signal = (
                        value.getnext().xpath("span")[0].text_content().strip().lower()
                    )
                    sma_value = float(
                        value.getnext()
                        .text_content()
                        .lower()
                        .replace(sma_signal, "")
                        .strip()
                    )
                    value = value.getnext()
                    ema_signal = (
                        value.getnext()
                        .xpath(".//span")[0]
                        .text_content()
                        .strip()
                        .lower()
                    )
                    ema_value = float(
                        value.getnext()
                        .text_content()
                        .lower()
                        .replace(ema_signal, "")
                        .strip()
                    )

                    moving_avgs.append(
                        {
                            "period": ma_period,
                            "sma_value": sma_value,
                            "sma_signal": sma_signal,
                            "ema_value": ema_value,
                            "ema_signal": ema_signal,
                        }
                    )

    return pd.DataFrame(moving_avgs)

# def investing_data_from_tag(tag, name, country, id, product_type, interval="daily"):
def investing_data_from_tag(tag, interval="daily"):
    """
    product_type = unidecode(product_type.lower().strip())

    name = unidecode(name.lower().strip())
    product_id = id
    data_values = {
        "pairID": product_id,
        "period": config.INTERVAL_FILTERS[interval],
        "viewType": "normal",
    }
    """
    data_values = {
        "period": config.INTERVAL_FILTERS[interval],
    }

    headers = {
        "User-Agent": tools.my_random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


    url = 'https://www.investing.com/equities/' + tag + '-technical'
    # req = requests.post(url, headers={'User-Agent': 'Mozilla/5.0'}, data=data_values)
    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        return "-", "-", "-"

    soup = BeautifulSoup(req.text, 'lxml')
    # title = soup.title.text
    recom_summary = soup.find(class_='newTechStudiesRight instrumentTechTab').find(class_="summary").text[8:]
    table_line = soup.find(class_='newTechStudiesRight instrumentTechTab').find_all(class_="summaryTableLine")

    recom_moving_avg = table_line[0].text
    result = re.search('Moving Averages:(.*)Buy ', recom_moving_avg)
    recom_moving_avg = result.group(1)

    recom_technical_ind = table_line[1].text
    result = re.search('Technical Indicators:(.*)Buy ', recom_technical_ind)
    recom_technical_ind = result.group(1)

    return recom_summary, recom_technical_ind, recom_moving_avg


def investing_validate_tag(tag):
    if (tag.find('?cid=') != -1):
        pos = tag.index("?")
        tag = tag[:pos]
    return tag
