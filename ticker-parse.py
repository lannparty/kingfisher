import ast

ticker_details_string = open('data/ticker_details.txt', 'r').read()
ticker_details_map = ast.literal_eval(ticker_details_string)

for i in ticker_details_map:
  if "bid" in ticker_details_map[i] and "ask" in ticker_details_map[i] and "averageVolume" in ticker_details_map[i]:
    print(i, ticker_details_map[i]["bid"], ticker_details_map[i]["ask"], round((ticker_details_map[i]["ask"] - ticker_details_map[i]["bid"]), 2), ticker_details_map[i]["averageVolume"])
