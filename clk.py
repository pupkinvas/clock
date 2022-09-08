#! /usr/bin/env python3

import tkinter as tk
from time import localtime
from math import sin, cos, pi
from os import name


cos_table12 = [cos(i * pi / 6) for i in range(12)]
sin_table12 = [sin(i * pi / 6) for i in range(12)]
cos_table60 = [cos(pi * (15 - i) / 30) for i in range(60)]
sin_table60 = [sin(pi * (15 - i) / 30) for i in range(60)]

hr = mins = secs = y_mid = x_mid = dial_radius = 0


def draw():
    global hr, mins, secs, y_mid, x_mid, dial_radius
    (_, _, _, hr, mins, secs, _, _, _) = localtime()
    root.title(f"{hr: =2}:{mins:0=2}:{secs:0=2}")
    hr %= 12
    y_mid = w.winfo_height() // 2
    x_mid = w.winfo_width() // 2
    dial_radius = min(x_mid, y_mid)
    draw_dial()
    draw_sec_arrow()
    draw_min_arrow()
    draw_hr_arrow()
    w.after(200, draw)


def draw_dial():
    short_tick, long_tick = dial_radius // 18, dial_radius // 9
    for i, dial_line in enumerate(dial_lines):
        w.itemconfigure(dial_line, width=1 + dial_radius // 50)
        tick_length = long_tick if i % 3 == 0 else short_tick
        w.coords(dial_line, x_mid + (dial_radius - tick_length) * cos_table12[i], 
                 y_mid + (dial_radius - tick_length) * sin_table12[i],
                 x_mid + dial_radius * cos_table12[i], y_mid + dial_radius * sin_table12[i])


def draw_sec_arrow():
    w.itemconfigure(secs_arrow, width=1 + dial_radius // 100)
    arrow_length = .9 * dial_radius
    w.coords(secs_arrow, x_mid, y_mid, 
             x_mid + arrow_length * cos_table60[secs], y_mid - arrow_length * sin_table60[secs])


def draw_min_arrow():
    w.itemconfigure(mins_arrow, width=1 + dial_radius // 60)
    arrow_length = 2 / 3 * dial_radius
    w.coords(mins_arrow, x_mid, y_mid, 
             x_mid + arrow_length * cos_table60[mins], y_mid - arrow_length * sin_table60[mins])


def draw_hr_arrow():
    w.itemconfigure(hr_arrow, width=1 + dial_radius // 30)
    i = 5 * hr + mins // 12
    arrow_length = 1 / 3 * dial_radius
    w.coords(hr_arrow, x_mid, y_mid, 
             x_mid + arrow_length * cos_table60[i], y_mid - arrow_length * sin_table60[i])


root = tk.Tk()
w = tk.Canvas(root)
if name == 'nt':
    import ctypes
    ES_CONTINUOUS       = 0x80000000
    ES_SYSTEM_REQUIRED  = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)
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
