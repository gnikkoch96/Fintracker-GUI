import yfinance as yf
import configs


# todo cleanup (current solution to slowdown in retrieving data from yfinance api)
def retrieve_info(ticker):
    stock = yf.Ticker(ticker)

    if stock is None:
        return

    stock_info = stock.get_info()
    name = stock_info[configs.YFINANCE_SHORTNAME]
    price = stock_info[configs.YFINANCE_REGULARMARKETPRICE]
    market_cap = stock_info[configs.YFINANCE_MARKETCAP]
    shares_short = stock_info[configs.YFINANCE_SHARESHORT]
    shares_short_prior_month = stock_info[configs.YFINANCE_SHARESHORTPRIORMONTH]
    shares_short_per = stock_info[configs.YFINANCE_SHORTPERCENTFLOAT]
    bus_sum = stock_info[configs.YFINANCE_LONGBUSINESSSUMMARY]

    return name, price, market_cap, shares_short, shares_short_prior_month, shares_short_per, bus_sum


# checks if ticker exists
def validate_ticker(ticker):
    stock = yf.Ticker(ticker)

    # if it doesn't have a regular market price then it is invalid (all stocks do)
    return stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is not None


def get_stock_name(ticker):
    stock = yf.Ticker(ticker)

    # stock doesn't exist
    if stock is None:
        return

    return stock.get_info()[configs.YFINANCE_SHORTNAME]


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)

    # stock doesn't exist
    if stock is None:
        return 0

    return stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE]


def get_options_date(ticker):
    # stock doesn't exist
    if not validate_ticker(ticker):
        return

    stock = yf.Ticker(ticker)
    return list(stock.options)


def get_options(ticker, contract_type, date):
    # stock doesn't exist
    if not validate_ticker(ticker):
        return

    stock = yf.Ticker(ticker)
    stock_options = stock.option_chain(date)

    # returns call contracts
    if contract_type == configs.OPTIONS_CALL_TEXT:
        return stock_options[0]
    else:  # returns put contracts
        return stock_options[1]


def get_long_business_summary(ticker):
    stock = yf.Ticker(ticker)
    return stock.get_info()[configs.YFINANCE_LONGBUSINESSSUMMARY]


def get_shares_short(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHARESHORT])


def get_shares_short_prior_month(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHARESHORTPRIORMONTH])


def get_short_percent_float(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHORTPERCENTFLOAT])


def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_MARKETCAP])


def get_major_holders(ticker):
    stock = yf.Ticker(ticker)
    return stock.major_holders


def get_institutional_holders(ticker):
    stock = yf.Ticker(ticker)
    return stock.institutional_holders
