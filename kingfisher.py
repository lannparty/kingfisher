from ib_insync import *
from transitions import Machine
from yahooquery import Ticker

class Merchant(object):
    def __init__(self, target, quantity, price_step, fraction_of_spread, wait_for_fill):
        self.target = target
        self.quantity = quantity
        self.price_step = price_step
        self.fraction_of_spread = fraction_of_spread
        self.wait_for_fill = wait_for_fill

        self.order = None

        self.stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
        self.reset()

    def reset(self):
        self.buy_quantity = self.quantity
        self.sell_quantity = self.quantity
    
    def scout(self):
        ticker = Ticker(self.target, validate=True)
        ticker_details = ticker.summary_detail
        self.bid = ticker_details[self.target].get("bid")
        self.ask = ticker_details[self.target].get("ask")
        self.spread = round((self.ask - self.bid), 2)
    
    def buy_low(self):
        max_price = round(self.bid + (self.spread * self.fraction_of_spread), 2)
        print("Bidding up from bid of", self.bid, "to max price of", max_price, "in steps of", self.price_step, "with buy quantity of", self.buy_quantity)

        if self.order == None:
            trade = ib.placeOrder(self.stock, LimitOrder('BUY', self.buy_quantity, self.bid))
            ib.sleep(1)
            self.order = trade.order
        else:
            self.order.lmtPrice = self.bid
            trade = ib.placeOrder(self.stock, self.order)

        while self.bid < max_price:
            timer = 0
            while timer < self.wait_for_fill:
                ib.sleep(1)
                print("Submitted price:", self.bid, "status:", trade.orderStatus.status)
                timer += 1
            if trade.orderStatus.remaining == 0:
                self.buy_quantity = trade.orderStatus.remaining
                self.order = None
                return trade.orderStatus.remaining
            else:
                self.bid = round(self.bid + self.price_step, 2)
                self.order.lmtPrice = self.bid
                trade = ib.placeOrder(self.stock, self.order)
        self.buy_quantity = trade.orderStatus.remaining
        return trade.orderStatus.remaining
    
    def sell_high(self):
        min_price = round(self.ask - (self.spread * self.fraction_of_spread), 2)
        print("Asking down from ask of", self.ask, "to min price of", min_price, "in steps of", self.price_step, "with buy quantity of", self.quantity)
        
        if self.order == None:
            trade = ib.placeOrder(self.stock, LimitOrder('SELL', self.quantity, self.ask))
            ib.sleep(1)
            order = trade.order
        else:
            self.order.lmtPrice = self.bid
            trade = ib.placeOrder(self.stock, self.order)

        while self.ask > min_price:
            timer = 0
            while timer < self.wait_for_fill:
                ib.sleep(1)
                print("Submitted price:", self.ask, "status:", trade.orderStatus.status)
                timer += 1
            if trade.orderStatus.remaining == 0:
                self.sell_quantity = trade.orderStatus.remaining
                self.order = None
                return trade.orderStatus.remaining
            else:
                self.ask = round(self.ask - self.price_step, 2)
                order.lmtPrice = self.ask
                trade = ib.placeOrder(self.stock, order)
        self.sell_quantity = trade.orderStatus.remaining
        return trade.orderStatus.remaining

ib = IB()
clientId = 1
ib.connect('127.0.0.1', 7497, clientId=1)
anfortas = Merchant(target="USLM", quantity=5, price_step=.05, fraction_of_spread=.35, wait_for_fill=30)

machine = Machine(anfortas, ['content', 'greedy', 'fearful'], initial='content')
machine.add_transition('buy', 'content', 'greedy', before='scout', after='buy_low')
machine.add_transition('buy', 'greedy', 'greedy', before='scout', after='buy_low')
machine.add_transition('sell', 'greedy', 'fearful', before='scout', after='sell_high')
machine.add_transition('sell', 'fearful', 'fearful', before='scout', after='sell_high')
machine.add_transition('sleep', 'fearful', 'content', before='reset')  

anfortas.buy()
while USLM.buy_quantity > 0:
    USLM.buy()

anfortas.sell()
while USLM.sell_quantity > 0:
    USLM.sell()
    
anfortas.sleep()
