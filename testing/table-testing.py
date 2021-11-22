import dearpygui.dearpygui as dpg

dpg.create_context()


def clipper_toggle(sender):
    dpg.configure_item("table_clip", clipper=dpg.get_value(sender))


with dpg.window(label="Tutorial"):
    dpg.add_checkbox(label="clipper", callback=clipper_toggle, default_value=True)

    with dpg.table(header_row=False, tag="table_clip", clipper=True):

        for i in range(5):
            dpg.add_table_column()

        for i in range(30000):
            with dpg.table_row():
                for j in range(5):
                    dpg.add_text(f"Row{i} Column{j}")

dpg.show_metrics()

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()