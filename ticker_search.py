import configs
import yfinance as yf
import yfinance_tool as yft
import firebase_conn
from ticker_search_info import CryptoStockOptionInfo
from datetime import date


class TickerSearch:
    def __init__(self, dpg, user_id):
        self.dpg = dpg
        self.user_id = user_id
        self.investment_types = [configs.TICKER_RADIO_BTN_CRYPTO_TEXT,
                                 configs.TICKER_RADIO_BTN_STOCK_TEXT,
                                 configs.TICKER_RADIO_BTN_OPTION_TEXT]

        # default will be on Crypto
        self.investment_type = configs.TICKER_RADIO_BTN_CRYPTO_TEXT
        self.create_ticker_search_win()

    def create_ticker_search_win(self):
        with self.dpg.window(tag=configs.TICKER_WINDOW_ID,
                             label=configs.TICKER_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup,
                             no_resize=True):
            self.create_ticker_search_items()

    def create_ticker_search_items(self):
        # type of investment (i.e. crypto, stocks, options)
        self.dpg.add_radio_button(tag=configs.TICKER_RADIO_BTNS_ID,
                                  items=self.investment_types,
                                  horizontal=True,
                                  callback=self.define_investment_type)

        # ticker search
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.TICKER_INPUT_TICKER_ID,
                                    hint=configs.TICKER_INPUT_TICKER_TEXT)

            self.dpg.add_button(tag=configs.TICKER_SEARCH_BTN_ID,
                                label=configs.TICKER_SEARCH_BTN_TEXT,
                                callback=self.load_stock_info)

        # ticker info
        # depending on the radio button choice, it will load a specific child window
        with self.dpg.child_window(tag=configs.TICKER_INFO_WINDOW_ID,
                                   label=configs.TICKER_INFO_WINDOW_TEXT,
                                   width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2.5,
                                   height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5,
                                   parent=configs.TICKER_WINDOW_ID):
            self.create_add_investment_info_items()

        # add button
        self.dpg.add_button(tag=configs.TICKER_ADD_BTN_ID,
                            label=configs.ADD_BTN_TEXT,
                            callback=self.add_callback)

    def define_investment_type(self, sender, app_data, user_data):
        self.cleanup_ticker_info_win()
        self.investment_type = app_data

        # ticker info
        with self.dpg.child_window(tag=configs.TICKER_INFO_WINDOW_ID,
                                   label=configs.TICKER_INFO_WINDOW_TEXT,
                                   width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2.5,
                                   height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5,
                                   parent=configs.TICKER_WINDOW_ID):
            self.create_add_investment_info_items()

        # add button
        self.dpg.add_button(tag=configs.TICKER_ADD_BTN_ID,
                            label=configs.ADD_BTN_TEXT,
                            callback=self.add_callback,
                            parent=configs.TICKER_WINDOW_ID)

    def create_add_investment_info_items(self):
        # enter ticker
        # todo figure out what to do when user puts an invalid ticker
        self.dpg.add_input_text(tag=configs.TICKER_INFO_WINDOW_TICKER_ID,
                                hint=configs.TICKER_INFO_WINDOW_TICKER_TEXT)

        # if options, allow user to choose contract
        if self.investment_type == configs.TICKER_RADIO_BTN_OPTION_TEXT:
            self.dpg.add_button(tag=configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID,
                                label=configs.TICKER_INFO_WINDOW_CONTRACT_BTN_TEXT,
                                callback=self.choose_option_contract)

            # show this text once the user has chosen a contract
            self.dpg.add_text(tag=configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)
            self.dpg.hide_item(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)

        # enter count
        # todo figure out what to do when user puts a negative number
        # todo add hints
        self.dpg.add_input_int(tag=configs.TICKER_INFO_WINDOW_COUNT_ID)

        #  enter bought price
        # todo figure out what to do when user puts a negative number
        # todo add hints
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_float(tag=configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)

            # current price button
            if self.investment_type != configs.TICKER_RADIO_BTN_OPTION_TEXT:
                self.dpg.add_button(tag=configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID,
                                    label=configs.TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT,
                                    callback=self.get_current_price)

        # enter reason
        self.dpg.add_input_text(tag=configs.TICKER_INFO_WINDOW_REASON_ID,
                                hint=configs.TICKER_INFO_WINDOW_REASON_TEXT)

    def get_current_price(self):
        ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID)
        curr_price = yft.get_stock_price(ticker)
        self.dpg.set_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID, curr_price)

    # todo cleanup this code
    def add_callback(self):
        if self.validate_inputs():
            try:
                bought_price = round(self.dpg.get_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID), 2)
                count = self.dpg.get_value(configs.TICKER_INFO_WINDOW_COUNT_ID)
                ticker = self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID).upper()
                type = self.investment_type.upper()
                date_val = str(date.today())

                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_TICKER: ticker,
                        configs.FIREBASE_TYPE: type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_REASON: self.dpg.get_value(configs.TICKER_INFO_WINDOW_REASON_ID).capitalize()
                        }

                firebase_conn.add_open_trade_db(self.user_id, data)
                print("Successfully added to database")

                # update the investment tracker gui
                # todo think about making this into a table as opposed to creating buttons
                format = f"{date_val} | {ticker} | {type} | {count} | {bought_price}"
                self.dpg.add_button(label=format,
                                    parent=configs.FINTRACKER_OPEN_TRADES_ID)

                # reset the input fields
                # todo might want to put this in a separate method
                self.dpg.set_value(configs.TICKER_INFO_WINDOW_TICKER_ID, "")
                self.dpg.set_value(configs.TICKER_INFO_WINDOW_COUNT_ID, "")
                self.dpg.set_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID, "")
                self.dpg.set_value(configs.TICKER_INFO_WINDOW_REASON_ID, "")
            except:
                print("Error: Data is invalid...Could not push to database")

    def choose_option_contract(self):
        pass

    def load_stock_info(self):
        # todo this is where we will call the respective api to get the information
        CryptoStockOptionInfo(self.dpg)

    # todo cleanup: might want to move this to a tools.py or something
    def validate_inputs(self):
        # todo also make sure to validate if the ticker is crypto or stock

        # todo also see if the user enters the company name then you can return with the correct ticker
        ticker = yf.Ticker(self.dpg.get_value(configs.TICKER_INFO_WINDOW_TICKER_ID))

        # ticker is empty or did not return a result
        invalid_ticker = ticker.get_info()[configs.YFINANCE_REGULARMARKETPRICE] is None or self.dpg.get_value(
            configs.TICKER_INFO_WINDOW_TICKER_ID) is None

        # no negative or 0 count values and no negative bought price values
        invalid_count = self.dpg.get_value(configs.TICKER_INFO_WINDOW_COUNT_ID) <= 0

        # no negative bought price values
        invalid_bought_price = self.dpg.get_value(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID) <= 0

        if invalid_ticker or invalid_count or invalid_bought_price:
            if invalid_ticker:
                # todo display an error message
                print("Error: Invalid Ticker (It has to be the ticker name and not the full name")

            if invalid_count:
                # todo display an error message
                print("Error: You can't have negative or 0 for count")

            if invalid_bought_price:
                # todo display an error message
                print("Error: You can't have negative or 0 for bought price")

            return False

        return True

    def cleanup_ticker_info_win(self):
        self.dpg.delete_item(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.delete_item(configs.TICKER_ADD_BTN_ID)
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

    # todo this might get fixed in future updates
    def cleanup(self):
        self.dpg.enable_item(configs.FINTRACKER_ADD_BTN_ID)

        self.dpg.remove_alias(configs.TICKER_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_INPUT_TICKER_ID)
        self.dpg.remove_alias(configs.TICKER_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_RADIO_BTNS_ID)

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
