import time
import loading_win
import configs
from datetime import date
from dialog_win import DialogWin


# desc: handles the selling of a trade
class SellTrade:
    def __init__(self, dpg, fintracker, trade_id, is_option, row_tag):
        self.dpg = dpg
        self.trade_id = trade_id
        self.row_tag = row_tag
        self.is_option = is_option

        # fintracker related
        self.fintracker = fintracker
        self.firebase_client = fintracker.firebase_client

        self.create_sell_trade_win()

    def create_sell_trade_win(self):
        # sell trades window
        with self.dpg.window(tag=configs.SELL_TRADE_WINDOW_ID,
                             label=configs.SELL_TRADE_WINDOW_TEXT,
                             width=configs.SELL_TRADE_WINDOW_SIZE[0],
                             height=configs.SELL_TRADE_WINDOW_SIZE[1],
                             pos=configs.SELL_TRADE_WINDOW_POS,
                             no_resize=True,
                             on_close=self.cleanup_alias):
            self.create_sell_trade_win_items()

    def create_sell_trade_win_items(self):
        self.dpg.add_spacer(height=configs.SELL_TRADE_WINDOW_SPACERY)

        # number sold
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.SELL_TRADE_COUNT_TEXT)
            self.dpg.add_input_int(tag=configs.SELL_TRADE_COUNT_ID)

        # sold price
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.SELL_TRADE_SOLD_PRICE_TEXT)
            self.dpg.add_input_float(tag=configs.SELL_TRADE_SOLD_PRICE_ID)

        # reason for selling
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.SELL_TRADE_REASON_TEXT)
            self.dpg.add_input_text(tag=configs.SELL_TRADE_REASON_ID,
                                    height=100,
                                    multiline=True)

        # sell button
        self.dpg.add_spacer(height=configs.SELL_TRADE_SELL_BTN_SPACERY)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SELL_TRADE_SELL_BTN_SPACERX)
            self.dpg.add_button(tag=configs.SELL_TRADE_SELL_BTN_ID,
                                label=configs.SELL_TRADE_SELL_BTN_TEXT,
                                callback=self.sell_trade_callback)

    def sell_trade_callback(self):
        if self.validate_input():
            self.dpg.disable_item(configs.SELL_TRADE_SELL_BTN_ID)

            self.dpg.configure_item(configs.LOADING_WINDOW_ID, show=True)

            # retrieve the trade that we are selling
            trade = self.firebase_client.get_open_trade_by_id(self.trade_id, self.is_option)

            # connection loss
            if trade == configs.CONNECTION_ERROR_TEXT:
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

            # data
            date_val = str(date.today())
            count = self.dpg.get_value(configs.SELL_TRADE_COUNT_ID)
            invest_type = trade[configs.FIREBASE_TYPE]
            bought_price = trade[configs.FIREBASE_BOUGHT_PRICE]
            sold_price = self.dpg.get_value(configs.SELL_TRADE_SOLD_PRICE_ID)
            net_profit = round((sold_price - bought_price) * count, 2)
            profit_per = round((net_profit / (count * bought_price)) * 100, 2)
            reason = self.dpg.get_value(configs.SELL_TRADE_REASON_ID)

            if self.is_option:  # contains a contract
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
            else:  # contains a ticker
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

            add_to_db_status = self.firebase_client.add_closed_trade_db(data, self.is_option)

            if add_to_db_status:
                self.update_closed_table(data)
                self.update_open_trades(trade, data)

                loading_win.hide_load_win()

                # display success message
                DialogWin(self.dpg, configs.SELL_TRADE_SOLD_SUCCESS_MSG_TEXT, self)

                # todo cleanup quick fix (user could still press the sell button which leads to an error)
                time.sleep(0.1)

                self.dpg.enable_item(configs.SELL_TRADE_SELL_BTN_ID)
            else:  # connection lost
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

    # delete window and cleanup_aliases alias
    def close_sell_trade_win(self):
        self.dpg.delete_item(configs.SELL_TRADE_WINDOW_ID)
        self.cleanup_alias()

    # updates the open trades table
    def update_open_trades(self, selling_trade, sold_data):
        current_holdings = selling_trade[configs.FIREBASE_COUNT]
        sold_holdings = self.dpg.get_value(configs.SELL_TRADE_COUNT_ID)

        # update selling trade's count and remove if it is 0
        if sold_holdings >= current_holdings:
            # attempt to update the firebase data
            remove_status = self.firebase_client.remove_open_trade_by_id(self.is_option, self.trade_id)

            # remove trade from open table
            if remove_status:
                self.dpg.delete_item(self.row_tag)
            else:  # lost connection
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

        else:  # user is only selling a percentage of their holdings
            # update current holdings
            current_holdings = current_holdings - sold_holdings

            # update to the difference of counts
            sold_data[configs.FIREBASE_COUNT] = current_holdings

            # update the count in the open table
            self.fintracker.update_table_row(self.row_tag, sold_data, self.is_option, True)

            # attempt to update db
            update_status = self.firebase_client.update_open_trade_by_id_key(self.trade_id, configs.FIREBASE_COUNT,
                                                                             current_holdings, self.is_option)

            # connection loss
            if update_status == configs.CONNECTION_ERROR_TEXT:
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

    # updates the closed trades table
    def update_closed_table(self, row_data):
        # place in corresponding table (i.e.crypto/stock vs. options)
        if self.is_option:
            table_id = configs.FINTRACKER_CLOSED_TRADES_OPTION_TABLE_ID
        else:
            table_id = configs.FINTRACKER_CLOSED_TRADES_CRYPTO_STOCK_TABLE_ID

        self.fintracker.calculate_total_profit_win_rate_thread()
        self.fintracker.add_to_closed_table(table_id, row_data, self.is_option)

    # todo cleanup (we have a validations class)
    def validate_input(self):
        trade = self.firebase_client.get_open_trade_by_id(self.trade_id, self.is_option)

        # connection loss
        if trade == configs.CONNECTION_ERROR_TEXT:
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
            return

        # has to be above the number of held positions
        valid_count = trade[configs.FIREBASE_COUNT] >= self.dpg.get_value(configs.SELL_TRADE_COUNT_ID) > 0

        # has to be above 0
        valid_sold_price = self.dpg.get_value(configs.SELL_TRADE_SOLD_PRICE_ID) >= 0

        if not valid_count or not valid_sold_price:
            # display invalid input message
            DialogWin(self.dpg, configs.SELL_TRADE_INVALID_INPUT_MSG_TEXT, self)
            return False

        return True

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.SELL_TRADE_WINDOW_ID):
            self.dpg.remove_alias(configs.SELL_TRADE_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.SELL_TRADE_REASON_ID):
            self.dpg.remove_alias(configs.SELL_TRADE_REASON_ID)

        if self.dpg.does_alias_exist(configs.SELL_TRADE_COUNT_ID):
            self.dpg.remove_alias(configs.SELL_TRADE_COUNT_ID)

        if self.dpg.does_alias_exist(configs.SELL_TRADE_SOLD_PRICE_ID):
            self.dpg.remove_alias(configs.SELL_TRADE_SOLD_PRICE_ID)

        if self.dpg.does_alias_exist(configs.SELL_TRADE_SELL_BTN_ID):
            self.dpg.remove_alias(configs.SELL_TRADE_SELL_BTN_ID)
