import configs
from ticker_search_add_crypto_stock import Add_Crypto_Stock


class TickerSearch:
    def __init__(self, dpg):
        self.dpg = dpg
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
        self.dpg.add_input_int(tag=configs.TICKER_INFO_WINDOW_COUNT_ID)

        #  enter bought price
        # todo figure out what to do when user puts a negative number
        self.dpg.add_input_float(tag=configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)

        # enter reason
        self.dpg.add_input_text(tag=configs.TICKER_INFO_WINDOW_REASON_ID,
                                hint=configs.TICKER_INFO_WINDOW_REASON_TEXT)

    def add_callback(self):
        self.validate_inputs()

    def choose_option_contract(self):
        pass

    def load_stock_info(self):
        # todo this is where we will call the respective api to get the information
        Add_Crypto_Stock(self.dpg)

    def validate_inputs(self):
        pass

    def cleanup_ticker_info_win(self):
        self.dpg.delete_item(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.delete_item(configs.TICKER_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_TICKER_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_COUNT_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_BOUGHT_PRICE_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_REASON_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID):
            self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_SHOW_CONTRACT_ID)

    # todo this might get fixed in future updates
    def cleanup(self):
        self.dpg.remove_alias(configs.TICKER_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_INPUT_TICKER_ID)
        self.dpg.remove_alias(configs.TICKER_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_RADIO_BTNS_ID)
