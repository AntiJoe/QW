import socket
import sys
import time
import threading
from datetime import datetime
from tkinter import *

localhost = '127.0.0.1'
root = Tk()
dt = datetime.now()
print(dt)

global ThreadFlag
ThreadFlag = True


class JoesPacketSend(threading.Thread):
    def run(self):
        print('Started Joe')
        while True:
            dt = datetime.now()
            print(dt)
            message = '{:%b %d, %Y  %H:%M:%S}'.format(dt).encode(encoding='utf-8')

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            server_address = ("127.0.0.1", 7777)

            try:
                # Send data
                print('sending {!r}'.format(message))
                sent = sock.sendto(message, server_address)

            finally:
                print('closing socket')
                sock.close()
            time.sleep(10)
            if not ThreadFlag:
                break


joe = JoesPacketSend(name="Joe's packet send")


def startjoe():
    joe.setDaemon(True)
    if joe.is_alive():
        ThreadFlag = False
        print("trying to stop joe")
    else:
        joe.start()


bn1 = Button(root, text = "Start Joe", command = startjoe)
bn1.pack()
bn2 = Button(root, text = "Test", command = lambda: print("Test"))
bn2.pack()
bn3 = Button(root, text = "Quit", command = quit)
bn3.pack()


root.geometry("220x120")
root.mainloop()
