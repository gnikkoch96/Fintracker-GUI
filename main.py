import dearpygui.dearpygui as dpg
import configs
from login import Login
from register import Register


def create_windows():
    dpg.create_context()
    dpg.create_viewport(title=configs.FINTRACKER_VIEWPORT_TITLE,
                        width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0],
                        height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1])
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(configs.FONT_SCALE)
    dpg.set_viewport_small_icon(configs.FINTRACKER_VIEWPORT_ICON_PATH)

    # fonts
    create_dpg_fonts()

    # themes
    create_dpg_themes()

    # load login and register windows
    Register(dpg)
    Login(dpg)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def create_dpg_fonts():
    with dpg.font_registry():
        dpg.add_font(configs.OSWALD_FONT_PATH, 20, tag=configs.DEFAULT_FONT)
        dpg.add_font(configs.OSWALD_FONT_PATH, 30, tag=configs.HEADER_FONT)
        dpg.bind_font(configs.DEFAULT_FONT)


def create_dpg_themes():
    # todo once you setup your themes for each window, see similarities and put them as default

    # default theme
    with dpg.theme(tag=configs.DEFAULT_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 0, 0), category=dpg.mvThemeCat_Core)

    # etc. themes

    # used to display positive changes of stock/crypto prices
    with dpg.theme(tag=configs.GREEN_TEXT_COLOR):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (163, 239, 97), category=dpg.mvThemeCat_Core)

    # used to display negative changes of stock/crypto prices
    with dpg.theme(tag=configs.RED_TEXT_COLOR):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (242, 65, 65), category=dpg.mvThemeCat_Core)

    # login theme
    with dpg.theme(tag=configs.LOGIN_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 15, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 17, category=dpg.mvThemeCat_Core)

    # register theme
    with dpg.theme(tag=configs.REGISTER_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 15, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 17, category=dpg.mvThemeCat_Core)

    # fintracker theme
    with dpg.theme(tag=configs.FINTRACKER_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
    # dialog theme
    with dpg.theme(tag=configs.DIALOG_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)

    # trade input theme
    with dpg.theme(tag=configs.TRADE_INPUT_THEME_ID):
        with dpg.theme_component(dpg.mvRadioButton):
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 20, 20, category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 8, category=dpg.mvThemeCat_Core)

    dpg.bind_theme(configs.DEFAULT_THEME_ID)


if __name__ == '__main__':
    create_windows()
