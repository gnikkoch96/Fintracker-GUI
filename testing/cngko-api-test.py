from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
print(cg.get_price(ids='tron', vs_currencies='usd'))

coin = cg.get_coin_by_id(id='helium')

print(coin['symbol'], coin['name'], coin['hashing_algorithm'], coin['categories'], coin['description']['en'], coin['market_data']['current_price']['usd'],
      coin['market_data']['circulating_supply'], coin['market_data']['total_supply'], coin['market_data']['market_cap']['usd'])
