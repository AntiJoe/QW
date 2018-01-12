# Quality Window Rev 0
# December 16, 2017
# Newest data: 12/1/2017 13:35

# import datetime
# import sys
# import time
# import mysql.connector
# import pandas as pd

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
# from matplotlib import style
# import urllib
# import json


# Capture Host Name (computer name)
hostname = socket.gethostname()
# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename= "QWindow.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger = logging.getLogger()
logger.info('QWindow rev0.0 started on: {}'.format(hostname))
conn = sqlite3.connect("./tests/test3.db")
query = """select * from pulpeye 
        where SampleTime > :pull_time 
        order by BatchID desc"""

SQLpullTo = datetime(2018, 1, 1, 10, 0, 0)


def refresh_data(query_in, params_dict):
    data = pd.read_sql_query(query_in, conn, params=params_dict)
    return data


def update_data(query_in, hours_back):
    params_dict = {'pull_time': hours_back}
    data = pd.read_sql_query(query_in, conn, params=params_dict)
    return data


def changeLine(hr):
    global df
    query_dict = {'line': hr, 'pull_time': SQLpullTo}
    df = refresh_data(query, query_dict)
    print(df.head())


global df
df = refresh_data("""select * from pulpeye 
        where SampleTime > :pull_time 
        order by BatchID desc""", {'pull_time': SQLpullTo})

print(df.head())

LARGE_FONT = ('Verdana', 12)
# style.use('ggplot')

y_ticks = np.arange(1.35, 1.85, 0.05)
y_major = np.arange(1.4, 1.8, 0.1)
y_minor = np.arange(1.35, 1.75, 0.1)

f = Figure()
a = f.add_subplot(111)


def LookBack(hours):
    global df
    df = update_data(query, hours)
    print(hours)


def animate(i):
    a.clear()
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "Quality Window"
    a.set_title(title)
    a.scatter(df.CSF, df.FL, c=df.SamplePoint, alpha=0.5, marker='.')
    a.set_xlim(50, 220)
    a.set_ylim(1.35, 1.8)
    a.grid(True, color='black', linestyle='-', linewidth=0.5, alpha=0.2)
    a.set_ylabel('Fibre Length (mm)\n')
    a.set_xlabel('\nFreeness (ml)')
    a.set_xticks(list(range(50, 230, 10)))
    a.set_yticks(y_ticks)
    # a.set_yticks(y_minor, minor=True)
    a.legend(df.PulpName)


class QWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "TMP Quality Window")
        tk.Tk.iconbitmap(self, default="PHP.ico")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        settingsmenu = tk.Menu(menubar, tearoff=1)
        settingsmenu.add_command(label="Show All", command=lambda: changeLine(0))
        settingsmenu.add_command(label="Show Line 1", command=lambda: changeLine(1))
        settingsmenu.add_command(label="Show Line 2", command=lambda: changeLine(2))
        settingsmenu.add_command(label="Show Line 3", command=lambda: changeLine(3))
        settingsmenu.add_command(label="Show Rejects", command=lambda: changeLine(4))
        settingsmenu.add_command(label="Show MC 1", command=lambda: changeLine(6))
        settingsmenu.add_command(label="Show MC 6", command=lambda: changeLine(5))
        settingsmenu.add_command(label="Show last 12 hours", command=lambda: LookBack(12))
        settingsmenu.add_command(label="Show last 24 hours", command=lambda: LookBack(24))
        settingsmenu.add_command(label="Show last week", command=lambda: LookBack(joepulp.admtpd(1000, 3)))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Save settings", command=lambda: print("Computer Name: ", hostname))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        timemenu = tk.Menu(menubar, tearoff=1)
        timemenu.add_command(label="Last 24 hours", command=lambda: print("Samples from {} hours ago".format(24)))
        timemenu.add_command(label="Last 12 hours", command=lambda: print("Samples from {} hours ago".format(12)))
        timemenu.add_command(label="Last 8 hours", command=lambda: print("Samples from {} hours ago".format(8)))
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
        # label.pack(pady=10, padx=10)

        # button2 = ttk.Button(self, text="Exit",
        #                      command=quit)
        # button2.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = QWindow()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
