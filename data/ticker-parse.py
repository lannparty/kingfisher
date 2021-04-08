import ast

ticker_details_string = open('raw/ticker_details.txt', 'r').read()
ticker_details_map = ast.literal_eval(ticker_details_string)

for i in ticker_details_map:
  if "bid" in ticker_details_map[i] and "ask" in ticker_details_map[i] and "averageVolume" in ticker_details_map[i]:
    bid = ticker_details_map[i]["bid"]
    ask = ticker_details_map[i]["ask"]
    spread = round((ask - bid), 2)
    volume = ticker_details_map[i]["averageVolume"]
    if bid < 200 and bid > 50 and spread > .5 and volume > 10000:
      print(i, bid, ask, spread, volume)
