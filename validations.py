import configs
import yfinance_tool as yft
import cngko_tool as cgt


def validate_type(trade_type):
    # has to be Crypto, Stock, or Option
    valid_type = (trade_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT)

    if not valid_type:
        return False, configs.VALIDATE_ERROR_TYPE_MSG + "\n"

    return True, ""


def validate_count(count):
    # count should be greater than 0
    valid_count = count > 0

    if not valid_count:
        return False, configs.VALIDATE_ERROR_COUNT_MSG + "\n"

    return True, ""


def validate_bought_price(bought_price):
    # bought_price has to have valid format

    # todo cleanup (quick fix)
    try:
        float(bought_price)
    except:
        return False, configs.VALIDATE_ERROR_INVALID_BOUGHT_PRICE_MSG + "\n"

    # bought_price should be greater than 0
    valid_bought_price = float(bought_price) > 0

    if not valid_bought_price:
        return False, configs.VALIDATE_ERROR_BOUGHT_PRICE_MSG + "\n"

    return True, ""


# validates the ticker depending on the invest type
def validate_ticker(ticker, invest_type):
    if invest_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT:
        valid_ticker = cgt.validate_coin(ticker.lower())

        if not valid_ticker:  # invalid crypto ticker
            return False, configs.VALIDATE_ERROR_CRYPTO_TICKER_MSG + "\n"

    elif invest_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT:
        valid_ticker = yft.validate_ticker(ticker)

        if not valid_ticker:  # invalid stock ticker
            return False, configs.VALIDATE_ERROR_STOCK_TICKER_MSG + "\n"

    return True, ""


def validate_sold_price(sold_price, for_open):
    if not for_open:
        # sold price greater than or equal to 0
        valid_sold_price = sold_price >= 0

        if not valid_sold_price:
            return False, configs.VALIDATE_ERROR_SOLD_PRICE_MSG + "\n"

    return True, ""


# checks if the show contract field is empty
def is_contract_empty(contract, is_option):
    if is_option:
        valid_contract = contract != ""

        if not valid_contract:
            return False, configs.VALIDATE_ERROR_CONTRACT_MSG + "\n"

    return True, ""
