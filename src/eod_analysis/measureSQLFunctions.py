#!/usr/bin/env python

import pandas as pd

def checkRSI(x):
    if x <25:
        return 'Oversold' + " : " + str(x)
    elif x >=25 and x <45:
        return 'Bearish' + " : " + str(x)
    elif x >=45 and x <55:
        return 'Neutral' + " : " + str(x)
    elif x >=55 and x <75:
        return 'Bullish ' + " : " + str(x)
    else:
        return 'Overbought' + " : " + str(x)

def checkRangeWithin(x, lower=30, upper=70):
    if x <=lower:
        return 'Oversold' + " : " + str(x)
    elif x >=upper:
        return 'Overbrought' + " : " + str(x)
    else:
        return 'Bullish' + " : " + str(x)
    
def checkRangeOutside(x, lower=-100, upper=+100):
    if x <=lower:
        return 'Bearish' + " : " + str(x)
    elif x >=upper:
        return 'Bullish' + " : " + str(x)
    else:
        return 'Neutral' + " : " + str(x)
    
def checkPolarity(x, limit=0):
    if x >=limit:
        return 'Bullish' + " : " + str(x)
    else:
        return 'Bearish' + " : " + str(x)
    
def checkCCI(x):
    if x <-200:
        return 'Oversold' + " : " + str(x)
    elif x >=-200 and x <-50:
        return 'Bearish' + " : " + str(x)
    elif x >=-50 and x <50:
        return 'Neutral' + " : " + str(x)
    elif x >=50 and x <200:
        return 'Bullish ' + " : " + str(x)
    else:
        return 'Overbought' + " : " + str(x)
    
def checkADX(x):
    if x >=0 and x <25:
        return 'Weak Trend' + " : " + str(x)
    elif x >=25 and x <50:
        return 'Strong Trend' + " : " + str(x)
    elif x >=50 and x <75:
        return 'Very Strong Trend' + " : " + str(x)
    elif x >=75 and x <100:
        return 'Extremely Strong Trend' + " : " + str(x)
    else:
        return 'Neutral' + " : " + str(x)
    
def ruleEngine(row, append=""):
    if pd.isna(row['Reco_Daily' + append]):
        "NOT_CALCULATED"
    elif float(row['RSI' + append].split(":")[-1]) > 75:
            return 'OVERBROUGHT'
    elif float(row['RSI' + append].split(":")[-1]) < 25:
            return 'OVERSOLD'
    elif ( "BUY" in row['Reco_Daily' + append] and
    "BUY" in row['MACD' + append] and
    float(row['RSI' + append].split(":")[-1]) >= 50 and
    float(row['RSI' + append].split(":")[-1]) <= 75 and
    float(row['CCI20' + append].split(":")[-1]) >= 50 and
    float(row['AO' + append].split(":")[-1]) >= 0 and
    float(row['Mom' + append].split(":")[-1]) >= 0):
            return 'STRONG_BUY'
    elif ( "SELL" in row['Reco_Daily' + append] and
    "SELL" in row['MACD' + append] and
    float(row['RSI' + append].split(":")[-1]) < 50 and
    float(row['RSI'+ append ].split(":")[-1]) >= 25 and
    float(row['CCI20'+ append ].split(":")[-1]) <= -50 and
    float(row['AO'+ append ].split(":")[-1]) < 0 and
    float(row['Mom'+ append].split(":")[-1]) <= 0):
            return 'STRONG_SELL'
    elif ( "BUY" in row['Reco_Daily' + append] and
    "BUY" in row['MACD' + append] and
    float(row['RSI' + append].split(":")[-1]) >= 50 and
    float(row['RSI' + append].split(":")[-1]) <= 75):
            return 'BUY'
    elif ( "SELL" in row['Reco_Daily' + append] and
    "SELL" in row['MACD' + append] and
    float(row['RSI' + append].split(":")[-1]) < 50 and
    float(row['RSI'+ append ].split(":")[-1]) >= 25):
            return 'SELL'
    else:
        return 'NEUTRAL'

def trendSignal(row,append=""):
    if pd.isna(row['Reco_4_hrs' + append]):
        "NOT_CALCULATED"
    elif ("BUY" in row['Reco_4_hrs' + append] and
    "BUY" in row['Reco_Daily' + append] and
    "BUY" in row['Reco_Weekly' + append]):
        return 'STRONG_BUY'
    elif ("SELL" in row['Reco_4_hrs' + append] and
    "SELL" in row['Reco_Daily' + append] and
    "SELL" in row['Reco_Weekly' + append]):
        return 'STRONG_SELL'
    elif ("BUY" in row['Reco_4_hrs' + append] and
    "BUY" in row['Reco_Daily' + append]):
        return 'BUY'
    elif ("SELL" in row['Reco_4_hrs' + append] and
    "SELL" in row['Reco_Daily' + append]):
        return 'SELL'
    else:
        return 'NEUTRAL'
