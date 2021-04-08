import pathlib
import json
import sys

from yahooquery import Ticker


def get_symbols():
    stocks_json = pathlib.Path(__file__).parent / "data" / "stocks.json"
    symbols = []
    with open(stocks_json, "r") as f:
        stocks = json.load(f)
        for stock in stocks["data"]["rows"]:
            symbol = stock["symbol"]
            if symbol.isalpha():
                symbols.append(symbol)
    return symbols


def get_bid_ask(symbols: list):
    ticker = Ticker(symbols, validate=True, progress=True)
    ticker_details = ticker.summary_detail
    spreads = []
    for symbol in symbols:
        try:
            bid = ticker_details[symbol].get("bid")
            ask = ticker_details[symbol].get("ask")
            volume = ticker_details[symbol].get("volume")
            if bid and ask:
                spread = round(ask - bid, 2)
                print(f"{symbol} {spread}", file=sys.stderr)
                spreads.append((symbol, bid, ask, spread, volume))
            else:
                continue
        except Exception as e:
            print(f"{symbol} - Error {e}", file=sys.stderr)
            continue
    return spreads


if __name__ == "__main__":
    symbols = get_symbols()
    print(symbols)
    spreads = get_bid_ask(symbols)
    spreads.sort(key=lambda i: i[3])
    for spread in spreads:
        print(spread)
