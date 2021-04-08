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

if __name__ == "__main__":
    symbols = get_symbols()
    NASDAQ = Ticker(symbols, validate=True, progress=True)
    print(NASDAQ.summary_detail)
