import configs


class DialogWin:
    # prev_win refers to the window that created the dialog
    def __init__(self, dpg, message, prev_win):
        self.dpg = dpg
        self.message = message
        self.prev_win = prev_win

        self.create_dialog_win()

    def create_dialog_win(self):
        with self.dpg.window(tag=configs.DIALOG_WINDOW_ID,
                             modal=True,
                             on_close=self.cleanup_alias,
                             no_title_bar=True):
            self.create_dialog_win_items()

    def create_dialog_win_items(self):
        self.dpg.add_text(self.message)
        self.dpg.add_button(tag=configs.DIALOG_CONFIRMATION_BTN_ID,
                            label=configs.DIALOG_CONFIRMATION_BTN_TEXT,
                            callback=self.confirmation_callback)

    def confirmation_callback(self):
        self.close_dialog_win()
        self.close_prev_win()

    # close previous window for success messages
    def close_prev_win(self):
        # close the previous window if it was a success message
        if configs.DIALOG_SUCCESS_TEXT in self.message:
            if self.dpg.does_alias_exist(configs.SELL_TRADE_WINDOW_ID):
                self.dpg.delete_item(configs.SELL_TRADE_WINDOW_ID)

            if self.dpg.does_alias_exist(configs.VIEW_TRADE_WINDOW_ID):
                self.dpg.delete_item(configs.VIEW_TRADE_WINDOW_ID)

            # leave the trade input window alone as users might want to add multiple trades at once
            if not self.dpg.does_alias_exist(configs.TRADE_INPUT_INFO_WINDOW_ID):
                self.prev_win.cleanup_alias()

    def close_dialog_win(self):
        self.dpg.delete_item(configs.DIALOG_WINDOW_ID)
        self.cleanup_alias()

    def cleanup_alias(self):
        if self.dpg.does_alias_exist(configs.DIALOG_WINDOW_ID):
            self.dpg.remove_alias(configs.DIALOG_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.DIALOG_CONFIRMATION_BTN_ID):
            self.dpg.remove_alias(configs.DIALOG_CONFIRMATION_BTN_ID)
