# Quality Window Rev 0
# December 16, 2017
# Newest data: 12/1/2017 13:35

# import datetime
# import sys
# import time
# import mysql.connector
# import pandas as pd
import pulpeye_data
import sqlite3
from datetime import datetime
import logging
import socket
import tkinter as tk
# from tkinter import ttk
import pandas as pd
import joepulp
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

# Capture Host Name (computer name)
hostname = socket.gethostname()
# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename="QWindow.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()
logger.info('QWindow rev0.0 started on: {}'.format(hostname))

pe = pulpeye_data.PulpEyeData()

df = pe.data

LARGE_FONT = ('Verdana', 12)
# style.use('ggplot')

y_ticks = np.arange(1.35, 1.85, 0.05)
y_major = np.arange(1.4, 1.8, 0.1)
y_minor = np.arange(1.35, 1.75, 0.1)

f = Figure()
a = f.add_subplot(111)

for sample in range(1, 7):
    a.legend(df.PulpName)


def renew_data(hours):
    pe.look_back = hours
    pe.update()
    pe.get_data_period_str()


def animate(i):
    a.clear()
    df = pe.data
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "Quality Window...   past {} hours\nData length: {} records\n{} --- {}".format(pe.look_back,
                                                                                len(pe.data),
                                                                                pe.latest_SampleTime,
                                                                                pe.test_look_back)
    a.set_title(title)
    a.legend(df.PulpName)

    for sample in range(1, 7):
        dft = pe.data.query('SamplePoint == {}'.format(sample))
        a.scatter(dft.CSF, dft.FL, alpha=0.4, marker=pe.my_markers[sample])  # , label=dft.PulpName
        # a.legend()

    a.set_xlim(50, 220)
    a.set_ylim(1.35, 1.8)
    a.grid(True, color='black', linestyle='-', linewidth=0.5, alpha=0.2)
    a.set_ylabel('Fibre Length (mm)\n')
    a.set_xlabel('\nFreeness (ml)')
    a.set_xticks(list(range(50, 230, 10)))
    a.set_yticks(y_ticks)
    # a.legend()


class QWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "TMP Quality Window")
        tk.Tk.iconbitmap(self, default="PHP.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        settingsmenu = tk.Menu(menubar, tearoff=1)
        settingsmenu.add_command(label="Show last 12 hours", command=lambda: renew_data(12))
        settingsmenu.add_command(label="Show last 24 hours", command=lambda: renew_data(24))
        settingsmenu.add_command(label="Show last week", command=lambda: renew_data(168))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Save settings", command=lambda: print("Computer Name: ", hostname))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        timemenu = tk.Menu(menubar, tearoff=1)
        timemenu.add_command(label="Reset to now", command=lambda: pe.reset_start_time())
        timemenu.add_command(label="Back one day", command=lambda: pe.offset_start_time(-1))
        timemenu.add_command(label="Advance one day", command=lambda: pe.offset_start_time(1))
        timemenu.add_command(label="Back one week", command=lambda: pe.offset_start_time(-7))
        timemenu.add_command(label="Advance one week", command=lambda: pe.offset_start_time(7))
        timemenu.add_separator()
        timemenu.add_command(label="Last 24 hours", command=lambda: renew_data(24))
        timemenu.add_command(label="Last 12 hours", command=lambda: renew_data(12))
        timemenu.add_command(label="Last 8 hours", command=lambda: renew_data(8))
        timemenu.add_command(label="Last week", command=lambda: renew_data(168))
        timemenu.add_command(label="Last 4 weeks", command=lambda: renew_data(4*168))
        menubar.add_cascade(label="Time Settings", menu=timemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        logger.debug("StartPage init")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = QWindow()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=500)
app.mainloop()
