import configs


class Fintracker:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_fintracker_win()

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
                self.dpg.add_input_text()

            # child: open trades container (holds the open trades window and buttons)
            with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_CONTAINER_ID,
                                       width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                       height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65):
                # sub-child: open trades window
                with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_ID,
                                           width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                           height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.45):
                    self.dpg.add_input_text()

                # sub-child: buttons
                with self.dpg.child_window(tag=configs.FINTRACKER_OPEN_TRADES_BUTTONS_ID,
                                           width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                           height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.20):
                    self.dpg.add_button(tag=configs.FINTRACKER_NEWS_BTN_ID,
                                        label=configs.FINTRACKER_NEWS_BTN_TEXT)

                    self.dpg.add_button(tag=configs.FINTRACKER_ADD_BTN_ID,
                                        label=configs.FINTRACKER_ADD_BTN_TEXT)

        # display profit and win-rate
        with self.dpg.group(horizontal=True):
            self.dpg.add_text(configs.FINTRACKER_PROFIT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_ID,
                              default_value=configs.FINTRACKER_PROFIT_TEXT)

            self.dpg.add_text(configs.FINTRACKER_PROFIT_PERCENT_LABEL_TEXT)
            self.dpg.add_text(tag=configs.FINTRACKER_PROFIT_PERCENT_ID,
                              default_value=configs.FINTRACKER_PROFIT_PERCENT_TEXT)