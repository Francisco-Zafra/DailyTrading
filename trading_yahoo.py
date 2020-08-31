#Using the Public API (without authentication), you are limited to 2,000 requests per hour per IP (or up to a total of 48,000 requests a day).

import yfinance as yf
import json

from stock_finder import getStocks

msft = yf.Ticker("PRO.MC")

# get stock info
data = msft.history(period="5d", interval="1m")

output = open('data.json', 'w')
output.write(data.to_json(orient='table', indent=4))

print(getStocks())