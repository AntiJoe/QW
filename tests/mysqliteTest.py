# File to create sqlite3 database file for QW project

import sqlite3

conn = sqlite3.connect("PulpEye_SQLite.db")
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE pulpeye
         (PulpName text,
         SamplePoint int,
         BatchID int,
         SampleTime text,
         CSF real,
         FL real,
         ShiveSum int,
         ShiveWide int,
         ShiveLong int)''')

# Insert a row of data
c.execute("CREATE UNIQUE INDEX batchindex ON pulpeye (BatchID)")

c.execute("INSERT INTO pulpeye VALUES ('Line 1', 1, 12, '2018-01-04 8:00:01', 124,1.56, 412, 6, 7)")
c.execute("INSERT INTO pulpeye VALUES ('Line 2', 2, 13, '2018-01-04 8:07:02', 134,1.66, 367, 24, 3)")

conn.commit()

conn.close()


