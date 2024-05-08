# TradeIndicatorAnalysis

This project contan 2 main reports

eod_report - This fetch data from tradingview and yahoo finance. The report generate the STock list which we producing strong buy or sell signal. it also contains many useful technical and fundamental signals. The timeframe used are daily, weekly and monthly
    - Make sure you have path created under C:\Report or change it accordingly
    - It uses the previous day report for trend analysis.

Sample output:
        Following stocks are new BUY:
        | Symbol   | ADX          |
        |----------+--------------|
        | ABBV     | Strong Trend |
        | KO       | Weak Trend   |
        | XLV      | Weak Trend   |

        Following stocks are new Sell:
        | Symbol   | ADX          |
        |----------+--------------|
        | SMH      | Strong Trend |
        | AMD      | Strong Trend |
        | AMAT     | Strong Trend |
        | GOLD     | Strong Trend |
        | GDXJ     | Strong Trend |
        | XME      | Strong Trend |

intraday_report - This report generate very concise view on different technical indicators for timeframe like '1m','5m','15m',"30m",'1h',"2h",'4h','1d','1W'. this is suppose to used when market is open and select the stock which is showing trend.

Sample output:

    | Symbol   | Interval   | Trend   | Summary     | MACD   | VWMA   | EMA50   | EMA100   | EMA200   |   ADX |   Price | Change   |     S2 |     S1 |      P |     R3 |     R2 |
    |----------+------------+---------+-------------+--------+--------+---------+----------+----------+-------+---------+----------+--------+--------+--------+--------+--------|
    | LT       | 1m         | SELL    | SELL        | BUY    | SELL   | SELL    | SELL     | SELL     |    33 | 3429.1  | NA       | 3425.6 | 3445.9 | 3478.7 | 3511.5 | 3531.8 |
    | LT       | 5m         | SELL    | SELL        | SELL   | SELL   | SELL    | SELL     | SELL     |    32 | 3429.1  | NA       | 3425.6 | 3445.9 | 3478.7 | 3511.5 | 3531.8 |
    | LT       | 15m        | SELL    | SELL        | SELL   | SELL   | SELL    | SELL     | SELL     |    23 | 3429.1  | NA       | 3425.6 | 3445.9 | 3478.7 | 3511.5 | 3531.8 |
    | LT       | 30m        | SELL    | STRONG_SELL | SELL   | SELL   | SELL    | SELL     | SELL     |    31 | 3429.1  | NA       | 3446.3 | 3484.4 | 3546   | 3607.7 | 3645.8 |
    | LT       | 1h         | SELL    | SELL        | BUY    | SELL   | SELL    | SELL     | SELL     |    38 | 3429.1  | NA       | 3446.3 | 3484.4 | 3546   | 3607.7 | 3645.8 |
    | LT       | 2h         | SELL    | SELL        | SELL   | SELL   | SELL    | SELL     | SELL     |    34 | 3429.1  | NA       | 3446.3 | 3484.4 | 3546   | 3607.7 | 3645.8 |
    | LT       | 4h         | SELL    | SELL        | SELL   | SELL   | SELL    | SELL     | SELL     |    25 | 3429.1  | NA       | 3446.3 | 3484.4 | 3546   | 3607.7 | 3645.8 |
    | LT       | 1d         | SELL    | SELL        | SELL   | SELL   | SELL    | SELL     | BUY      |    20 | 3427.75 | -1.03    | 3402.7 | 3494.2 | 3642.2 | 3790.3 | 3881.8 |
    | LT       | 1W         | SELL    | NEUTRAL     | SELL   | SELL   | BUY     | BUY      | BUY      |    33 | 3427.75 | -2.06    | 2119.8 | 2474.2 | 3048   | 3621.7 | 3976.2 |