# pulpeye

import json
import time
import socket
import datetime

from pulpeye_secrets import server_list

hostname = socket.gethostname()

# pedb = mysql.connector.connect(user='pulpeye_remote', password='pulp',
#                               host='10.11.2.129',
#                               database='PULPEYE')

SQLpullTo = datetime.datetime(2017, 12, 28, 7, 0, 0)

QUERY_MIN = ("SELECT bi.PulpName, "
             "bi.BatchID, bi.LABELTEXT, bi.SampleTime, "
             "cs.CsfAvg AS CSF, "
             "ss.Sum1 AS ShiveSum, "
             "ss.Sum2 AS ShiveWide, "
             "ss.Sum3 AS ShiveLong, "
             "bi.ResultTime, "
             "bi.SampleTime, "
             "fs.LWeightLen as FL, "
             "bi.SamplePoint, "
             "fs.LenFrac1 as Fines, "
             "fs.LenFrac2 as r100, "
             "fs.LenFrac3 as r48, "
             "fs.LenFrac4 as r28, "
             "fs.LenFrac5 as r14, "
             "bi.AfterPrepConc "
             "FROM batchinfo AS bi "
             "LEFT JOIN csfsummary AS cs "
             "ON bi.BatchId = cs.BatchId "
             "LEFT JOIN fibersummary AS fs "
             "ON bi.BatchId = fs.BatchId "
             "LEFT JOIN shivesummary AS ss "
             "ON bi.BatchId = ss.BatchId "
             "WHERE bi.SampleTime > '{}'").format(str(SQLpullTo))

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

packet_string_new = """
{
    "meta":{
        "packet_time": "2017-12-22 9:05:26",
        "host": "Null",
        "records": 0,
        "command" : 0,
        "show_meta" : 1,
        "show_raw" : 0,
        "log" : "empty",
        "extra_lines" : 15
        },
    "samples": 
         {
            "name": "sample1",
            "SamplePoint": 1,
            "sampletime": "2017-12-22 8:05:26",
            "batchID": 0,
            "csf": 0,
            "fl": 0,
            "shives_sum": 0
         }    
}
"""

packet_json_new = json.loads(packet_string_new)
samples = packet_json_new['samples']
meta = packet_json_new['meta']
meta['host'] = hostname

def new_packet():
    meta = dict()
    samples = dict()
    out = dict()
    out['meta'] = meta
    out['samples'] = samples
    out['log'] = "Empty log..."
    new_json_out = json.dumps(out, indent=2).encode(encoding='utf-8')
    return new_json_out


class pulpeye:
    out = {}
    out2 = {}
    def __init__(self):
        self.packet_json_new = json.loads(packet_string_new)
        self.samples = self.packet_json_new['samples']
        self.meta = self.packet_json_new['meta']
        self.meta['host'] = hostname

    def connect_pulpeye(self):
        pass

    def meta_update(self):
        meta['packet_time'] = now

    def add_sample(self):
        pass

    def new_packet(self):
        now = datetime.now()
        self.meta['packet_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
        self.out['log'] = "Empty log...   Hey Brother... "
        self.out['meta'] = meta
        self.out['samples'] = samples
        self.out['log'] = "Hey Brother.."
        # return self.out


    def build_packet(self):
        pass

    def send_packet(self):
        pass


print(packet_json_new)
pe = pulpeye()

print("test\n", pe.out)
time.sleep(1)
# pe.new_packet()
print("test2\n", pe.out)