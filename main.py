import dearpygui.dearpygui as dpg
import configs
from login import Login
from register import Register

def create_windows():
    dpg.create_context()
    dpg.create_viewport(title="Investment-Tracker GUI",
                        width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0],
                        height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1])
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(1.25)

    # fonts

    # themes

    # load login and register windows
    Register(dpg)
    Login(dpg)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    dpg.show_style_editor()
    create_windows()
