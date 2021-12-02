import configs
import firebase_conn
import threading
from view_trade import ViewTrade
from trade_input import InputTrade
from sell_trade import SellTrade


class Fintracker:
    # user_id is none if the user chooses to go offline
    def __init__(self, dpg, is_offline=False, user_id=None):
        self.dpg = dpg
        self.user_id = user_id
        self.view_trade = None  # stores reference to currently viewed trade

        # open trades thread
        self.num_open_trade_rows = 0
        self.load_open_trades_thread = threading.Thread(target=self.load_open_trades,
                                                        daemon=True)

        # closed trades thread
        self.num_closed_trade_rows = 0
        self.load_closed_trades_thread = threading.Thread(target=self.load_closed_trades,
                                                          daemon=True)

        self.create_fintracker_win()

        # todo if offline then we read a file instead of accessing the firebase
        if is_offline:
            pass

    def create_fintracker_win(self):
        with self.dpg.window(tag=configs.FINTRACKER_WINDOW_ID,
                             label=configs.FINTRACKER_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1],
                             no_resize=True):
            self.create_fintracker_win_items()

    def create_fintracker_win_items(self):
        # profit, win-rate, news and add new trade button
        with self.dpg.group(horizontal=True):
            # profit
            self.dpg.add_text(configs.FINTRACKER_PROFIT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_ID,
                              default_value=configs.FINTRACKER_PROFIT_TEXT)

            # win-rate
            self.dpg.add_text(configs.FINTRACKER_PROFIT_PERCENT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_PERCENT_ID,
                              default_value=configs.FINTRACKER_PROFIT_PERCENT_TEXT)

            # news button
            self.dpg.add_button(tag=configs.FINTRACKER_NEWS_BTN_ID,
                                label=configs.FINTRACKER_NEWS_BTN_TEXT)

            # add trade button
            self.dpg.add_button(tag=configs.FINTRACKER_ADD_BTN_ID,
                                label=configs.FINTRACKER_ADD_BTN_TEXT,
                                callback=self.add_callback)

        # closed and open trade windows group
        with self.dpg.group(tag=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID,
                            horizontal=True):
            # start loading closed trades
            self.load_closed_trades_thread.start()

            # start loading open trades
            self.load_open_trades_thread.start()

    def load_closed_trades(self):
        # close trade window
        with self.dpg.child_window(tag=configs.FINTRACKER_CLOSED_TRADES_ID,
                                   width=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[0],
                                   height=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[1],
                                   parent=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
            self.dpg.add_text(configs.FINTRACKER_CLOSED_TRADES_TEXT)

            # stock/crypto table
            self.dpg.add_text(default_value=configs.FIREBASE_STOCK_CRYPTO,
                              parent=configs.FINTRACKER_CLOSED_TRADES_ID)
            self.load_closed_table(False)

            # options table
            self.dpg.add_text(default_value=configs.FIREBASE_OPTION,
                              parent=configs.FINTRACKER_CLOSED_TRADES_ID)
            self.load_closed_table(True)

    # is_option flag will load the corresponding table (i.e crypto/stock or option)
    def load_closed_table(self, is_option):
        if is_option:
            table_tag = configs.FINTRACKER_CLOSED_TRADES_OPTION_TABLE_ID
        else:
            table_tag = configs.FINTRACKER_CLOSED_TRADES_CRYPTO_STOCK_TABLE_ID

        # table
        with self.dpg.table(tag=table_tag,
                            resizable=True,
                            header_row=True,
                            parent=configs.FINTRACKER_CLOSED_TRADES_ID):

            # column headers
            self.dpg.add_table_column()
            self.dpg.add_table_column(label=configs.FIREBASE_DATE)
            self.dpg.add_table_column(label=configs.FIREBASE_TYPE)

            if not is_option:
                self.dpg.add_table_column(label=configs.FIREBASE_TICKER)
            else:
                self.dpg.add_table_column(label=configs.FIREBASE_CONTRACT)

            self.dpg.add_table_column(label=configs.FIREBASE_COUNT)
            self.dpg.add_table_column(label=configs.FIREBASE_BOUGHT_PRICE)
            self.dpg.add_table_column(label=configs.FIREBASE_SOLD_PRICE)
            self.dpg.add_table_column(label=configs.FIREBASE_NET_PROFIT)
            self.dpg.add_table_column(label=configs.FIREBASE_PROFIT_PERCENTAGE)
            self.dpg.add_table_column(label=configs.FINTRACKER_REMOVE_TEXT)

            # don't continue if there are no trades
            if firebase_conn.get_closed_trades_db(self.user_id, is_option) is None:
                return

            # retrieve the closed trades
            closed_trades = firebase_conn.get_closed_trades_db(self.user_id, is_option)

            # load data to the table
            for closed_trade_id in closed_trades:
                # int value used for generating tag rows
                self.num_closed_trade_rows += 1

                # retrieve individual trade based on trade id
                closed_trade = firebase_conn.get_closed_trade_by_id_db(self.user_id, closed_trade_id, is_option)

                if not is_option:
                    trade_type = closed_trade[configs.FIREBASE_TICKER]
                else:
                    trade_type = closed_trade[configs.FIREBASE_CONTRACT]

                bought_price = closed_trade[configs.FIREBASE_BOUGHT_PRICE]
                count = closed_trade[configs.FIREBASE_COUNT]
                invest_type = closed_trade[configs.FIREBASE_TYPE]
                date = closed_trade[configs.FIREBASE_DATE]
                sold_price = closed_trade[configs.FIREBASE_SOLD_PRICE]
                net_profit = closed_trade[configs.FIREBASE_NET_PROFIT]
                profit_per = closed_trade[configs.FIREBASE_PROFIT_PERCENTAGE]

                # crypto prices are not rounded
                if invest_type != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT:
                    bought_price = round(bought_price, 2)

                # table row
                row_tag = configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)
                with self.dpg.table_row(tag=row_tag,
                                        parent=table_tag):

                    # id (user clicks this to find about their trade)
                    with self.dpg.table_cell():
                        self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                            callback=self.view_trade_callback,
                                            user_data=(closed_trade_id, is_option, row_tag))

                    # date
                    with self.dpg.table_cell():
                        self.dpg.add_text(date)

                    # investment type
                    with self.dpg.table_cell():
                        self.dpg.add_text(invest_type)

                    # trade (ticker or contract)
                    with self.dpg.table_cell():
                        self.dpg.add_text(trade_type)

                    # count
                    with self.dpg.table_cell():
                        self.dpg.add_text(count)

                    # bought price
                    with self.dpg.table_cell():
                        self.dpg.add_text(bought_price)

                    # sold price
                    with self.dpg.table_cell():
                        self.dpg.add_text(sold_price)

                    # net profit
                    with self.dpg.table_cell():
                        self.dpg.add_text(net_profit)

                    # profit percentage
                    with self.dpg.table_cell():
                        self.dpg.add_text(profit_per)

                    # remove button
                    with self.dpg.table_cell():
                        self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                            callback=self.closed_trade_remove_callback,
                                            user_data=(row_tag, is_option, closed_trade_id))

    def load_open_trades(self):
        # open trades window
        with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                   width=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[0],
                                   height=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[1],
                                   parent=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
            self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_TEXT)

            # stock/crypto table
            self.dpg.add_text(default_value=configs.FIREBASE_STOCK_CRYPTO,
                              parent=configs.FINTRACKER_OPEN_TRADES_ID)
            self.load_open_table(False)

            # options table
            self.dpg.add_text(default_value=configs.FIREBASE_OPTION,
                              parent=configs.FINTRACKER_OPEN_TRADES_ID)
            self.load_open_table(True)

    # is_option flag will load the corresponding table (i.e crypto/stock or option)
    def load_open_table(self, is_option):
        if is_option:
            table_tag = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        else:
            table_tag = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID

        # table
        with self.dpg.table(tag=table_tag,
                            resizable=True,
                            header_row=True,
                            parent=configs.FINTRACKER_OPEN_TRADES_ID):

            # column headers
            self.dpg.add_table_column()
            self.dpg.add_table_column(label=configs.FIREBASE_DATE)
            self.dpg.add_table_column(label=configs.FIREBASE_TYPE)

            if not is_option:
                self.dpg.add_table_column(label=configs.FIREBASE_TICKER)
            else:
                self.dpg.add_table_column(label=configs.FIREBASE_CONTRACT)

            self.dpg.add_table_column(label=configs.FIREBASE_COUNT)
            self.dpg.add_table_column(label=configs.FIREBASE_BOUGHT_PRICE)
            self.dpg.add_table_column(label=configs.FINTRACKER_SELL_TEXT)
            self.dpg.add_table_column(label=configs.FINTRACKER_REMOVE_TEXT)

            # return if there are no trades to retrieve
            if firebase_conn.get_open_trades_db(self.user_id, is_option) is None:
                return

            open_trades = firebase_conn.get_open_trades_db(self.user_id, is_option)

            for open_trade_id in open_trades:
                self.num_open_trade_rows += 1

                if not is_option:
                    open_trade = firebase_conn.get_open_trade_by_id(self.user_id, open_trade_id, is_option)
                    trade_type = open_trade[configs.FIREBASE_TICKER]
                else:
                    open_trade = firebase_conn.get_open_trade_by_id(self.user_id, open_trade_id, is_option)
                    trade_type = open_trade[configs.FIREBASE_CONTRACT]

                bought_price = open_trade[configs.FIREBASE_BOUGHT_PRICE]
                count = open_trade[configs.FIREBASE_COUNT]
                invest_type = open_trade[configs.FIREBASE_TYPE]
                date = open_trade[configs.FIREBASE_DATE]

                if invest_type == configs.TRADE_INPUT_RADIO_BTN_STOCK_TEXT:
                    bought_price = round(bought_price, 2)

                row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
                with self.dpg.table_row(tag=row_tag,
                                        parent=table_tag):
                    with self.dpg.table_cell():
                        # id (user clicks this to find about their trade)
                        self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                            callback=self.view_trade_callback,
                                            user_data=(open_trade_id, is_option, row_tag))

                    with self.dpg.table_cell():
                        # date
                        self.dpg.add_text(date)

                    with self.dpg.table_cell():
                        # type
                        self.dpg.add_text(invest_type)

                    with self.dpg.table_cell():
                        # ticker
                        self.dpg.add_text(trade_type)

                    with self.dpg.table_cell():
                        # count
                        self.dpg.add_text(count)

                    with self.dpg.table_cell():
                        # bought price
                        self.dpg.add_text(bought_price)

                    with self.dpg.table_cell():
                        # sell button
                        self.dpg.add_button(label=configs.FINTRACKER_SELL_TEXT,
                                            callback=self.sell_callback,
                                            user_data=(is_option,
                                                       open_trade_id, row_tag))

                    with self.dpg.table_cell():
                        # remove button
                        self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                            callback=self.open_trade_remove_callback,
                                            user_data=(row_tag, is_option, open_trade_id))

    # used by other classes to add to the fintracker tables
    # todo cleanup this contains code that is similar to load_open_table()
    def add_to_open_table(self, table_id, row_data, is_option):
        self.num_open_trade_rows += 1

        # data
        date_val = row_data[0]
        invest_type = row_data[1]
        trade = row_data[2]
        count = row_data[3]
        bought_price = row_data[4]

        # get the recent trade
        open_trade_keys = firebase_conn.get_open_trades_keys(self.user_id, is_option)
        open_trade_id = list(open_trade_keys)[-1]

        row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
        with self.dpg.table_row(tag=row_tag,
                                parent=table_id):
            with self.dpg.table_cell():
                self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                    callback=self.view_trade_callback,
                                    user_data=(open_trade_id, is_option, row_tag))

            with self.dpg.table_cell():
                # date
                self.dpg.add_text(date_val)

            with self.dpg.table_cell():
                # type
                self.dpg.add_text(invest_type)

            with self.dpg.table_cell():
                # ticker
                self.dpg.add_text(trade)

            with self.dpg.table_cell():
                # count
                self.dpg.add_text(count)

            with self.dpg.table_cell():
                # bought price
                self.dpg.add_text(bought_price)

            with self.dpg.table_cell():
                # sell button
                self.dpg.add_button(label=configs.FINTRACKER_SELL_TEXT,
                                    callback=self.sell_callback,
                                    user_data=(is_option,
                                               open_trade_id, row_tag))

            with self.dpg.table_cell():
                # remove button
                self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                    callback=self.open_trade_remove_callback,
                                    user_data=(row_tag, is_option, open_trade_id))

    # used by other classes to update the fintracker table
    # todo cleanup this contains code that is similar to load_open_table()
    def add_to_closed_table(self, table_id, row_data, is_option=False):
        self.num_closed_trade_rows += 1

        if not is_option:
            trade_type = row_data[configs.FIREBASE_TICKER]
        else:
            trade_type = row_data[configs.FIREBASE_CONTRACT]

        bought_price = row_data[configs.FIREBASE_BOUGHT_PRICE]
        count = row_data[configs.FIREBASE_COUNT]
        invest_type = row_data[configs.FIREBASE_TYPE]
        date = row_data[configs.FIREBASE_DATE]
        sold_price = row_data[configs.FIREBASE_SOLD_PRICE]
        net_profit = row_data[configs.FIREBASE_NET_PROFIT]
        profit_per = row_data[configs.FIREBASE_PROFIT_PERCENTAGE]

        # get the recent trade that was added
        closed_trade_keys = firebase_conn.get_closed_trades_keys(self.user_id, is_option)
        closed_trade_id = list(closed_trade_keys)[-1]

        row_tag = configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)
        with self.dpg.table_row(tag=row_tag,
                                parent=table_id):
            with self.dpg.table_cell():
                # id (user clicks this to find about their trade)
                self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                    callback=self.view_trade_callback,
                                    user_data=(closed_trade_id, is_option, row_tag))

            with self.dpg.table_cell():
                # date
                self.dpg.add_text(date)

            with self.dpg.table_cell():
                # type
                self.dpg.add_text(invest_type)

            with self.dpg.table_cell():
                # ticker
                self.dpg.add_text(trade_type)

            with self.dpg.table_cell():
                # count
                self.dpg.add_text(count)

            with self.dpg.table_cell():
                # bought price
                self.dpg.add_text(bought_price)

            with self.dpg.table_cell():
                # sold price
                self.dpg.add_text(sold_price)

            with self.dpg.table_cell():
                # net profit
                self.dpg.add_text(net_profit)

            with self.dpg.table_cell():
                # profit percentage
                self.dpg.add_text(profit_per)

            with self.dpg.table_cell():
                # remove button
                self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                    callback=self.closed_trade_remove_callback,
                                    user_data=(row_tag, is_option, closed_trade_id))

    def update_table_row(self, row_tag, new_data, is_options, for_open_table):
        row_cols = self.dpg.get_item_children(row_tag, 1)

        # data
        if is_options:
            new_trade = new_data[configs.FIREBASE_CONTRACT]
        else:
            new_trade = new_data[configs.FIREBASE_TICKER]

        new_date = new_data[configs.FIREBASE_DATE]
        new_type = new_data[configs.FIREBASE_TYPE]
        new_count = new_data[configs.FIREBASE_COUNT]
        new_bought_price = new_data[configs.FIREBASE_BOUGHT_PRICE]

        if not for_open_table:
            new_sold_price = new_data[configs.FIREBASE_SOLD_PRICE]
            new_net_profit = new_data[configs.FIREBASE_NET_PROFIT]
            new_profit_per = new_data[configs.FIREBASE_PROFIT_PERCENTAGE]

        # todo make this cleaner
        counter = 0
        for row_col_id in row_cols:
            row_col_items = self.dpg.get_item_children(row_col_id, 1)
            for item_id in row_col_items:
                if self.dpg.get_value(item_id) is not None:
                    if counter == 0:  # date
                        self.dpg.set_value(item_id, new_date)
                    elif counter == 1:  # type
                        self.dpg.set_value(item_id, new_type)
                    elif counter == 2:  # trade
                        self.dpg.set_value(item_id, new_trade)
                    elif counter == 3:  # count
                        self.dpg.set_value(item_id, new_count)
                    elif counter == 4:  # bought_price
                        self.dpg.set_value(item_id, new_bought_price)

                    if not for_open_table:
                        if counter == 5:  # sold_price
                            self.dpg.set_value(item_id, new_sold_price)
                        elif counter == 6:  # net_profit
                            self.dpg.set_value(item_id, new_net_profit)
                        elif counter == 7:  # profit_percentage
                            self.dpg.set_value(item_id, new_profit_per)

                    counter += 1

    def view_trade_callback(self, sender, app_data, user_data):
        trade_id = user_data[0]
        is_option = user_data[1]
        row_tag = user_data[2]  # used to update the row if any changes were made

        if not self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option, row_tag)
        else:
            self.close_view_trade_win()
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option, row_tag)

    def sell_callback(self, sender, app_data, user_data):
        self.close_view_trade_win()

        is_option = user_data[0]
        trade_id = user_data[1]
        row_tag = user_data[2]
        SellTrade(self.dpg, self, trade_id, is_option, row_tag)

    def close_view_trade_win(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
            self.view_trade.cleanup_alias()

    # removing a trade from open table
    def open_trade_remove_callback(self, sender, app_data, user_data):
        # close the window of the removed trade
        self.close_view_trade_win()

        row_tag = user_data[0]
        is_option = user_data[1]
        open_trade_id = user_data[2]
        firebase_conn.remove_open_trade_by_id(self.user_id, is_option, open_trade_id)

        # todo update the table once it has been removed
        self.dpg.delete_item(row_tag)

    # removing a trade from closed table will affect the total profit and win-rate
    def closed_trade_remove_callback(self, sender, app_data, user_data):
        pass

    def add_callback(self):
        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID):
            self.dpg.focus_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        else:
            InputTrade(self.dpg, self.user_id, self)
