import time

import firebase_conn
import configs
import loading_win
import tools

from dialog_win import DialogWin


# desc: creates the register GUI
class Register:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_register_win()

        # login is displayed first, so it needs to hide
        self.dpg.hide_item(configs.REGISTER_WINDOW_ID)

    def create_register_win(self):
        with self.dpg.window(tag=configs.REGISTER_WINDOW_ID,
                             width=configs.REGISTER_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.REGISTER_WINDOW_VIEWPORT_SIZE[1],
                             pos=configs.REGISTER_WINDOW_POS_VALUE,
                             no_title_bar=True,
                             no_move=True,
                             no_resize=True):
            self.create_register_items()
            self.apply_fonts()
            self.apply_theme()

    def apply_fonts(self):
        self.dpg.bind_item_font(configs.REGISTER_HEADER_ID, configs.HEADER_FONT_THEME_ID)

    def apply_theme(self):
        self.dpg.bind_item_theme(configs.REGISTER_WINDOW_ID, configs.REGISTER_THEME_ID)

    def create_register_items(self):
        # logo + header text
        self.dpg.add_spacer(height=configs.REGISTER_SPACERY_VALUE)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.REGISTER_SPACERX_VALUE)

            # logo
            tools.add_and_load_image(self.dpg, configs.FINTRACKER_LOGO_PATH)

            # header text
            self.dpg.add_text(tag=configs.REGISTER_HEADER_ID,
                              default_value=configs.REGISTER_HEADER_TEXT)

        # email input
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.REGISTER_SPACERX_VALUE)

            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_EMAIL_ID,
                                    hint=configs.REGISTER_INPUT_EMAIL_TEXT)

        # pass input
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.REGISTER_SPACERX_VALUE)

            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_PASS_ID,
                                    hint=configs.REGISTER_INPUT_PASS_TEXT,
                                    password=True)

        # confirm pass input (validation)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.REGISTER_SPACERX_VALUE)

            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_CONFIRM_PASS_ID,
                                    hint=configs.REGISTER_INPUT_CONFIRM_PASS_TEXT,
                                    password=True)

        # register + sign in button
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.REGISTER_SPACERX_VALUE)

            # register button
            self.dpg.add_button(tag=configs.REGISTER_BTN_ID,
                                label=configs.REGISTER_BTN_TEXT,
                                callback=self.register_callback)

            # login button (returns user to login screen)
            self.dpg.add_button(tag=configs.REGISTER_LOGIN_BTN_ID,
                                label=configs.REGISTER_LOGIN_BTN_TEXT,
                                callback=self.login_callback)

    # attempt to register new user
    def register_callback(self, sender, app_data, user_data):
        loading_win.show_load_win()

        if self.validate_inputs():
            loading_win.hide_load_win()

            # success register dialog
            DialogWin(self.dpg, configs.REGISTER_SUCCESS_MSG_TEXT, self)

            # returns use to login screen
            self.login_callback()
        else:
            loading_win.hide_load_win()

            # error register dialog
            DialogWin(self.dpg, configs.REGISTER_FAILED_MSG_TEXT, self)

        # resets the input fields
        self.reset_fields()

    def validate_inputs(self):
        email = self.dpg.get_value(configs.REGISTER_INPUT_EMAIL_ID)
        password = self.dpg.get_value(configs.REGISTER_INPUT_PASS_ID)
        confirm_pass = self.dpg.get_value(configs.REGISTER_INPUT_CONFIRM_PASS_ID)

        # confirm password validation
        valid_pass = password == confirm_pass

        # check if email is already being used
        valid_email = firebase_conn.create_user_account(email, password)

        if not valid_pass or not valid_email:
            return False

        return True

    # resets the fields
    def reset_fields(self):
        self.dpg.set_value(configs.REGISTER_INPUT_EMAIL_ID, "")
        self.dpg.set_value(configs.REGISTER_INPUT_PASS_ID, "")
        self.dpg.set_value(configs.REGISTER_INPUT_CONFIRM_PASS_ID, "")

    # goes back to the login screen
    def login_callback(self):
        self.dpg.show_item(configs.LOGIN_WINDOW_ID)
        self.dpg.hide_item(configs.REGISTER_WINDOW_ID)
