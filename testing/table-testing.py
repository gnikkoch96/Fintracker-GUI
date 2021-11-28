import dearpygui.dearpygui as dpg

import investment_tracker

dpg.create_context()


def delete_row_1():
    dpg.delete_item("what_what1")

def delete_row_2():
    dpg.delete_item("what_what2")

with dpg.window(label="Tutorial"):
    with dpg.table(header_row=True):

        # use add_table_column to add columns to the table,
        # table columns use child slot 0
        dpg.add_table_column(label="1")
        dpg.add_table_column(label="2")
        dpg.add_table_column(label="3")

        # add_table_next_column will jump to the next row
        # once it reaches the end of the columns
        # table next column use slot 1
        for i in range(0, 4):
            with dpg.table_row(tag="what_what" + str(i)):
                for j in range(0, 3):
                    dpg.add_text(f"Row{i} Column{j}")
    dpg.add_button(label="delete row 1",
                   callback=delete_row_1)
    dpg.add_button(label="delete row 2",
                   callback=delete_row_2)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
