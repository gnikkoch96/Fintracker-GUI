import firebase_conn
import configs
from investment_tracker import Fintracker

# desc: creates the login GUI
class Login:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_login_win()

    def create_login_win(self):
        with self.dpg.window(tag=configs.LOGIN_WINDOW_ID,
                             label=configs.LOGIN_WINDOW_TEXT,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            self.create_login_items()

    def create_login_items(self):
        with self.dpg.group(horizontal=True) as email_login:
            self.dpg.add_input_text(tag=configs.LOGIN_INPUT_EMAIL_ID,
                                    hint=configs.LOGIN_INPUT_EMAIL_TEXT)

        with self.dpg.group(horizontal=True) as pass_login:
            self.dpg.add_input_text(tag=configs.LOGIN_INPUT_PASS_ID,
                                    hint=configs.LOGIN_INPUT_PASS_TEXT,
                                    password=True)

        self.dpg.add_text(tag=configs.LOGIN_INPUT_ERROR_ID,
                          default_value=configs.LOGIN_INPUT_ERROR_TEXT)
        self.dpg.hide_item(configs.LOGIN_INPUT_ERROR_ID)

        self.dpg.add_button(tag=configs.LOGIN_INPUT_BTN_ID,
                            label=configs.LOGIN_INPUT_BTN_TEXT,
                            callback=self.login_callback)

        self.dpg.add_button(tag=configs.LOGIN_REGISTER_BTN_ID,
                            label=configs.LOGIN_REGISTER_BTN_TEXT,
                            callback=self.register_callback)

        self.dpg.add_button(tag=configs.LOGIN_OFFLINE_BTN_ID,
                            label=configs.LOGIN_OFFLINE_BTN_TEXT,
                            callback=self.offline_callback)

    def login_callback(self, sender, app_data, user_data):
        email = self.dpg.get_value(configs.LOGIN_INPUT_EMAIL_ID)
        password = self.dpg.get_value(configs.LOGIN_INPUT_PASS_ID)

        user = firebase_conn.authenticate_user_login(email, password)
        if user is not None:
            # todo create a dialogue that shows sign-in was successful
            Fintracker(self.dpg, False, user)
            self.dpg.hide_item(configs.LOGIN_WINDOW_ID)
        else:
            self.dpg.show_item(configs.LOGIN_INPUT_ERROR_ID)
            self.dpg.set_value(configs.LOGIN_INPUT_EMAIL_ID, "")
            self.dpg.set_value(configs.LOGIN_INPUT_PASS_ID, "")

    # goes to the register screen
    def register_callback(self, sender, app_data, user_data):
        self.dpg.show_item(configs.REGISTER_WINDOW_ID)
        self.dpg.hide_item(configs.LOGIN_WINDOW_ID)

    def offline_callback(self, sender, app_data, user_data):
        # todo also display a warning for choosing to go online
        Fintracker(self.dpg, True)