import requests
import json
import numpy
import pandas

def get_price_history_intraday(
    symbol, interval="15min", datatype="json", outputsize="full", api_key="J5BDISO0AXMODBWO"
):
    """
    Uses the TIME_SERIES_INTRADAY endpoint in alphavantage to retrieve a pandas
    dataframe of price, dividend, split, and volume history over the selected interval
    for the most recent trading day.
    """

    # default of 1min intervals and full output to ensure most recent data is included

    url = "https://www.alphavantage.co/query"
    args = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,  # 1min, 5min, 15min, 30min, or 60min
        "datatype": datatype,  # csv or json
        "outputsize": outputsize,  # compact or full
        "apikey": api_key,
        "adjusted": "false",
    }

    req = requests.get(url, params=args)
    quote_dict = json.loads(req.text)["Time Series ({})".format(interval)]

    quote_df = pandas.DataFrame.from_dict(
        quote_dict, orient="index", dtype="float"
    ).sort_index()
    quote_df.columns = [c[3:] for c in quote_df.columns]

    return quote_df


print(get_price_history_intraday("USLM").to_string())
