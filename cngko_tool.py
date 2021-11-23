from pycoingecko import CoinGeckoAPI


coin_gecko = CoinGeckoAPI()

def validate_coin(ticker):
    try:
        coin_gecko.get_coin_by_id(id=ticker)
        return True
    except:
        return False