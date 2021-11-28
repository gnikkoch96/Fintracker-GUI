import configs
import investment_tracker
import yfinance_tool as yft
import cngko_tool as cgt
import firebase_conn
import threading
from ticker_search_info import CryptoStockInfo
from datetime import date


class InputTrade:
    def __init__(self, dpg, user_id, fintracker_gui):
        self.dpg = dpg
        self.user_id = user_id
        self.fintracker = fintracker_gui

        self.investment_types = [configs.TICKER_RADIO_BTN_CRYPTO_TEXT,
                                 configs.TICKER_RADIO_BTN_STOCK_TEXT,
                                 configs.TICKER_RADIO_BTN_OPTION_TEXT]
        # default will be on Crypto
        self.investment_type = configs.TICKER_RADIO_BTN_CRYPTO_TEXT
        self.option = None

        # threading to make gui responsive
        self.ticker_search_thread = None

        self.create_ticker_search_win()

    def create_ticker_search_win(self):
        with self.dpg.window(tag=configs.TICKER_WINDOW_ID,
                             label=configs.TICKER_WINDOW_TEXT,
                             width=configs.TICKER_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.TICKER_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup_alias,
                             no_resize=True):
            self.create_ticker_search_items()

    def create_ticker_search_items(self):
        # type of investment (i.e. crypto, stocks, options)
        self.dpg.add_radio_button(tag=configs.TICKER_RADIO_BTNS_ID,
                                  items=self.investment_types,
                                  horizontal=True,
                                  callback=self.define_investment_type)

        # depending on the radio button choice, it will load a specific child window
        with self.dpg.child_window(tag=configs.TICKER_INFO_WINDOW_ID,
                                   width=configs.TICKER_INFO_WINDOW_VIEWPORT_SIZE[0],
                                   height=configs.TICKER_INFO_WINDOW_VIEWPORT_SIZE[1],
                                   parent=configs.TICKER_WINDOW_ID):
            self.create_add_investment_info_items()

        # add button
        self.dpg.add_button(tag=configs.TICKER_ADD_BTN_ID,
                            label=configs.ADD_BTN_TEXT,
                            callback=self.add_callback)

    def define_investment_type(self, sender, app_data, user_data):
        self.reset_ticker_info_win_items()
        self.investment_type = app_data

        # display corresponding items depending on investment type
        if self.investment_type == configs.TICKER_RADIO_BTN_OPTION_TEXT:
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_TICKER_ID)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_SEARCH_BTN_ID)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID)

            self.dpg.show_item(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID)
            self.dpg.show_item(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)
        else:
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)

            self.dpg.show_item(configs.TICKER_INFO_WINDOW_TICKER_ID)
            self.dpg.show_item(configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID)
            self.dpg.show_item(configs.TICKER_INFO_WINDOW_SEARCH_BTN_ID)

    def create_add_investment_info_items(self):
        # enter ticker
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.TICKER_INFO_WINDOW_TICKER_ID,
                                    hint=configs.TICKER_INFO_WINDOW_TICKER_TEXT,
                                    width=self.dpg.get_viewport_width() / 4)
            self.dpg.add_button(tag=configs.TICKER_INFO_WINDOW_SEARCH_BTN_ID,
                                label=configs.SEARCH_BTN_TEXT,
                                callback=self.search_callback)

        # options
        with self.dpg.group(horizontal=True):
            self.dpg.add_button(tag=configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID,
                                label=configs.TICKER_INFO_WINDOW_CONTRACT_BTN_TEXT,
                                callback=self.contract_callback)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID)

            # show this text once the user has chosen a contract
            self.dpg.add_text(tag=configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)

        # enter count
        # todo add hints
        self.dpg.add_input_int(tag=configs.TICKER_INFO_WINDOW_COUNT_ID)

        #  enter bought price
        # todo add hints
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_float(tag=configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)

            # current price button
            self.dpg.add_button(tag=configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID,
                                label=configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT,
                                callback=self.get_current_price)

        # enter reason
        self.dpg.add_input_text(tag=configs.TICKER_INFO_WINDOW_REASON_ID,
                                hint=configs.TICKER_INFO_WINDOW_REASON_TEXT)

    def get_current_price(self):
        if self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID) != "":
            ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID)
            curr_price = 0

            if self.investment_type == configs.TICKER_RADIO_BTN_STOCK_TEXT:
                if yft.validate_ticker(ticker):
                    curr_price = yft.get_stock_price(ticker)
                else:
                    # todo display an error message
                    pass
            else:
                if cgt.validate_coin(ticker):
                    curr_price = cgt.get_current_price(ticker)
                else:
                    # todo display an error message
                    pass

            self.dpg.set_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID, curr_price)
        else:
            # todo add a dialogue
            print("Error: Ticker is Empty, cannot load current price")

    # todo cleanup this code
    def add_callback(self):
        if self.validate_inputs():
            bought_price = self.dpg.get_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)
            count = self.dpg.get_value(configs.TICKER_INFO_WINDOW_COUNT_ID)
            invest_type = self.investment_type.upper()
            date_val = str(date.today())
            reason = self.dpg.get_value(configs.TICKER_INFO_WINDOW_REASON_ID).capitalize()

            if self.investment_type != configs.TICKER_RADIO_BTN_OPTION_TEXT:
                ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID).upper()

                if self.investment_type == configs.TICKER_RADIO_BTN_STOCK_TEXT:
                    bought_price = round(bought_price, 2)

                self.update_stock_crypto_to_table(date_val, invest_type, ticker, count, bought_price)

                # store the symbol of crypto as opposed to their name
                if self.investment_type == configs.TICKER_RADIO_BTN_CRYPTO_TEXT:
                    ticker = cgt.get_symbol(ticker.lower())

                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_TICKER: ticker,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_REASON: reason
                        }
                firebase_conn.add_open_trade_db(self.user_id, data)


            else:
                # todo remove hardcode
                contract = f"{self.option.contract[0]} | {self.option.contract[1]} | {self.option.contract[2]} | {self.option.contract[3]}"

                bought_price = round(bought_price, 2)

                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_CONTRACT: contract,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_REASON: reason
                        }
                firebase_conn.add_open_trade_db(self.user_id, data, True)
                self.update_option_to_table(date_val, invest_type, contract, count, bought_price)

            # todo make this message a dialog to the player
            print("Successfully added to database")

            # reset the input fields
            self.reset_ticker_info_win_items()

    def reset_ticker_info_win_items(self):
        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_TICKER_ID):
            self.dpg.set_value(configs.TICKER_INFO_WINDOW_TICKER_ID, "")

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_COUNT_ID):
            self.dpg.set_value(configs.TICKER_INFO_WINDOW_COUNT_ID, 0)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID):
            self.dpg.set_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID, 0)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_REASON_ID):
            self.dpg.set_value(configs.TICKER_INFO_WINDOW_REASON_ID, "")

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID):
            self.dpg.set_value(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID, "")

    def update_stock_crypto_to_table(self, date_val, invest_type, ticker, count, bought_price):
        table_id = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID
        row_data = (date_val, invest_type, ticker, count, bought_price)
        self.fintracker.add_to_open_table(table_id, row_data)

    def update_option_to_table(self, date_val, invest_type, contract, count, bought_price):
        table_id = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        row_data = (date_val, invest_type, contract, count, bought_price)
        self.fintracker.add_to_open_table(table_id, row_data, True)

    def open_trade_callback(self, sender, app_data, user_data):
        print(sender, app_data, user_data)

    # choose the options contract
    def contract_callback(self):
        self.option = Options(self.dpg)

    def search_callback(self):
        self.ticker_search_thread = threading.Thread(target=self.load_stock_info,
                                                     daemon=True)
        self.ticker_search_thread.start()

    def load_stock_info(self):
        # todo this is where we will call the respective api to get the information
        ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID)

        # todo think about putting this in a separate method
        if ticker != "":
            if self.investment_type == configs.TICKER_RADIO_BTN_CRYPTO_TEXT:
                if cgt.validate_coin(ticker):
                    CryptoStockInfo(self.dpg, ticker, True)
                else:
                    print("Error: Invalid Token")
            elif self.investment_type == configs.TICKER_RADIO_BTN_STOCK_TEXT:
                if yft.validate_ticker(ticker):
                    CryptoStockInfo(self.dpg, ticker)
                else:
                    print("Error: Invalid Ticker")
        else:
            print("Error: Ticker field is empty")

    # todo cleanup: might want to move this to a tools.py or something
    def validate_inputs(self):
        # todo also make sure to validate if the ticker is crypto or stock
        if self.investment_type != configs.TICKER_RADIO_BTN_OPTION_TEXT:
            ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID)

            if self.investment_type == configs.TICKER_RADIO_BTN_STOCK_TEXT:
                # ticker is empty or did not return a result
                invalid_ticker = not yft.validate_ticker(ticker) or ticker == ""

            else:  # crypto
                # ticker is empty or did not return a result
                invalid_ticker = not cgt.validate_coin(ticker) or ticker == ""
        else:
            # they did not choose a contract
            invalid_ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID) == ""

        # no negative or 0 count values and no negative bought price values
        invalid_count = self.dpg.get_value(configs.TICKER_INFO_WINDOW_COUNT_ID) <= 0

        # no negative bought price values
        invalid_bought_price = self.dpg.get_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID) <= 0

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

    # todo this might get fixed in future updates
    def cleanup_alias(self):
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_RADIO_BTNS_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_TICKER_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_TICKER_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_COUNT_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_REASON_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)


