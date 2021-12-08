import configs
import investment_tracker


# desc: this class will be used to create dialogs throughout the program
class DialogWin:
    # message will be displayed on the dialog
    # prev_win refers to the window that created the dialog
    def __init__(self, dpg, message, prev_win):
        self.dpg = dpg
        self.message = message
        self.prev_win = prev_win

        self.create_dialog_win()

    def create_dialog_win(self):
        with self.dpg.window(tag=configs.DIALOG_WINDOW_ID,
                             width=configs.DIALOG_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.DIALOG_WINDOW_VIEWPORT_SIZE[1],
                             modal=True,
                             on_close=self.cleanup_alias,
                             pos=configs.DIALOG_CENTER_WINDOW_POS,
                             no_resize=True,
                             no_title_bar=True):
            self.create_dialog_win_items()
            self.apply_theme()

    def apply_theme(self):
        self.dpg.bind_item_theme(configs.DIALOG_WINDOW_ID, configs.DIALOG_THEME_ID)

    def create_dialog_win_items(self):
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.DIALOG_WINDOW_VIEWPORT_SIZE[0] / 5.5)
            self.dpg.add_text(default_value=self.message,
                              wrap=configs.DIALOG_MESSAGE_WRAP_COUNT)

        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.DIALOG_WINDOW_VIEWPORT_SIZE[0] / 2.5)
            self.dpg.add_button(tag=configs.DIALOG_CONFIRMATION_BTN_ID,
                                label=configs.DIALOG_CONFIRMATION_BTN_TEXT,
                                callback=self.confirmation_callback)

    # closes this dialog and attempts to close previous window
    def confirmation_callback(self):
        self.close_dialog_win()
        self.close_prev_win()

    # close previous window for success messages
    def close_prev_win(self):
        # close the previous window if it was a success message
        if configs.DIALOG_SUCCESS_TEXT in self.message:
            # attempts to close the sell trade window if possible
            self.close_sell_trade_win()

            # attempts to close the view trade window if possible
            self.close_view_trade_win()

            # only cleanup alias if it isn't trade_input, fintracker, login, and register
            if not self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_ID) \
                    and not isinstance(self.prev_win, investment_tracker.Fintracker) \
                    and not self.dpg.does_alias_exist(configs.LOGIN_WINDOW_ID) \
                    and not self.dpg.does_alias_exist(configs.REGISTER_WINDOW_ID):
                self.prev_win.cleanup_alias()

    def close_sell_trade_win(self):
        if self.dpg.does_alias_exist(configs.SELL_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.SELL_TRADE_WINDOW_ID)
            self.prev_win.cleanup_alias()

    def close_view_trade_win(self):
        if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
            self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)
            self.prev_win.cleanup_alias()

    def close_dialog_win(self):
        self.dpg.delete_item(configs.DIALOG_WINDOW_ID)
        self.cleanup_alias()

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.DIALOG_WINDOW_ID):
            self.dpg.remove_alias(configs.DIALOG_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.DIALOG_CONFIRMATION_BTN_ID):
            self.dpg.remove_alias(configs.DIALOG_CONFIRMATION_BTN_ID)
