__author__ = 'Christian'

from bs4 import BeautifulSoup
from urllib2 import urlopen,build_opener,Request
import pandas as pd

def getAdvfnFinancials(symbol,headers,startDateNumber=0,output="file",quickTest=False):

  #The starting datenumber
  dateNumber = startDateNumber

  #Set som booleans and checkerssh
  dataExist = False
  _quicktest = False #Only scrape first page if quickTest = True
  lastDate = ""
  breakit = False

  #Define dataframe to store the data
  df_Full = pd.DataFrame()

  #Loop through the pages
  while True:

    #If the length of the symbol is greater or equal to 4, the symbol correspond to NASDAQ. Else NYSE
    if len(symbol)>=4:
      url = "http://uk.advfn.com/p.php?pid=financials&btn=istart_date&mode=quarterly_reports&symbol=NASDAQ%3A" + symbol + "&istart_date=" + str(dateNumber)
    else:
      url = "http://uk.advfn.com/p.php?pid=financials&btn=istart_date&mode=quarterly_reports&symbol=NYSE%3A" + symbol + "&istart_date=" + str(dateNumber)

    # Instantiate soup and urllib2 objects
    req = Request(url, None, headers)
    html_doc = urlopen(req)
    soup = BeautifulSoup(html_doc, 'html.parser')
    rows = soup.findAll('tr')

    #Check if data exist or quicktest
    if "No financial data available from this page" in soup.text or _quicktest:
      print "No data exist for " + symbol + " where dateNumber = " + str(dateNumber)
      print "Terminating scrape for " + symbol
      break
    else:
      dataExist = True
      if quickTest:
        _quicktest = True

    variableName=[]
    q1=[]
    q2=[]
    q3=[]
    q4=[]
    q5=[]

    q1ColumnName = ""
    q2ColumnName = ""
    q3ColumnName = ""
    q4ColumnName = ""
    q5ColumnName = ""

    for i in range(12,len(rows)):
      if len(rows[i]) == 6:

        #Create variables for the column-names which will be the dates
        if rows[i].contents[0].text == "quarter end date":

          # If this if statement is not true, no data exist for the ticker
          if not dataExist:
            print "Scraping possible. Starting..."

          q1ColumnName = rows[i].contents[1].text
          q2ColumnName = rows[i].contents[2].text
          q3ColumnName = rows[i].contents[3].text
          q4ColumnName = rows[i].contents[4].text
          q5ColumnName = rows[i].contents[5].text

          #Sometimes the data does not change on advfn. If this is the case, we need to terminate
          if lastDate == q1ColumnName:
            breakit = True
            break
          else:
            lastDate = q1ColumnName

        #Store the advfn data in lists which will be used in the dataframe
        variableName.append(rows[i].contents[0].text)
        q1.append(rows[i].contents[1].text)
        q2.append(rows[i].contents[2].text)
        q3.append(rows[i].contents[3].text)
        q4.append(rows[i].contents[4].text)
        q5.append(rows[i].contents[5].text)

    if breakit:
      print "Terminating scrape for " + symbol
      break

    df_advfn = pd.DataFrame()
    df_advfn["variableName"] = variableName
    df_advfn[q1ColumnName] = q1
    df_advfn[q2ColumnName] = q2
    df_advfn[q3ColumnName] = q3
    df_advfn[q4ColumnName] = q4
    df_advfn[q5ColumnName] = q5


    df_advfn = df_advfn.set_index("variableName")
    df_advfn = df_advfn.stack()
    df_advfn = df_advfn.reset_index()
    df_advfn.columns = ["VARIABLE_NAME","TODATE","VARIABLE_VALUE"]

    #Replace all "," with "". This is for converting "1,204.0" -> "1204.0"
    #After replacement, convert everything to numeric, and put "nan" at non-numeric rows
    df_advfn["VARIABLE_NUMERIC"] = pd.to_numeric(df_advfn["VARIABLE_VALUE"].replace(regex=True,inplace=False,to_replace=r',',value=r''), errors='coerce')

    #Remove nan (i.e non-numeric data)
    df_advfn = df_advfn.dropna()

    #Append to the full dataframe
    df_Full = df_Full.append(df_advfn)

    #Give a little info...
    print "Scraped %s, URL = %s , Quarters = (%s,%s,%s,%s,%s) " %(symbol,url,q1ColumnName,q2ColumnName,q3ColumnName,q4ColumnName,q5ColumnName)

    #Iterate 5 pages at the time
    dateNumber += 5

  if dataExist:
    #Clean the dataframe, sort, and add the ticker
    df_Full = df_Full.drop_duplicates()
    df_Full["TICKER_SYMBOL"] = symbol
    df_Full = df_Full[["TICKER_SYMBOL","VARIABLE_NAME","TODATE","VARIABLE_VALUE"]]
    df_Full = df_Full.sort_values(by=["VARIABLE_NAME","TODATE"])

    if output == "file":
      output_file = "/home/christian/Dev/Projects/MagicForumula/Data/advfn_financials_%s.csv" %(symbol)
      df_Full.to_csv(output_file, index=False, sep=";", header=1)

  else:
    df_Full = pd.DataFrame(data={"TICKER_SYMBOL": symbol, "VARIABLE_NAME": ["no_data"], "TODATE": ["no_data"], "VARIABLE_VALUE": ["no_data"]})

  return df_Full

def getWikiIndexConstituents(csvFileNameExtention,url,output="file"):

  html_doc = urlopen(url)
  soup = BeautifulSoup(html_doc, "html.parser")

  ticker_table = soup.find('table', {'class': 'wikitable sortable'})

  rows = ticker_table.findAll('tr')

  ticker = []
  name = []
  gics = []
  subGics = []

  for i in range(1,len(rows)):
    cols = rows[i].findAll("td")
    ticker.append(cols[0].text)
    name.append(cols[1].text)
    gics.append(cols[3].text)
    subGics.append(cols[4].text)


  df_IndexConstituents = pd.DataFrame()
  df_IndexConstituents["TICKER"] = ticker
  df_IndexConstituents["NAME"] = name
  df_IndexConstituents["GICS"] = gics
  df_IndexConstituents["SUBGICS"] = subGics

  if output == "file":
    output_file = "/home/christian/Dev/Projects/MagicForumula/Data/wikilist_%s.csv" %(csvFileNameExtention)
    df_IndexConstituents.to_csv(output_file,index=False, sep=";", header=1)

  return df_IndexConstituents







