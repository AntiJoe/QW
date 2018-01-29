# PulpEye Watch...   January 2018
# watch for new results from PulpEye...  send to plot when new data arrives.
#
# create thread to watch PulpEye
#
#

# imports required
import json
import time
import socket
import threading
import mysql.connector
from datetime import datetime
import pulpeye
from pulpeye_secrets import server_list



server_address = ("127.0.0.1", 7777)

class PulpEyeWatch(threading.Thread):

    def run(self):
        print("PE watcher started")

        while True:
            dt = datetime.now()
            print(dt)
            message = '{:%b %d, %Y  %H:%M:%S}'.format(dt).encode(encoding='utf-8')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            try:
                # Send data
                print('sending {!r}'.format(message))
                sent = sock.sendto(message, server_address)
            finally:
                print('closing socket')
                sock.close()

            time.sleep(5)




pe_watcher = PulpEyeWatch(name="PulpEye Watcher")
pe_watcher.setDaemon(True)

pe_watcher.start()
print("Running {} threads".format(threading.active_count()))
time.sleep(30)