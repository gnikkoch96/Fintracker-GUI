import configs
import firebase_conn


class ViewTrade:
    # fintracker will be needed to update the table after edit
    def __init__(self, dpg, fintracker, trade_id, is_options):
        self.dpg = dpg
        self.is_options = is_options
        self.trade_id = trade_id
        self.fintracker = fintracker
        self.user_id = fintracker.user_id

        # get the trade data from db
        self.trade_data = self.load_trade_data()

        self.create_view_trades_win()

    def create_view_trades_win(self):
        with self.dpg.window(tag=configs.VIEW_TRADE_WINDOW_ID,
                             label=configs.VIEW_TRADE_WINDOW_TEXT,
                             width=configs.VIEW_TRADE_WINDOW_SIZE[0],
                             height=configs.VIEW_TRADE_WINDOW_SIZE[1],
                             on_close=self.cleanup_alias,
                             modal=True):
            self.create_view_trades_items()

    def create_view_trades_items(self):
        if self.is_options:
            trade = self.trade_data[configs.FIREBASE_CONTRACT]
        else:
            trade = self.trade_data[configs.FIREBASE_TICKER]
        date = self.trade_data[configs.FIREBASE_DATE]
        trade_type = self.trade_data[configs.FIREBASE_TYPE]
        count = self.trade_data[configs.FIREBASE_COUNT]
        bought_price = self.trade_data[configs.FIREBASE_BOUGHT_PRICE]
        reason = self.trade_data[configs.FIREBASE_REASON]

        # display contract or ticker
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_INPUT_TEXT)
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_INPUT_ID,
                                    default_value=trade)

            # change contract button
            self.dpg.add_button(tag=configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID,
                                label=configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_TEXT,
                                callback=self.change_contract_callback)

        # display date
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_DATE_TEXT)
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_DATE_ID,
                                    default_value=date)

        # display stock type
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_TYPE_TEXT)
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_TYPE_ID,
                                    default_value=trade_type)

        # display count
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_COUNT_TEXT)
            self.dpg.add_input_int(tag=configs.VIEW_TRADE_COUNT_ID,
                                   default_value=count)

        # display bought price
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_BOUGHT_PRICE_TEXT)
            self.dpg.add_input_float(tag=configs.VIEW_TRADE_BOUGHT_PRICE_ID,
                                   default_value=bought_price)

        # display reason
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.VIEW_TRADE_REASON_TEXT)
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_REASON_ID,
                                    default_value=reason)

        # edit button
        self.dpg.add_button(tag=configs.VIEW_TRADE_EDIT_BTN_ID,
                            label=configs.VIEW_TRADE_EDIT_BTN_TEXT,
                            callback=self.edit_callback)

        # save button
        self.dpg.add_button(tag=configs.VIEW_TRADE_SAVE_BTN_ID,
                            label=configs.VIEW_TRADE_SAVE_BTN_TEXT,
                            callback=self.save_callback)

        # cancel button
        self.dpg.add_button(tag=configs.VIEW_TRADE_CANCEL_BTN_ID,
                            label=configs.VIEW_TRADE_CANCEL_BTN_TEXT,
                            callback=self.cancel_callback)

        self.disable_items()
    # disable the items so that the user doesn't accidentally edit them
    def disable_items(self):
        # hide buttons only until user wants to edit their trades
        self.dpg.hide_item(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID)
        self.dpg.hide_item(configs.VIEW_TRADE_SAVE_BTN_ID)
        self.dpg.hide_item(configs.VIEW_TRADE_CANCEL_BTN_ID)

        self.dpg.disable_item(configs.VIEW_TRADE_REASON_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_TYPE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_DATE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_INPUT_ID)

    def enable_items(self):
        self.dpg.enable_item(configs.VIEW_TRADE_REASON_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_TYPE_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_DATE_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_INPUT_ID)

    def edit_callback(self):
        self.dpg.hide_item(configs.VIEW_TRADE_EDIT_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_SAVE_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_CANCEL_BTN_ID)

    def cancel_callback(self):
        if self.is_options:
            trade = self.trade_data[configs.FIREBASE_CONTRACT]
        else:
            trade = self.trade_data[configs.FIREBASE_TICKER]
        date = self.trade_data[configs.FIREBASE_DATE]
        trade_type = self.trade_data[configs.FIREBASE_TYPE]
        count = self.trade_data[configs.FIREBASE_COUNT]
        bought_price = self.trade_data[configs.FIREBASE_BOUGHT_PRICE]
        reason = self.trade_data[configs.FIREBASE_REASON]

        # reset to default values
        self.dpg.set_value(configs.VIEW_TRADE_INPUT_ID, trade)
        self.dpg.set_value(configs.VIEW_TRADE_DATE_ID, date)
        self.dpg.set_value(configs.VIEW_TRADE_TYPE_ID, trade_type)
        self.dpg.set_value(configs.VIEW_TRADE_COUNT_ID, count)
        self.dpg.set_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID, bought_price)
        self.dpg.set_value(configs.VIEW_TRADE_REASON_ID, reason)

        self.disable_items()
        self.dpg.show_item(configs.VIEW_TRADE_EDIT_BTN_ID)

    def save_callback(self):
        pass

    def change_contract_callback(self):
        pass

    def load_trade_data(self):
        return firebase_conn.get_open_trade_by_id_db(self.user_id, self.trade_id, self.is_options)

    def cleanup_alias(self):
        self.dpg.remove_alias(configs.VIEW_TRADE_WINDOW_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_INPUT_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_DATE_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_TYPE_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_REASON_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_EDIT_BTN_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_SAVE_BTN_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID)
