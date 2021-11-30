from dearpygui.dearpygui import *

def callback():
    configure_item(888, show=False)
    configure_item(999, show=True)


with window(id=888, label="POP2", modal=True, show=False, no_resize=True, no_move=True, no_close=True,
            width=200, height=300):
        add_button(label="Cancel", width=75,
                   callback=callback)

with window(id=999, label="POP1", modal=True, show=False, no_resize=True, no_move=True, no_close=True,
            width=200, height=300):
        add_button(label='pop2', callback=lambda: configure_item(888, show=True))
        add_button(label="Cancel", width=75,
                   callback=lambda: configure_item(999, show=False))

with window(label='test') as win:
    add_button(label='pop1', callback=lambda: configure_item(999, show=True))

set_primary_window(win, True)
start_dearpygui()