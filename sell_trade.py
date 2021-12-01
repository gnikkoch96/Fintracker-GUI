import configs
from datetime import date

import firebase_conn


class SellTrade:
    def __init__(self, dpg, fintracker, trade_id, is_option):
        self.dpg = dpg
        self.fintracker = fintracker
        self.user_id = fintracker.user_id
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

        # reason for selling
        self.dpg.add_text(configs.SELL_TRADE_REASON_TEXT)
        self.dpg.add_input_text(tag=configs.SELL_TRADE_REASON_ID)

        # sell button
        self.dpg.add_button(tag=configs.SELL_TRADE_SELL_BTN_ID,
                            label=configs.SELL_RADE_SELL_BTN_TEXT,
                            callback=self.sell_trade_callback)

    def sell_trade_callback(self):
        if self.validate_input():
            trade = firebase_conn.get_open_trade_by_id_db(self.user_id, self.trade_id, self.is_option)

            date_val = date.today()
            count = self.dpg.get_value(configs.SELL_TRADE_COUNT_ID)
            invest_type = trade[configs.FIREBASE_TYPE]
            bought_price = trade[configs.FIREBASE_BOUGHT_PRICE]
            sold_price = self.dpg.get_value(configs.SELL_TRADE_SOLD_PRICE_ID)
            net_profit = sold_price - bought_price
            profit_per = net_profit/bought_price * 100
            reason = self.dpg.get_value(configs.SELL_TRADE_REASON_ID)

            if self.is_option: # contains a contract
                contract = trade[configs.FIREBASE_CONTRACT]
                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_CONTRACT: contract,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_SOLD_PRICE: sold_price,
                        configs.FIREBASE_NET_PROFIT: net_profit,
                        configs.FIREBASE_PROFIT_PERCENTAGE: profit_per,
                        configs.FIREBASE_REASON: reason
                        }
            else: # contains a ticker
                ticker = trade[configs.FIREBASE_TICKER]
                data = {configs.FIREBASE_DATE: date_val,
                        configs.FIREBASE_TICKER: ticker,
                        configs.FIREBASE_TYPE: invest_type,
                        configs.FIREBASE_COUNT: count,
                        configs.FIREBASE_BOUGHT_PRICE: bought_price,
                        configs.FIREBASE_SOLD_PRICE: sold_price,
                        configs.FIREBASE_NET_PROFIT: net_profit,
                        configs.FIREBASE_PROFIT_PERCENTAGE: profit_per,
                        configs.FIREBASE_REASON: reason
                        }
            firebase_conn.add_closed_trade_db(self.user_id, data, self.is_option)
            print("Sold Successfully")

    def validate_input(self):
        # has to be above 0
        valid_count = self.dpg.get_value(configs.SELL_TRADE_COUNT_ID) > 0

        # has to be above 0
        valid_sold_price = self.dpg.get_value(configs.SELL_TRADE_SOLD_PRICE_ID) > 0

        if not valid_count or valid_sold_price:
            # todo add an error dialog
            if not valid_count:
                pass

            if not valid_sold_price:
                pass

            return False

        return True
