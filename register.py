import firebase_conn
import configs


# desc: creates the register GUI
class Register:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_register_win()

        # hide the register (prevent circular imports)
        self.dpg.hide_item(configs.REGISTER_WINDOW_ID)

    def create_register_win(self):
        with self.dpg.window(tag=configs.REGISTER_WINDOW_ID,
                             label=configs.REGISTER_WINDOW_TEXT,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            self.create_register_items()

    def create_register_items(self):
        # email input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_EMAIL_ID,
                                    hint=configs.REGISTER_INPUT_EMAIL_TEXT)

        # pass input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_PASS_ID,
                                    hint=configs.REGISTER_INPUT_PASS_TEXT,
                                    password=True)

        # confirm pass input (validation)
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.REGISTER_INPUT_CONFIRM_PASS_ID,
                                    hint=configs.REGISTER_INPUT_CONFIRM_PASS_TEXT,
                                    password=True)

        # error message
        self.dpg.add_text(tag=configs.REGISTER_INPUT_ERROR_ID,
                          default_value=configs.REGISTER_INPUT_ERROR_TEXT)
        self.dpg.hide_item(configs.REGISTER_INPUT_ERROR_ID)

        # register button
        self.dpg.add_button(tag=configs.REGISTER_BTN_ID,
                            label=configs.REGISTER_BTN_TEXT,
                            callback=self.register_callback)

        # login button
        self.dpg.add_button(tag=configs.REGISTER_LOGIN_BTN_ID,
                            label=configs.REGISTER_LOGIN_BTN_TEXT,
                            callback=self.login_callback)

    def register_callback(self, sender, app_data, user_data):
        email = self.dpg.get_value(configs.REGISTER_INPUT_EMAIL_ID)
        password = self.dpg.get_value(configs.REGISTER_INPUT_PASS_ID)
        confirm_pass = self.dpg.get_value(configs.REGISTER_INPUT_CONFIRM_PASS_ID)

        # check to see if the confirm pass is the same as the pass if not return an error
        # try to make the account and see if the email is already being used or not
        if confirm_pass != password or not firebase_conn.create_user_account(email, password):
            self.dpg.show_item(configs.REGISTER_INPUT_ERROR_ID)
        else:
            # todo display login then a success dialogue
            self.login_callback()

    # goes back to the login screen
    def login_callback(self):
        self.dpg.show_item(configs.LOGIN_WINDOW_ID)
        self.dpg.hide_item(configs.REGISTER_WINDOW_ID)
