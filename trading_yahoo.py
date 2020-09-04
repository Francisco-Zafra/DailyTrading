#Using the Public API (without authentication), you are limited to 2,000 requests per hour per IP (or up to a total of 48,000 requests a day).

import yfinance as yf
import json
from stock_finder import getStocks
import threading
import time
import logging

def stockbroker(stock, budget, wait):
    fin = False
    logging.basicConfig(filename='trading.log',level=logging.INFO, format='%(asctime)s %(message)s')
    cartera = budget
    while(not fin):
        time.sleep(wait)
        msft = yf.Ticker(stock)
        data = msft.history(period="7d", interval="1m")

        len = data['High'].size

        # output = open('data.json', 'w')
        # output.write(data.to_json(orient='table', indent=4))
        #logging.info(stock + ' ' + str(data['Close'][len-1]))
        print(stock, str(data['Close'][len-1]))
        media_7_dias = sum(data['High'])/(data['High'].size)
        #Condicion: Lleva tres veces seguidas bajando
        if esta_bajando(data):

            cierre_actual = data['Close'][len-1]
            if(cond_compra(data, cartera)):
                comprar(cierre_actual, cartera, stock)
                cartera -= cierre_actual * int(cartera/cierre_actual)
                print('Me queda: ', cartera)
                logging.info('Me queda: ' + str(cartera))
                
        for stock_vender in noVendidos():
            #print('Vender', stock_vender['coste'], 'a', data['Close'][len-1])
            if cond_venta(stock_vender, data, stock):
                vender(data['Close'][len-1], stock_vender)
                cartera = budget
                print('Cartera vuelve a: ', budget)
                logging.info('Cartera vuelve a: ' + str(budget))
        time.sleep(60 - wait)
        if horaCierre():
            fin = True

    logging.info(stock + ' cerrado, hasta mañana')

def esta_bajando(data):
    len = data['High'].size
    vez1 = data['Close'][len-2]
    vez2 = data['Close'][len-3]
    cont = 4
    while(vez1 == vez2):
        vez2 = data['Close'][len-cont]
        cont += 1
        if(cont > len):
            return False
    vez3 = data['Close'][len-cont]
    while(vez2 == vez3):
        vez3 = data['Close'][len-cont]
        cont += 1 
        if(cont > len):
            return False         

    return vez1 < vez2 and vez2 < vez3

def cond_compra(data, cartera):
    len = data['High'].size
    cierre_anterior = data['Close'][len-2]
    low_anterior = data['Low'][len-2]
    high_anterior = data['High'][len-2]
    cierre_actual = data['Close'][len-1]

    ATR = max(high_anterior - low_anterior, high_anterior - cierre_anterior, cierre_anterior - low_anterior)

    return cierre_anterior - ATR > cierre_actual and cierre_actual < cartera
    

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

def cond_venta(stock_vender, data, stock):
    len = data['High'].size
    return stock_vender['coste'] < data['Close'][len-1] and stock_vender['empresa'] == stock


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

def broker_antiguo(stock):
    noVendido = True
    msft = yf.Ticker(stock)
    data = msft.history(period="7d", interval="1m")

    while(noVendido):
        for stock_vender in noVendidos():
            #print('Vender', stock_vender['coste'], 'a', data['Close'][len-1])
            if cond_venta(stock_vender, data, stock):
                vender(data['Close'][len-1], stock_vender)
                noVendido = False
                print('Venta antigua completada: ', stock)
                logging.info('Venta antigua completada: ' + stock)
        time.sleep(60)
    

def hebras(stocks):
    i = 0
    budget = 100
    for s in stocks:
        hilo = threading.Thread(target=stockbroker, 
                                args=(s, budget, i))
        hilo.start()
        i += 1
        print('Inicio Hebra: ', s)

def hebras_ventas_antiguas(stocks):
    noV = noVendidos()
    for n in noV:
        esta = False
        for stock in stocks:
            if n['empresa'] == stock:
                esta = True
        if not esta:
            hilo = threading.Thread(target=broker_antiguo,
                                    args=(n['empresa'],))
            hilo.start()
            print('Inicio Hebra venta antigua: ', n['empresa'])    
    return

def horaCierre():
    reloj = time.ctime().split()[3]
    horas = int(reloj.split(':')[0])
    minutos = int(reloj.split(':')[1])

    if horas > 17 and minutos > 30:
        return True
    return False

def horaApertura():
    reloj = time.ctime().split()[3]
    horas = int(reloj.split(':')[0])
    minutos = int(reloj.split(':')[1])

    if horas == 9 and minutos >= 0 and minutos <= 5:
        return True
    return False

while(True):
    if horaApertura():
        stocks = getStocks(10)
        hebras(stocks)
        hebras_ventas_antiguas(stocks)
        time.sleep(600)
    print('Esperando hora de apertura (9:00)')
    time.sleep(60)
    


