import configs
from pycoingecko import CoinGeckoAPI

coin_gecko = CoinGeckoAPI()


def validate_coin(ticker):
    # empty ticker (coin gecko sets search to bitcoin for empty strings)
    if ticker == "":
        return False

    try:
        coin_gecko.get_coin_by_id(id=ticker.lower())
        return True
    except:
        return False


# returns the simplified name for the coin (i.e Bitcoin -> BTC)
def get_symbol(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_SYMBOL].upper()


# returns the full name of the coin (i.e. Bitcoin, Etherium)
def get_name(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_NAME].upper()


# returns the hashing algorithm the coin uses (i.e. Proof of Stake)
def get_hashing_algorithm(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_HASHINGALGO]

# returns the 
def get_description(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_DESC][configs.COINGECKO_ENGLISH]


def get_current_price(ticker):
    print(ticker)
    coin = coin_gecko.get_coin_by_id(id=ticker.lower())
    return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_CURRENTPRICE][configs.COINGECKO_USD]


def get_circulating_supply(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_CIRCULATINGSUPPLY]


def get_total_supply(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_TOTALSUPPLY]


def get_market_cap(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_MARKETCAP][configs.COINGECKO_USD]


def get_price_change_percentage_24h(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_PRICECHANGEPERCENT24H]
