import configs
import firebase_conn
from ticker_search import TickerSearch

class Fintracker:
    def __init__(self, dpg, is_offline, user_id=None):
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
                self.load_closed_trades()

            # child: open trades container (holds the open trades window and buttons)
            with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_CONTAINER_ID,
                                       width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                       height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65):
                # sub-child: open trades window
                with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                           width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                           height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.45):
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

    def load_closed_trades(self):
        # todo make it so that if the local file exists we read from there as opposed to firebase
        for closed_trade_id in firebase_conn.get_closed_trades_db(self.user_id):
            closed_trade = firebase_conn.get_closed_trade_db(self.user_id, closed_trade_id)
            bought_price = closed_trade['bought_price']
            count = closed_trade['count']
            ticker = closed_trade['ticker']
            type = closed_trade['type']
            date = closed_trade['date']

            format = f"{date} | {ticker} | {type} | {count} | {bought_price}"
            self.dpg.add_button(label=format,
                                parent=configs.FINTRACKER_CLOSED_TRADES_ID)

    def load_open_trades(self):
        # todo make it so that if the local file exists we read from there as opposed to firebase
        for open_trade_id in firebase_conn.get_open_trades_db(self.user_id):
            open_trade = firebase_conn.get_open_trade_db(self.user_id, open_trade_id)
            bought_price = open_trade['bought_price']
            count = open_trade['count']
            ticker = open_trade['ticker']
            type = open_trade['type']
            date = open_trade['date']

            format = f"{date} | {ticker} | {type} | {count} | {bought_price}"
            self.dpg.add_button(label=format,
                                parent=configs.FINTRACKER_OPEN_TRADES_ID)

    def add_callback(self):
        # data = {'date':'12/12/21', 'ticker':'VUZI', 'type':'stock', 'count':100, 'bought_price':1.25}
        # firebase_conn.add_to_db(self.user_id, data)
        TickerSearch(self.dpg)
