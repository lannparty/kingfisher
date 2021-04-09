import datetime
from ib_insync import *
from transitions import Machine
from yahooquery import Ticker
import os

class Merchant(object):
    def __init__(self, account, target, quantity, price_step, fraction_of_spread, wait_for_fill, position_reconciled):
        self.account = account
        self.target = target
        self.quantity = quantity
        self.price_step = price_step
        self.fraction_of_spread = fraction_of_spread
        self.wait_for_fill = wait_for_fill
        self.position_reconciled = position_reconciled

        self.order = None
        self.stock = Contract(symbol=target, exchange='SMART', secType='STK', currency='USD')
        self.reset()

    # Reset desired quantity back to init quantity. To ready the Merchant for a new cycle of buy and sell.
    def reset(self):
        self.buy_quantity = self.quantity
        self.sell_quantity = self.quantity

    # Refreshes bid/ask/spread.
    def get_spread(self):
        ticker = Ticker(self.target, validate=True)
        ticker_details = ticker.summary_detail
        self.bid = ticker_details[self.target].get("bid")
        self.ask = ticker_details[self.target].get("ask")
        self.spread = round((self.ask - self.bid), 2)
        if self.spread < .5:
            print("Spread on", self.target, "is less than 50 cents.")
            exit(2)

    def buy_low(self):
        max_price = round(self.bid + (self.spread * self.fraction_of_spread), 2)
        
        # If currently short and want to reconcile, buy extra to cover.
        if not self.position_reconciled:
            additional_buy = 0
            for i in ib.positions(account=self.account):
                if self.target == i.contract.symbol:
                    print("Currently own", i.position, "shares of", i.contract.symbol, "buying additional shares to reconcile")
                    if i.position < 0:
                        additional_buy = abs(i.position)
            self.buy_quantity = self.quantity + additional_buy
        self.position_reconciled = True
        print(datetime.datetime.now(), "Bidding up from bid of", self.bid, "to max price of", max_price, "in steps of", self.price_step, "with buy quantity of", self.buy_quantity)
        
        # Create new order if order has not been initialized.
        if self.order == None:
            trade = ib.placeOrder(self.stock, LimitOrder('BUY', self.buy_quantity, self.bid))
            ib.sleep(1)
            self.order = trade.order
        else:
            self.order.lmtPrice = self.bid
            trade = ib.placeOrder(self.stock, self.order)

        # Modify the order incrementing the bid until max_price is reached, then return leftover order.
        while self.bid < max_price:
            timer = 0
            while timer < self.wait_for_fill:
                ib.sleep(1)
                print(datetime.datetime.now(), "Submitted price:", self.bid, "status:", trade.orderStatus.status)
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

        # If currently own and want to reconcile, sell down to zero.
        if not self.position_reconciled:
            additional_sell = 0
            for i in ib.positions(account=self.account):
                if self.target == i.contract.symbol:
                    print("Currently own", i.position, "shares of", i.contract.symbol, "selling additional shares to reconcile")
                    if i.position > 0:
                        additional_sell = abs(i.position)
            self.sell_quantity = self.quantity + additional_sell
        self.position_reconciled = True
        print(datetime.datetime.now(), "Asking down from ask of", self.ask, "to min price of", min_price, "in steps of", self.price_step, "with sell quantity of", self.sell_quantity)
        
        # Create new order if order has not been initialized.
        if self.order == None:
            trade = ib.placeOrder(self.stock, LimitOrder('SELL', self.sell_quantity, self.ask))
            ib.sleep(1)
            self.order = trade.order
        else:
            self.order.lmtPrice = self.ask
            trade = ib.placeOrder(self.stock, self.order)

        # Modify the order incrementing the bid until max_price is reached, then return leftover order.
        while self.ask > min_price:
            timer = 0
            while timer < self.wait_for_fill:
                ib.sleep(1)
                print(datetime.datetime.now(), "Submitted price:", self.ask, "status:", trade.orderStatus.status)
                timer += 1
            if trade.orderStatus.remaining == 0:
                self.sell_quantity = trade.orderStatus.remaining
                self.order = None
                return trade.orderStatus.remaining
            else:
                self.ask = round(self.ask - self.price_step, 2)
                self.order.lmtPrice = self.ask
                trade = ib.placeOrder(self.stock, self.order)
        self.sell_quantity = trade.orderStatus.remaining
        return trade.orderStatus.remaining

