# used by other classes to add to the fintracker tables
import configs
# todo cleanup this contains code that is similar to load_open_table()
    def add_to_open_table(self, table_id, row_data, is_option):
        self.num_open_trade_rows += 1

        # data
        date_val = row_data[configs.FIREBASE_DATE]
        invest_type = row_data[configs.FIREBASE_TYPE]
        if is_option:
            trade = row_data[configs.FIREBASE_CONTRACT]
        else:
            trade = row_data[configs.FIREBASE_TICKER]

        count = row_data[configs.FIREBASE_COUNT]
        bought_price = row_data[configs.FIREBASE_BOUGHT_PRICE]

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