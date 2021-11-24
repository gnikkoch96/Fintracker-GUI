import yfinance as yf
import configs


def validate_ticker(ticker):
    stock = yf.Ticker(ticker)

    # if it doesn't have a regularmarketprice then it is invalid (all stocks do)
    return stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
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
        return stock_options[0]
    else:  # puts
        return stock_options[1]


def validate_ticker(ticker):
    stock = yf.Ticker(ticker)

    if stock.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None:
        return False

    return True


def get_long_business_summary(ticker):
    stock = yf.Ticker(ticker)
    return stock.get_info()[configs.YFINANCE_LONGBUSINESSSUMMARY_TEXT]


def get_shares_short(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHARESHORT_TEXT])


def get_shares_short_prior_month(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHARESHORTPRIORMONTH_TEXT])


def get_short_percent_float(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_SHORTPERCENTFLOAT_TEXT])


def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return str(stock.get_info()[configs.YFINANCE_MARKETCAP_TEXT])


def get_major_holders(ticker):
    stock = yf.Ticker(ticker)
    return stock.major_holders


def get_institutional_holders(ticker):
    stock = yf.Ticker(ticker)
    return stock.institutional_holders
