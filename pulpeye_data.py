import numpy as np
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
# import json
# import time
# import socket
# import datetime

SQLITE_DB = "test3.db"


class PulpEyeData:
    look_back = 12
    my_markers = ['.', '.', '^', '*', 'h', '+', 'd']
    my_colors = ['b', 'b', 'y', 'r', 'bn', 'b', 'g']
    latest_SampleTime = datetime(2017, 9, 5, 0, 0, 00)  # latest timestamp in sqlite db for testing

    # sql queries
    max_SampleTime_query = "select max(SampleTime) from pulpeye"
    min_SampleTime_query = "select min(SampleTime) from pulpeye"
    max_BatchID_query = "select max(BatchID) from pulpeye"
    delete_BatchID_query = "DELETE from pulpeye WHERE BatchID = ?"
    validate_BatchID_query = "SELECT CSF, FL, ShiveSum from pulpeye WHERE BatchID = ?"

    query = """select * from pulpeye 
            where SampleTime > :pull_time and SampleTime < :end_time 
            order by BatchID desc"""

    def validate_sample(self, batch, complete=False):
        if complete:
            r = 3
        else:
            r = 2
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.validate_BatchID_query, (batch,))
            valid = c.fetchall()
            valid_flag = True
            for i in range(r):
                print(valid[0][i])
                if valid[0][i] is None:
                    valid_flag = False
            return valid_flag  # return valid status

    def delete_batch(self, batch):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.delete_BatchID_query, (batch,))
            return 0  # return max batchID

    def reset_start_time(self):
        self.latest_SampleTime = datetime.today()
        self.look_back = 12
        self.update()

    def set_start_time(self, date):
        self.latest_SampleTime = date

    def offset_start_time(self, delta):  # delta in days
        self.latest_SampleTime = self.latest_SampleTime + timedelta(delta)
        self.update()

    def max_batch(self):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.max_BatchID_query)
            max_batch = c.fetchall()
            return max_batch[0][0]  # return max batchID

    def latest(self):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.max_SampleTime_query)
            dtstr = c.fetchall()
            dt = datetime.strptime(dtstr[0][0], '%Y-%m-%d %H:%M:%S')
            return dt  # return datetime object

    def earliest(self):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.min_SampleTime_query)
            dtstr = c.fetchall()
            dt = datetime.strptime(dtstr[0][0], '%Y-%m-%d %H:%M:%S')
            return dt  # return datetime object

    def get_data_period_str(self):
        print("latest is {}".format(self.latest_SampleTime))
        print("look back is {} hours".format(self.look_back))

    def update(self):
        self.test_look_back = self.latest_SampleTime - timedelta(hours=self.look_back)
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': self.test_look_back, 'end_time': self.latest_SampleTime})

    def __init__(self):
        self.test_look_back = self.latest_SampleTime - timedelta(hours=self.look_back)
        self.conn = sqlite3.connect(SQLITE_DB)
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': self.test_look_back, 'end_time': self.latest_SampleTime})


if __name__ == '__main__':
    pe = PulpEyeData()
    print("default now is: {}".format(pe.latest_SampleTime))

    # joe = datetime.strptime(pe.latest(), '%Y-%m-%d %H:%M:%S')
    print("Latest Sample in db is {}".format(pe.latest()))
    # print(type(joe))

    print("Instance look back: {}".format(pe.look_back))
    print("Module look back: {}".format(PulpEyeData.look_back))
    print(pe.data.query('SamplePoint == 1'))

    pe.look_back = 168
    pe.update()

    sample = 70292
    print("validate sample {} is: {}".format(sample, pe.validate_sample(sample)))
    sample = 10
    print("validate sample {} is: {}".format(sample, pe.validate_sample(sample, 1)))
    print("Instance look back: {}".format(pe.look_back))
    print("Instance max BatchID: {} sampled at {}".format(pe.max_batch(), pe.latest()))






