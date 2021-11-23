import configs


class CryptoStockInfo:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_search_win()

    def create_search_win(self):
        with self.dpg.window(tag=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID,
                             label=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_TEXT,
                             width=self.dpg.get_viewport_width() /3,
                             height=self.dpg.get_viewport_height() /1.5,
                             on_close=self.cleanup,
                             modal=True):
            self.create_search_win()

    def create_search_win_items(self):
        pass

    def cleanup(self):
        self.dpg.remove_alias(configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID)
