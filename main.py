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
    # login theme
    with dpg.theme(tag=configs.LOGIN_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 15, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 17, category=dpg.mvThemeCat_Core)


if __name__ == '__main__':
    dpg.show_style_editor()
    create_windows()
