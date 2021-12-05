import configs
import firebase_conn
import validations
from search_options import Options
from dialog_win import DialogWin


class ViewTrade:
    # fintracker will be needed to update the table after edit
    def __init__(self, dpg, fintracker, trade_id, is_option, row_tag):
        self.dpg = dpg
        self.is_option = is_option
        self.trade_id = trade_id
        self.row_tag = row_tag

        # fintracker
        self.fintracker = fintracker
        self.user_id = fintracker.user_id

        # get the trade data from db based on the trade id
        self.trade_data = self.load_trade_data()

        self.create_view_trades_win()

    def create_view_trades_win(self):
        # view trade window
        with self.dpg.window(tag=configs.VIEW_TRADE_WINDOW_ID,
                             label=configs.VIEW_TRADE_WINDOW_TEXT,
                             width=configs.VIEW_TRADE_WINDOW_SIZE[0],
                             height=configs.VIEW_TRADE_WINDOW_SIZE[1],
                             on_close=self.cleanup_alias):
            self.create_view_trades_win_items()

    def create_view_trades_win_items(self):
        # data
        if self.is_option:
            trade = self.trade_data[configs.FIREBASE_CONTRACT]
        else:
            trade = self.trade_data[configs.FIREBASE_TICKER]
        date = self.trade_data[configs.FIREBASE_DATE]
        trade_type = self.trade_data[configs.FIREBASE_TYPE]
        count = self.trade_data[configs.FIREBASE_COUNT]
        bought_price = self.trade_data[configs.FIREBASE_BOUGHT_PRICE]
        reason = self.trade_data[configs.FIREBASE_REASON]

        # retrieve net profit, profit percentage, and sold price for closed trades
        if not self.for_open_table():
            net_profit = self.trade_data[configs.FIREBASE_NET_PROFIT]
            profit_per = self.trade_data[configs.FIREBASE_PROFIT_PERCENTAGE]
            sold_price = self.trade_data[configs.FIREBASE_SOLD_PRICE]

        # display contract or ticker
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_TICKER_CONTRACT_TEXT)

            # trade value
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_TICKER_CONTRACT_ID,
                                    default_value=trade)

            # change contract button (hidden in the beginning)
            self.dpg.add_button(tag=configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID,
                                label=configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_TEXT,
                                callback=self.change_contract_callback)

        # display date
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_DATE_TEXT)

            # date value
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_DATE_ID,
                                    default_value=date)

            # change date button (hidden in the beginning)
            self.dpg.add_button(tag=configs.VIEW_TRADE_CHANGE_DATE_BTN_ID,
                                label=configs.VIEW_TRADE_CHANGE_DATE_BTN_TEXT,
                                callback=self.change_date_callback)

        # display stock type
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_TYPE_TEXT)

            # trade type value
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_TYPE_ID,
                                    default_value=trade_type)

        # display count
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_COUNT_TEXT)

            # count value
            self.dpg.add_input_int(tag=configs.VIEW_TRADE_COUNT_ID,
                                   default_value=count)

        # display bought price
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_BOUGHT_PRICE_TEXT)

            # bought price value
            self.dpg.add_input_float(tag=configs.VIEW_TRADE_BOUGHT_PRICE_ID,
                                     default_value=bought_price)

        # if viewing closing trade
        if not self.for_open_table():
            # display sold price
            with self.dpg.group(horizontal=True):
                # label
                self.dpg.add_text(configs.VIEW_TRADE_SOLD_PRICE_TEXT)

                # sold price value
                self.dpg.add_input_int(tag=configs.VIEW_TRADE_SOLD_PRICE_ID,
                                       default_value=sold_price)

            # display net profit (not editable)
            with self.dpg.group(horizontal=True):
                # label
                self.dpg.add_text(configs.VIEW_TRADE_NET_PROFIT_TEXT)

                # net profit value
                self.dpg.add_input_float(tag=configs.VIEW_TRADE_NET_PROFIT_ID,
                                         default_value=net_profit)

            # display profit percentage (not editable)
            with self.dpg.group(horizontal=True):
                # label
                self.dpg.add_text(configs.VIEW_TRADE_PROFIT_PERCENTAGE_TEXT)

                # profit percentage value
                self.dpg.add_input_float(tag=configs.VIEW_TRADE_PROFIT_PERCENTAGE_ID,
                                         default_value=profit_per)
        # display reason
        with self.dpg.group(horizontal=True):
            # label
            self.dpg.add_text(configs.VIEW_TRADE_REASON_TEXT)

            # reason value
            self.dpg.add_input_text(tag=configs.VIEW_TRADE_REASON_ID,
                                    default_value=reason)

        # edit button
        self.dpg.add_button(tag=configs.VIEW_TRADE_EDIT_BTN_ID,
                            label=configs.VIEW_TRADE_EDIT_BTN_TEXT,
                            callback=self.edit_callback)

        # save button (hidden in the beginning)
        self.dpg.add_button(tag=configs.VIEW_TRADE_SAVE_BTN_ID,
                            label=configs.VIEW_TRADE_SAVE_BTN_TEXT,
                            callback=self.save_callback)

        # cancel button (hidden in the beginning)
        self.dpg.add_button(tag=configs.VIEW_TRADE_CANCEL_BTN_ID,
                            label=configs.VIEW_TRADE_CANCEL_BTN_TEXT,
                            callback=self.cancel_callback)

        self.disable_items()

    # enables items to be edited and shows corresponding buttons
    def edit_callback(self):
        self.enable_items()

        self.dpg.hide_item(configs.VIEW_TRADE_EDIT_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_SAVE_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_CANCEL_BTN_ID)
        self.dpg.show_item(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID)

    # restores values back to default and disables items again
    def cancel_callback(self):
        self.restore_default_values()

        self.dpg.show_item(configs.VIEW_TRADE_EDIT_BTN_ID)
        self.disable_items()

    # stores the edited values to firebase
    def save_callback(self):
        if self.validate_edit():
            # getting edited data
            trade = self.dpg.get_value(configs.VIEW_TRADE_TICKER_CONTRACT_ID)
            date_val = self.dpg.get_value(configs.VIEW_TRADE_DATE_ID)
            invest_type = self.dpg.get_value(configs.VIEW_TRADE_TYPE_ID)
            count = self.dpg.get_value(configs.VIEW_TRADE_COUNT_ID)
            bought_price = round(self.dpg.get_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID), 2)
            reason = self.dpg.get_value(configs.VIEW_TRADE_REASON_ID)

            # editing closed trade
            if not self.for_open_table():
                sold_price = self.dpg.get_value(configs.VIEW_TRADE_SOLD_PRICE_ID)

                # recalculate net profit and profit percentage after edit
                net_profit = round(sold_price - bought_price, 2)
                profit_per = round(net_profit / bought_price * 100, 2)

                if self.is_option:
                    new_data = {configs.FIREBASE_DATE: date_val,
                                configs.FIREBASE_CONTRACT: trade,
                                configs.FIREBASE_TYPE: invest_type,
                                configs.FIREBASE_COUNT: count,
                                configs.FIREBASE_BOUGHT_PRICE: bought_price,
                                configs.FIREBASE_SOLD_PRICE: sold_price,
                                configs.FIREBASE_NET_PROFIT: net_profit,
                                configs.FIREBASE_PROFIT_PERCENTAGE: profit_per,
                                configs.FIREBASE_REASON: reason
                                }
                else:
                    new_data = {configs.FIREBASE_DATE: date_val,
                                configs.FIREBASE_TICKER: trade,
                                configs.FIREBASE_TYPE: invest_type,
                                configs.FIREBASE_COUNT: count,
                                configs.FIREBASE_BOUGHT_PRICE: bought_price,
                                configs.FIREBASE_SOLD_PRICE: sold_price,
                                configs.FIREBASE_NET_PROFIT: net_profit,
                                configs.FIREBASE_PROFIT_PERCENTAGE: profit_per,
                                configs.FIREBASE_REASON: reason
                                }

                firebase_conn.update_closed_trade_by_id(self.user_id, self.trade_id, new_data, self.is_option)
                self.fintracker.update_table_row(self.row_tag, new_data, self.is_option, False)

            # editing open trade
            else:
                if self.is_option:
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

                firebase_conn.update_open_trade_by_id(self.user_id, self.trade_id, new_data, self.is_option)
                self.fintracker.update_table_row(self.row_tag, new_data, self.is_option, True)

            # edit success msg
            DialogWin(self.dpg, configs.VIEW_TRADE_SUCCESS_EDIT_MSG_TEXT, self)
        else:
            # load dialog
            pass

    # create option window for the user to choose another option
    def change_contract_callback(self):
        Options(self.dpg, configs.VIEW_TRADE_TICKER_CONTRACT_ID)

    # creates the calendar window for user to pick a new date
    def change_date_callback(self):
        with self.dpg.window(tag=configs.VIEW_TRADE_DATE_PICKER_WINDOW_ID,
                             label=configs.VIEW_TRADE_DATE_PICKER_WINDOW_TEXT,
                             width=configs.VIEW_TRADE_CHANGE_DATE_WINDOW_SIZE[0],
                             height=configs.VIEW_TRADE_CHANGE_DATE_WINDOW_SIZE[1],
                             modal=True):
            self.dpg.add_date_picker(tag=configs.VIEW_TRADE_DATE_PICKER_ID,
                                     default_value=configs.DEFAULT_DATE,
                                     callback=self.date_picker_callback)

    # retrieves the date user selected
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
        trade_type = self.dpg.get_value(configs.VIEW_TRADE_TYPE_ID).lower().capitalize()
        count = self.dpg.get_value(configs.VIEW_TRADE_COUNT_ID)
        bought_price = self.dpg.get_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        ticker = self.dpg.get_value(configs.VIEW_TRADE_TICKER_CONTRACT_ID)
        sold_price = self.dpg.get_value(configs.VIEW_TRADE_SOLD_PRICE_ID)

        # todo cleanup remove hardcode (using a dict possibly instead of tuple)
        # 0 - True or False
        # 1 - error message
        if not validations.validate_type(trade_type)[0] \
                or not validations.validate_count(count)[0] \
                or not validations.validate_bought_price(bought_price)[0] \
                or not validations.validate_ticker(ticker, self.is_option)[0] \
                or not validations.validate_sold_price(sold_price, self.for_open_table())[0]:

            message = "[ERROR]\n"

            # invalid type
            if not validations.validate_type(trade_type)[0]:
                message += validations.validate_type(trade_type)[1]

            # invalid count
            if not validations.validate_count(count)[0]:
                message += validations.validate_count(count)[1]

            # invalid bought price
            if not validations.validate_bought_price(bought_price)[0]:
                message += validations.validate_bought_price(bought_price)[1]

            # invalid ticker
            if not validations.validate_ticker(ticker, self.is_option)[0]:
                message += validations.validate_ticker(ticker, self.is_option)[1]

            # invalid sold price
            if not validations.validate_sold_price(sold_price, self.for_open_table())[0]:
                message += validations.validate_sold_price(sold_price, self.for_open_table())[1]

            # error message
            DialogWin(self.dpg, message, self)
            return False

        return True

    # checks if we are viewing a trade from open table
    def for_open_table(self):
        return configs.FINTRACKER_OPEN_TRADES_ROW_TEXT in self.row_tag

    # reset to default values from the trade_data
    def restore_default_values(self):
        # default data
        if self.is_option:
            trade = self.trade_data[configs.FIREBASE_CONTRACT]
        else:
            trade = self.trade_data[configs.FIREBASE_TICKER]
        date = self.trade_data[configs.FIREBASE_DATE]
        trade_type = self.trade_data[configs.FIREBASE_TYPE]
        count = self.trade_data[configs.FIREBASE_COUNT]
        bought_price = self.trade_data[configs.FIREBASE_BOUGHT_PRICE]
        reason = self.trade_data[configs.FIREBASE_REASON]

        self.dpg.set_value(configs.VIEW_TRADE_TICKER_CONTRACT_ID, trade)
        self.dpg.set_value(configs.VIEW_TRADE_DATE_ID, date)
        self.dpg.set_value(configs.VIEW_TRADE_TYPE_ID, trade_type)
        self.dpg.set_value(configs.VIEW_TRADE_COUNT_ID, count)
        self.dpg.set_value(configs.VIEW_TRADE_BOUGHT_PRICE_ID, bought_price)
        self.dpg.set_value(configs.VIEW_TRADE_REASON_ID, reason)

    # loads corresponding data from database
    def load_trade_data(self):
        # return closed trade info
        if not self.for_open_table():
            return firebase_conn.get_closed_trade_by_id(self.user_id, self.trade_id, self.is_option)

        # return open trade info
        return firebase_conn.get_open_trade_by_id(self.user_id, self.trade_id, self.is_option)

    # closing window
    def close_view_trade_win(self):
        self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
        self.cleanup_alias()

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
        self.dpg.disable_item(configs.VIEW_TRADE_TICKER_CONTRACT_ID)

        if configs.FINTRACKER_CLOSED_TRADES_ROW_TEXT in self.row_tag:
            self.dpg.disable_item(configs.VIEW_TRADE_SOLD_PRICE_ID)
            self.dpg.disable_item(configs.VIEW_TRADE_NET_PROFIT_ID)
            self.dpg.disable_item(configs.VIEW_TRADE_PROFIT_PERCENTAGE_ID)

    # enable the items to be edited
    def enable_items(self):
        if self.is_option:
            self.dpg.show_item(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID)
        else:  # only change trade input if it isn't options related (a button will replace it instead)
            self.dpg.enable_item(configs.VIEW_TRADE_TICKER_CONTRACT_ID)

        self.dpg.enable_item(configs.VIEW_TRADE_REASON_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_BOUGHT_PRICE_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_COUNT_ID)
        self.dpg.enable_item(configs.VIEW_TRADE_TYPE_ID)

        if not self.for_open_table():
            self.dpg.enable_item(configs.VIEW_TRADE_SOLD_PRICE_ID)

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_SOLD_PRICE_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_SOLD_PRICE_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_NET_PROFIT_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_NET_PROFIT_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_PROFIT_PERCENTAGE_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_PROFIT_PERCENTAGE_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_TICKER_CONTRACT_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_TICKER_CONTRACT_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_DATE_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_DATE_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_TYPE_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_TYPE_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_COUNT_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_COUNT_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_BOUGHT_PRICE_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_BOUGHT_PRICE_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_REASON_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_REASON_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_EDIT_BTN_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_EDIT_BTN_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_SAVE_BTN_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_SAVE_BTN_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_CHANGE_CONTRACT_BTN_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_CANCEL_BTN_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_CANCEL_BTN_ID)

        if self.dpg.does_alias_exist(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID):
            self.dpg.remove_alias(configs.VIEW_TRADE_CHANGE_DATE_BTN_ID)
