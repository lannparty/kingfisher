from ib_insync import *
from transitions import Machine
from yahooquery import Ticker
import logging

class Merchant(object):
    states = ['rest', 'greedy', 'fearful']

    def __init__(self, target, quantity, price_step, fraction_of_spread, wait_for_fill):
        self.target = target
        self.quantity = quantity
        self.price_step = price_step
        self.fraction_of_spread = fraction_of_spread
        self.wait_for_fill = wait_for_fill
        
        self.bought = 0
        self.sold = 0
        
        self.machine = Machine(model=self, states=Merchant.states, initial='rest')
        self.machine.add_transition('advance', 'content', 'greedy', before='scout', after='buy_low')
        self.machine.add_transition('advance', 'greedy', 'fearful', before='scout', after='sell_high')
        self.machine.add_transition('advance', 'fearful', 'content')

    def scout(self):
        ticker = Ticker(self.target, validate=True)
        ticker_details = ticker.summary_detail
        bid = ticker_details[self.target].get("bid")
        ask = ticker_details[self.target].get("ask")
        spread = round((ask - bid), 2)
        return bid, ask, spread
    
    def buy_low(self):
        bid, ask, spread = self.scout()
        order = Contract(symbol=self.target, exchange='SMART', secType='STK', currency='USD')
        max_price = round(bid + (spread * self.fraction_of_spread), 2)
        while bid < max_price:
            
        

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("transitions").setLevel(logging.INFO)

    trader = Trader(ticker="GME", quantity=1, price_step=0.1, wait_fill=30)
    trader.get_graph().draw('my_state_diagram.png', prog='dot')
    while True:
        trader.advance()
        
USLM = Merchant("USLM", 10, .05, .35, 30)
USLM.buy_low()
print(USLM.state)