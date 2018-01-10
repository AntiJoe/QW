import sqlite3
import datetime
import time

# conn = sqlite3.connect('testdb.db')
conn = sqlite3.connect("test3.db")
c = conn.cursor()

# Create table

# c.execute('''CREATE TABLE pulpeye
#          (PulpName text,
#          SamplePoint int,
#          BatchID int,
#          SampleTime text,
#          CSF real,
#          FL real,
#          ShiveSum int)''')

# c.execute('''
#
# ''')

# Insert a row of data
# c.execute("INSERT INTO pulpeye VALUES ('Line 1', 1, 12, '2018-01-04 8:00:01', 124,1.56, 412)")
# c.execute("INSERT INTO pulpeye VALUES ('Line 2', 2, 13, '2018-01-04 8:07:02', 134,1.66, 367)")
# c.execute("CREATE UNIQUE INDEX batchindex ON pulpeye (BatchID)")

# c.execute("""select * from pulpeye
#         where SampleTime > '2018-01-04' and
#         SamplePoint == 4
#         order by BatchID desc""")
#
# for r in c.fetchall():
#     print(r)
#     # time.sleep(1)
#
# print("result has: {} rows".format(c.rowcount))
# # Save (commit) the changes
# conn.commit()


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

SQLpullTo = datetime.datetime(2018, 1, 5, 10, 0, 0)

query = """SELECT * FROM pulpeye 
        WHERE SampleTime > :pulltime and 
        SamplePoint != 0 and
        SamplePoint < 7
        ORDER by BatchID desc"""

parameters = {
    'keys': "CSF, FL ",
    'line': 3,
    'pulltime': SQLpullTo
}


def pull_data():
    c.execute(query, parameters)
    return c.fetchall()


df = pull_data()

for row in df:
    print(row)

conn.close()


