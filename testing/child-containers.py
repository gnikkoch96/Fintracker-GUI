import dearpygui.dearpygui as dpg

dpg.create_context()

def button_action(sender, app_data, user_data):
    print(sender)

with dpg.window(tag="window", label="about", width=400, height=400):
    dpg.add_button(label="Press me", callback=button_action)
    dpg.draw_line((0, 10), (100, 100), color=(255, 0, 0, 255), thickness=1)

# print children
print(dpg.get_item_children("window"))

# print children in slot 1
print(dpg.get_item_children(dpg.last_root(), 1))

# check draw_line's slot
print(dpg.get_item_slot(dpg.last_item()))

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()