class Options:
    def __init__(self, dpg):
        self.dpg = dpg
        self.contract = None
        self.search_options_thread = None

        self.create_options_win()

    def create_options_win(self):
        with self.dpg.window(tag=configs.OPTIONS_WINDOW_ID,
                             label=configs.OPTIONS_WINDOW_TEXT,
                             width=configs.OPTIONS_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.OPTIONS_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup_alias,
                             modal=True):
            self.create_options_items()

    def create_options_items(self):
        # ticker input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.OPTION_WINDOW_TICKER_INPUT_ID,
                                    hint=configs.OPTION_WINDOW_TICKER_INPUT_TEXT)
            self.dpg.add_button(tag=configs.OPTION_WINDOW_SEARCH_BTN_ID,
                                label=configs.SEARCH_BTN_TEXT,
                                callback=self.search_callback)

    def create_option_type_combo_list(self):
        option_types = [configs.OPTIONS_CALL_TEXT, configs.OPTIONS_PUT_TEXT]
        return option_types

    def create_option_date_combo_list(self):
        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        option_dates = yft.get_options_date(ticker)
        return option_dates

    def search_callback(self):
        self.search_options_thread = threading.Thread(target=self.load_option_combos,
                                                      daemon=True)
        self.search_options_thread.start()

    def load_option_combos(self):
        # resets the option window every search
        self.delete_option_win_items()

        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        if self.validate_input(ticker):
            with self.dpg.group(horizontal=True, parent=configs.OPTIONS_WINDOW_ID):

                # call or put combo (user chooses)
                self.dpg.add_combo(tag=configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID,
                                   items=self.create_option_type_combo_list(),
                                   width=configs.OPTIONS_WINDOW_COMBO_WIDTH,
                                   default_value=configs.OPTIONS_CALL_TEXT)

                # date combo (callback will search)
                self.dpg.add_combo(tag=configs.OPTION_WINDOW_DATE_COMBO_ID,
                                   items=self.create_option_date_combo_list(),
                                   width=configs.OPTIONS_WINDOW_COMBO_WIDTH,
                                   default_value=self.create_option_date_combo_list()[0])

                # search contract button
                self.dpg.add_button(tag=configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID,
                                    label=configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_TEXT,
                                    callback=self.load_options)
        else:
            # todo add a dialog that says invalid ticker
            print("Error: Ticker is invalid or does not support options")
            pass

    def delete_option_win_items(self):
        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_DATE_COMBO_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_DATE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID)

    def validate_input(self, ticker):
        # test to see if it is a valid ticker
        valid_ticker = yft.validate_ticker(ticker)

        # test to see if it has options
        has_options = len(self.create_option_date_combo_list()) > 0

        if not valid_ticker or not has_options:
            return False

        return True

    def load_options(self):
        # todo might put this in a separate method
        if self.dpg.does_alias_exist(configs.OPTION_TABLE_ID):
            self.dpg.delete_item(configs.OPTION_TABLE_ID)

        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        contract_type = self.dpg.get_value(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)
        date_combo = self.dpg.get_value(configs.OPTION_WINDOW_DATE_COMBO_ID)
        options_list = yft.get_options(ticker, contract_type, date_combo)

        with self.dpg.table(tag=configs.OPTION_TABLE_ID,
                            parent=configs.OPTIONS_WINDOW_ID,
                            header_row=True):
            # column headers
            self.dpg.add_table_column(label=configs.OPTION_STRIKE_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_VOLUME_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_OPEN_INTEREST_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_IV_LABEL_TEXT)

            for row in range(0, len(options_list)):
                with self.dpg.table_row():
                    with self.dpg.table_cell():
                        # strike price
                        strike_price = options_list[configs.YFINANCE_STRIKE_PRICE_TEXT][row]
                        self.dpg.add_button(label=strike_price,
                                            callback=self.row_callback,
                                            user_data=(self.dpg.get_value(configs.OPTION_WINDOW_DATE_COMBO_ID),
                                                       strike_price))

                    with self.dpg.table_cell():
                        # volume
                        volume = options_list[configs.YFINANCE_VOLUME_TEXT][row]
                        self.dpg.add_text(volume)

                    with self.dpg.table_cell():
                        # open interest
                        open_int = options_list[configs.YFINANCE_OPEN_INTEREST_TEXT][row]
                        self.dpg.add_text(open_int)

                    with self.dpg.table_cell():
                        # implied volatility
                        iv = round(options_list[configs.YFINANCE_IV_TEXT][row] * 100, 2)
                        self.dpg.add_text(iv)

    def row_callback(self, sender, app_data, user_data):
        # user_data = (date, strike)
        date_value = user_data[0]
        strike = user_data[1]
        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        option_type = self.dpg.get_value(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)

        self.contract = (date_value, ticker.upper(), option_type, strike)

        self.dpg.set_value(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID,
                           f"{date_value}, {ticker.upper()}, {option_type}, {strike}")
        self.dpg.show_item(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)

        # todo think about putting this in a method
        self.dpg.delete_item(configs.OPTIONS_WINDOW_ID)
        self.cleanup_alias()

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.OPTIONS_WINDOW_ID):
            self.dpg.remove_alias(configs.OPTIONS_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_TICKER_INPUT_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_TICKER_INPUT_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_SEARCH_BTN_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_SEARCH_BTN_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.OPTION_TABLE_ID):
            self.dpg.remove_alias(configs.OPTION_TABLE_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_DATE_COMBO_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_DATE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID)
