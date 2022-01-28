import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import config

from bs4 import BeautifulSoup


def get_chrome_driver():
    if (config.COLAB == True):
        options = webdriver.ChromeOptions()
        options.add_argument('-headless')
        options.add_argument('-no-sandbox')
        options.add_argument('-disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver', options=options)
    else:
        #DRIVER_PATH = "C:/Users/despo/chromedriver_win32/chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('-headless')
        options.headless = True
        options.add_argument('-no-sandbox')
        # options.add_argument('-window-size=1920,1200')
        # options.add_argument('-disable-gpu')
        options.add_argument('-ignore-certificate-errors')
        options.add_argument('-disable-extensions')
        options.add_argument('-disable-dev-shm-usage')
        #driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        driver = webdriver.Chrome(executable_path=config.DRIVER_PATH, options=options)

    # driver.get('https://finance.yahoo.com/gainers')
    # if (config.COLAB == False):
    #     driver.find_element_by_name("agree").click()

    return driver



def use_yfinance_scraping(df):
    list_stocks = df.symbol.tolist()
    df = df.set_index('symbol')

    driver = get_chrome_driver()

    toto = True

    for stock in list_stocks:
        stock = "AAPL"
 #       try:
        if toto == True:
            url = 'https://finance.yahoo.com/quote/' + stock + '?p=' + stock + '&.tsrc=fin-srch'
            print(url)

            """
            headers = {
                "User-Agent": my_random_user_agent(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }

            page = requests.get(url, headers=headers)
            """

            driver.get(url)

            # element = driver.find_element(By.XPATH, "//*[text()'Recommendation Rating']")
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div/div/div/div[10]/div/div/div/section/div/div/div[1]")


            element = driver.find_element(By.ID, 'mrt-node-Col2-9-QuoteModule')
            print(element.text)

            element = driver.find_element(By.XPATH, "//*[@id='Aside']")
            print(element.text)


            print(element.text)

            element = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div/div/div/div[10]/div/div/div/section/div/div/div[1]")

            print(element.text)

            element = driver.find_element(By.XPATH, "//*[@id='Aside']/div[10]")

            print(element.text)

            element = driver.find_elements_by_xpath("//*[@id='Col2-9-QuoteModule-Proxy']/div/section/div/div/div[1]")

            print(element.text)

            html_text = driver.page_source

            # if(page.status_code == 404):
            #     raise Exception('err. 404')

            #soup = BeautifulSoup(page.text, 'html.parser')
            # soup = BeautifulSoup(page.text, 'lxml')
            soup = BeautifulSoup(html_text, 'lxml')

            # recom = soup.find('data-test', 'html.parser')

            toto = soup.find_all('div')
            # toto = soup.find_all('class')
            print(toto)

            # yf_rec refers to yahoo finance recommendation

            content = soup.find('div', attrs={'class': 'B(8px) Pos(a) C(white) Py(2px) Px(0) Ta(c) Bdrs(3px) Trstf(eio) Trsde(0.5) Arrow South Bdtc(i)::a Fw(b) Bgc($buy) Bdtc($buy)'}).text.strip()


            content = soup.find('div',       {"class": "B(8px) Pos(a) C(white) Py(2px) Px(0) Ta(c) Bdrs(3px) Trstf(eio) Trsde(0.5) Arrow South Bdtc(i)::a Fw(b) Bgc($buy) Bdtc($buy)"})

            content = soup.find('div', {"class": "B"})


            tags = {tag.name for tag in soup.find_all()}
            class_list = set()
            for tag in tags:
                # find all element of tag
                for i in soup.find_all(tag):
                    # if tag has attribute of class
                    if i.has_attr("class"):
                        if len(i['class']) != 0:
                            class_list.add(" ".join(i['class']))
            class_list = []
            tag = "div"
            for i in soup.find_all(tag):
                # if tag has attribute of class
                if i.has_attr("class"):
                    if len(i['class']) != 0:
                        class_list.add(" ".join(i['class']))
            print(class_list)

            recom = soup.find(class_='quote-mdl')
            print(recom)


            soup = BeautifulSoup(page.text, 'lxml')
            html_text = soup.text

            match = re.findall(r'Rating...1StrongBuy', html_text)
            if (len(match) == 19):
                string = match[0]
                string = string[6:10]

                Y_recom = float(string)
                df["Y_r_Mean"][stock] = Y_recom
                df["Y_r_Key"][stock] = config.DF_YAHOO_RECOMENDATTION['recom_key'][int(Y_recom)-1]

                print("symbol requests: ", stock)
            else:
                raise Exception('This is the exception')
#        except:
        else:
            print('exception')
            print("no requests data symbol: ", stock)

    df.reset_index(inplace=True)
    return df
