import yfinance as yf
import configs


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    print(type(stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE]))

    if stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None:
        return 0

    return stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE]


def get_options_date(ticker):
    stock = yf.Ticker(ticker)
    return list(stock.options)


def get_options(ticker, contract_type, date):
    stock = yf.Ticker(ticker)
    stock_options = stock.option_chain(date)
    if contract_type == configs.OPTIONS_CALL_TEXT:
        print(stock_options[0])
    else:  # puts
        print(stock_options[1])


def validate_ticker(ticker):
    stock = yf.Ticker(ticker)

    if stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None:
        return False

    return True
