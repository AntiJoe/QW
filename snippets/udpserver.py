import socket
import logging
import json
import time
from datetime import datetime

# pulpeye_secrets to hold private information
from pulpeye_secrets import HOME

vnum = 0.5
vmsg = "Now on GitHub..."

hostname = socket.gethostname()

UDP_IP = ""
UDP_PORT = 7777

home_msg = "udpserver calling home"
meta = {}
meta['records'] = 1
meta['command'] = 0
meta['show_meta'] = 1
meta['show_raw'] = 0
meta['log'] = "empty"
meta['host'] = hostname
out = {}
out['log'] = "Version {} calling home... ".format(vnum)
meta['extra_lines'] = 15
meta['show_meta'] = 1
meta['uri'] = 'x-sonosapi-hls:r%3aestreetradio?sid=49&amp;flags=8480&amp;sn=8'
meta['records'] = 0
out['meta'] = meta
out['samples'] = 0
new_json = json.dumps(out, indent=2).encode(encoding='utf-8')


def call_home():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Send data
        sent = sock.sendto(new_json, HOME)
    finally:
        print('Called home')
        sock.close()

# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename= "PacketLogger.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger = logging.getLogger()
# logger.info('Packet Receiver rev0.0 started on: {}'.format(hostname))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print("UDP server listening on port: ",UDP_PORT)
print("version: ", vnum)
print("version message: ", vmsg)
print ()
call_home()
print ()
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    # type(data)

    jdata = json.loads(data.decode("utf-8"))
    samples = jdata['samples']
    meta = jdata['meta']
    log = jdata['log']
    # logger.info(log)
    dt = datetime.now()

    if meta['extra_lines'] > 0:
        for i in range(meta['extra_lines']):
            print ()
            if meta['show_raw'] == 1:
                print ("received: ", data)
            print ()
            print ("Packet Received: ", dt.strftime('%Y-%m-%d %H:%M:%S'), " from ", meta['host'])
            if meta['show_meta'] == 1:
                print ("Meta:   ", meta)
            if meta['records'] > 0:
                print ("Sample: ", samples)
            print ("Log:    ", log)
            for i in range(1):
                print ()
	
	

