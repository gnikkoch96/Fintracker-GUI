def validate_type():
    trade_type = self.dpg.get_value(configs.VIEW_TRADE_TYPE_ID).lower().capitalize()

    # has to be Crypto, Stock, or Option
    valid_type = (trade_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT or
                  trade_type == configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT)

    if not valid_type:
        return False, "Invalid Type (Crypto, Stock, or Option)\n"

    return True, ""


def validate_count():
    count = self.dpg.get_value(configs.VIEW_TRADE_COUNT_ID)

    # count should be greater than 0
    valid_count = count > 0

    if not valid_count:
        return False, "Invalid Count (Can't be below 0)\n"

    return True, ""


def validate_bought_price():
    bought_price = self.dpg.get_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID)

    # bought_price should be greater than 0
    valid_bought_price = bought_price > 0

    if not valid_bought_price:
        return False, "Invalid Count (Can't be below 0)\n"

    return True, ""


def validate_ticker():
    ticker = self.dpg.get_value(configs.VIEW_TRADE_TICKER_CONTRACT_ID)

    # ticker has to exist
    valid_ticker = yft.validate_ticker(ticker) or cgt.validate_coin(ticker.lower())

    if not valid_ticker:
        return False, "Invalid Ticker (For Crypto, type full name i.e. Bitcoin)\n"

    return True, ""  # return nothing


def validate_sold_price():
    sold_price = self.dpg.get_value(configs.VIEW_TRADE_SOLD_PRICE_ID)

    # sold price greater than 0
    valid_sold_price = sold_price > 0

    if not valid_sold_price:
        return False, "Invalid Sold Price (Can't be below 0)\n"

    return True, "" # return nothing
