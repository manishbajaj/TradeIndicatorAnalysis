import array
from pyparsing import Iterable
from tradingview_ta import TA_Handler, Interval
import sys,os, glob
import datetime 
from tabulate import tabulate
from multiprocessing.pool import ThreadPool as Pool
from tabulate import tabulate
from datetime import date, timedelta
import pandas as pd
import timeit


start = timeit.default_timer()

print('=' * 20)

localRun = "F"
sendEmail = "T"
runType = "intra" #portfolio
display = "no"
now = datetime.datetime.now()
today7 = now.replace(hour=7, minute=0, second=0, microsecond=0)
today18 = now.replace(hour=18, minute=0, second=0, microsecond=0)

if now < today18 and now > today7:
    screener = "india"
else:
    screener = "america" 

config_suffix=""

if len(sys.argv) == 2:
    display =  sys.argv[1]
elif len(sys.argv) == 3:
    display =  sys.argv[1]
    screener =  sys.argv[2]
elif len(sys.argv) == 4:
    display =  sys.argv[1]
    screener =  sys.argv[2]
    config_suffix = sys.argv[3]

configFile = f"C:\Report\config\config_{screener}_{runType}.csv"

if config_suffix != "":
    configFile = f"C:\Report\config\config_{screener}_{runType}_{config_suffix}.csv"

def getLatestFileName(filePath,screener,runType):
    list_of_files = glob.glob(f"{filePath}\\{screener}*{runType}.csv")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def processSymbol(configLine):
    (exchange, symbol) = configLine.split(",")
    intervals = ['1m','5m','15m',"30m",'1h',"2h",'4h','1d','1W']

    data = []
    for interval in intervals:
        if symbol == 'NIFTY':
            stock = TA_Handler(symbol=symbol,screener='cfd',exchange=exchange,interval=interval)
        else:
            stock = TA_Handler(symbol=symbol,screener=screener,exchange=exchange,interval=interval)
        s3 = s2 = s1 = p = r1 = r2 = r3 = 0
        analysis = stock.get_analysis()
        summary = analysis.summary["RECOMMENDATION"] 
        macd = analysis.indicators["MACD.macd"]
        signal = analysis.indicators["MACD.signal"]
        adx = round(analysis.indicators["ADX"],0)
        vwma = analysis.indicators["VWMA"]
        ema50 = analysis.indicators["EMA50"]
        ema100 = analysis.indicators["EMA100"]
        ema200 = analysis.indicators["EMA200"]
        price = analysis.indicators["close"]
        change = round(analysis.indicators["change"],2) if interval in ['1d','1W'] else 'NA'
        s3 = round(analysis.indicators["Pivot.M.Fibonacci.S3"],1) if analysis.indicators["Pivot.M.Fibonacci.S3"] is not None else 0
        s2 = round(analysis.indicators["Pivot.M.Fibonacci.S2"],1) if analysis.indicators["Pivot.M.Fibonacci.S2"] is not None else 0
        s1 = round(analysis.indicators["Pivot.M.Fibonacci.S1"],1) if analysis.indicators["Pivot.M.Fibonacci.S1"] is not None else 0
        p  = round(analysis.indicators["Pivot.M.Fibonacci.Middle"],1) if analysis.indicators["Pivot.M.Fibonacci.Middle"] is not None else 0
        r1 = round(analysis.indicators["Pivot.M.Fibonacci.R1"],1) if analysis.indicators["Pivot.M.Fibonacci.R1"] is not None else 0
        r2 = round(analysis.indicators["Pivot.M.Fibonacci.R2"],1) if analysis.indicators["Pivot.M.Fibonacci.R2"] is not None else 0
        r3 = round(analysis.indicators["Pivot.M.Fibonacci.R3"],1) if analysis.indicators["Pivot.M.Fibonacci.R3"] is not None else 0
        
        macdSignal = 'BUY' if macd > signal else 'SELL'
        ema50Signal = 'BUY' if price > ema50 else 'SELL'
        ema100Signal = 'BUY' if price > ema100 else 'SELL'
        ema200Signal = 'BUY' if price > ema200 else 'SELL'
        vwmaSignal = 'BUY' if symbol != 'NIFTY' and price > vwma else 'SELL'
        data.append([symbol,interval,summary,macdSignal,adx,vwmaSignal,ema50Signal,ema100Signal,ema200Signal,price,change,s3,s2,s1,p,r1,r2,r3])

    trend = 'NEUTRAL'

    indicators = [data[2][2], data[3][2], data[4][2], data[5][2], data[6][2]]

    if (all(value in ('BUY', 'STRONG_BUY', 'NEUTRAL') for value in indicators)):
        trend = 'BUY'
    elif (all( value in ('SELL', 'STRONG_SELL', 'NEUTRAL') for value in indicators)):
        trend = 'SELL'
    
    for row in data:
        row.append(trend)

    df = pd.DataFrame(data, columns=['Symbol','Interval','Summary','MACD','ADX','VWMA','EMA50','EMA100','EMA200','Price','Change', 'S3','S2','S1','P','R3','R2','R1','Trend'])
    df = df[['Symbol','Interval','Trend','Summary','MACD','VWMA','EMA50','EMA100','EMA200','ADX','Price','Change', 'S2','S1','P','R3','R2']]
    
    output = f"""
{tabulate(df, headers=['Symbol','Interval','Trend','Summary','MACD','VWMA','EMA50','EMA100','EMA200','ADX', 'Price','Change','S2','S1','P','R3','R2'],tablefmt="orgtbl",showindex=False)}
        """
    if  display == 'all':
        print(f"{output}")
    elif symbol in ['SPY','QQQ','NIFTY']:
        print(f"{output}")
    elif symbol == display:
        print(f"{output}")
    elif trend == display:
        print(f"{output}")
    elif trend != 'NEUTRAL' and display == 'no':
        print(f"{output}")
    else:
        pass
   
if __name__ == '__main__':
    configs = []
    with open(configFile, "r") as fp:
        for i in fp.readlines():
            tmp = i.rstrip()
            configs.append(tmp)
    
    configs = [value for value in configs if display in value] if(config_suffix ==  'all' and display not in ('BUY', 'SELL','NEUTRAL')) else configs

    threading = 'YES'
    pool = Pool(len(configs))
    for item in configs:
        if threading == 'YES':
            pool.apply_async(processSymbol, (item,))
        else:
            processSymbol(item)
    
    pool.close()
    pool.join()
    stop = timeit.default_timer()
    
    print('Time: ', stop - start)  
    print('=' * 20)
