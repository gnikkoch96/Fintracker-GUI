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
    return coin[configs.COINGECKO_SYMBOL_TEXT].upper()


def get_name(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_NAME_TEXT].upper()


def get_hashing_algorithm(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_HASHINGALGO_TEXT]


def get_categories(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_CATEGORIES_TEXT]


def get_description(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_DESC_TEXT][configs.COINGECKO_ENGLISH_TEXT]


def get_current_price(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA_TEXT][configs.COINGECKO_CURRENTPRICE_TEXT][configs.COINGECKO_USD_TEXT]


def get_circulating_supply(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA_TEXT][configs.COINGECKO_CIRCULATINGSUPPLY_TEXT]


def get_total_supply(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA_TEXT][configs.COINGECKO_TOTALSUPPLY_TEXT]


def get_market_cap(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA_TEXT][configs.COINGECKO_MARKETCAP_TEXT][configs.COINGECKO_USD_TEXT]

def get_price_change_percentage_24h(ticker):
    coin = coin_gecko.get_coin_by_id(id=ticker)
    return coin[configs.COINGECKO_MARKETDATA_TEXT][configs.COINGECKO_PRICECHANGEPERCENT24H_TEXT]