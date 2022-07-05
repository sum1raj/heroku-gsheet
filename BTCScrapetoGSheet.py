#############
#
#  To launch the script on Pyzo, press Ctrl + E
#
#  The last data is available on the Excel file Analysis (use the Update button to refresh)
#
#  All the historical data is available on the csv file Exportcsv
#
#  To restart the script, close the window and restart
#
#############
#path=r'C:/Users/arnau/Dropbox/WebScraping Crypto/'
#path=r'C:/Users/Arnaud Lorioz/Dropbox/WebScraping Crypto/'
path=r'C:\Users\moham\PycharmProjects\HerokuScriptToGSheet'
# import b
## Import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
import pandas as pd
import gspread
from datetime import datetime, timedelta
from gspread_formatting import *
import gspread_dataframe as gd
i=0
t = ""
PATH = 'C:\\bin\\chromedriver.exe'

gc = gspread.service_account(filename="C:\\bin\\bil.json")
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/12c5L6ArSNBJgMAalhtxdvKfz1mZ5cBUzSqUzADqj1F0/edit#gid=818333264")
worksheet = sh.worksheet("Sheet1")
while True :    # création d'une boucle while qui s'executera tant que True == True
        ## Step 1 : Extract the HTML page
    try:
        # s=Service(path+'chromedriver')
        #s=Service(path+'chromedrivermac')
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('--headless')
        # driver = webdriver.Chrome(service=s,chrome_options=options)
        try:
            driver = webdriver.Chrome(PATH,options=options)
        except Exception as e:
            print(e)
        print("driver", driver)
        driver.get('https://www.coinglass.com/FundingRate')
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")
        t=str(datetime.now())[:-7]
        print(t,"Here T is")
        driver.quit()
 # print "This report has no legal value"
        #Bitcoin Price extract
        req = urllib.request.Request('https://fr.investing.com/crypto/bitcoin/btc-usd',headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        soupBTC = BeautifulSoup(webpage,'html.parser')
        price_BTC=float(soupBTC.find('span',attrs={"data-test":"instrument-price-last"}).get_text().replace('.','').replace(',','.'))
        print(price_BTC,"Here I am now")
        ## Step 2 : Extract requested data
        #import of the list of requested currencies
        list_cc=['BTC','ETH','SOL','DOT','BNB','LUNA','XRP','ADA','DOGE','LTC','AVAX','MATIC','AXS','LINK','BCH','SAND','EOS','FIL','ATOM','GALA','FTT','MANA','USDT','XTZ','ETC','FTM','NEAR','CRV','ALGO','SUSHI','BIT','UNI','EGLD','TRX','XLM','1INCH','LRC','DYDX','1000SHIB','ZEC','BTT','ICP','AAVE','CRO','OMG','BSV','SHIB','VET','THETA','ALICE','SRM','YFI','MKR','COMP','SLP','ENJ','RUNE','BAT','GRT','RAY','AR','CHZ','SNX','ONE','SXP','TLM','SPELL','KSM','ENS','XMR','SHIB1000','IOTA','DASH','CHR','STORJ','TRU','NEO','ALT','QTUM','SHIT','HNT','ATLAS','RSR','YGG','FLOW','HBAR','ZRX','GTC','SFP','IOST','BOBA','ANKR','ALPHA','IOTX','C98','CELR','DEFI','KSHIB','LINA','REN','REEF','WAVES','KAVA','AUDIO','BADGER','ZEN','BZRX','KEEP','XEM','KNC','HT','MASK','EXCH','CAKE','ICX','SKL','OKB','BAL','CTK','ZIL','POLIS','YFII','DODO','SC','HOT','ONT','BAND','STX','COTI','BLZ','LIT','BAKE','CVC','DENT','KIN','CTSI','PEOPLE','MID','AGLD','TONCOIN']
        BTC = [t,price_BTC]
        Pred = [t,price_BTC]
        row1=True
        for p in soup.find_all('a',attrs={"href":"/funding/BTC"}):
            if p.get_text()!='BTC' and p.get_text()!='-':
                if row1 :
                    BTC.append(float(p.get_text()[:-1]))  # % removed + conversion into float
                    row1=False
                else :
                    Pred.append(float(p.get_text()[:-1]))
                    row1=True
            elif p.get_text()=='-':
                if row1 :
                    BTC.append(p.get_text())
                    row1=False
                else :
                    Pred.append(p.get_text())
                    row1=True
        simple_list=[BTC]
        for cc in list_cc[1:]:
            Crypto = [t,price_BTC]
            for p in soup.find_all('a',attrs={"href":"/funding/"+cc}):
                if p.get_text()!=cc and p.get_text()!='-':
                    Crypto.append(float(p.get_text()[:-1]))
                elif p.get_text()=='-':
                    Crypto.append(p.get_text())
            simple_list.append(Crypto)
        ## Step 3 : Updating of GoogleSheet files
        df=pd.DataFrame(simple_list,columns=['Time','Price BTC','Binance','Okex','Bybit','FTX','Huobi','Gate','Bitget','CoinEx','Binance Token','Okex Token','Bybit Token','Bitmex Token','Huobi Token','Deribit Token'])
        df.insert(0,'Crypto',list_cc)
        print(len(df),"Length of DF")
        try:
            gd.set_with_dataframe(worksheet, df)
        except Exception as e:
            print(e)
    except Exception:
        print("Sorry network issue on",t)
    i+=1
    time.sleep(300)