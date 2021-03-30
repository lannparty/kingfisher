from ib_insync import *
util.startLoop()
from yahooquery import Ticker
import sys

ticker = 'USLM'
buy_quantity = 5
step = .05
fraction_of_spread = .4
wait_for_fill = 30
extended_time = 600

def get_bid_ask(symbol):
    ticker = Ticker(symbol, validate=True)
    ticker_details = ticker.summary_detail
    bid = ticker_details[symbol].get("bid")
    ask = ticker_details[symbol].get("ask")
    spread = round((ask - bid), 2)
    print("bid", bid, "ask", ask, "spread", spread)
    return bid, ask, spread

def find_bid_limit(stock, bid, ask, spread):
  stock = Contract(symbol=ticker, exchange='SMART', secType='STK', currency='USD')
  max_price = round(bid + (spread * fraction_of_spread), 2)
  print("Bidding up from bid of", bid, "to max price of", max_price, "in steps of", step, "with buy quantity of", buy_quantity)
  while bid < max_price:
    order = LimitOrder('BUY', buy_quantity, bid)
    trade = ib.placeOrder(stock, order)
    timer = 0 
    while timer < wait_for_fill:
      ib.sleep(1)
      print("Desired price at", bid, trade.orderStatus.status)
      timer += 1
      if trade.orderStatus.status == 'Filled':
        print("bought", round(trade.orderStatus.filled), "shares at", trade.orderStatus.avgFillPrice)
        if trade.orderStatus.remaining != 0:
          print("Still remaining buy orders to be filled.")
          extended_timer = 0
          while extended_timer < extended_time or trade.orderStatus.remaining == 0:
            ib.sleep(1)
            print("Remaining buy:", trade.orderStatus.remaining)
            extended_timer += 1
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
  
def find_ask_limit(stock, bid, ask, spread, sell_quantity):
  stock = Contract(symbol=ticker, exchange='SMART', secType='STK', currency='USD')
  min_price = round(ask - (spread * fraction_of_spread), 2)
  print("Asking down from ask of", ask, "in steps of", step, "on sell quantity of", sell_quantity)
  while ask > min_price:
    order = LimitOrder('SELL', sell_quantity, ask)
    trade = ib.placeOrder(stock, order)
    timer = 0 
    while timer < wait_for_fill:
      ib.sleep(1)
      print("Desired price at", ask, trade.orderStatus.status)
      timer += 1
      if trade.orderStatus.status == 'Filled':
        print("sold", trade.orderStatus.filled, "shares at", trade.orderStatus.avgFillPrice)
        if trade.orderStatus.remaining != 0:
          print("Still remaining sell orders to be filled.")
          extended_timer = 0
          while extended_timer < extended_time or trade.orderStatus.remaining == 0:
            ib.sleep(1)
            print("Remaining sell:", trade.orderStatus.remaining)
            extended_timer += 1
        return round(trade.orderStatus.remaining)
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

completed_buy_order = None
while completed_buy_order == None:
  bid, ask, spread = get_bid_ask(ticker)
  completed_buy_order = find_bid_limit(ticker, bid, ask, spread)

remaining_sell_order = find_ask_limit(ticker, bid, ask, spread, completed_buy_order)
while remaining_sell_order != 0:
  bid, ask, spread = get_bid_ask(ticker)
  remaining_sell_orders = find_ask_limit(ticker, bid, ask, spread, remaining_sell_order)