# Quality Window Rev 0
# December 16, 2017
# Newest data: 12/1/2017 13:35

import pulpeye_data
import logging
import socket
import tkinter as tk
from tkinter import *
from tkinter import Tk, Label, Button
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

matplotlib.use("TkAgg")
LARGE_FONT = ('Verdana', 12)
# style.use('ggplot')

# Capture Host Name (computer name)
hostname = socket.gethostname()
AT_PHP = False

if hostname == 'uphjan2':
    AT_PHP = True
else:
    print("{} not in PHP domain...  no access to PulpEye database".format(hostname))

# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename="QWindow.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()
logger.info('QWindow rev0.0 started on: {}'.format(hostname))

# create instance of PulpEyeData to use sqlite3 database
pe = pulpeye_data.PulpEyeData()

df = pe.data

y_ticks = np.arange(1.35, 1.85, 0.05)
y_major = np.arange(1.4, 1.8, 0.1)
y_minor = np.arange(1.35, 1.75, 0.1)

LEGEND_LABEL = ['Manual', 'Line 1', 'Line 2', 'Line 3', 'Rejects', 'MC6', 'MC1']

cross_hairs = [100, 1.55]

f = Figure()
a = f.add_subplot(111)


def update_pe_data():
    max_batch = pe.max_batch()
    new_samples = pe.get_PulpEye_data(max_batch)
    print("Newest updated batchID after refresh is {}".format(pe.max_batch()))
    pe.reset_start_time()
    app.status_bar['text'] = "testing status....."


def test_routine():
    newest_points = pe.get_max_batch_list()
    tt = pe.data['BatchID'].isin(newest_points)
    print(pe.data[tt])
    # a.scatter(tt['CSF'], tt['FL'], alpha=1)

def renew_data(hours):
    pe.look_back = hours
    pe.update()
    pe.get_data_period_str()


def animate(i):
    a.clear()
    df = pe.data
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "Quality Window   past {} hours\n{} --- {}".format(pe.look_back,
                                pe.latest_SampleTime.strftime('%Y-%m-%d %H:%M:%S'),
                                pe.test_look_back)
    a.set_title(title)
    a.legend(df.PulpName)

    for point in range(1, 7):
        dft = pe.data.query('SamplePoint == {}'.format(point))
        a.scatter(dft.CSF, dft.FL, alpha=0.4, marker=pe.my_markers[point], label=LEGEND_LABEL[point])


    a.set_xlim(50, 220)
    a.set_ylim(1.35, 1.8)
    a.grid(True, color='black', linestyle='-', linewidth=0.5, alpha=0.2)
    a.set_ylabel('Fibre Length (mm)\n')
    a.set_xlabel('\nFreeness (ml)')
    a.set_xticks(list(range(50, 230, 10)))
    a.set_yticks(y_ticks)

    # test_routine()

    # cross hairs
    a.plot([120, 120], [1.5, 1.65], 'g-', linewidth=1)
    a.plot([100, 140], [1.575, 1.575], 'g-', linewidth=1)
    a.legend()
    app.status_bar['text'] = pe.get_status()


class QWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "TMP Quality Window")
        tk.Tk.iconbitmap(self, default="PHP.ico")

        self.toolbar = tk.Frame(self, bg="light green")

        # left hand buttons
        self.show_24_button = Button(self.toolbar, text="Show 24 hours", width=15, command=lambda: renew_data(24))
        self.show_24_button.pack(side=LEFT, pady=2, padx=2)
        self.show_12_button = Button(self.toolbar, text="Show 12 hours", width=15, command=lambda: renew_data(12))
        self.show_12_button.pack(side=LEFT, pady=2, padx=2)

        self.status_label = Label(self.toolbar, text='thread test', bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=LEFT)

        # right hand buttons
        self.update_button = Button(self.toolbar, text="Update", width=10, command=lambda: update_pe_data())
        self.update_button.pack(side=RIGHT, pady=2)
        self.test_button = Button(self.toolbar, text="Test", width=10, command=lambda: test_routine())
        self.test_button.pack(side=RIGHT, pady=2)

        self.toolbar.pack(side=TOP, fill=X)

        container = tk.Frame(self, bg="blue")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        settingsmenu = tk.Menu(menubar, tearoff=1)
        settingsmenu.add_command(label="Show last 12 hours", command=lambda: renew_data(24))
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

        self.status_bar = Label(self, text=pe.get_status(), bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)


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
        # label = tk.Label(self, text="Start Page", font=LARGE_FONT)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = QWindow()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
