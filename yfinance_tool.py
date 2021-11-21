import yfinance as yf
import configs


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    print(type(stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE]))

    if stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None:
        return 0

    return stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE]

def get_options_date(ticker):
    pass