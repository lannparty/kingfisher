from ib_insync import *
util.startLoop()
from yahooquery import Ticker
import sys

target = 'AAPL'
size = 1

def get_bid_ask(symbol):
    ticker = Ticker(symbol, validate=True)
    ticker_details = ticker.summary_detail
    bid = ticker_details[symbol].get("bid")
    ask = ticker_details[symbol].get("ask")
    return bid, ask

def find_bid_limit(stock, bid, ask):
  stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
  while bid < (ask + bid / 2):
    order = LimitOrder('BUY', size, bid)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < 10:
      print("Waiting for fill")
      ib.sleep(1)
      print(bid, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        print(trade.orderStatus.avgFillPrice)
        return
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(1)
        print(trade.orderStatus.status)
        break
    bid = round(bid + .01, 2)
  
def find_ask_limit(stock, bid, ask):
  stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
  while ask > ((ask + bid) / 2):
    order = LimitOrder('SELL', size, ask)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < 10:
      ib.sleep(1)
      print(ask, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        print(trade.orderStatus.avgFillPrice)
        return
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(1)
        print(trade.orderStatus.status)
        break
    ask = round(ask - .01, 2)

ib = IB()
clientId = 1
ib.connect('127.0.0.1', 7497, clientId=1)

bid, ask = get_bid_ask(target)

find_bid_limit(target, bid, ask)
find_ask_limit(target, bid, ask)