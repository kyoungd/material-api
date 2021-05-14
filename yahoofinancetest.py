import yfinance as yf
from datetime import date, datetime


def parse_interval(period_code):
    if period_code == "1m":
        return "1d", "1m"
    elif period_code == "5m":
        return "1d", "5m"
    elif period_code == "15m":
        return "1d", "15m"
    elif period_code == "30m":
        return "1d", "30m"
    elif period_code == "1h":
        return "1d", "1h"
    elif period_code == "4h":
        return "1d", "1h"
    elif period_code == "1d":
        return "1d", "1d"
    elif period_code == "1w":
        return "1d", "1wk"
    else:
        return "", ""


symbol = "BTX"
period = "1d"

msft = yf.Ticker(symbol)

# get stock info
print(msft.info)

period, interval = parse_interval(period)

# https://algotrading101.com/learn/yfinance-guide/
# get historical market data
# PARAMETERS
# period: data period to download(either use period parameter or use start and end) Valid periods are:
# “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
# interval: data interval(1m data is only for available for last 7 days, and data interval < 1d for the last 60 days) Valid intervals are:
# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
# start: If not using period – in the format(yyyy-mm-dd) or datetime.
# end: If not using period – in the format(yyyy-mm-dd) or datetime.
# prepost: Include Pre and Post regular market data in results? (Default is False) - no need usually to change this from False
# auto_adjust: Adjust all OHLC(Open/High/Low/Close prices) automatically? (Default is True) - just leave this always as true and don’t worry about it
# actions: Download stock dividends and stock splits events? (Default is True)
hist = msft.history(start="2020-01-01",
                    period=period, interval=interval)
format = "%Y-%m-%d %H:%M:%S"
dt_object = datetime.strptime("2020-01-15 00:00:00", format)
stocks = list(filter(lambda item: item.name > dt_object, hist.iloc))

for item in stocks:
    print(symbol, period, item.name, item.Open, item.Close,
          item.High, item.Close, item.Volume, item.Dividends, item["Stock Splits"])


print(hist.iloc[0].name)
# Open, High, Low, Close, Volume, Divideneds, Stock Splits
print(hist.iloc[0]["Open"])
print(hist.iloc[0]["Stock Splits"])

# hist.iloc[lambda item:]
# for ix in range(0, hist.iloc.length):

# show actions (dividends, splits)
msft.actions

# show dividends
msft.dividends

# show splits
msft.splits

# show financials
msft.financials
msft.quarterly_financials

# show major holders
msft.major_holders

# show institutional holders
msft.institutional_holders

# show balance sheet
msft.balance_sheet
msft.quarterly_balance_sheet

# show cashflow
msft.cashflow
msft.quarterly_cashflow

# show earnings
msft.earnings
msft.quarterly_earnings

# show sustainability
msft.sustainability

# show analysts recommendations
msft.recommendations

# show next event (earnings, etc)
msft.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
msft.isin

# show options expirations
msft.options

# get option chain for specific expiration
opt = msft.option_chain('2021-04-30')
# data available via: opt.calls, opt.puts
