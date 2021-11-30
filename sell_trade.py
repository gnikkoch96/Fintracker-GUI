import configs


class SellTrade:
    def __init__(self, dpg, fintracker, trade_id, is_option):
        self.dpg = dpg
        self.fintracker = fintracker
        self.trade_id = trade_id
        self.is_option = is_option
        self.create_sell_trade_win()

    def create_sell_trade_win(self):
        with self.dpg.window(tag=configs.SELL_TRADE_WINDOW_ID,
                             label=configs.SELL_TRADE_WINDOW_TEXT,
                             width=configs.SELL_TRADE_WINDOW_SIZE[0],
                             height=configs.SELL_TRADE_WINDOW_SIZE[1],
                             modal=True):
            self.create_sell_trade_items()

    def create_sell_trade_items(self):
        # count amount
        self.dpg.add_text(configs.SELL_TRADE_COUNT_TEXT)
        self.dpg.add_input_int(tag=configs.SELL_TRADE_COUNT_ID)

        # sold price
        self.dpg.add_text(configs.SELL_TRADE_SOLD_PRICE_TEXT)
        self.dpg.add_input_float(tag=configs.SELL_TRADE_SOLD_PRICE_ID)

        # sell button
        self.dpg.add_button(tag=configs.SELL_TRADE_SELL_BTN_ID,
                            label=configs.SELL_RADE_SELL_BTN_TEXT,
                            callback=self.sell_trade_callback)

    def sell_trade_callback(self):
        pass

    def validate_input(self):
        pass
