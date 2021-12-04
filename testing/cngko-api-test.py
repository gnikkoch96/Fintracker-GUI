from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def validate_coin(ticker):
    try:
        coin = cg.get_coin_by_id(id=ticker)
        print(coin)
        return True
    except:
        return False


print(validate_coin(""))

# print(coin['symbol'], coin['name'], coin['hashing_algorithm'], coin['categories'], coin['description']['en'],
# coin['market_data']['current_price']['usd'], coin['market_data']['circulating_supply'], coin['market_data'][
# 'total_supply'], coin['market_data']['market_cap']['usd'])
