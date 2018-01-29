import json
import time
import socket
# import threading
import datetime
import pulpeye
from pulpeye_secrets import server_list

hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)


def send_packet(msg):
    for server_address in server_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send data
            print('Destination: {}'.format(server_address))
            print('sending to {!r}'.format(msg))
            sent = sock.sendto(msg, server_address)
        finally:
            print('closing socket')
            sock.close()


packet_string = """
{
    "meta":{
        "packet_time": "2017-12-22 9:05:26",
        "host": "operator",
        "records": 4
        },
    "samples": [
         {
            "name": "Line 1",
            "SamplePoint": 1,
            "sampletime": "2017-12-22 8:05:26",
            "batchID": 1,
            "csf": 130,
            "fl": 1.56,
            "shives_sum": 412
         },
         {
            "name": "Line 3",
            "SamplePoint": 3,
            "sampletime": "2017-12-22 8:05:26",
            "batchID": 2,
            "csf": 135,
            "fl": 1.59,
            "shives_sum": 823
        },
         {
            "name": "Line 2",
            "SamplePoint": 2,
            "sampletime": "2017-12-22 8:06:26",
            "batchID": 3,
            "csf": 140,
            "fl": 1.66,
            "shives_sum": 367
        },
        {
            "name": "Rejects",
            "SamplePoint": 4,
            "sampletime": "2017-12-22 8:06:26",
            "batchID": 5,
            "csf": 140,
            "fl": 1.71,
            "shives_sum": 67
        }
    ]
}
"""

# pe = pulpeye.pulpeye()
# pe.connect_pulpeye()

data = json.loads(pulpeye.packet_string)
samples = data['samples']
meta = data['meta']

print("Original string:\n", packet_string)
while True:
    meta['records'] = 1
    meta['command'] = 0
    meta['show_meta'] = 1
    meta['show_raw'] = 0
    meta['log'] = "empty"
    out = {}
    out['log'] = "Empty log...   Hey Brother... "
    meta['extra_lines'] = 15
    meta['show_meta'] = 0
    meta['records'] = 0
    out['meta'] = meta
    out['samples'] = 0


    new_json = json.dumps(out, indent=2).encode(encoding='utf-8')
    send_packet(new_json)
    send_packet(pulpeye.new_packet())
    meta['extra_lines'] = 1
    meta['show_meta'] = 1
    meta['records'] = 1
    out['samples'] = 1
    # send_packet("test")

    for sample in data['samples']:
        dt = datetime.datetime.now
        meta['packet_time'] = dt.strftime('%Y-%m-%d %H:%M:%S')
        meta['host'] = hostname
        meta['command'] = 0
        # print(meta, sample)
        out['meta'] = meta
        if meta['records'] > 0:
            out['samples'] = sample
        out['log'] = "Sample from " + sample['name'] + " CSF:" + str(sample['csf']) + " FL:" + str(sample['fl'])
        # out['log'] = "Hey Brother..."

        new_json = json.dumps(out, indent=2).encode(encoding='utf-8')
        send_packet(new_json)
        print("packet sent:\n", format(new_json))
        time.sleep(5)

# print(type(new_json))