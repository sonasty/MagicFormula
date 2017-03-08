__author__ = 'Christian'

import functions as f
import pandas as pd

#No data at all: AARN
#Even number of quarters:

df_indexConstituents = f.getWikiIndexConstituents(csvFileNameExtention="sp500", url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", output="")

tickerList = df_indexConstituents["TICKER"][0:2]

df_advfnFinancials_sp500 = pd.DataFrame()
i = 0

# Some new comments

# Even more comments

#df_advfnFinancials_sp500 = f.getAdvfnFinancials(symbol="ARNC",startDateNumber=0,output="",quickTest=True)


for ticker in tickerList:
  i += 1
  print ""
  print "ticker number: " + str(i)
  df_advfnFinancials_sp500 = df_advfnFinancials_sp500.append(f.getAdvfnFinancials(symbol=ticker,startDateNumber=0,output="",quickTest=False))

#df_advfnFinancials_sp500.to_csv("/home/christian/Dev/Projects/MagicForumula/Data/advfn_financials_sp500_400_X.csv", index=False, sep=";", header=1)
