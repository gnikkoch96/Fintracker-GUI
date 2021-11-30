import dearpygui.dearpygui as dpg
import configs


dpg.create_context()

def date_callback(sender, app_data, user_data):
    date = app_data
    print(date['year'] + 1900, date['month'] + 1, date['month_day'])

with dpg.window(label="Choose Date",
                     width=configs.VIEW_TRADE_WINDOW_SIZE[0] / 2,
                     height=configs.VIEW_TRADE_WINDOW_SIZE[1] / 2,
                     modal=True):
    dpg.add_date_picker(tag=configs.VIEW_TRADE_DATE_PICKER_ID,
                        callback=date_callback)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
