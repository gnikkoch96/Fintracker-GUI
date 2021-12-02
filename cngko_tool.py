import configs
from pycoingecko import CoinGeckoAPI

coin_gecko = CoinGeckoAPI()


def validate_coin(ticker):
    try:
        coin_gecko.get_coin_by_id(id=ticker)
        return True
    except:
        return False


def get_symbol(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_SYMBOL].upper()


def get_name(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_NAME].upper()


def get_hashing_algorithm(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_HASHINGALGO]


def get_categories(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_CATEGORIES]


def get_description(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_DESC][configs.COINGECKO_ENGLISH]


def get_current_price(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
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
