# Class PulpEyeData provides QW.py gui app have access to sqlite3 database

import mysql.connector
import sqlite3
import socket
import pandas as pd
import time
from datetime import datetime, timedelta

# Capture Host Name (computer name)
hostname = socket.gethostname()
AT_PHP = False
if hostname == 'uphjan2':
    AT_PHP = True
else:
    print("{} not in PHP domain...  no access to PulpEye database".format(hostname))

SQLITE_DB = "./tests\PulpEye_SQLite.db"


class PulpEyeData:
    look_back = 12
    my_markers = ['.', '.', '^', '*', 'h', '+', 'd']
    my_colors = ['b', 'b', 'y', 'r', 'bn', 'b', 'g']
    latest_SampleTime = datetime(2017, 9, 5, 0, 0, 00)  # latest timestamp in sqlite db for testing
      # latest timestamp in sqlite db for testing

    # sql queries
    max_SampleTime_query = "select max(SampleTime) from pulpeye"
    min_SampleTime_query = "select min(SampleTime) from pulpeye"
    max_BatchID_query = "select max(BatchID) from pulpeye"
    max_BatchID_query_point = "select max(BatchID) from pulpeye WHERE SamplePoint = ?"
    delete_BatchID_query = "DELETE from pulpeye WHERE BatchID = ?"
    validate_BatchID_query = "SELECT PulpName, CSF, FL, ShiveSum, SampleTime from pulpeye WHERE BatchID = ?"

    query = """select * from pulpeye 
            where SampleTime > :pull_time and SampleTime < :end_time 
            order by BatchID desc"""

    def get_status(self):
        dt = datetime.now()
        max = self.max_batch()
        results = self.get_sample_results(max)
        status_msg = "{}  --  Name: {}  CSF: {}  FL: {}  Shives: {}  Sampled at {}".format(dt,
            results[0],
            results[1],
            results[2],
            results[3],
            results[4])
        return status_msg

    def get_PulpEye_data(self, batch):
        sample_list = list()  # create empty list... to hold samples
        if not AT_PHP:
            self.latest_SampleTime = datetime(2017, 10, 7, 6, 0, 00)
            return sample_list
        else:
            pedb = mysql.connector.connect(user='pulpeye_remote', password='pulp',
                                       host='10.11.2.129',
                                       database='PULPEYE')
            pe_cursor = pedb.cursor()
            sqlite_conn = sqlite3.connect(SQLITE_DB)
            sqlite_cursor = sqlite_conn.cursor()
            query_test = ("SELECT bi.PulpName, "
                      "bi.SamplePoint, "
                      "bi.BatchID, "
                      "bi.SampleTime, "
                      "cs.CsfAvg AS CSF, "
                      "fs.LWeightLen as FL, "
                      "ss.Sum1 AS ShiveSum, "
                      "ss.Sum2 AS ShiveWide, "
                      "ss.Sum3 AS ShiveLong "
                      "FROM batchinfo AS bi "
                      "LEFT JOIN csfsummary AS cs "
                      "ON bi.BatchId = cs.BatchId "
                      "LEFT JOIN fibersummary AS fs "
                      "ON bi.BatchId = fs.BatchId "
                      "LEFT JOIN shivesummary AS ss "
                      "ON bi.BatchId = ss.BatchId "
                      "WHERE bi.BatchId > '{}'".format(batch))
            pe_cursor.execute(query_test)
            results = pe_cursor.fetchall()
            for row in results:
                sample = dict()
                for i in range(len(row)):
                    # print("     {}: {}".format(cursor.column_names[i].lower(), row[i]))
                    sample[pe_cursor.column_names[i].lower()] = row[i]
                sample_list.append(sample)
                try:
                    sqlite_cursor.execute("INSERT OR IGNORE INTO pulpeye VALUES (?,?,?,?,?,?,?,?,?)", row)
                except (RuntimeError, TypeError, NameError, IntegrityError):
                    print("SQLITE error on {}".format(row['BatchID']))

            sqlite_cursor.close()
            pedb.close()
            sqlite_conn.commit()
            sqlite_conn.close()
            return sample_list

    def get_sample_results(self, batch):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.validate_BatchID_query, (batch,))
            results = c.fetchall()
            return results[0]

    def validate_sample(self, batch, complete=False):
        if complete:
            r = 4
        else:
            r = 3
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute("select count(*) from pulpeye where BatchID = ?", (batch,))
            count = c.fetchall()[0][0]
            # print("count: {}".format(count))
            if not count:
                valid_flag = False
                return valid_flag
            else:
                c.execute(self.validate_BatchID_query, (batch,))
                valid = c.fetchall()
                valid_flag = True
                for i in range(1, r):
                    # print(valid[0][i])
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
        self.latest_SampleTime = self.latest()
        self.look_back = 12
        self.update()

    def set_start_time(self, date):
        self.latest_SampleTime = date

    def offset_start_time(self, delta):  # delta in days
        self.latest_SampleTime = self.latest_SampleTime + timedelta(delta)
        self.update()

    def get_max_batch_list(self):
        max_list = list()
        for i in range(1, 7):
            maxb = self.max_batch_point(i)
            max_list.append(maxb)
        return max_list

    def max_batch_point(self, pt):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.max_BatchID_query_point, (pt,))
            max_batch_ = c.fetchall()
            return max_batch_[0][0]  # return max batchID

    def max_batch(self):
        with sqlite3.connect(SQLITE_DB) as conn:
            c = conn.cursor()
            c.execute(self.max_BatchID_query)
            max_batch_ = c.fetchall()
            return max_batch_[0][0]  # return max batchID

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
        self.conn = sqlite3.connect(SQLITE_DB)
        self.latest_SampleTime = self.latest()
        self.test_look_back = self.latest_SampleTime - timedelta(hours=self.look_back)
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': self.test_look_back, 'end_time': self.latest_SampleTime})


if __name__ == '__main__':
    pe = PulpEyeData()

    pe.look_back = 168
    pe.update()

    print("SQLite database max BatchID: {} sampled at {}".format(pe.max_batch(), pe.latest()))

    max_batch = pe.max_batch()
    # max_batch = 143056
    for b in range(max_batch, max_batch - 5, -1):
        if not pe.validate_sample(b, False):
            pe.delete_batch(b)
            print("deleted BatchID: {}".format(b))
        else:
            print("validate sample {} is: {}".format(b, pe.validate_sample(b, False)))

    max_batch = pe.max_batch()
    new_samples = pe.get_PulpEye_data(max_batch)
    sample_results = pe.get_sample_results(max_batch)
    print("SQLite database max BatchID: {} sampled at {}".format(pe.max_batch(), pe.latest()))
    print("Sample {}   Name: {}  CSF: {}  FL: {}  Shives: {}  Sampled at {}".format(max_batch, sample_results[0],
        sample_results[1],
        sample_results[2],
        sample_results[3],
        sample_results[4]))

    # print(pe.get_sample_results(13))

    max_batch_list = list()
    for i in range(1, 7):
        maxb = pe.max_batch_point(i)
        max_batch_list.append(maxb)
        print("Max points {} ".format(maxb), end='')
        for _ in range(5):
            print(pe.get_sample_results(maxb)[_], end=', ')
        #pe.get_sample_results(maxb))
        print()
    print(max_batch_list)
    print(len(pe.data))
    tt = pe.data['BatchID'].isin(max_batch_list)
    print(pe.data[tt])
    print(len(tt))


