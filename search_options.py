import configs
import yfinance_tool as yft
import threading


# desc: search options gui that will display contracts to the user based on
# ticker, call/put, and expiration date
class Options:
    # item_id refers to the component that will display the contract
    def __init__(self, dpg, item_id):
        self.dpg = dpg
        self.item_id = item_id
        self.contract = None
        self.search_options_thread = None

        self.create_options_win()

    def create_options_win(self):
        with self.dpg.window(tag=configs.OPTION_WINDOW_ID,
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
                                label=configs.OPTION_SEARCH_BTN_TEXT,
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
            with self.dpg.group(horizontal=True, parent=configs.OPTION_WINDOW_ID):

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
                            parent=configs.OPTION_WINDOW_ID,
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
                        strike_price = options_list[configs.YFINANCE_STRIKE_PRICE][row]
                        self.dpg.add_button(label=strike_price,
                                            callback=self.row_callback,
                                            user_data=(self.dpg.get_value(configs.OPTION_WINDOW_DATE_COMBO_ID),
                                                       strike_price))

                    with self.dpg.table_cell():
                        # volume
                        volume = options_list[configs.YFINANCE_VOLUME][row]
                        self.dpg.add_text(volume)

                    with self.dpg.table_cell():
                        # open interest
                        open_int = options_list[configs.YFINANCE_OPEN_INTEREST][row]
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

        self.dpg.set_value(self.item_id,
                           f"{date_value} | {ticker.upper()} | {option_type} | {strike}")
        self.dpg.show_item(self.item_id)

        # todo think about putting this in a method
        self.dpg.delete_item(configs.OPTION_WINDOW_ID)
        self.cleanup_alias()

    def cleanup_alias(self):
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
