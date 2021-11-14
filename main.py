import dearpygui.dearpygui as dpg
from login import Login
from register import Register

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

def create_windows():
    dpg.create_context()
    dpg.create_viewport(title="Investment-Tracker GUI",
                        width=VIEWPORT_WIDTH,
                        height=VIEWPORT_HEIGHT)
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(1.25)

    # fonts

    # themes

    # start login window
    Register(dpg)
    Login(dpg)


    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    create_windows()