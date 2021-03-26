from ib_insync import *
util.startLoop()
from yahooquery import Ticker
import sys

target_stock = 'AAPL'
order_size = 1
time_to_fill = 10
ib_sleep = 1

def get_bid_ask(symbol):
    ticker = Ticker(symbol, validate=True)
    ticker_details = ticker.summary_detail
    bid = ticker_details[symbol].get("bid")
    ask = ticker_details[symbol].get("ask")
    return bid, ask

def find_bid_limit(stock, bid, ask):
  stock = Contract(symbol=target_stock, exchange='SMART', secType='STK', currency='USD')
  while True:
    order = LimitOrder('BUY', order_size, bid)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < time_to_fill:
      print("Waiting for fill")
      ib.sleep(ib_sleep)
      print(bid, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        return trade.orderStatus.avgFillPrice
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(ib_sleep)
        print(trade.orderStatus.status)
        break
    bid = round(bid + .01, 2)
  
def find_ask_limit(stock, bid, ask):
  stock = Contract(symbol=target_stock, exchange='SMART', secType='STK', currency='USD')
  while True:
    order = LimitOrder('SELL', order_size, ask)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < time_to_fill:
      ib.sleep(ib_sleep)
      print(ask, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        return trade.orderStatus.avgFillPrice
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(ib_sleep)
        print(trade.orderStatus.status)
        break
    ask = round(ask - .01, 2

ib = IB()
clientId = 1
ib.connect('127.0.0.1', 7497, clientId=1)

bid, ask = get_bid_ask(target)
bid_limit = find_bid_limit(target, bid, ask)
print(bid_limit)
ask_limit = find_ask_limit(target, bid, ask)
print(ask_limit)