from tradingview_ta import TA_Handler, Interval
import sys,os, glob
import pandas as pd
from datetime import date, timedelta
import datetime 
import yfinance as yf
from email_utils import sendmail
from measureSQLFunctions import checkRSI, checkRangeWithin,checkCCI, checkADX, checkPolarity,ruleEngine,trendSignal
import numpy as np
from tabulate import tabulate

localRun = "F"
sendEmail = "T"
runType = "portfolio" #portfolio
#runType = "spy" #portfolio

now = datetime.datetime.now()
today12 = now.replace(hour=12, minute=0, second=0, microsecond=0)
today18 = now.replace(hour=18, minute=0, second=0, microsecond=0)

if now < today18:
    screener = "america"
elif  now > today18:
    screener = "india" 

if len(sys.argv) == 2:
    screener =  sys.argv[1]
elif len(sys.argv) == 3:
    screener =  sys.argv[1]
    runType =  sys.argv[2]

#screener = "america" 
#screener = "india" 
#runType = "spy"
#runType = "nse200"
weekly_recom = ''
daily_recom = ''

today = date.today().strftime("%d%m%Y")
todayF = date.today().strftime("%d-%m-%Y")
runTime = date.today().strftime("%p")

filepath= "C:\Report\\final"
fileNameUnsorted = f"C:\Report\\temp\\{screener}_report_unsorted.csv"
fileName = f"C:\Report\\final\\{screener}_report_{today}_{runType}.csv"
rawOutputFile = f"C:\\Report\\raw\\{screener}_raw_{today}.csv"
configFile = f"C:\Report\config\config_{screener}_{runType}_test.csv"
finalMsgFie = f"C:\Report\\final\{screener}_{runType}.txt"

header = ["Category","Symbol", "Reco_4_hrs","RSI","Stoch_K",
          "Stoch_D","CCI20","ADX","AO","Mom","MACD_macd","MACD_signal","UO","P_SAR","TrailingPE",
          "ForwardPE","TrailingEps","ForwardEps","PriceToBook","EarningsQuarterlyGrowth",
          "Sector","Stock","Institutions_pct","Earning_Date","Price","52WeekHigh",
          "52WeekLow", "PreviousClose","ShortInterest","RecommdationMean","RecommadationKey", 
          "pegRatio","totalCashPerShare","earningsGrowth","currentRatio","returnOnAssets","returnOnEquity",
          "debtToEquity","quickRatio","Reco_Weekly","LotSize","Reco_Daily"]

def getLatestFileName(filePath,screener,runType):
    list_of_files = glob.glob(f"{filePath}\\{screener}*{runType}.csv")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
         
                
def getDetailsSlow():
    with open(fileNameUnsorted, "w") as tmpFileHandler:
        tmpFileHandler.write(','.join(header) + '\n' )
        with open(configFile, "r") as fp:
            for i in fp.readlines():
                tmp = i.rstrip().split(",")
                line = getDetailsFromTV(tmp[0], tmp[1], tmp[2],tmp[3],tmp[4])
                tmpFileHandler.write(line)
        fp.close()
    tmpFileHandler.close()

   
