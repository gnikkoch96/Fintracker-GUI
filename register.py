import firebase_conn
import configs


# desc: creates the register GUI
class Register:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_register_win()

    def create_register_win(self):
        with self.dpg.window(tag=configs.REGISTER_WINDOW_ID,
                             label=configs.REGISTER_WINDOW_TEXT,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            self.create_register_items()

    def create_register_items(self):
        with self.dpg.group(horizontal=True) as email_login:
            self.dpg.add_text(configs.REGISTER_INPUT_EMAIL_TEXT)
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_EMAIL_ID)

        with self.dpg.group(horizontal=True) as pass_login:
            self.dpg.add_text(configs.REGISTER_INPUT_PASS_TEXT)
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_PASS_ID,
                                    password=True)

        with self.dpg.group(horizontal=True) as confirm_pass_login:
            self.dpg.add_text(configs.REGISTER_INPUT_CONFIRM_PASS_TEXT)
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_CONFIRM_PASS_ID,
                                    password=True)

        self.dpg.add_text(tag=configs.REGISTER_INPUT_ERROR_ID,
                          default_value=configs.REGISTER_INPUT_ERROR_TEXT)
        self.dpg.hide_item(configs.REGISTER_INPUT_ERROR_ID)

        self.dpg.add_button(tag=configs.REGISTER_BTN_ID,
                            label=configs.REGISTER_BTN_TEXT,
                            callback=self.register_callback)

        self.dpg.add_button(tag=configs.REGISTER_LOGIN_BTN_ID,
                            label=configs.REGISTER_LOGIN_BTN_TEXT,
                            callback=self.login_callback)

    def register_callback(self, sender, app_data, user_data):
        email = self.dpg.get_value(configs.REGISTER_INPUT_EMAIL_ID)
        password = self.dpg.get_value(configs.REGISTER_INPUT_PASS_ID)
        confirm_pass = self.dpg.get_value(configs.REGISTER_INPUT_CONFIRM_PASS_ID)

        # check to see if the confirm pass is the same as the pass if not return an error
        if confirm_pass != password:
            self.dpg.show_item(configs.REGISTER_INPUT_ERROR_ID)

        # try to make the account and see if the email is already being used or not
        if not firebase_conn.create_user_account(email, password):
            self.dpg.show_item(configs.REGISTER_INPUT_ERROR_ID)

        # todo display login then a success dialogue

    # goes back to the login screen
    def login_callback(self, sender, app_data, user_data):
        pass
