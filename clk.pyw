import tkinter as tk
from time import localtime
from math import sin, cos, pi

from os import name
if name == 'nt':
    import ctypes
    ES_CONTINUOUS       = 0x80000000
    ES_SYSTEM_REQUIRED  = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)


def draw():
    (_, _, _, hr, mins, secs, _, _, _) = localtime()
    root.title(f"{hr: =2}:{mins:0=2}:{secs:0=2}")
    y_mid = w.winfo_height() // 2
    x_mid = w.winfo_width() // 2
    dial_radius = min(x_mid, y_mid)
    draw_dial(dial_radius, x_mid, y_mid)
    draw_sec_arrow(dial_radius, x_mid, y_mid, secs)
    draw_min_arrow(dial_radius, x_mid, y_mid, mins)
    draw_hr_arrow(dial_radius, x_mid, y_mid, hr, mins)
    w.after(200, draw)


def draw_dial(dial_radius, x_mid, y_mid):
    short_tick, long_tick = dial_radius // 18, dial_radius // 9
    for i, dial_line in enumerate(dial_lines):
        w.itemconfigure(dial_line, width=1 + dial_radius // 50)
        phi = i * pi / 6
        tick_length = long_tick if i % 3 == 0 else short_tick
        w.coords(dial_line, x_mid + (dial_radius - tick_length) * cos(phi), 
                 y_mid + (dial_radius - tick_length) * sin(phi),
                 x_mid + dial_radius * cos(phi), y_mid + dial_radius * sin(phi))


def draw_sec_arrow(dial_radius, x_mid, y_mid, secs):
    w.itemconfigure(secs_arrow, width=1 + dial_radius // 100)
    phi_secs = pi * (15 - secs) / 30
    arrow_lenght = .9 * dial_radius
    w.coords(secs_arrow, x_mid, y_mid, 
             x_mid + arrow_lenght * cos(phi_secs), y_mid - arrow_lenght * sin(phi_secs))


def draw_min_arrow(dial_radius, x_mid, y_mid, mins):
    w.itemconfigure(mins_arrow, width=1 + dial_radius // 60)
    phi_mins = pi * (15 - mins) / 30
    arrow_lenght = 2 / 3 * dial_radius
    w.coords(mins_arrow, x_mid, y_mid, 
             x_mid + arrow_lenght * cos(phi_mins), y_mid - arrow_lenght * sin(phi_mins))


def draw_hr_arrow(dial_radius, x_mid, y_mid, hr, mins):
    hr %= 12
    w.itemconfigure(hr_arrow, width=1 + dial_radius // 30)
    phi_hr = pi * (3 - hr - mins / 60) / 6
    arrow_lenght = 1 / 3 * dial_radius
    w.coords(hr_arrow, x_mid, y_mid, 
             x_mid + arrow_lenght * cos(phi_hr), y_mid - arrow_lenght * sin(phi_hr))


root = tk.Tk()
w = tk.Canvas(root)
root.state("zoomed")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
w.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
secs_arrow = w.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
mins_arrow = w.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
hr_arrow = w.create_line(0, 0, 0, 0, capstyle=tk.ROUND)
dial_lines = [w.create_line(0, 0, 5, 5) for _ in range(12)]
draw()
root.mainloop()
