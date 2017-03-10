__author__ = 'Christian'

import functions as f
import pandas as pd

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

df_indexConstituents = f.getWikiIndexConstituents(csvFileNameExtention="sp500", url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", output="")

tickerList = df_indexConstituents["TICKER"][400:-1]

df_advfnFinancials_sp500 = pd.DataFrame()
i = 0

for ticker in tickerList:
  i += 1
  print ""
  print "ticker number: " + str(i)
  df_advfnFinancials_sp500 = df_advfnFinancials_sp500.append(f.getAdvfnFinancials(symbol=ticker,headers=hdr,startDateNumber=0,output="",quickTest=False))

#df_advfnFinancials_sp500.to_csv("/home/christian/Dev/PYTHON/Projects/MagicForumula/Data/advfn_financials_sp500_500.csv", index=False, sep=";", header=1)

