import numpy as np
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
# import json
# import time
# import socket
# import datetime


class PulpEyeData:
    look_back = 12

    my_markers = ['.', 'o', '^', '+', 's', '+', '^']

    latest_SampleTime = datetime(2017, 9, 5, 13, 50, 00)  # latest timestamp in sqlite db for testing

    max_SampleTime_query = "select max(SampleTime) from pulpeye"
    min_SampleTime_query = "select min(SampleTime) from pulpeye"

    query = """select * from pulpeye 
            where SampleTime > :pull_time and SampleTime < :end_time 
            order by BatchID desc"""

    def latest(self):
        conn = sqlite3.connect("./tests/test3.db")
        c = conn.cursor()
        c.execute(self.max_SampleTime_query)
        dtstr = c.fetchall()
        dt = datetime.strptime(dtstr[0][0], '%Y-%m-%d %H:%M:%S')
        conn.close()
        return dt  # return datetime object

    def earliest(self):
        conn = sqlite3.connect("./tests/test3.db")
        c = conn.cursor()
        c.execute(self.min_SampleTime_query)
        dtstr = c.fetchall()
        dt = datetime.strptime(dtstr[0][0], '%Y-%m-%d %H:%M:%S')
        conn.close()
        return dt  # return datetime object

    def get_data_period_str(self):
        print("latest is {}".format(self.latest()))
        print("earliest is {}".format(self.earliest()))

    def update(self):
        self.test_look_back = self.latest_SampleTime - timedelta(hours=self.look_back)
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': self.test_look_back, 'end_time': self.latest_SampleTime})

    def __init__(self):
        self.test_look_back = self.latest_SampleTime - timedelta(hours=self.look_back)
        self.conn = sqlite3.connect("./tests/test3.db")
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': self.test_look_back, 'end_time': self.latest_SampleTime})


if __name__ == '__main__':
    pe = PulpEyeData()
    print("default now is: {}".format(pe.latest_SampleTime))

    # joe = datetime.strptime(pe.latest(), '%Y-%m-%d %H:%M:%S')
    print("Latest Sample in db is {}".format(pe.latest()))
    # print(type(joe))

    print("Instance look back: {}".format(pe.look_back))
    print("Module look back: {}".format(PulpEyeData.look_back))
    print(pe.data.query('SamplePoint == 4'))

    pe.look_back = 168
    pe.update()

    print("Instance look back: {}".format(pe.look_back))
    print("Module look back: {}".format(PulpEyeData.look_back))
    print(len(pe.data))
    # print(pe.data)





