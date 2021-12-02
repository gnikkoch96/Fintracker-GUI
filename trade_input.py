import configs
import yfinance_tool as yft
import cngko_tool as cgt
import firebase_conn
import threading
from search_options import Options
from ticker_search_info import CryptoStockInfo
from datetime import date


class InputTrade:
    def __init__(self, dpg, user_id, fintracker):
        self.dpg = dpg
        self.user_id = user_id
        self.fintracker = fintracker

        # default will be on Crypto
        self.investment_types = [configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT,
                                 configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT,
                                 configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT]
        self.investment_type = configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT

        # stores option obj for contract reference
        self.option = None

        # threading to make gui responsive
        self.ticker_search_thread = None

        self.create_trade_input_win()

    def create_trade_input_win(self):
        # trade input window
        with self.dpg.window(tag=configs.TRADE_INPUT_WINDOW_ID,
                             label=configs.TRADE_INPUT_WINDOW_TEXT,
                             width=configs.TRADE_INPUT_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.TRADE_INPUT_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup_alias,
                             no_resize=True):
            self.create_trade_input_win_items()

    def create_trade_input_win_items(self):
        # radio buttons - type of investment (i.e. crypto, stocks, options)
        self.dpg.add_radio_button(tag=configs.TRADE_INPUT_RADIO_BTNS_ID,
                                  items=self.investment_types,
                                  horizontal=True,
                                  callback=self.define_investment_type)

        # depending on the radio button choice, it will load a specific child window
        with self.dpg.child_window(tag=configs.TRADE_INPUT_INFO_WINDOW_ID,
                                   width=configs.TRADE_INPUT_INFO_WINDOW_VIEWPORT_SIZE[0],
                                   height=configs.TRADE_INPUT_INFO_WINDOW_VIEWPORT_SIZE[1],
                                   parent=configs.TRADE_INPUT_WINDOW_ID):
            self.create_add_trade_info_items()

        # add trade button
        self.dpg.add_button(tag=configs.TRADE_INPUT_ADD_BTN_ID,
                            label=configs.TRADE_INPUT_ADD_BTN_TEXT,
                            callback=self.add_callback)

    def create_add_trade_info_items(self):
        # ticker input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID,
                                    hint=configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT,
                                    width=configs.TRADE_INPUT_INFO_WINDOW_TICKER_WIDTH)
            self.dpg.add_button(tag=configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID,
                                label=configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_TEXT,
                                callback=self.search_callback)

        # options input (hidden in the beginning)
        with self.dpg.group(horizontal=True):
            # choose contract btn
            self.dpg.add_button(tag=configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID,
                                label=configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_TEXT,
                                callback=self.contract_callback)

            # displays contract
            self.dpg.add_text(tag=configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

        # count input
        # todo add hints
        self.dpg.add_input_int(tag=configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)

        # bought_price input
        # todo add hints
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_float(tag=configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)

            # current price button
            self.dpg.add_button(tag=configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID,
                                label=configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT,
                                callback=self.current_price_callback)

        # reason input
        self.dpg.add_input_text(tag=configs.TRADE_INPUT_INFO_WINDOW_REASON_ID,
                                hint=configs.TRADE_INPUT_INFO_WINDOW_REASON_TEXT)

        self.hide_option_items()

    def current_price_callback(self):
        if not self.is_ticker_empty():
            ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
            curr_price = 0

            # get stock price
            if self.investment_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT:
                if yft.validate_ticker(ticker):
                    curr_price = yft.get_stock_price(ticker)
                else:
                    # todo display an error message
                    pass
            else:  # get crypto price
                if cgt.validate_coin(ticker):
                    curr_price = cgt.get_current_price(ticker)
                else:
                    # todo display an error message
                    pass

            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID, curr_price)

        else:
            # todo add a dialogue
            print("Error: Ticker is Empty, cannot load current price")

    def add_callback(self):
        if self.validate_inputs():
            bought_price = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)
            count = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)
            invest_type = self.investment_type.upper()
            date_val = str(date.today())
            reason = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_REASON_ID).capitalize()

            # stock and crypto
            if not self.is_option():
                ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID).upper()

                # round price of bought price for stock
                if self.is_stock():
                    bought_price = round(bought_price, 2)

                # store the symbol of crypto as opposed to their name
                if self.is_crypto():
                    ticker = cgt.get_symbol(ticker.lower())

                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_TICKER: ticker,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_REASON: reason
                        }

                firebase_conn.add_open_trade_db(self.user_id, data, False)
                self.update_to_open_table(data, False)

            # options
            else:
                # get contract
                contract = self.option.contract
                contract_format = f"{contract[configs.OPTIONS_EXPIRATION_DATE]} | {contract[configs.OPTIONS_TICKER]} | {contract[configs.OPTIONS_TYPE]} | {contract[configs.OPTIONS_STRIKE_PRICE]} "

                # round contract price if necessary
                bought_price = round(bought_price, 2)

                # trade data
                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_CONTRACT: contract_format,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_REASON: reason
                        }

                firebase_conn.add_open_trade_db(self.user_id, data, True)
                self.update_to_open_table(data, True)

            # todo make this message a dialog to the player
            print("Successfully added to database")

            # reset the input fields
            self.reset_ticker_info_win_items()

    # choose the options contract
    def contract_callback(self):
        self.option = Options(self.dpg, configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

    def search_callback(self):
        self.ticker_search_thread = threading.Thread(target=self.load_stock_info,
                                                     daemon=True)
        self.ticker_search_thread.start()

    def load_stock_info(self):
        # todo this is where we will call the respective api to get the information
        ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)

        # todo think about putting this in a separate method
        if not self.is_ticker_empty():
            if self.is_crypto():
                if cgt.validate_coin(ticker.lower()):
                    CryptoStockInfo(self.dpg, ticker, True)
                else:
                    print("Error: Invalid Token")
            elif self.is_stock():
                if yft.validate_ticker(ticker):
                    CryptoStockInfo(self.dpg, ticker)
                else:
                    print("Error: Invalid Ticker")
        else:
            print("Error: Ticker field is empty")

    # add trade to open trades table
    def update_to_open_table(self, data, is_option):
        if is_option:  # update to options table
            table_id = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        else:  # update to crypto/stock table
            table_id = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID

        self.fintracker.add_to_open_table(table_id, data, is_option)

    def validate_inputs(self):
        if not self.is_option():
            ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)

            if self.is_stock():
                # ticker is empty or did not return a result
                invalid_ticker = not yft.validate_ticker(ticker) or self.is_ticker_empty()

            else:  # crypto
                # ticker is empty or did not return a result
                invalid_ticker = not cgt.validate_coin(ticker) or self.is_ticker_empty()
        else:
            # they did not choose a contract
            invalid_ticker = self.is_contract_empty()

        # no negative or 0 count values and no negative bought price values
        invalid_count = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID) <= 0

        # no negative bought price values
        invalid_bought_price = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID) <= 0

        if invalid_count or invalid_bought_price or invalid_ticker:
            if invalid_ticker:
                # todo display an error message (mention the rules for each radio button)
                print("Error: Invalid Ticker (It has to be the ticker name and not the full name)")

            if invalid_count:
                # todo display an error message
                print("Error: You can't have negative or 0 for count")

            if invalid_bought_price:
                # todo display an error message
                print("Error: You can't have negative or 0 for bought price")

            return False

        return True

    # defines the investment type depending on current radio button
    def define_investment_type(self, sender, app_data, user_data):
        self.reset_ticker_info_win_items()
        self.investment_type = app_data

        self.display_correct_investment_type_items()

    # display corresponding items depending on investment type
    def display_correct_investment_type_items(self):
        if self.investment_type == configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT:
            # hide: ticker input, search, current price
            # show: contract btn, show contract text
            self.hide_stock_crypto_items()
            self.show_option_items()
        else:
            # hide: contract btn, show contract text
            # show: ticker input, search, current price
            self.hide_option_items()
            self.show_stock_crypto_items()

    def hide_stock_crypto_items(self):
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID)

    def show_stock_crypto_items(self):
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)

    def hide_option_items(self):
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID)
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

    def show_option_items(self):
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

    # checks if user highlights option radio button
    def is_option(self):
        return self.investment_type == configs.TRADE_INPUT_RADIO_BTN_OPTION_TEXT

    # checks if user highlights stock radio button
    def is_stock(self):
        return self.investment_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT

    # checks if user highlights crypto radio button
    def is_crypto(self):
        return self.investment_type == configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT

    # checks if ticker input is empty
    def is_ticker_empty(self):
        return self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID) == ""

    # checks if the show contract field is empty
    def is_contract_empty(self):
        return self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID) == ""

    # clears the input fields
    def reset_ticker_info_win_items(self):
        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID):
            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID, "")

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID):
            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID, 0)

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID):
            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID, 0)

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_REASON_ID):
            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_REASON_ID, "")

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID):
            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID, "")

    # cleanup alias usage - might be fixed in next update (1.1.1)
    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID):
            self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID):
            self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID)

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID):
            self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_WINDOW_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_RADIO_BTNS_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_REASON_ID)
