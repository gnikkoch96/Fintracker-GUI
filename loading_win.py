import time
import dearpygui.dearpygui as dpg
import configs


# desc: this class will be used to display a loading screen
def launch_load_win():
    with dpg.window(tag=configs.LOADING_WINDOW_ID,
                    width=configs.LOADING_WINDOW_VIEWPORT_SIZE[0],
                    height=configs.LOADING_WINDOW_VIEWPORT_SIZE[1],
                    pos=configs.LOADING_WINDOW_CENTER_WINDOW_POS,
                    modal=True,
                    no_move=True,
                    no_title_bar=True,
                    no_resize=True):
        dpg.add_text(configs.LOADING_TEXT)

        # todo add a cancel button


def show_load_win():
    dpg.configure_item(configs.LOADING_WINDOW_ID, show=True)


def hide_load_win():
    dpg.configure_item(configs.LOADING_WINDOW_ID, show=False)

    # timer sleep to allow next window to load
    time.sleep(0.01)
