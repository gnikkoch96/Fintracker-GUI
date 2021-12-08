import dearpygui.dearpygui as dpg
import configs

dpg.create_context()
dpg.create_viewport(title=configs.FINTRACKER_VIEWPORT_TITLE,
                    width=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[0],
                    height=configs.FINTRACKER_WINDOW_VIEWPORT_SIZE[1])
dpg.setup_dearpygui()
dpg.set_global_font_scale(configs.FONT_SCALE)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

dpg.add_progress_bar()