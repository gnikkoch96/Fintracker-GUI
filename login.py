import firebase_conn
import configs
import tools
from investment_tracker import Fintracker


class Login:
    def __init__(self, dpg):
        self.dpg = dpg
        self.create_login_win()

    # todo cleanup (label probably not needed)
    def create_login_win(self):
        with self.dpg.window(tag=configs.LOGIN_WINDOW_ID,
                             width=configs.LOGIN_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.LOGIN_WINDOW_VIEWPORT_SIZE[1],
                             pos=configs.LOGIN_WINDOW_POS_VALUE,
                             no_title_bar=True,
                             no_move=True,
                             no_resize=True):
            self.create_login_items()

    def create_login_items(self):
        # logo + header text
        with self.dpg.group(horizontal=True):
            # logo
            tools.add_and_load_image(self.dpg, configs.FINTRACKER_LOGO_PATH)

            # header text
            self.dpg.add_text(configs.LOGIN_HEADER_TEXT)

        # email input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.LOGIN_INPUT_EMAIL_ID,
                                    hint=configs.LOGIN_INPUT_EMAIL_TEXT)

            # login button
            self.dpg.add_button(tag=configs.LOGIN_INPUT_BTN_ID,
                                label=configs.LOGIN_INPUT_BTN_TEXT,
                                callback=self.login_callback)

        # pass input
        with self.dpg.group(horizontal=True):
            self.dpg.add_input_text(tag=configs.LOGIN_INPUT_PASS_ID,
                                    hint=configs.LOGIN_INPUT_PASS_TEXT,
                                    password=True)

        # error message
        self.dpg.add_text(tag=configs.LOGIN_INPUT_ERROR_ID,
                          default_value=configs.LOGIN_INPUT_ERROR_TEXT)
        self.dpg.hide_item(configs.LOGIN_INPUT_ERROR_ID)

        with self.dpg.group(horizontal=True):
            # register button
            self.dpg.add_button(tag=configs.LOGIN_REGISTER_BTN_ID,
                                label=configs.LOGIN_REGISTER_BTN_TEXT,
                                callback=self.register_callback)

            # go offline button
            self.dpg.add_button(tag=configs.LOGIN_OFFLINE_BTN_ID,
                                label=configs.LOGIN_OFFLINE_BTN_TEXT,
                                callback=self.offline_callback)

    def login_callback(self):
        # todo uncomment this in final product
        # email = self.dpg.get_value(configs.LOGIN_INPUT_EMAIL_ID)
        # password = self.dpg.get_value(configs.LOGIN_INPUT_PASS_ID)

        # todo remove in final product
        email = "n2@email.com"
        password = "123456"

        user = firebase_conn.authenticate_user_login(email, password)

        if user is not None:
            # todo create a dialogue that shows sign-in was successful
            Fintracker(self.dpg, False, user)
            self.dpg.hide_item(configs.LOGIN_WINDOW_ID)
        else:
            self.dpg.show_item(configs.LOGIN_INPUT_ERROR_ID)
            self.reset_input_fields()

    def reset_input_fields(self):
        self.dpg.set_value(configs.LOGIN_INPUT_EMAIL_ID, "")
        self.dpg.set_value(configs.LOGIN_INPUT_PASS_ID, "")

    # goes to the register screen
    def register_callback(self, sender, app_data, user_data):
        self.dpg.show_item(configs.REGISTER_WINDOW_ID)
        self.dpg.hide_item(configs.LOGIN_WINDOW_ID)

    def offline_callback(self, sender, app_data, user_data):
        # todo also display a warning for choosing to go online
        pass
        # Fintracker(self.dpg, True)
