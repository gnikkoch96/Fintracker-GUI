import configs


class TickerSearch:
    def __init__(self, dpg):
        self.dpg = dpg
        self.investment_types = [configs.TICKER_RADIO_BTN_CRYPTO_TEXT,
                                 configs.TICKER_RADIO_BTN_STOCK_TEXT,
                                 configs.TICKER_RADIO_BTN_OPTION_TEXT]

        self.create_ticker_search_win()

    def create_ticker_search_win(self):
        with self.dpg.window(tag=configs.TICKER_WINDOW_ID,
                             label=configs.TICKER_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0]/2,
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1]):
            self.create_ticker_search_items()

    def create_ticker_search_items(self):
        # type of investment (i.e. crypto, stocks, options)
        self.dpg.add_radio_button(tag=configs.TICKER_RADIO_BTN_CRYPTO_ID,
                                  items=self.investment_types,
                                  horizontal=True)

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