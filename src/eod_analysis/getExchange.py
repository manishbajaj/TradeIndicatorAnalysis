import os, glob
import pandas as pd
from datetime import date, timedelta
import datetime 
import yfinance as yf
from email_utils import sendmail
from measureSQLFunctions import checkRSI, checkRangeWithin,checkCCI, checkADX, checkPolarity
import numpy as np

inputFile = f"C:\Report\\temp\\input.csv"
outputFile = f"C:\Report\\temp\\output.csv"

def processFile():
    with open(outputFile, "w") as tmpFileHandler:
        with open(inputFile, "r") as fp:
            for i in fp.readlines():
                tmp = i.rstrip().split(",")
                exchange = getchange(tmp[0])
                if exchange == 'NYQ':
                    exchange = 'NYSE'
                else:
                    exchange = 'NASDAQ'
                output = ['SPY',exchange,tmp[0],tmp[0],'100']
                line = ','.join(output) + '\n'
                tmpFileHandler.write(line)
        fp.close()
    tmpFileHandler.close()

   
def getchange(symbol):
    print(f"Yahoo: {symbol}")
    ystock = yf.Ticker(symbol)
    financialInfohandler = ystock.get_info()
    exchange = financialInfohandler.get("exchange")
    return exchange
    
processFile()
