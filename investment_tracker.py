import configs
import firebase_conn
from ticker_search import TickerSearch


class Fintracker:
    def __init__(self, dpg, is_offline=False, user_id=None):
        self.dpg = dpg
        self.user_id = user_id
        self.create_fintracker_win()


        # todo if offline then we read a file instead of accessing the firebase

    def create_fintracker_win(self):
        with self.dpg.window(tag=configs.FINTRACKER_WINDOW_ID,
                             label=configs.FINTRACKER_WINDOW_TEXT,
                             width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1],
                             no_resize=True):
            self.create_fintracker_items()

    def create_fintracker_items(self):
        with self.dpg.group(horizontal=True):
            # child: closed trades window
            with self.dpg.child_window(tag=configs.FINTRACKER_CLOSED_TRADES_ID,
                                       width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                       height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65):
                self.dpg.add_text(configs.FINTRACKER_CLOSED_TRADES_TEXT)
                self.load_closed_trades()

            # child: open trades container (holds the open trades window and buttons)
            with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_CONTAINER_ID,
                                       width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                       height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65):
                # sub-child: open trades window
                with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                           width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                           height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.45):
                    self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_TEXT)
                    self.load_open_trades()

                # sub-child: buttons
                with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_BUTTONS_ID,
                                           width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                           height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.20):
                    self.dpg.add_button(tag=configs.FINTRACKER_NEWS_BTN_ID,
                                        label=configs.FINTRACKER_NEWS_BTN_TEXT)

                    self.dpg.add_button(tag=configs.FINTRACKER_ADD_BTN_ID,
                                        label=configs.ADD_BTN_TEXT,
                                        callback=self.add_callback)

        # display profit and win-rate
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.FINTRACKER_PROFIT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_ID,
                              default_value=configs.FINTRACKER_PROFIT_TEXT)

            self.dpg.add_text(configs.FINTRACKER_PROFIT_PERCENT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_PERCENT_ID,
                              default_value=configs.FINTRACKER_PROFIT_PERCENT_TEXT)

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
        # todo make it so that if the local file exists we read from there as opposed to firebase
        if firebase_conn.get_open_trades_stock_crypto_db(self.user_id) is not None:
            self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_TEXT)
            self.load_stock_crypto_table()

        if firebase_conn.get_open_trades_options_db(self.user_id) is not None:
            self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_TEXT)
            self.load_option_table()

    def load_stock_crypto_table(self):
        with self.dpg.table(tag=configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID,
                            resizable=True,
                            header_row=True):
            # column headers
            self.dpg.add_table_column()
            self.dpg.add_table_column(label=configs.FIREBASE_DATE)
            self.dpg.add_table_column(label=configs.FIREBASE_TYPE)
            self.dpg.add_table_column(label=configs.FIREBASE_TICKER)
            self.dpg.add_table_column(label=configs.FIREBASE_COUNT)
            self.dpg.add_table_column(label=configs.FIREBASE_BOUGHT_PRICE)

            for open_trade_id in firebase_conn.get_open_trades_stock_crypto_db(self.user_id):
                open_trade = firebase_conn.get_open_trade_by_id_db(self.user_id, open_trade_id)
                bought_price = round(open_trade[configs.FIREBASE_BOUGHT_PRICE], 2)
                count = open_trade[configs.FIREBASE_COUNT]
                ticker = open_trade[configs.FIREBASE_TICKER]
                invest_type = open_trade[configs.FIREBASE_TYPE]
                date = open_trade[configs.FIREBASE_DATE]

                with self.dpg.table_row():
                    with self.dpg.table_cell():
                        # id (user clicks this to find about their trade)
                        self.dpg.add_button(label=configs.FINTRACKER_OPEN_TRADES_VIEW_TRADE_TEXT,
                                            callback=self.open_trade_callback,
                                            user_data=open_trade_id)

                    with self.dpg.table_cell():
                        # date
                        self.dpg.add_text(date)

                    with self.dpg.table_cell():
                        # type
                        self.dpg.add_text(invest_type)

                    with self.dpg.table_cell():
                        # ticker
                        self.dpg.add_text(ticker)

                    with self.dpg.table_cell():
                        # count
                        self.dpg.add_text(count)

                    with self.dpg.table_cell():
                        # bought price
                        self.dpg.add_text(bought_price)

    def load_option_table(self):
        with self.dpg.table(tag=configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID,
                            resizable=True,
                            header_row=True):
            # column headers
            self.dpg.add_table_column()
            self.dpg.add_table_column(label=configs.FIREBASE_DATE)
            self.dpg.add_table_column(label=configs.FIREBASE_TYPE)
            self.dpg.add_table_column(label=configs.FIREBASE_CONTRACT)
            self.dpg.add_table_column(label=configs.FIREBASE_COUNT)
            self.dpg.add_table_column(label=configs.FIREBASE_BOUGHT_PRICE)

            for open_trade_id in firebase_conn.get_open_trades_options_db(self.user_id):
                open_trade = firebase_conn.get_open_trade_by_id_db(self.user_id, open_trade_id, True)
                bought_price = round(open_trade[configs.FIREBASE_BOUGHT_PRICE], 2)
                count = open_trade[configs.FIREBASE_COUNT]
                contract = open_trade[configs.FIREBASE_CONTRACT]
                invest_type = open_trade[configs.FIREBASE_TYPE]
                date = open_trade[configs.FIREBASE_DATE]

                with self.dpg.table_row():
                    with self.dpg.table_cell():
                        # id (user clicks this to find about their trade)
                        self.dpg.add_button(label=configs.FINTRACKER_OPEN_TRADES_VIEW_TRADE_TEXT,
                                            callback=self.open_trade_callback,
                                            user_data=open_trade_id)

                    with self.dpg.table_cell():
                        # date
                        self.dpg.add_text(date)

                    with self.dpg.table_cell():
                        # type
                        self.dpg.add_text(invest_type)

                    with self.dpg.table_cell():
                        # ticker
                        self.dpg.add_text(contract)

                    with self.dpg.table_cell():
                        # count
                        self.dpg.add_text(count)

                    with self.dpg.table_cell():
                        # bought price
                        self.dpg.add_text(bought_price)

    def open_trade_callback(self):
        pass

    def add_callback(self):
        self.dpg.disable_item(configs.FINTRACKER_ADD_BTN_ID)
        TickerSearch(self.dpg, self.user_id)
