import firebase_conn
import configs
import loading_win
import tools
from investment_tracker import Fintracker
from dialog_win import DialogWin


# dec: Login GUI
class Login:
    def __init__(self, dpg):
        self.dpg = dpg
        self._user = None
        self.email = None
        self.password = None
        self.create_login_win()

    @property
    def user(self):
        return self._user

    def create_login_win(self):
        with self.dpg.window(tag=configs.LOGIN_WINDOW_ID,
                             width=configs.LOGIN_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.LOGIN_WINDOW_VIEWPORT_SIZE[1],
                             pos=configs.LOGIN_WINDOW_POS_VALUE,
                             no_title_bar=True,
                             no_move=True,
                             no_resize=True):
            self.create_login_items()
            self.apply_fonts()
            self.apply_themes()

    def apply_fonts(self):
        self.dpg.bind_item_font(configs.LOGIN_HEADER_ID, configs.HEADER_FONT_THEME_ID)

    def apply_themes(self):
        self.dpg.bind_item_theme(configs.LOGIN_WINDOW_ID, configs.LOGIN_THEME_ID)

    def create_login_items(self):
        # logo + header text
        with self.dpg.group(horizontal=True):
            # logo
            tools.add_and_load_image(self.dpg, configs.FINTRACKER_LOGO_PATH)

            # header text
            self.dpg.add_text(tag=configs.LOGIN_HEADER_ID,
                              default_value=configs.LOGIN_HEADER_TEXT)

        # email input
        with self.dpg.group(horizontal=True):
            # email field
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

        # register + offline
        with self.dpg.group(horizontal=True):
            # register button
            self.dpg.add_button(tag=configs.LOGIN_REGISTER_BTN_ID,
                                label=configs.LOGIN_REGISTER_BTN_TEXT,
                                callback=self.register_callback)

            # go offline button
            self.dpg.add_button(tag=configs.LOGIN_OFFLINE_BTN_ID,
                                label=configs.LOGIN_OFFLINE_BTN_TEXT,
                                callback=self.offline_callback)

            # todo remove once added
            with self.dpg.tooltip(configs.LOGIN_OFFLINE_BTN_ID):
                self.dpg.add_text("Not Working Yet")

    def login_callback(self):
        loading_win.show_load_win()

        # enter email and password
        self.email = self.dpg.get_value(configs.LOGIN_INPUT_EMAIL_ID)
        self.password = self.dpg.get_value(configs.LOGIN_INPUT_PASS_ID)

        self._user = firebase_conn.authenticate_user_login(self.email, self.password)

        if self._user is not None:
            Fintracker(self.dpg, False, self.user)
            self.dpg.hide_item(configs.LOGIN_WINDOW_ID)

        else:
            loading_win.hide_load_win()

            DialogWin(self.dpg, configs.LOGIN_FAILED_MSG_TEXT, self)
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
