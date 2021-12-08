import time

import configs
import loading_win
import yfinance_tool as yft
import threading
from dialog_win import DialogWin


# desc: search options gui that will display contracts to the user based on
# ticker, call/put, and expiration date
def create_option_type_combo_list():
    option_types = [configs.OPTION_CALL_TEXT, configs.OPTION_PUT_TEXT]
    return option_types


class Options:
    # item_id refers to the dpg item that will display the contract
    def __init__(self, dpg, item_id):
        self.dpg = dpg
        self.item_id = item_id

        # used for reference from other classes (i.e. using the getter method)
        self._contract = None

        # search options thread (created to prevent waiting)
        # self.search_options_thread = None

        self.create_options_win()

    @property
    def contract(self):
        return self._contract

    @contract.setter
    def contract(self, contract_data):
        date_val = contract_data[0]
        ticker = contract_data[1]
        option_type = contract_data[2]
        strike = contract_data[3]

        self._contract = {configs.OPTIONS_EXPIRATION_DATE: date_val,
                          configs.OPTIONS_TICKER: ticker,
                          configs.OPTIONS_TYPE: option_type,
                          configs.OPTIONS_STRIKE_PRICE: strike,
                          }

    def create_options_win(self):
        # options window
        with self.dpg.window(tag=configs.OPTION_WINDOW_ID,
                             label=configs.OPTION_WINDOW_TEXT,
                             width=configs.OPTIONS_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.OPTIONS_WINDOW_VIEWPORT_SIZE[1],
                             pos=configs.OPTIONS_WINDOW_POS,
                             no_resize=True,
                             on_close=self.cleanup_alias):
            self.create_options_win_items()

    def create_options_win_items(self):
        # retrieve ticker option data
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.OPTION_WINDOW_INPUT_SEARCH_GROUP_SPACERX)

            # ticker input
            self.dpg.add_input_text(tag=configs.OPTION_WINDOW_TICKER_INPUT_ID,
                                    hint=configs.OPTION_WINDOW_TICKER_INPUT_TEXT)

            # search button
            self.dpg.add_button(tag=configs.OPTION_WINDOW_SEARCH_BTN_ID,
                                label=configs.OPTION_SEARCH_BTN_TEXT,
                                callback=self.search_callback)

    # search options thread (created to prevent waiting)
    def search_callback(self):
        threading.Thread(target=self.load_option_combos, daemon=True).start()

    # loads data to the combos (type and expiration date)
    def load_option_combos(self):
        # instead of creating another window, we can just configure it
        self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=True)

        # resets the table
        self.delete_option_win_items()

        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)

        # combos + search contract button
        if self.validate_input(ticker):
            with self.dpg.group(horizontal=True, parent=configs.OPTION_WINDOW_ID):
                self.dpg.add_spacer(width=configs.OPTION_WINDOW_COMBOS_GROUP_SPACERX)

                # call or put combo (user chooses)
                self.dpg.add_combo(tag=configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID,
                                   items=create_option_type_combo_list(),
                                   width=configs.OPTIONS_WINDOW_COMBO_WIDTH,
                                   default_value=configs.OPTION_CALL_TEXT)

                # date combo (callback will search)
                self.dpg.add_combo(tag=configs.OPTION_WINDOW_DATE_COMBO_ID,
                                   items=self.create_option_date_combo_list(),
                                   width=configs.OPTIONS_WINDOW_COMBO_WIDTH,
                                   default_value=self.create_option_date_combo_list()[0])

                # search contract button
                self.dpg.add_button(tag=configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID,
                                    label=configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_TEXT,
                                    callback=self.load_options)
                self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=False)

        else:
            self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=False)

            # todo cleanup this was a quick fix (sleeping wastes cpu cycle)
            time.sleep(0.1)

            DialogWin(self.dpg, configs.OPTION_INVALID_TICKER_MSG_TEXT, self)

    def search_contract_callback(self):
        threading.Thread(target=self.load_options(), daemon=True).start()

    # displays table listing all strike prices corresponding to call/put and expiration date
    def load_options(self):
        self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=True)

        self.delete_option_win_table()

        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        contract_type = self.dpg.get_value(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)
        date_combo = self.dpg.get_value(configs.OPTION_WINDOW_DATE_COMBO_ID)
        options_list = yft.get_options(ticker, contract_type, date_combo)

        # option table
        with self.dpg.table(tag=configs.OPTION_TABLE_ID,
                            parent=configs.OPTION_WINDOW_ID,
                            header_row=True):
            # column headers
            self.dpg.add_table_column(label=configs.OPTION_STRIKE_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_VOLUME_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_OPEN_INTEREST_LABEL_TEXT)
            self.dpg.add_table_column(label=configs.OPTION_IV_LABEL_TEXT)

            for row in range(0, len(options_list)):
                with self.dpg.table_row():
                    # strike price
                    with self.dpg.table_cell():
                        strike_price = options_list[configs.YFINANCE_STRIKE_PRICE][row]
                        self.dpg.add_button(label=strike_price,
                                            callback=self.row_callback,
                                            user_data=strike_price)
                    # volume
                    with self.dpg.table_cell():
                        volume = options_list[configs.YFINANCE_VOLUME][row]
                        self.dpg.add_text(volume)

                    # open interest
                    with self.dpg.table_cell():
                        open_int = options_list[configs.YFINANCE_OPEN_INTEREST][row]
                        self.dpg.add_text(open_int)

                    # implied volatility
                    with self.dpg.table_cell():
                        iv = round(options_list[configs.YFINANCE_IV_TEXT][row] * 100, 2)
                        self.dpg.add_text(iv)

        self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=False)

    # storing contract choice
    def row_callback(self, sender, app_data, user_data):
        # data
        date_value = self.dpg.get_value(configs.OPTION_WINDOW_DATE_COMBO_ID)
        strike_price = user_data
        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        option_type = self.dpg.get_value(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)

        # store contract
        # self._contract = (date_value, ticker.upper(), option_type, strike_price)
        contract_data = (date_value, ticker.upper(), option_type, strike_price)
        self.contract = contract_data

        # display contract information in item_id
        self.dpg.set_value(self.item_id,
                           f"{date_value} | {ticker.upper()} | {option_type} | {strike_price}")
        self.dpg.show_item(self.item_id)

        self.delete_options_win()

    # validates ticker and whether or not it contains options
    def validate_input(self, ticker):
        # must be valid ticker
        valid_ticker = yft.validate_ticker(ticker)

        # there has to be at least one option
        if valid_ticker:
            has_options = len(self.create_option_date_combo_list()) > 0

            if not has_options:
                return False

        if not valid_ticker:
            return False

        return True

    # returns a list of possible expiration dates for ticker
    def create_option_date_combo_list(self):
        ticker = self.dpg.get_value(configs.OPTION_WINDOW_TICKER_INPUT_ID)
        option_dates = yft.get_options_date(ticker)
        return option_dates

    # closes the options window
    def delete_options_win(self):
        self.dpg.delete_item(configs.OPTION_WINDOW_ID)
        self.cleanup_alias()

    # resets the option window every search
    def delete_option_win_items(self):
        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_OPTION_TYPE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_DATE_COMBO_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_DATE_COMBO_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID):
            self.dpg.delete_item(configs.OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.OPTION_TABLE_ID):
            self.dpg.delete_item(configs.OPTION_TABLE_ID)

    # deletes the options table
    def delete_option_win_table(self):
        if self.dpg.does_alias_exist(configs.OPTION_TABLE_ID):
            self.dpg.delete_item(configs.OPTION_TABLE_ID)

    # removes aliases - might get fixed in the next update
    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID):
            self.dpg.enable_item(configs.TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.OPTION_WINDOW_ID):
            self.dpg.remove_alias(configs.OPTION_WINDOW_ID)

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
