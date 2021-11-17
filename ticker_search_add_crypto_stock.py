import configs


class Add_Crypto_Stock:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_add_crypto_stock_win()

    def create_add_crypto_stock_win(self):
        with self.dpg.window(tag=configs.TICKER_ADD_CRYPTO_STOCK_WINDOW_ID,
                             label=configs.TICKER_ADD_CRYPTO_STOCK_WINDOW_TEXT,
                             width=self.dpg.get_viewport_width() /3,
                             height=self.dpg.get_viewport_height() /1.5,
                             on_close=self.cleanup,
                             modal=True):
            self.create_add_crypto_stock_items()

    def create_add_crypto_stock_items(self):
        pass

    def cleanup(self):
        self.dpg.remove_alias(configs.TICKER_ADD_CRYPTO_STOCK_WINDOW_ID)
