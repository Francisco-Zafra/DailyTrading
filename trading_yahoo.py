#Using the Public API (without authentication), you are limited to 2,000 requests per hour per IP (or up to a total of 48,000 requests a day).

import yfinance as yf
import json
from stock_finder import getStocks
import threading
import time
import logging

def stockbroker(stock, budget, wait):
    logging.basicConfig(filename='trading.log',level=logging.INFO, format='%(asctime)s %(message)s')
    cartera = budget
    while(True):
        time.sleep(wait)
        msft = yf.Ticker(stock)
        data = msft.history(period="7d", interval="1m")

        len = data['High'].size

        # output = open('data.json', 'w')
        # output.write(data.to_json(orient='table', indent=4))
        logging.info(stock + ' ' + str(data['Close'][len-1]))
        print(stock, str(data['Close'][len-1]))
        media_7_dias = sum(data['High'])/(data['High'].size)
        if data['Close'][len-2] <= data['Close'][len-3] and data['Close'][len-3] <= data['Close'][len-4]:
            cierre_anterior = data['Close'][len-2]
            low_anterior = data['Low'][len-2]
            high_anterior = data['High'][len-2]

            cierre_actual = data['Close'][len-1]

            ATR = max(high_anterior - low_anterior, high_anterior - cierre_anterior, cierre_anterior - low_anterior)
            if(cierre_anterior - ATR > cierre_actual and cierre_actual < cartera):
                comprar(cierre_actual, cartera, stock)
                cartera -= cierre_actual * int(cartera/cierre_actual)
                print('Me queda: ', cartera)
                logging.info('Me queda: ' + str(cartera))
                
        for stock_vender in noVendidos():
            #print('Vender', stock_vender['coste'], 'a', data['Close'][len-1])
            if stock_vender['coste']  < data['Close'][len-1] and stock_vender['empresa'] == stock:
                vender(data['Close'][len-1], stock_vender)
                cartera = budget
                print('Cartera vuelve a: ', budget)
                logging.info('Cartera vuelve a: ' + str(budget))
        time.sleep(60 - wait)

def comprar(valor, budget, empresa):
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    print('Compra', empresa, valor)
    logging.info('Compra' + empresa + ' ' + str(valor))
    n_acciones = int(budget/valor)
    with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        d['compras'].append({'coste': valor, 'n_acciones': n_acciones, 'empresa': empresa})
    
        with open("stocks.json", "w") as outfile: 
            json.dump(d, outfile, indent=4)

        with open("dinero.txt", "r") as outfile: 
            dinero = outfile.readline()
            dinero = float(dinero) - n_acciones*valor
            with open("dinero.txt", "w") as outfile:
                outfile.write(str(dinero))

def noVendidos():
   with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        return d['compras']

def vender(precio, stock):
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    print('Vende', stock['empresa'], precio)
    logging.info('Vende' + stock['empresa'] + ' ' + str(precio))
    with open("stocks.json", "r") as outfile: 
        d = json.load(outfile)
        d['compras'].remove(stock)
        with open("stocks.json", "w") as outfile: 
            json.dump(d, outfile, indent=4)

        with open("dinero.txt", "r") as outfile: 
            dinero = outfile.readline()
            dinero = float(dinero) + stock['n_acciones'] * precio
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

stocks = getStocks(10)
msft = yf.Ticker('MSFT')
data = msft.history(period="7d", interval="1m")

hebras(stocks)