target = os.getenv("KINGFISHER_TARGET")
strategy = os.getenv("KINGFISHER_STRATEGY")
quantity = int(os.getenv("KINGFISHER_QUANTITY"))
price_step = float(os.getenv("KINGFISHER_PRICE_STEP"))
fraction_of_spread = float(os.getenv("KINGFISHER_FRACTION_OF_SPREAD"))
wait_for_fill = int(os.getenv("KINGFISHER_WAIT_FOR_FILL"))
position_reconciled = bool(os.getenv("KINGFISHER_POSITION_RECONCILED"))
client_id = int(os.getenv("KINGFISHER_CLIENT_ID"))
ib_account = os.getenv("KINGFISHER_IB_ACCOUNT")
ib_host = os.getenv("KINGFISHER_IB_ADDRESS")
ib_port = int(os.getenv("KINGFISHER_IB_PORT"))
cleaning_mode = bool(os.getenv("KINGFISHER_CLEANING_MODE"))

print("target:", target)
print("strategy:", strategy)
print("quantity:", quantity)
print("price_step:", price_step)
print("fraction_of_spread:", fraction_of_spread)
print("wait_for_fill:", wait_for_fill)
print("position_reconciled:", position_reconciled)
print("client_id:", client_id)
print("ib_account:", ib_account)
print("ib_host:", ib_host)
print("ib_port:", ib_port)

ib = IB()
ib.connect(ib_host, ib_port, clientId=client_id)

anfortas = Merchant(account=ib_account, target=target, quantity=quantity, price_step=price_step, fraction_of_spread=fraction_of_spread, wait_for_fill=wait_for_fill, position_reconciled=position_reconciled)

# Declare state, transitions and prereqs.
machine = Machine(anfortas, ['content', 'greedy', 'fearful'], initial='content')

machine.add_transition('buy', 'content', 'greedy', before='get_spread', after='buy_low')
machine.add_transition('buy', 'greedy', 'greedy', before='get_spread', after='buy_low')
machine.add_transition('buy', 'fearful', 'greedy', before='get_spread', after='buy_low')

machine.add_transition('sell', 'content', 'fearful', before='get_spread', after='sell_high')
machine.add_transition('sell', 'greedy', 'fearful', before='get_spread', after='sell_high')
machine.add_transition('sell', 'fearful', 'fearful', before='get_spread', after='sell_high')

machine.add_transition('sleep', 'content', 'content', before='reset')
machine.add_transition('sleep', 'greedy', 'content', before='reset')
machine.add_transition('sleep', 'fearful', 'content', before='reset')

# For clean.sh, cancel all orders.
if cleaning_mode:
    if len(ib.reqOpenOrders()) > 0:
        for i in ib.reqOpenOrders():
            print("Canceling order:", i)
            ib.cancelOrder(i)
    exit()

if strategy == "buy_first":
    while True:
        # While there's leftover, keep buying.
        anfortas.buy()
        while anfortas.buy_quantity > 0:
            anfortas.buy()
        # While there's leftover, keep selling.
        anfortas.sell()
        while anfortas.sell_quantity > 0:
            anfortas.sell()
        # Reset quantity.
        anfortas.sleep()
elif strategy == "sell_first":
    while True:
        anfortas.sell()
        while anfortas.sell_quantity > 0:
            anfortas.sell()
        anfortas.buy()
        while anfortas.buy_quantity > 0:
            anfortas.buy()
        anfortas.sleep()
