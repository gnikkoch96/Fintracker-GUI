import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=600, resizable=False)
dpg.setup_dearpygui()

def select_cell():
    pos = dpg.get_mouse_pos()
    print(pos)
    items = dpg.get_all_items()
    for item in items:
        print(dpg.get_item_width(item))
        if dpg.get_item_pos(item)[0] >= pos[0] <= dpg.get_item_pos(item)[0] + dpg.get_item_width(item) \
                and dpg.get_item_pos(item)[1] >= pos[1] <= dpg.get_item_pos(item)[1] + dpg.get_item_height(item) :
            dpg.set_value(item, True)

with dpg.window(label="PathFinder Window"):
    dpg.add_text("Hello, world")
    with dpg.handler_registry():
        dpg.add_mouse_down_handler(callback=select_cell)
        # basic usage of the table api
    with dpg.table(header_row=False):

        # use add_table_column to add columns to the table,
        # table columns use slot 0
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()

        # add_table_next_column will jump to the next row
        # once it reaches the end of the columns
        # table next column use slot 1
        for i in range(4):

            with dpg.table_row():
                for j in range(3):
                    dpg.add_selectable(label=f"Row{i} Column{j}", width=50)

dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    print("this will run every frame")
    dpg.render_dearpygui_frame()

dpg.destroy_context()