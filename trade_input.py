import configs
import yfinance_tool as yft
import cngko_tool as cgt
import firebase_conn
import threading
import validations
from search_options import Options
from ticker_search_info import CryptoStockInfo
from datetime import date
from dialog_win import DialogWin


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
                             pos=configs.TRADE_INPUT_WINDOW_POS_VALUE,
                             on_close=self.cleanup_alias,
                             no_resize=True):
            self.create_trade_input_win_items()
            self.apply_theme()

    def apply_theme(self):
        self.dpg.bind_item_theme(configs.TRADE_INPUT_WINDOW_ID, configs.TRADE_INPUT_THEME_ID)

    def create_trade_input_win_items(self):
        # radio buttons - type of investment (i.e. crypto, stocks, options)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.TRADE_INPUT_RADIO_BTN_SPACERX)
            self.dpg.add_radio_button(tag=configs.TRADE_INPUT_RADIO_BTNS_ID,
                                      items=self.investment_types,
                                      horizontal=True,
                                      callback=self.define_investment_type)

        # add trade info
        self.create_add_trade_info_win()

        # add trade button
        self.dpg.add_spacer(width=configs.TRADE_INPUT_ADD_BTN_SPACERY)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.TRADE_INPUT_ADD_BTN_SPACERX)
            self.dpg.add_button(tag=configs.TRADE_INPUT_ADD_BTN_ID,
                                label=configs.TRADE_INPUT_ADD_BTN_TEXT,
                                callback=self.add_callback)

    def create_add_trade_info_win(self):
        with self.dpg.child_window(tag=configs.TRADE_INPUT_INFO_WINDOW_ID,
                                   width=configs.TRADE_INPUT_INFO_WINDOW_VIEWPORT_SIZE[0],
                                   height=configs.TRADE_INPUT_INFO_WINDOW_VIEWPORT_SIZE[1],
                                   parent=configs.TRADE_INPUT_WINDOW_ID):
            self.create_add_trade_info_win_items()

    def create_add_trade_info_win_items(self):
        self.dpg.add_spacer(height=configs.TRADE_INPUT_ADD_INFO_WIN_SPACERY)

        # ticker input
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(tag=configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT_ID,
                              default_value=configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT)
            self.dpg.add_input_text(tag=configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID,
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

        with self.dpg.group(horizontal=True):
            # count input
            self.dpg.add_text(configs.TRADE_INPUT_INFO_WINDOW_COUNT_TEXT)
            self.dpg.add_input_int(tag=configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)

        with self.dpg.group(horizontal=True):
            # bought_price input
            self.dpg.add_text(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_TEXT)
            self.dpg.add_input_float(tag=configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)

            # current price button
            self.dpg.add_button(tag=configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID,
                                label=configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT,
                                callback=self.current_price_callback)

        # reason input
        self.dpg.add_spacer(height=configs.TRADE_INPUT_REASON_INPT_SPACERY)
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.TRADE_INPUT_INFO_WINDOW_REASON_TEXT)
            self.dpg.add_input_text(tag=configs.TRADE_INPUT_INFO_WINDOW_REASON_ID,
                                    multiline=True)

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
                    DialogWin(self.dpg, configs.TRADE_INPUT_CURRENT_PRICE_FAIL_MSG, self)

            else:  # get crypto price
                if cgt.validate_coin(ticker):
                    curr_price = cgt.get_current_price(ticker)
                else:
                    DialogWin(self.dpg, configs.TRADE_INPUT_CURRENT_PRICE_FAIL_MSG, self)

            self.dpg.set_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID, curr_price)

        else:
            DialogWin(self.dpg, configs.TRADE_INPUT_CURRENT_PRICE_EMPTY_FAIL_MSG, self)


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

                # edit: removed because it was causing issues when editing the crypto trades
                # due to the api using full names as opposed to their symbol
                # store the symbol of crypto as opposed to their name
                # if self.is_crypto():
                #     ticker = cgt.get_symbol(ticker.lower())

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

            # success add message
            DialogWin(self.dpg, configs.TRADE_INPUT_SUCCESS_ADD_MSG_TEXT, self)

            # reset the input fields
            self.reset_ticker_info_win_items()

    # choose the options contract
    def contract_callback(self):
        # todo focus back on the choose contract win if present

        self.dpg.disable_item(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID)

        self.option = Options(self.dpg, configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)

    def search_callback(self):
        self.ticker_search_thread = threading.Thread(target=self.load_stock_info,
                                                     daemon=True)
        self.ticker_search_thread.start()

    def load_stock_info(self):
        ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)

        # todo think about putting this in a separate method
        if not self.is_ticker_empty():
            if self.is_crypto():
                if cgt.validate_coin(ticker.lower()):
                    CryptoStockInfo(self.dpg, ticker, True)
                else:
                    # invalid token msg
                    DialogWin(self.dpg, configs.TRADE_INPUT_INVALID_TOKEN_MSG_TEXT, self)
            elif self.is_stock():
                if yft.validate_ticker(ticker):
                    CryptoStockInfo(self.dpg, ticker)
                else:
                    # invalid ticker msg
                    DialogWin(self.dpg, configs.TRADE_INPUT_INVALID_TICKER_MSG_TEXT, self)

        else:
            # empty input msg
            DialogWin(self.dpg, configs.TRADE_INPUT_TICKER_INPUT_EMPTY_MSG_TEXT, self)

    # add trade to open trades table
    def update_to_open_table(self, data, is_option):
        if is_option:  # update to options table
            table_id = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        else:  # update to crypto/stock table
            table_id = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID

        self.fintracker.add_to_open_table(table_id, data, is_option)

    def validate_inputs(self):
        ticker = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        contract = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID)
        count = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)
        bought_price = self.dpg.get_value(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)

        check_ticker = validations.validate_trade_ticker(ticker, self.investment_type, self.is_option())
        check_contract_empty = validations.is_contract_empty(contract, self.is_option())
        check_count = validations.validate_count(count)
        check_bought_price = validations.validate_bought_price(bought_price)

        # 0 - True or False
        # 1 - Error Message
        if not check_ticker[0] or not check_contract_empty[0] or not check_count[0] or not check_bought_price[0]:
            message = "[ERROR]\n"

            # invalid ticker
            if not check_ticker[0]:
                message += check_ticker[1]

            # empty contract
            if not check_contract_empty[0]:
                message += check_contract_empty[1]

            # invalid count
            if not check_count[0]:
                message += check_count[1]

            # invalid bought_price
            if not check_bought_price[0]:
                message += check_bought_price[1]

            # error message
            DialogWin(self.dpg, message, self)
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
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT_ID)
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.hide_item(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID)

    def show_stock_crypto_items(self):
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.show_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT_ID)

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

        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT_ID):
            self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_TICKER_TEXT_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_ID)
            self.option.cleanup_alias()

        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_WINDOW_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_RADIO_BTNS_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_COUNT_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID)
        self.dpg.remove_alias(configs.TRADE_INPUT_INFO_WINDOW_REASON_ID)
