# pulpeye v2 Jan 2018

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
            "PulpName": "Line 1",
            "SamplePoint": 1,
            "sampletime": "2017-12-22 8:05:26",
            "BatchID": 1,
            "csf": 130,
            "fl": 1.56,
            "shives_sum": 412
         },
         {
            "PulpName": "Line 3",
            "SamplePoint": 3,
            "SampleTime": "2017-12-22 8:05:26",
            "BatchID": 2,
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
        "packet_time": "2017-12-29 9:05:26",
        "host": "Null",
        "records": 0,
        "command" : 0,
        "show_meta" : 1,
        "show_raw" : 0,
        "log" : "empty",
        "extra_lines" : 15
        },
    "samples": [
         {
            "pulpname": "sample1",
            "samplepoint": 1,
            "sampletime": "2018-01-01 8:05:26",
            "batchid": 0,
            "csf": 0,
            "fl": 0,
            "shivesum": 0
         },
         {
            "pulpname": "sample1",
            "samplepoint": 1,
            "sampletime": "2018-01-01 8:05:26",
            "batchid": 0,
            "csf": 0,
            "fl": 0,
            "shivesum": 0
         }
         ]        
}
"""

packet_json_new = json.loads(packet_string_new)


def create_new_packet_dict():
    dt = datetime.datetime.now()
    meta = dict()
    meta['packet_time'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    meta['host'] = hostname
    meta['records'] = 0
    meta['command'] = 0
    meta['log'] = "Empty..."

    meta['show_meta'] = 0 # for testing only
    meta['show_raw'] = 0  # for testing only
    meta['extra_lines'] = 10 # for testing only

    samples = packet_json_new['samples']

    out = dict()
    out['meta'] = meta
    out['samples'] = samples
    # out['log'] = "Empty log..."

    # new_json_out = json.dumps(out, indent=2).encode(encoding='utf-8')
    return out


testpacket = create_new_packet_dict()
new_json_out = json.dumps(testpacket, indent=4)

# print("Test 1 {}".format(testpacket))
print("Test packet {}".format(new_json_out.__str__()))


class pulpeye():
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

# print(packet_json_new)
# pe = pulpeye()
# print("test\n", pe.out)
# time.sleep(1)
# # pe.new_packet()
# print("test2\n", pe.out)