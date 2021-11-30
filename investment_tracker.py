import configs
import firebase_conn
import threading
from view_trade import ViewTrade
from trade_input import InputTrade


class Fintracker:
    def __init__(self, dpg, is_offline=False, user_id=None):
        self.dpg = dpg
        self.user_id = user_id

        # threads to create a more responsive gui
        self.num_open_trade_rows = 0
        self.load_open_trades_table_thread = threading.Thread(target=self.load_open_trades,
                                                              daemon=True)

        self.num_closed_trade_rows = 0
        self.load_closed_trades_thread = threading.Thread(target=self.load_closed_trades,
                                                          daemon=True)

        # todo cleanup
        self.view_trade = None

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
            self.create_fintracker_items()

    def create_fintracker_items(self):
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
                                label=configs.ADD_BTN_TEXT,
                                callback=self.add_callback)

        with self.dpg.group(horizontal=True):
            # child: closed trades window
            with self.dpg.child_window(tag=configs.FINTRACKER_CLOSED_TRADES_ID,
                                       width=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[0],
                                       height=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[1]):
                self.dpg.add_text(configs.FINTRACKER_CLOSED_TRADES_TEXT)

                # todo start the thread for loading of closed trades
                self.load_closed_trades()

            # start the thread for loading of open trades
            self.load_open_trades_table_thread.start()

    # todo think about making this into a table as opposed to creating buttons
    def load_closed_trades(self):
        # todo make it so that if the local file exists we read from there as opposed to firebase
        if firebase_conn.get_closed_trades_db(self.user_id) is None:
            return

        for closed_trade_id in firebase_conn.get_closed_trades_db(self.user_id):
            closed_trade = firebase_conn.get_closed_trade_by_id_db(self.user_id, closed_trade_id)
            bought_price = closed_trade[configs.FIREBASE_BOUGHT_PRICE]
            count = closed_trade[configs.FIREBASE_COUNT]
            ticker = closed_trade[configs.FIREBASE_TICKER]
            type = closed_trade[configs.FIREBASE_TYPE]
            date = closed_trade[configs.FIREBASE_DATE]

            format = f"{date} | {ticker} | {type} | {count} | {bought_price}"
            self.dpg.add_button(label=format,
                                parent=configs.FINTRACKER_CLOSED_TRADES_ID)

    # todo think about making this into a table as opposed to creating buttons
    def load_open_trades(self):
        # child: open trades container (holds the open trades window and buttons)
        with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_CONTAINER_ID,
                                   width=configs.FINTRACKER_OPEN_TRADES_CONTAINER_VIEWPORT_SIZE[0],
                                   height=configs.FINTRACKER_OPEN_TRADES_CONTAINER_VIEWPORT_SIZE[1]):
            # sub-child: open trades window
            with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                       width=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[0],
                                       height=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[1]):
                self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_TEXT)

                # todo make it so that if the local file exists we read from there as opposed to firebase
                # if firebase_conn.get_open_trades_stock_crypto_db(self.user_id) is not None:
                self.dpg.add_text(default_value=configs.FIREBASE_STOCK_CRYPTO_TEXT,
                                  parent=configs.FINTRACKER_OPEN_TRADES_ID)
                self.load_open_table()

                # if firebase_conn.get_open_trades_options_db(self.user_id) is not None:
                self.dpg.add_text(default_value=configs.FIREBASE_OPTION_TEXT,
                                  parent=configs.FINTRACKER_OPEN_TRADES_ID)
                self.load_open_table(True)

    # depending on is_option it will load different tables
    def load_open_table(self, is_option=False):
        if is_option:
            table_tag = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        else:
            table_tag = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID

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
            self.dpg.add_table_column(label=configs.SELL_TEXT)
            self.dpg.add_table_column(label=configs.REMOVE_TEXT)

            if not is_option:
                # no stock or crypto trades
                if firebase_conn.get_open_trades_stock_crypto_db(self.user_id) is None:
                    return

                open_trades = firebase_conn.get_open_trades_stock_crypto_db(self.user_id)
            else:
                # no option trades
                if firebase_conn.get_open_trades_options_db(self.user_id) is None:
                    return

                open_trades = firebase_conn.get_open_trades_options_db(self.user_id)

            for open_trade_id in open_trades:
                self.num_open_trade_rows += 1

                if not is_option:
                    open_trade = firebase_conn.get_open_trade_by_id_db(self.user_id, open_trade_id, is_option)
                    trade_type = open_trade[configs.FIREBASE_TICKER]
                else:
                    open_trade = firebase_conn.get_open_trade_by_id_db(self.user_id, open_trade_id, is_option)
                    trade_type = open_trade[configs.FIREBASE_CONTRACT]

                bought_price = open_trade[configs.FIREBASE_BOUGHT_PRICE]
                count = open_trade[configs.FIREBASE_COUNT]
                invest_type = open_trade[configs.FIREBASE_TYPE]
                date = open_trade[configs.FIREBASE_DATE]

                if invest_type == configs.TICKER_RADIO_BTN_STOCK_TEXT:
                    bought_price = round(bought_price, 2)

                row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
                with self.dpg.table_row(tag=row_tag,
                                        parent=table_tag):
                    with self.dpg.table_cell():
                        # id (user clicks this to find about their trade)
                        self.dpg.add_button(label=configs.FINTRACKER_OPEN_TRADES_VIEW_TRADE_TEXT,
                                            callback=self.view_trade_callback,
                                            user_data=(open_trade_id, is_option))

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
                        self.dpg.add_button(label=configs.SELL_TEXT,
                                            callback=self.sell_callback,
                                            user_data=(is_option,
                                                       open_trade_id))

                    with self.dpg.table_cell():
                        # remove button
                        self.dpg.add_button(label=configs.REMOVE_TEXT,
                                            callback=self.remove_callback,
                                            user_data=(row_tag, is_option, open_trade_id))

    # used by other classes to update the fintracker table
    def add_to_open_table(self, table_id, row_data, is_option=False):
        self.num_open_trade_rows += 1

        date_val = row_data[0]
        invest_type = row_data[1]
        trade = row_data[2]
        count = row_data[3]
        bought_price = row_data[4]

        # todo figure out how to get the open trade id
        if is_option:
            open_trades = firebase_conn.get_open_trades_keys(self.user_id, is_option)
        else:
            open_trades = firebase_conn.get_open_trades_keys(self.user_id, is_option)

        # the recent trade should represent the last value of the trades
        open_trade_id = list(open_trades)[-1]

        row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
        with self.dpg.table_row(tag=row_tag,
                                parent=table_id):
            with self.dpg.table_cell():
                self.dpg.add_button(label=configs.FINTRACKER_OPEN_TRADES_VIEW_TRADE_TEXT,
                                    callback=self.view_trade_callback,
                                    user_data=(open_trade_id, is_option))

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
                self.dpg.add_button(label=configs.SELL_TEXT,
                                    callback=self.sell_callback,
                                    user_data=(is_option,
                                               open_trade_id))

            with self.dpg.table_cell():
                # remove button
                self.dpg.add_button(label=configs.REMOVE_TEXT,
                                    callback=self.remove_callback,
                                    user_data=(row_tag, is_option, open_trade_id))

    def view_trade_callback(self, sender, app_data, user_data):
        trade_id = user_data[0]
        is_option = user_data[1]

        if not self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option)
        else:
            self.close_view_trade_win()
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option)

    def sell_callback(self):
        pass

    def close_view_trade_win(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
            self.view_trade.cleanup_alias()

    def remove_callback(self, sender, app_data, user_data):
        # close the window of the removed trade
        self.close_view_trade_win()

        row_tag = user_data[0]
        is_option = user_data[1]
        open_trade_id = user_data[2]
        firebase_conn.remove_open_trade_by_id(self.user_id, is_option, open_trade_id)

        # todo update the table once it has been removed
        self.dpg.delete_item(row_tag)



    def add_callback(self):
        if self.dpg.does_alias_exist(configs.TICKER_INFO_WINDOW_TICKER_ID):
            self.dpg.focus_item(configs.TICKER_INFO_WINDOW_TICKER_ID)
        else:
            InputTrade(self.dpg, self.user_id, self)
