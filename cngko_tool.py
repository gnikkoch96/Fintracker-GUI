import configs
from pycoingecko import CoinGeckoAPI
from requests.exceptions import ConnectionError

# connect to coin gecko api
coin_gecko = CoinGeckoAPI()


# validates the token's ticker input
def validate_coin(ticker):
    try:
        # empty ticker (coin gecko sets search to bitcoin for empty strings)
        if ticker == "":
            return False

        coin_gecko.get_coin_by_id(id=ticker.lower())
        return True

    except ValueError:
        return False
    
    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the simplified name for the coin (i.e Bitcoin -> BTC)
def get_symbol(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_SYMBOL].upper()

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the full name of the coin (i.e. Bitcoin, Etherium)
def get_name(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_NAME].upper()

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the hashing algorithm the coin uses (i.e. Proof of Stake)
def get_hashing_algorithm(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_HASHINGALGO]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the description of the token
def get_description(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_DESC][configs.COINGECKO_ENGLISH]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the current market price the coin is going for
def get_current_price(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker.lower())
        return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_CURRENTPRICE][configs.COINGECKO_USD]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the number of coins currently in the pool
def get_circulating_supply(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_CIRCULATINGSUPPLY]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the number of possible coins that exist
def get_total_supply(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_TOTALSUPPLY]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the market cap of the token (i.e. coin price * circ supply)
def get_market_cap(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_MARKETCAP][configs.COINGECKO_USD]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT


# returns the price change of the token within the 24 hour range
def get_price_change_percentage_24h(ticker):
    try:
        coin = coin_gecko.get_coin_by_id(id=ticker)
        return coin[configs.COINGECKO_MARKETDATA][configs.COINGECKO_PRICECHANGEPERCENT24H]

    except ConnectionError:
        return configs.CONNECTION_ERROR_TEXT
