from ib_insync import *
util.startLoop()
from yahooquery import Ticker
import sys

target = 'USLM'
size = 5
step = .05
fraction_of_spread = .3


def get_bid_ask(symbol):
    ticker = Ticker(symbol, validate=True)
    ticker_details = ticker.summary_detail
    bid = ticker_details[symbol].get("bid")
    ask = ticker_details[symbol].get("ask")
    spread = round((ask - bid) * fraction_of_spread)
    print("bid", bid, "ask", ask, "spread", spread)
    return bid, ask, spread

def find_bid_limit(stock, bid, ask, spread):
  stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
  max_price = ((bid + round((spread / 4), 2)))
  print("Bidding up from bid of", bid, "to max price of", max_price, "in steps of", step)
  while bid < max_price:
    order = LimitOrder('BUY', size, bid)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < 10:
      ib.sleep(1)
      print("Desired price at", bid, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        print("bought", round(trade.orderStatus.filled), "shares at", trade.orderStatus.avgFillPrice)
        return round(trade.orderStatus.filled)
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(1)
        print(trade.orderStatus.status)
        break
    bid = round(bid + step, 2)
  print("Couldn't buy low.")
  return None
  
def find_ask_limit(stock, bid, ask, quantity):
  stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
  print("Asking down from ask of", ask, "in steps of", step)
  while True:
    order = LimitOrder('SELL', quantity, ask)
    trade = ib.placeOrder(stock, order)
    counter = 0 
    while counter < 10:
      ib.sleep(1)
      print("Desired price at", ask, trade.orderStatus.status)
      counter += 1
      if trade.orderStatus.status == 'Filled':
        print("sold", trade.orderStatus.filled, "shares at", trade.orderStatus.avgFillPrice)
        return None
    trade = ib.cancelOrder(order)
    while True:
      if trade.orderStatus.status != 'Cancelled':
        ib.sleep(1)
        print(trade.orderStatus.status)
        break
    ask = round(ask - step, 2)


ib = IB()
clientId = 1
ib.connect('127.0.0.1', 7497, clientId=1)

completed_order = None
while completed_order == None:
  bid, ask, spread = get_bid_ask(target)
  completed_order = find_bid_limit(target, bid, ask, spread)

find_ask_limit(target, bid, ask, completed_order)