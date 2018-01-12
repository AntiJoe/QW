import numpy as np
import sqlite3
import pandas as pd
from datetime import datetime
import json
import time
import socket
import datetime


class PulpEyeData:

    query = """select * from pulpeye 
            where SampleTime > :pull_time 
            order by BatchID desc"""

    def set_look_back(self, hours):
        look_back_hours = hours
        return {'pull_time': hours}


    def update(self):
        self.data = pd.read_sql_query(self.query, self.conn, params=set_look_back(self.look_back_hours))

    def __init__(self, hours):
        self.look_back_hours = hours
        self.conn = sqlite3.connect("./tests/test3.db")
        self.data = pd.read_sql_query(self.query, self.conn, params={'pull_time': hours})


if __name__ == '__main__':
    pe = PulpEyeData(24)

    print(pe.look_back_hours)
    print(pe.data)




