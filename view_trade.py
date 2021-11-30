import configs
import firebase_conn
import yfinance_tool as yft
import cngko_tool as cgt
from search_options import Options


class ViewTrade:
    # fintracker will be needed to update the table after edit
    def __init__(self, dpg, fintracker, trade_id, is_options, row_tag):
        self.dpg = dpg
        self.is_options = is_options
        self.trade_id = trade_id
        self.row_tag = row_tag
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
                             on_close=self.cleanup_alias):
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
            self.dpg.add_button(tag=configs.VIEW_TRADE_CHANGE_DATE_BTN_ID,
                                label=configs.VIEW_TRADE_CHANGE_DATE_BTN_TEXT,
                                callback=self.change_date)

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
        self.dpg.hide_item(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID)

        self.dpg.disable_item(configs.VIEW_TRADE_REASON_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_TYPE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_DATE_ID)
        self.dpg.disable_item(configs.VIEW_TRADE_INPUT_ID)

    def enable_items(self):
        if self.is_options:
            self.dpg.show_item(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID)
        else:  # only change trade input if it isn't options related (a button will replace it instead)
            self.dpg.enable_item(configs.VIEW_TRADE_INPUT_ID)

        self.dpg.enable_item(configs.VIEW_TRADE_REASON_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_TYPE_ID)

    def edit_callback(self):
        self.enable_items()

        self.dpg.hide_item(configs.VIEW_TRADE_EDIT_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_SAVE_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_CANCEL_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID)

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
        if self.validate_edit():
            trade = self.dpg.get_value(configs.VIEW_TRADE_INPUT_ID)
            date_val = self.dpg.get_value(configs.VIEW_TRADE_DATE_ID)
            invest_type = self.dpg.get_value(configs.VIEW_TRADE_TYPE_ID)
            count = self.dpg.get_value(configs.VIEW_TRADE_COUNT_ID)
            bought_price = round(self.dpg.get_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID), 2)
            reason = self.dpg.get_value(configs.VIEW_TRADE_REASON_ID)

            if self.is_options:
                new_data = {configs.FIREBASE_DATE: date_val,
                            configs.FIREBASE_CONTRACT: trade,
                            configs.FIREBASE_TYPE: invest_type,
                            configs.FIREBASE_COUNT: count,
                            configs.FIREBASE_BOUGHT_PRICE: bought_price,
                            configs.FIREBASE_REASON: reason
                            }
            else:
                new_data = {configs.FIREBASE_DATE: date_val,
                            configs.FIREBASE_TICKER: trade,
                            configs.FIREBASE_TYPE: invest_type,
                            configs.FIREBASE_COUNT: count,
                            configs.FIREBASE_BOUGHT_PRICE: bought_price,
                            configs.FIREBASE_REASON: reason
                            }

            firebase_conn.update_open_trade_by_id(self.user_id, self.trade_id, new_data, self.is_options)

            # todo create a dialog to display this notice
            print("Update Successful")


            # closing window
            self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
            self.cleanup_alias()

            self.fintracker.update_table_row(self.row_tag, new_data, self.is_options)


    def change_contract_callback(self):
        Options(self.dpg, configs.VIEW_TRADE_INPUT_ID)

    def change_date(self):
        with self.dpg.window(tag=configs.VIEW_TRADE_DATE_PICKER_WINDOW_ID,
                             label=configs.VIEW_TRADE_DATE_PICKER_WINDOW_TEXT,
                             width=configs.VIEW_TRADE_WINDOW_SIZE[0] / 2,
                             height=configs.VIEW_TRADE_WINDOW_SIZE[1] / 2,
                             modal=True):
            self.dpg.add_date_picker(tag=configs.VIEW_TRADE_DATE_PICKER_ID,
                                     default_value=configs.DEFAULT_DATE,
                                     callback=self.date_picker_callback)

    def date_picker_callback(self, sender, app_data, user_data):
        year = app_data[configs.DPG_DATE_PICKER_YEAR] + 1900
        month = app_data[configs.DPG_DATE_PICKER_MONTH] + 1
        day = app_data[configs.DPG_DATE_PICKER_DAY]
        new_date = f"{year}-{month}-{day}"

        self.dpg.set_value(configs.VIEW_TRADE_DATE_ID, new_date)
        self.dpg.delete_item(configs.VIEW_TRADE_DATE_PICKER_WINDOW_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_DATE_PICKER_ID)

    # makes sure the user is inputting valid data
    def validate_edit(self):
        # don't need to validate options because it will be properly formatted when user chooses contract
        if not self.is_options:
            ticker = self.dpg.get_value(configs.VIEW_TRADE_INPUT_ID)
            valid_ticker = yft.validate_ticker(ticker) or cgt.validate_coin(ticker)

        trade_type = self.dpg.get_value(configs.VIEW_TRADE_TYPE_ID).capitalize()
        count = self.dpg.get_value(configs.VIEW_TRADE_COUNT_ID)
        bought_price = self.dpg.get_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID)

        valid_type = (trade_type == configs.TICKER_RADIO_BTN_STOCK_TEXT or
                      trade_type == configs.TICKER_RADIO_BTN_CRYPTO_TEXT or
                      trade_type == configs.TICKER_RADIO_BTN_OPTION_TEXT)

        valid_count = count >= 0

        valid_bought_price = bought_price >= 0

        if not valid_type and not valid_count and not valid_bought_price:
            if not self.is_options:
                if not valid_ticker:
                    # todo display error message for corresponding errors (users want to know where they were wrong)
                    return False

        return True

    def load_trade_data(self):
        return firebase_conn.get_open_trade_by_id_db(self.user_id, self.trade_id, self.is_options)

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
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
        self.dpg.remove_alias(configs.VIEW_TRADE_CANCEL_BTN_ID)
        self.dpg.remove_alias(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID)
