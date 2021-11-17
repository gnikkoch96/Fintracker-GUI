import configs
from ticker_search_add_crypto_stock import Add_Crypto_Stock

class TickerSearch:
    def __init__(self, dpg):
        self.dpg = dpg
        self.investment_types = [configs.TICKER_RADIO_BTN_CRYPTO_TEXT,
                                 configs.TICKER_RADIO_BTN_STOCK_TEXT,
                                 configs.TICKER_RADIO_BTN_OPTION_TEXT]
        self.investment_type = ""
        self.create_ticker_search_win()

    def create_ticker_search_win(self):
        with self.dpg.window(tag=configs.TICKER_WINDOW_ID,
                             label=configs.TICKER_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0]/2,
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup):
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
                                label=configs.TICKER_SEARCH_BTN_TEXT)

        # ticker info
        with self.dpg.child_window(tag=configs.TICKER_INFO_WINDOW_ID,
                             label=configs.TICKER_INFO_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0]/2.5,
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1]/1.5):

            # todo this is where we will call the respective api to get the information
            pass

        # add button
        self.dpg.add_button(tag=configs.TICKER_ADD_BTN_ID,
                            label=configs.ADD_BTN_TEXT,
                            callback=self.add_callback)

    # todo this might get fixed in future updates
    def cleanup(self):
        self.dpg.remove_alias(configs.TICKER_SEARCH_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_INPUT_TICKER_ID)
        self.dpg.remove_alias(configs.TICKER_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_INFO_WINDOW_ID)
        self.dpg.remove_alias(configs.TICKER_ADD_BTN_ID)
        self.dpg.remove_alias(configs.TICKER_RADIO_BTNS_ID)

    def define_investment_type(self, sender, app_data, user_data):
        self.investment_type = app_data

    def add_callback(self):
        Add_Crypto_Stock(self.dpg)