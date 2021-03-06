import configs
import threading
from view_trade import ViewTrade
from trade_input import InputTrade
from sell_trade import SellTrade
from dialog_win import DialogWin


# desc: the main hub for displaying information (closed and open trades, total profit, and win rate)
class Fintracker:

    # user_id is none if the user chooses to go offline
    def __init__(self, dpg, is_offline=False, firebase_client=None):
        self.dpg = dpg
        self.firebase_client = firebase_client

        # created to prevent duplicates
        self.view_trade = None  # stores reference to currently viewed trade
        self.sell_trade = None  # stores reference to currently selling trade

        # calculate total profit and win-rate thread
        self.total_profit = 0
        self.win_rate = 0
        self.load_total_profit_win_rate_thread = None

        # open trades thread
        self.num_open_trade_rows = 0  # int value used for generating tag rows
        self.load_open_trades_thread = threading.Thread(target=self.load_open_trades,
                                                        daemon=True)

        # closed trades thread
        self.num_closed_trade_rows = 0  # int value used for generating tag rows
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
            self.apply_theme()
            self.dpg.set_primary_window(configs.FINTRACKER_WINDOW_ID, True)
            self.create_fintracker_win_menu()
            self.create_fintracker_win_items()

    def apply_theme(self):
        self.dpg.bind_item_theme(configs.FINTRACKER_WINDOW_ID, configs.FINTRACKER_THEME_ID)

    def create_fintracker_win_menu(self):
        # menu bar
        with self.dpg.menu_bar(label=configs.FINTRACKER_MENU_SYSTEM_TEXT):
            # logout menu choice
            self.dpg.add_menu_item(label=configs.FINTRACKER_MENU_LOGOUT_TEXT,
                                   callback=self.logout_menu_callback)

            # exit app menu choice
            self.dpg.add_menu_item(label=configs.FINTRACKER_MENU_EXIT_TEXT,
                                   callback=self.exit_menu_callback)

    def create_fintracker_win_items(self):
        # profit, win-rate, news and add new trade button
        self.dpg.add_spacer(height=configs.FINTRACKER_PROFIT_WINRATE_GROUP_SPACERY)
        with self.dpg.group(horizontal=True,
                            parent=configs.FINTRACKER_WINDOW_ID):
            # start the thread to calculate the total profit and win-rate
            self.calculate_total_profit_win_rate_thread()

            # profit
            self.dpg.add_spacer(width=configs.FINTRACKER_PROFIT_WINRATE_GROUP_SPACERX)
            self.dpg.add_text(configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_TEXT)
            self.dpg.add_input_text(tag=configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_ID,
                                    width=configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_WIDTH,
                                    default_value=self.total_profit)

            # win-rate
            self.dpg.add_text(configs.FINTRACKER_DISPLAY_WIN_RATE_TEXT)
            self.dpg.add_input_text(tag=configs.FINTRACKER_DISPLAY_WIN_RATE_ID,
                                    width=configs.FINTRACKER_DISPLAY_WIN_RATE_WIDTH,
                                    default_value=self.win_rate)

            # news button
            self.dpg.add_button(tag=configs.FINTRACKER_NEWS_BTN_ID,
                                label=configs.FINTRACKER_NEWS_BTN_TEXT)

            # todo remove once added
            with self.dpg.tooltip(configs.FINTRACKER_NEWS_BTN_ID):
                self.dpg.add_text("Not Working Yet")

            # add trade button
            self.dpg.add_button(tag=configs.FINTRACKER_ADD_BTN_ID,
                                label=configs.FINTRACKER_ADD_BTN_TEXT,
                                callback=self.add_callback)

            # disables appropriate items (like the win rate and profit rate from being edited)
            self.disable_items()

        # closed and open trade windows group
        self.dpg.add_spacer(height=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_SPACERY)
        with self.dpg.group(tag=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID,
                            horizontal=True):
            # start loading closed trades
            self.load_closed_trades_thread.start()

            # start loading open trades
            self.load_open_trades_thread.start()

    # disables editing total profit and win-rate
    def disable_items(self):
        self.dpg.disable_item(configs.FINTRACKER_DISPLAY_WIN_RATE_ID)
        self.dpg.disable_item(configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_ID)

    def load_closed_trades(self):
        # close trade window
        with self.dpg.child_window(tag=configs.FINTRACKER_CLOSED_TRADES_ID,
                                   width=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[0],
                                   height=configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[1],
                                   parent=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
            # closed trades text
            self.dpg.add_text(configs.FINTRACKER_CLOSED_TRADES_TEXT)
            self.dpg.add_separator()

            # stock/crypto table
            self.dpg.add_text(default_value=configs.FIREBASE_STOCK_CRYPTO,
                              parent=configs.FINTRACKER_CLOSED_TRADES_ID)
            self.load_closed_table(False)

            # options table
            self.dpg.add_text(default_value=configs.FIREBASE_OPTION,
                              parent=configs.FINTRACKER_CLOSED_TRADES_ID)
            self.load_closed_table(True)

    # is_option flag will load under corresponding table (i.e crypto/stock or option)
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
            self.dpg.add_table_column()  # view trade
            self.dpg.add_table_column(label=configs.FIREBASE_DATE)
            self.dpg.add_table_column(label=configs.FIREBASE_TYPE)

            if not is_option:
                self.dpg.add_table_column(label=configs.FIREBASE_TICKER)
            else:
                self.dpg.add_table_column(label=configs.FIREBASE_CONTRACT)

            self.dpg.add_table_column(label=configs.FIREBASE_COUNT,
                                      init_width_or_weight=1)
            self.dpg.add_table_column(label=configs.FIREBASE_BOUGHT_PRICE)
            self.dpg.add_table_column(label=configs.FIREBASE_SOLD_PRICE)
            self.dpg.add_table_column(label=configs.FIREBASE_NET_PROFIT)
            self.dpg.add_table_column(label=configs.FIREBASE_PROFIT_PERCENTAGE)
            self.dpg.add_table_column()

            # retrieve the closed trades
            closed_trades = self.firebase_client.get_closed_trades_db(is_option)

            # connection loss
            if closed_trades == configs.CONNECTION_ERROR_TEXT:
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

            # empty table (placed here so at least it loads the column headers)
            if closed_trades is None:
                return

            # load data to the table
            for closed_trade_id in closed_trades:
                # used for row tag
                self.num_closed_trade_rows += 1

                # retrieve individual trade based on trade id
                closed_trade = self.firebase_client.get_closed_trade_by_id(closed_trade_id, is_option)

                # connection loss
                if closed_trade == configs.CONNECTION_ERROR_TEXT:
                    DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                    return

                # closed trade data
                if not is_option:
                    trade = closed_trade[configs.FIREBASE_TICKER]
                else:
                    trade = closed_trade[configs.FIREBASE_CONTRACT]
                bought_price = closed_trade[configs.FIREBASE_BOUGHT_PRICE]
                count = closed_trade[configs.FIREBASE_COUNT]
                invest_type = closed_trade[configs.FIREBASE_TYPE]
                date = closed_trade[configs.FIREBASE_DATE]
                sold_price = closed_trade[configs.FIREBASE_SOLD_PRICE]
                net_profit = closed_trade[configs.FIREBASE_NET_PROFIT]
                profit_per = closed_trade[configs.FIREBASE_PROFIT_PERCENTAGE]

                # only round on non-crypto trades
                if invest_type.lower() != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT.lower():
                    bought_price = round(bought_price, 2)

                # used to cleanup row tag alias when logging out
                if self.dpg.does_alias_exist(
                        configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)):
                    self.dpg.remove_alias(configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows))

                # table row
                row_tag = configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)
                with self.dpg.table_row(tag=row_tag,
                                        parent=table_tag):

                    # id (user clicks this to find about their trade)
                    with self.dpg.table_cell():
                        self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                            width=configs.FINTRACKER_VIEW_CLOSED_TRADE_BTN_WIDTH,
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
                        trade_ref = self.dpg.add_text(trade)

                        # make reading option contracts easier
                        if is_option:
                            with self.dpg.tooltip(trade_ref):
                                self.dpg.add_text(trade)

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
                        with self.dpg.group(horizontal=True):
                            self.dpg.add_spacer(width=configs.FINTRACKER_CLOSED_REMOVE_SPACERX)
                            remove_btn = self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                                             callback=self.closed_trade_remove_callback,
                                                             user_data=(row_tag, is_option, closed_trade_id))

                            self.dpg.bind_item_theme(remove_btn, configs.RED_BTN_COLOR_THEME_ID)

    def load_open_trades(self):
        # open trades window
        with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                   width=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[0],
                                   height=configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[1],
                                   parent=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
            # open trades text
            self.dpg.add_text(configs.FINTRACKER_OPEN_TRADES_TEXT)
            self.dpg.add_separator()

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
            self.dpg.add_table_column()
            self.dpg.add_table_column()

            # retrieve open trades
            open_trades = self.firebase_client.get_open_trades_db(is_option)

            # connection loss
            if open_trades == configs.CONNECTION_ERROR_TEXT:
                DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                return

            # return if there are no trades to retrieve
            if open_trades is None:
                return

            for open_trade_id in open_trades:
                self.num_open_trade_rows += 1

                # retrieve open trade
                open_trade = self.firebase_client.get_open_trade_by_id(open_trade_id, is_option)

                # connection loss
                if open_trade == configs.CONNECTION_ERROR_TEXT:
                    DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                    return

                # open trade data
                if not is_option:
                    trade = open_trade[configs.FIREBASE_TICKER]
                else:
                    trade = open_trade[configs.FIREBASE_CONTRACT]
                bought_price = open_trade[configs.FIREBASE_BOUGHT_PRICE]
                count = open_trade[configs.FIREBASE_COUNT]
                invest_type = open_trade[configs.FIREBASE_TYPE]
                date = open_trade[configs.FIREBASE_DATE]

                # only round on non-crypto trades
                if invest_type.lower() != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT.lower():
                    bought_price = round(bought_price, 2)

                # used to cleanup alias when logging out
                # todo make this cleaner
                if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)):
                    self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows))

                # row
                row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
                with self.dpg.table_row(tag=row_tag,
                                        parent=table_tag):

                    # id (user clicks this to find about their trade)
                    with self.dpg.table_cell():
                        self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                            width=configs.FINTRACKER_VIEW_OPEN_TRADE_BTN_WIDTH,
                                            callback=self.view_trade_callback,
                                            user_data=(open_trade_id, is_option, row_tag))

                    # date
                    with self.dpg.table_cell():
                        self.dpg.add_text(date)

                    # type
                    with self.dpg.table_cell():
                        self.dpg.add_text(invest_type)

                    # ticker
                    with self.dpg.table_cell():
                        trade_ref = self.dpg.add_text(trade)

                        # make reading option contracts easier
                        if is_option:
                            with self.dpg.tooltip(trade_ref):
                                self.dpg.add_text(trade)

                    # count
                    with self.dpg.table_cell():
                        self.dpg.add_text(count)

                    # bought price
                    with self.dpg.table_cell():
                        self.dpg.add_text(bought_price)

                    # sell button
                    with self.dpg.table_cell():
                        self.dpg.add_button(label=configs.FINTRACKER_SELL_TEXT,
                                            width=configs.FINTRACKER_SELL_BTN_WIDTH,
                                            callback=self.sell_callback,
                                            user_data=(is_option,
                                                       open_trade_id, row_tag))

                    # remove button
                    with self.dpg.table_cell():
                        with self.dpg.group(horizontal=True):
                            self.dpg.add_spacer(width=configs.FINTRACKER_OPEN_REMOVE_SPACERX)
                            remove_btn = self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                                             callback=self.open_trade_remove_callback,
                                                             user_data=(row_tag, is_option, open_trade_id))
                            self.dpg.bind_item_theme(remove_btn, configs.RED_BTN_COLOR_THEME_ID)

    # used by other classes to add to the fintracker tables
    def add_to_open_table(self, table_id, row_data, is_option):
        self.num_open_trade_rows += 1

        # data
        if is_option:
            trade = row_data[configs.FIREBASE_CONTRACT]
        else:
            trade = row_data[configs.FIREBASE_TICKER]
        date_val = row_data[configs.FIREBASE_DATE]
        invest_type = row_data[configs.FIREBASE_TYPE]
        count = row_data[configs.FIREBASE_COUNT]
        bought_price = row_data[configs.FIREBASE_BOUGHT_PRICE]

        # only round on non-crypto trades
        if invest_type.lower() != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT.lower():
            bought_price = round(bought_price, 2)

        # get the recent trade
        open_trade_keys = self.firebase_client.get_open_trades_keys(is_option)

        # connection loss
        if open_trade_keys == configs.CONNECTION_ERROR_TEXT:
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
            return

        open_trade_id = list(open_trade_keys)[-1]

        row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
        with self.dpg.table_row(tag=row_tag,
                                parent=table_id):

            # id (user clicks this to find about their trade)
            with self.dpg.table_cell():
                self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                    width=configs.FINTRACKER_VIEW_OPEN_TRADE_BTN_WIDTH,
                                    callback=self.view_trade_callback,
                                    user_data=(open_trade_id, is_option, row_tag))

            # date
            with self.dpg.table_cell():
                self.dpg.add_text(date_val)

            # type
            with self.dpg.table_cell():
                self.dpg.add_text(invest_type)

            # ticker
            with self.dpg.table_cell():
                trade_ref = self.dpg.add_text(trade)

                # displays a tooltip for easier viewing of options
                if is_option:
                    with self.dpg.tooltip(trade_ref):
                        self.dpg.add_text(trade)

            # count
            with self.dpg.table_cell():
                self.dpg.add_text(count)

            # bought price
            with self.dpg.table_cell():
                self.dpg.add_text(bought_price)

            # sell button
            with self.dpg.table_cell():
                self.dpg.add_button(label=configs.FINTRACKER_SELL_TEXT,
                                    width=configs.FINTRACKER_SELL_BTN_WIDTH,
                                    callback=self.sell_callback,
                                    user_data=(is_option,
                                               open_trade_id, row_tag))

            # remove button
            with self.dpg.table_cell():
                with self.dpg.group(horizontal=True):
                    self.dpg.add_spacer(width=configs.FINTRACKER_OPEN_REMOVE_SPACERX)
                    remove_btn = self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                                     callback=self.open_trade_remove_callback,
                                                     user_data=(row_tag, is_option, open_trade_id))

                    # give a red color to the remove button
                    self.dpg.bind_item_theme(remove_btn, configs.RED_BTN_COLOR_THEME_ID)

    # used by other classes to update the fintracker table
    def add_to_closed_table(self, table_id, row_data, is_option):
        self.num_closed_trade_rows += 1

        # closed trade data
        if not is_option:
            trade = row_data[configs.FIREBASE_TICKER]
        else:
            trade = row_data[configs.FIREBASE_CONTRACT]
        bought_price = row_data[configs.FIREBASE_BOUGHT_PRICE]
        count = row_data[configs.FIREBASE_COUNT]
        invest_type = row_data[configs.FIREBASE_TYPE]
        date = row_data[configs.FIREBASE_DATE]
        sold_price = row_data[configs.FIREBASE_SOLD_PRICE]
        net_profit = row_data[configs.FIREBASE_NET_PROFIT]
        profit_per = row_data[configs.FIREBASE_PROFIT_PERCENTAGE]

        # only round on non-crypto trades
        if invest_type.lower() != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT.lower():
            bought_price = round(bought_price, 2)

        # get the recent trade that was added
        closed_trade_keys = self.firebase_client.get_closed_trades_keys(is_option)

        # connection loss
        if closed_trade_keys == configs.CONNECTION_ERROR_TEXT:
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
            return

        closed_trade_id = list(closed_trade_keys)[-1]

        # table row
        row_tag = configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)
        with self.dpg.table_row(tag=row_tag,
                                parent=table_id):

            # id (user clicks this to find about their trade)
            with self.dpg.table_cell():
                self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                    width=configs.FINTRACKER_VIEW_CLOSED_TRADE_BTN_WIDTH,
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
                trade_ref = self.dpg.add_text(trade)

                # make reading option contracts easier
                if is_option:
                    with self.dpg.tooltip(trade_ref):
                        self.dpg.add_text(trade)

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
                with self.dpg.group(horizontal=True):
                    self.dpg.add_spacer(width=configs.FINTRACKER_CLOSED_REMOVE_SPACERX)
                    remove_btn = self.dpg.add_button(label=configs.FINTRACKER_REMOVE_TEXT,
                                                     callback=self.closed_trade_remove_callback,
                                                     user_data=(row_tag, is_option, closed_trade_id))

                    # apply red color to remove button
                    self.dpg.bind_item_theme(remove_btn, configs.RED_BTN_COLOR_THEME_ID)

    # used by classes that update the values of a row from a given table
    def update_table_row(self, row_tag, new_data, is_options, for_open_table):
        # get the columns for the row (since no tag was given to them)
        row_cols = self.dpg.get_item_children(row_tag, 1)

        # new data
        if is_options:
            new_trade = new_data[configs.FIREBASE_CONTRACT]
        else:
            new_trade = new_data[configs.FIREBASE_TICKER]
        new_date = new_data[configs.FIREBASE_DATE]
        new_type = new_data[configs.FIREBASE_TYPE]
        new_count = new_data[configs.FIREBASE_COUNT]
        new_bought_price = new_data[configs.FIREBASE_BOUGHT_PRICE]

        # for closed table
        if not for_open_table:
            new_sold_price = new_data[configs.FIREBASE_SOLD_PRICE]
            new_net_profit = new_data[configs.FIREBASE_NET_PROFIT]
            new_profit_per = new_data[configs.FIREBASE_PROFIT_PERCENTAGE]

        counter = 0

        # updates the children (i.e. components) that are within the row
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

    # opens the trade input window
    def add_callback(self):
        # give focus back to the trade input window if present
        if self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID):
            self.dpg.focus_item(configs.TRADE_INPUT_INFO_WINDOW_TICKER_ID)
        else:
            # create a new trade input window
            InputTrade(self.dpg, self.firebase_client, self)

    # opens the sell trade window
    def sell_callback(self, sender, app_data, user_data):
        self.close_view_trade_win()

        is_option = user_data[0]
        trade_id = user_data[1]
        row_tag = user_data[2]

        if not self.dpg.does_alias_exist(configs.SELL_TRADE_WINDOW_ID):
            self.sell_trade = SellTrade(self.dpg, self, trade_id, is_option, row_tag)

        else:
            self.close_sell_trade_win()
            self.sell_trade = SellTrade(self.dpg, self, trade_id, is_option, row_tag)

    # launches the view trade window with current trade's info
    def view_trade_callback(self, sender, app_data, user_data):
        trade_id = user_data[0]
        is_option = user_data[1]
        row_tag = user_data[2]  # used to update the row if any changes were made

        if not self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option, row_tag)
        else:
            self.close_view_trade_win()
            self.view_trade = ViewTrade(self.dpg, self, trade_id, is_option, row_tag)

    # removing a trade from open table
    def open_trade_remove_callback(self, sender, app_data, user_data):
        # close the window of the removed trade if possible
        self.close_view_trade_win()
        self.close_sell_trade_win()

        row_tag = user_data[0]
        is_option = user_data[1]
        open_trade_id = user_data[2]
        remove_status = self.firebase_client.remove_open_trade_by_id(is_option, open_trade_id)

        # handling connection error
        if remove_status:
            self.dpg.delete_item(row_tag)
        else:  # lost connection
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)

    # removing a trade from closed table will affect the total profit and win-rate
    def closed_trade_remove_callback(self, sender, app_data, user_data):
        # close the window of the removed trade if possible
        self.close_view_trade_win()
        self.close_sell_trade_win()

        row_tag = user_data[0]
        is_option = user_data[1]
        close_trade_id = user_data[2]

        remove_status = self.firebase_client.remove_closed_trade_by_id(is_option, close_trade_id)

        # update the total profit and win-rate
        self.calculate_total_profit_win_rate_thread()

        # handling connection error
        if remove_status:
            self.dpg.delete_item(row_tag)
        else:  # lost connection
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)

    # logs the user out
    def logout_menu_callback(self):
        # close the fintracker window
        self.close_fintracker_win()

        # display login screen
        self.dpg.show_item(configs.LOGIN_WINDOW_ID)

    # stops the program
    def exit_menu_callback(self):
        self.dpg.stop_dearpygui()

    # used for calculating the total profit and win-rate thread (reduces lag upon logging in)
    def load_profit_win_rate(self):
        # calculate values
        self.total_profit = self.calculate_total_profit()
        self.win_rate = self.calculate_win_rate()

        # update values for the total profit and win-rate fields
        self.dpg.set_value(configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_ID, self.total_profit)
        self.dpg.set_value(configs.FINTRACKER_DISPLAY_WIN_RATE_ID, self.win_rate)

    # thread to start/update the total profit and win-rate
    def calculate_total_profit_win_rate_thread(self):
        self.load_total_profit_win_rate_thread = threading.Thread(target=self.load_profit_win_rate)
        self.load_total_profit_win_rate_thread.start()

    # calculates the total profit
    def calculate_total_profit(self):
        # get all closed trades
        closed_trades_crypto_stock = self.firebase_client.get_closed_trades_db(False)
        closed_trades_options = self.firebase_client.get_closed_trades_db(True)

        # connection loss
        if closed_trades_crypto_stock == configs.CONNECTION_ERROR_TEXT or \
                closed_trades_options == configs.CONNECTION_ERROR_TEXT:
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
            return

        # sum the net profit column for crypto stock table
        total_profit = 0
        if closed_trades_crypto_stock is not None:
            for closed_trade_id in closed_trades_crypto_stock:
                closed_trade = self.firebase_client.get_closed_trade_by_id(closed_trade_id, False)

                total_profit += float(closed_trade[configs.FIREBASE_NET_PROFIT])

        # sum the net profit column for options table
        if closed_trades_options is not None:
            for closed_trade_id in closed_trades_options:
                closed_trade = self.firebase_client.get_closed_trade_by_id(closed_trade_id, True)

                total_profit += float(closed_trade[configs.FIREBASE_NET_PROFIT] * 100)

        return round(total_profit, 2)

    # calculates the win rate percentage
    def calculate_win_rate(self):

        # get all closed trades
        closed_trades_crypto_stock = self.firebase_client.get_closed_trades_db(False)
        closed_trades_options = self.firebase_client.get_closed_trades_db(True)

        # connection loss
        if closed_trades_crypto_stock == configs.CONNECTION_ERROR_TEXT or \
                closed_trades_options == configs.CONNECTION_ERROR_TEXT:
            DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
            return

        # count the number of win and loss trades
        loss_trades = 0
        win_trades = 0

        # count the number of negative percentages and positive percentages for crypto and stock
        if closed_trades_crypto_stock is not None:
            for closed_trade_id in closed_trades_crypto_stock:
                # gets stock or crypto trade
                closed_trade = self.firebase_client.get_closed_trade_by_id(closed_trade_id, False)

                # connection loss
                if closed_trade == configs.CONNECTION_ERROR_TEXT:
                    DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                    return

                # a trade is a win if the net profit is positive
                if closed_trade[configs.FIREBASE_NET_PROFIT] > 0:
                    win_trades += 1
                else:
                    loss_trades += 1

        # count the number of negative percentages and positive percentages for options
        if closed_trades_options is not None:
            for closed_trade_id in closed_trades_options:
                # gets option trade
                closed_trade = self.firebase_client.get_closed_trade_by_id(closed_trade_id, True)

                # connection loss
                if closed_trade == configs.CONNECTION_ERROR_TEXT:
                    DialogWin(self.dpg, configs.LOST_CONNECTION_ERROR_MSG, self)
                    return

                # a trade is a win if the net profit is positive
                if closed_trade[configs.FIREBASE_NET_PROFIT] > 0:
                    win_trades += 1
                else:
                    loss_trades += 1

        # empty trades
        if win_trades + loss_trades <= 0:
            return 0

        return round(win_trades / (loss_trades + win_trades) * 100, 2)

    # deletes the view trade window if present and cleans up its aliases
    def close_view_trade_win(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
            self.view_trade.cleanup_alias()

    # deletes the sell trade window if present and cleans up its aliases
    def close_sell_trade_win(self):
        if self.dpg.does_alias_exist(configs.SELL_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.SELL_TRADE_WINDOW_ID)
            self.sell_trade.cleanup_alias()

    # deletes the fintracker window if present and cleans up its aliases
    def close_fintracker_win(self):
        self.dpg.delete_item(configs.FINTRACKER_WINDOW_ID)
        self.cleanup_alias()

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.FINTRACKER_CLOSED_TRADES_ID):
            self.dpg.remove_alias(configs.FINTRACKER_CLOSED_TRADES_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_BUTTONS_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_BUTTONS_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_ADD_BTN_ID):
            self.dpg.remove_alias(configs.FINTRACKER_ADD_BTN_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_NEWS_BTN_ID):
            self.dpg.remove_alias(configs.FINTRACKER_NEWS_BTN_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_DISPLAY_WIN_RATE_ID):
            self.dpg.remove_alias(configs.FINTRACKER_DISPLAY_WIN_RATE_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_ID):
            self.dpg.remove_alias(configs.FINTRACKER_DISPLAY_TOTAL_PROFIT_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_TEXT_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_TEXT_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_OPEN_TRADES_OPTIONS_TABLE_TEXT_ID):
            self.dpg.remove_alias(configs.FINTRACKER_OPEN_TRADES_OPTIONS_TABLE_TEXT_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_CLOSED_TRADES_OPTION_TABLE_ID):
            self.dpg.remove_alias(configs.FINTRACKER_CLOSED_TRADES_OPTION_TABLE_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_CLOSED_TRADES_CRYPTO_STOCK_TABLE_ID):
            self.dpg.remove_alias(configs.FINTRACKER_CLOSED_TRADES_CRYPTO_STOCK_TABLE_ID)

        if self.dpg.does_alias_exist(configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
            self.dpg.remove_alias(configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID)
