#Using the Public API (without authentication), you are limited to 2,000 requests per hour per IP (or up to a total of 48,000 requests a day).

import yfinance as yf
import json
from stock_finder import getStocks
import threading
import time

def stockbroker(stock, budget, wait):
    while(True):
        time.sleep(wait)
        msft = yf.Ticker(stock)
        data = msft.history(period="7d", interval="1m")

        len = data['High'].size

        # output = open('data.json', 'w')
        # output.write(data.to_json(orient='table', indent=4))

        media_7_dias = sum(data['High'])/(data['High'].size)
        if data['Close'][len-2] <= data['Close'][len-3] and data['Close'][len-3] <= data['Close'][len-4]:
            cierre_anterior = data['Close'][len-2]
            low_anterior = data['Low'][len-2]
            high_anterior = data['High'][len-2]

            cierre_actual = data['Close'][len-1]

            ATR = max(high_anterior - low_anterior, high_anterior - cierre_anterior, cierre_anterior - low_anterior)

            if(cierre_anterior - ATR > cierre_actual):
                comprar(cierre_actual, budget, stock)
                
        for stock_vender in noVendidos():
            if stock['Precio'] < data['Close'][len-1]:
                vender(cierre_actual, stock_vender)
        time.sleep(60 - wait)

def comprar(valor, budget, empresa):
    print('Compra')
    n_acciones = int(budget/valor)
    with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        d['compras'].append({'coste': valor, 'n_acciones': n_acciones, 'empresa': empresa})

        with open("dinero.txt", "r") as outfile: 
            dinero = outfile.readline()
            dinero = int(dinero) - n_acciones*valor
            with open("dinero.txt", "w") as outfile:
                outfile.write(str(dinero))

def noVendidos():
   with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        return d['compras']

def vender(precio, stock):
    print('Vende')
    with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        d['compras'].remove(stock)

        with open("dinero.txt", "r") as outfile: 
            dinero = outfile.readline()
            dinero = int(dinero) + stock['n_acciones'] * precio
            with open("dinero.txt", "w") as outfile:
                outfile.write(str(dinero))



def hebras(stocks):
    i = 0
    for s in stocks:
        hilo = threading.Thread(target=stockbroker, 
                                args=(s, 100, i))
        hilo.start()
        i += 1
        print('Inicio Hebra: ', s)

stocks = getStocks()
msft = yf.Ticker('MSFT')
data = msft.history(period="7d", interval="1m")

hebras(stocks)