def getDetailsFromTV(portfolio,exchange,symbol,ysymbol,lotSize):
    print(f"Tradingview: {symbol}")
    stock = TA_Handler(symbol=symbol,screener=screener,exchange=exchange,interval=Interval.INTERVAL_4_HOURS)
    analysis = stock.get_analysis()
    summary = analysis.summary["RECOMMENDATION"] + " - " + str(analysis.summary["BUY"]) + "|" + str(analysis.summary["SELL"]) + "|" + str(analysis.summary["NEUTRAL"])
    summary =[summary]
    greeks = [analysis.indicators["RSI"],       # ideal range is between 30-70. 30 being is oversold.
              analysis.indicators["Stoch.K"],   # ideal range is between 20-80.
              analysis.indicators["Stoch.D"],   # ideal range is between 20-80.
              analysis.indicators["CCI20"],     # +100 is well above the average price and -100 well below the average price
              analysis.indicators["ADX"],       # 0-25 Absent or Weak Trend, 25-50 Strong Trend, 50-75 Very Strong Trend, 75-100 Extremely Strong Trend 
              analysis.indicators["AO"],        # +ve value shows bullish momentum and -ve shows bearish momentum
              analysis.indicators["Mom"],       # should be positive
              analysis.indicators["MACD.macd"],     #MACD_macd > MACD_signal, BUY, both should be +ve
              analysis.indicators["MACD.signal"],   #MACD_signal > MACD_macd, SELL 
              analysis.indicators["UO"],            #ideal range is between 30-70. 30 being is buy signal.
              analysis.indicators["P.SAR"]]         # Should be less than closing price.

    greeks = [str(i) for i in greeks]
    
    print(f"Yahoo: {ysymbol}")
    ystock = yf.Ticker(ysymbol)
    financialInfohandler = ystock.get_info()
    earningDate = ""
    try: 
        earningDate = ystock.calendar.loc['Earnings Date'].get(0,"NA")
    except Exception:
        pass
    
    financialInfo = [financialInfohandler.get("trailingPE"), 
              financialInfohandler.get("forwardPE"),
              financialInfohandler.get("trailingEps"),   
              financialInfohandler.get("forwardEps"),     
              financialInfohandler.get("priceToBook"),       
              financialInfohandler.get("earningsQuarterlyGrowth"),
              financialInfohandler.get("sector"),
              financialInfohandler.get("shortName"),
              financialInfohandler.get("heldPercentInstitutions"),
              earningDate,
              financialInfohandler.get("regularMarketPrice"),
              financialInfohandler.get("fiftyTwoWeekHigh"),
              financialInfohandler.get("fiftyTwoWeekLow"),
              financialInfohandler.get("regularMarketPreviousClose"),
              financialInfohandler.get("shortRatio"),
              financialInfohandler.get("recommendationMean"),
              financialInfohandler.get("recommendationKey"),
              financialInfohandler.get("pegRatio"),
              financialInfohandler.get("totalCashPerShare"),
              financialInfohandler.get("earningsGrowth"),
              financialInfohandler.get("currentRatio"),
              financialInfohandler.get("returnOnAssets"),
              financialInfohandler.get("returnOnEquity"),
              financialInfohandler.get("debtToEquity"),
              financialInfohandler.get("quickRatio")]

    financialInfo = [str(i) for i in financialInfo]

    try:
        stock = TA_Handler(symbol=symbol,screener=screener,exchange=exchange,interval=Interval.INTERVAL_1_DAY)
        analysis = stock.get_analysis()
        global daily_recom
        daily_recom = analysis.summary["RECOMMENDATION"] + " - " + str(analysis.summary["BUY"]) + "|" + str(analysis.summary["SELL"]) + "|" + str(analysis.summary["NEUTRAL"])
    except Exception:
        pass
    
    try:
        stock = TA_Handler(symbol=symbol,screener=screener,exchange=exchange,interval=Interval.INTERVAL_1_WEEK)
        analysis = stock.get_analysis()
        global weekly_recom
        weekly_recom = analysis.summary["RECOMMENDATION"] + " - " + str(analysis.summary["BUY"]) + "|" + str(analysis.summary["SELL"]) + "|" + str(analysis.summary["NEUTRAL"])
    except Exception:
        pass
    
    recos = [weekly_recom, lotSize, daily_recom]
    output = [portfolio] + [analysis.symbol] + summary + greeks + financialInfo + recos
    output = [x.replace(',','.') for x in output]
    line = ','.join(output) + '\n'
    return line
    
if localRun == "F":
    getDetailsSlow()
    df = pd.read_csv(fileNameUnsorted).round(decimals=2)
    df.to_csv(rawOutputFile, index=False)
else:
    df = pd.read_csv(rawOutputFile).round(decimals=2)    

df = df.replace('None', '').round(decimals=2)
df['RSI'] = df.RSI.apply(checkRSI)
df['Stoch_K'] = df.Stoch_K.apply(checkRangeWithin,lower=20, upper=80)
df['Stoch_D'] = df.Stoch_D.apply(checkRangeWithin,lower=20, upper=80)
df['CCI20'] = df.CCI20.apply(checkCCI)
df['ADX'] = pd.to_numeric(df.ADX).apply(checkADX)
df['AO'] = pd.to_numeric(df.AO).apply(checkPolarity)
df['Mom'] = pd.to_numeric(df.Mom).apply(checkPolarity)
df['MACD_macd'] = pd.to_numeric(df.MACD_macd)
df['MACD_signal'] = pd.to_numeric(df.MACD_signal)
df['P_SAR'] = pd.to_numeric(df.P_SAR)
df['Price'] = pd.to_numeric(df.Price)
df['MACD'] =df.MACD_macd > df.MACD_signal
df['MACD'] =df['MACD'].apply(lambda x: "BUY" if(x) else "SELL")
df['PAR'] =df['P_SAR']<df['Price']
df['PAR'] =df.PAR.apply(lambda x: "BUY" if(x) else "SELL")
df['MACD_macd'] = df.MACD_macd.apply(checkPolarity)
df['MACD_signal'] = df.MACD_signal.apply(checkPolarity)
df['FutureLotValue'] = df.Price * df.LotSize
#df['Sector'][df.Sector == ""] = df.Stock
df.loc[df.Sector == "", 'Sector'] = df.Stock

#buyDF = df.loc[df['Reco_Daily'].str.match("STRONG_BUY")]
#ssellDF = df.loc[df['Reco_Daily'].str.match("STRONG_SELL")]
   
df = df.sort_values(by=["Reco_4_hrs", "Reco_Daily","Reco_Weekly"], 
                           ascending=[False,False,False])

## Get Previous daily rating
previousFile = getLatestFileName(filepath,screener,runType)
print(f"previousFile: {previousFile}")
previousDF = pd.read_csv(previousFile,skipinitialspace=True).round(decimals=2)
del previousDF['Reco_Daily_last']
df = pd.merge(df, previousDF, on='Symbol', how='left',suffixes=("", "_last"))

