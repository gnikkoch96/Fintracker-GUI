from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

print(cg.get_coin_ticker_by_id(id="tron"))



# print(coin['symbol'], coin['name'], coin['hashing_algorithm'], coin['categories'], coin['description']['en'], coin['market_data']['current_price']['usd'],
#       coin['market_data']['circulating_supply'], coin['market_data']['total_supply'], coin['market_data']['market_cap']['usd'])
