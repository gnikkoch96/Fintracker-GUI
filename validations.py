import configs
import yfinance_tool as yft
import cngko_tool as cgt


# todo cleanup
def validate_type(trade_type):
    # has to be Crypto, Stock, or Option
    valid_type = (trade_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT)

    if not valid_type:
        return False, "Invalid Type (Crypto, Stock, or Option)\n"

    return True, ""


# todo cleanup
def validate_count(count):
    # count should be greater than 0
    valid_count = count > 0

    if not valid_count:
        return False, "Invalid Count (Can't be below 0)\n"

    return True, ""


# todo cleanup
def validate_bought_price(bought_price):
    # bought_price should be greater than 0
    valid_bought_price = bought_price > 0

    if not valid_bought_price:
        return False, "Invalid Bought Price (Can't be below 0)\n"

    return True, ""


# todo cleanup
def validate_ticker(ticker, is_option):
    if not is_option:
        # ticker has to exist
        # todo might cause a slow down as it needs to check both apis
        valid_ticker = yft.validate_ticker(ticker) or cgt.validate_coin(ticker.lower())

        if not valid_ticker:
            return False, "Invalid Ticker (For Crypto, type full name i.e. Bitcoin)\n"

    return True, ""


# todo cleanup (duplicate name method)
def validate_trade_ticker(ticker, invest_type, is_option):
    if not is_option:
        if invest_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT:
            valid_ticker = cgt.validate_coin(ticker.lower())
        else:
            valid_ticker = yft.validate_ticker(ticker)

        if not valid_ticker:
            return False, "Invalid Ticker (For Crypto, type full name i.e. Bitcoin)\n"

    return True, ""


# todo cleanup
def validate_sold_price(sold_price, for_open):
    if not for_open:
        # sold price greater than or equal to 0
        valid_sold_price = sold_price >= 0

        if not valid_sold_price:
            return False, "Invalid Sold Price (Can't be below 0)\n"

    return True, ""


# checks if the show contract field is empty
def is_contract_empty(contract, is_option):
    if is_option:
        valid_contract = contract != ""

        if not valid_contract:
            return False, "No Contract was Chosen\n"

    return True, ""