df['Trend'] = df.apply(trendSignal, axis=1)
df['Trend_last'] = df.apply(trendSignal,append='_last', axis=1)

df['Rule'] = df.apply(ruleEngine,axis=1)
df['Rule_last'] = df.apply(ruleEngine,append='_last', axis=1)

buyTrendList = df[((df.Trend == 'STRONG_BUY') & (df.Rule == 'STRONG_BUY'))]['Symbol'].to_list()
sellTrendList = df[((df.Trend == 'STRONG_SELL') & (df.Rule == 'STRONG_SELL'))]['Symbol'].to_list()

buyTrendLastList = df[((df.Trend_last == 'STRONG_BUY') & (df.Rule_last == 'STRONG_BUY'))]['Symbol'].to_list()
sellTrendLastList = df[((df.Trend_last == 'STRONG_SELL') & (df.Rule_last == 'STRONG_SELL'))]['Symbol'].to_list()

overbroughtList = df[(pd.to_numeric(df['RSI'].str.split(":").str[-1]) > 75)]['Symbol'].to_list()
oversoldList = df[(pd.to_numeric(df['RSI'].str.split(":").str[-1]) < 25)]['Symbol'].to_list()

df = df[['Sector',
 'Symbol',
 'Rule',
 'Trend',
 'Price',
 'PreviousClose',
 '52WeekHigh',
 '52WeekLow',
 'TrailingPE',
 'ForwardPE',
 'pegRatio',
 'PriceToBook',
 'EarningsQuarterlyGrowth',
 'Institutions_pct',
 'Earning_Date',
 'Reco_4_hrs',
 'Reco_Daily',
 'Reco_Daily_last',
 'Reco_Weekly',
 'RSI',
 'MACD',
 'PAR',
 'Stoch_K',
 'Stoch_D',
 'ADX',
 'CCI20',
 'AO',
 'Mom',
 'MACD_macd',
 'MACD_signal',
 'UO',
 'P_SAR',
 'TrailingEps',
 'ForwardEps',
 'Stock',
 'Category',
 'LotSize',
 'ShortInterest',
 'RecommdationMean',
 'FutureLotValue',
 'RecommadationKey',
 'totalCashPerShare',
 'earningsGrowth',
 'currentRatio',
 'returnOnAssets',
 'returnOnEquity',
 'debtToEquity',
 'quickRatio']]

df.to_csv(fileName, index=False)

name = "StockAnalysis"
email = "..." # from email id
mail_server = "..." # email server 
to_email = "..." # recipient email id
to_name = ".." # recipient name
subject = f"Stock Analysis: {screener} : {runType}: {todayF}"
outputDF = df[['Symbol','Trend','Rule','ADX']].sort_values(by=['Rule','Trend'])
outputDF['ADX'] = outputDF['ADX'].str.split(":").str[0]
finalDF = tabulate(outputDF, headers=['Symbol','Trend','Rule','ADX'],tablefmt="orgtbl",showindex=False)
newBuy = np.setdiff1d(buyTrendList,buyTrendLastList)
newSell = np.setdiff1d(sellTrendList,sellTrendLastList)
newBuyDF = outputDF[outputDF['Symbol'].isin(list(newBuy))]
newSellDF = outputDF[outputDF['Symbol'].isin(list(newSell))]
newBuyDF = tabulate(newBuyDF[['Symbol','ADX']].sort_values(by=['ADX']), headers=['Symbol','ADX'],tablefmt="orgtbl",showindex=False)
newSellDF = tabulate(newSellDF[['Symbol','ADX']].sort_values(by=['ADX']), headers=['Symbol','ADX'],tablefmt="orgtbl",showindex=False)

message = f"""
Following stocks are new BUY:
{newBuyDF}

Following stocks are new Sell:
{newSellDF}

Following stocks are no longer BUY:
{np.setdiff1d(buyTrendLastList,buyTrendList)}

Following stocks are no longer SELL:
{np.setdiff1d(sellTrendLastList,sellTrendList)}


Following stocks oversold(RSI <25):
{oversoldList}

Following stocks overbrought(RSI >75)::
{overbroughtList}

Rule Engine Summary:
Buy Count: {len(df[((df['Trend'] == 'STRONG_BUY') & (df['Rule'] == 'STRONG_BUY'))]['Symbol'].index)}
Sell Count: {len(df[((df['Trend'] == 'STRONG_SELL') & (df['Rule'] == 'STRONG_SELL'))]['Symbol'].index)}
Neutral Count: {len(df[df['Rule'] == 'NEUTRAL'].index)}

Rule Engine Output:
{finalDF}
"""
with open(finalMsgFie, "w") as f:
    f.write(message)

print(message)

if sendEmail == "T":
    sendmail(name, email, mail_server, to_email, to_name, subject, message, fileName)

if localRun == "F":
    os.remove(fileNameUnsorted) 
    