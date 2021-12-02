import configs

# open trades thread
self.num_open_trade_rows = 0
self.load_open_trades_thread = threading.Thread(target=self.load_open_trades,
                                                args=[True],
                                                daemon=True)

# closed trades thread
self.num_closed_trade_rows = 0
self.load_closed_trades_thread = threading.Thread(target=self.load_closed_trades,
                                                  args=[False],
                                                  daemon=True)


def load_tables(self, for_open, is_option):
    if for_open:
        if is_option:
            table_tag = configs.FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID
        else:
            table_tag = configs.FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID
    else:
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

        if not for_open:
            self.dpg.add_table_column(label=configs.FIREBASE_SOLD_PRICE)
            self.dpg.add_table_column(label=configs.FIREBASE_NET_PROFIT)
            self.dpg.add_table_column(label=configs.FIREBASE_PROFIT_PERCENTAGE)

        self.dpg.add_table_column(label=configs.FINTRACKER_REMOVE_TEXT)

        if for_open:
            # don't continue if there are no open trades
            if firebase_conn.get_open_trades_db(self.user_id, is_option) is None:
                return

            # retrieve the open trades
            trades = firebase_conn.get_open_trades_db(self.user_id, is_option)

        else:
            # don't continue if there are no closed trades
            if firebase_conn.get_closed_trades_db(self.user_id, is_option) is None:
                return

            # retrieve the closed trades
            trades = firebase_conn.get_closed_trades_db(self.user_id, is_option)

        # load data to the table
        for trade_id in trades:
            # int value used for generating tag rows
            self.num_closed_trade_rows += 1

            # retrieve individual trade based on trade id
            if for_open:
                trade = firebase_conn.get_open_trade_by_id_db(self.user_id, trade_id, is_option)
            else:
                trade = firebase_conn.get_closed_trade_by_id_db(self.user_id, trade_id, is_option)

            if not is_option:
                trade_type = trade[configs.FIREBASE_TICKER]
            else:
                trade_type = trade[configs.FIREBASE_CONTRACT]

            bought_price = trade[configs.FIREBASE_BOUGHT_PRICE]
            count = trade[configs.FIREBASE_COUNT]
            invest_type = trade[configs.FIREBASE_TYPE]
            date = trade[configs.FIREBASE_DATE]

            if not for_open:
                sold_price = trade[configs.FIREBASE_SOLD_PRICE]
                net_profit = trade[configs.FIREBASE_NET_PROFIT]
                profit_per = trade[configs.FIREBASE_PROFIT_PERCENTAGE]

            # crypto prices are not rounded
            if invest_type != configs.TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT:
                bought_price = round(bought_price, 2)

            # table row
            if for_open:
                row_tag = configs.FINTRACKER_OPEN_TRADES_ROW_TEXT + str(self.num_open_trade_rows)
            else:
                row_tag = configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT + str(self.num_closed_trade_rows)

            with self.dpg.table_row(tag=row_tag,
                                    parent=table_tag):

                # id (user clicks this to find about their trade)
                with self.dpg.table_cell():
                    self.dpg.add_button(label=configs.FINTRACKER_VIEW_TRADE_BTN_TEXT,
                                        callback=self.view_trade_callback,
                                        user_data=(trade_id, is_option, row_tag))

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
                                        user_data=(row_tag, is_option, trade_id))


def load_trades(self, for_open):
    # loading configs for the window
    if for_open:  # open trades window
        table_tag = configs.FINTRACKER_OPEN_TRADES_ID
        table_width = configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[0]
        table_height = configs.FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE[1]
        table_text = configs.FINTRACKER_OPEN_TRADES_TEXT
    else:  # closed trades window
        table_tag = configs.FINTRACKER_CLOSED_TRADES_ID
        table_width = configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[0]
        table_height = configs.FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE[1]
        table_text = configs.FINTRACKER_CLOSED_TRADES_TEXT

    # trade window
    with self.dpg.child_window(tag=table_tag,
                               width=table_width,
                               height=table_height,
                               parent=configs.FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID):
        # window label
        self.dpg.add_text(table_text)

        # stock/crypto table
        self.dpg.add_text(default_value=configs.FIREBASE_STOCK_CRYPTO,
                          parent=table_tag)
        self.load_tables(for_open, False)


        # options table
        self.dpg.add_text(default_value=configs.FIREBASE_OPTION,
                          parent=table_tag)

