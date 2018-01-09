# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 17:46:54 2017

@author: joe
"""
import datetime
import mysql.connector
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# from ggplot import *

# df = pd.read_csv('pe.csv')
# df.head()
#
# df2 = df[(df.week_num.isin ([47])) & \
#          (df.SamplePoint<8) & \
#          (df.SamplePoint>0) & \
#          (df.millday == 'Tuesday')]
# df2.tail()
#
#
# def animate(i):
#
#     a.clear()
#     # a.plot(df2.CSF, df2.FL)
#     # a.plot_date(sellDates, sells["price"], "#183A54", label="sells")
#     a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
#              ncol=2, borderaxespad=0)
#
#     title = "BTC-e BTCUSD Prices\nLast Price: " + str(data["price"][1999])
#     a.set_title(title)


# plt.scatter(df2.CSF, df2.FL, c = df2.SamplePoint, alpha=0.4)
# plt.ylabel('\nFibre Length (mm)')
# plt.xlabel('Freeness (ml)\n')
# plt.xticks()
# plt.title('Quality Window\nFreeness vs Fibre Length\n')
# plt.legend(df.PulpName)
# plt.grid()
# plt.show()


#g = ggplot(df2) + \
#    aes('CSF', 'FL',colour='factor(SamplePoint)') + \
#    geom_point()+ \
#    labs(x="\nFreeness (ml)", \
#       y="Fibre Length (mm)\n", \
#       title="title")+ \
#    theme_bw()
#print(g)
#    
#    
#f = ggplot(df2, aes('CSF', 'FL',colour='factor(SamplePoint)')) + \
#    geom_point()+ \
#    labs(x="\nFreeness (ml)", \
#       y="Fibre Length (mm)\n", \
#       title="title")+ \
#    theme_bw()
#print(f)
sqlpullTo = datetime.datetime(2017, 1, 1, 4, 40, 0)

pedb = mysql.connector.connect(user='pulpeye_remote', password='pulp',
                              host='10.11.2.129',
                              database='PULPEYE')
cursor = pedb.cursor()

QUERY = ("SELECT bi.PulpName, "
         "bi.BatchID, bi.LABELTEXT, bi.SampleTime, "
         "cs.CsfAvg AS CSF, "
         "fs.FiberConc, "
         "ss.Sum1 AS ShiveSum, "
         "ss.Sum2 AS ShiveWide, "
         "ss.Sum3 AS ShiveLong, "
         "bi.ResultTime, "
         "bi.SampleTime, "
         "fs.FinesShare, "
         "cs.TempWater, "
         "fs.LWeightLen as FL, "
         "bi.SamplePoint, "
         "cs.CsfWater, "
         "fs.LenFrac1 as Fines, "
         "fs.LenFrac2 as r100, "
         "fs.LenFrac3 as r48, "
         "fs.LenFrac4 as r28, "
         "fs.LenFrac5 as r14, "
         "bi.AfterPrepConc, "
         "fs.LWeightCurl as LWCurl, "
         "fs.ArithmCurl as AWCurl "
         "FROM batchinfo AS bi "
         "LEFT JOIN csfsummary AS cs "
         "ON bi.BatchId = cs.BatchId "
         "LEFT JOIN fibersummary AS fs "
         "ON bi.BatchId = fs.BatchId "
         "LEFT JOIN shivesummary AS ss "
         "ON bi.BatchId = ss.BatchId "
         "WHERE bi.SampleTime > '{}'").format(str(sqlpullTo))

QUERY_MIN = ("SELECT bi.PulpName, "
             "bi.BatchID, bi.SampleTime, "
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
             "WHERE bi.SampleTime > '{}'").format(str(sqlpullTo))

query_test = ("SELECT bi.PulpName, "
             "bi.SamplePoint, "
             "bi.BatchID, "
             "bi.SampleTime, "   
             "cs.CsfAvg AS CSF, "
             "fs.LWeightLen as FL, "
             "ss.Sum1 AS ShiveSum "
             "FROM batchinfo AS bi "
             "LEFT JOIN csfsummary AS cs "
             "ON bi.BatchId = cs.BatchId "
             "LEFT JOIN fibersummary AS fs "
             "ON bi.BatchId = fs.BatchId "
             "LEFT JOIN shivesummary AS ss "
             "ON bi.BatchId = ss.BatchId "
             "WHERE bi.SampleTime > '{}'").format(str(sqlpullTo))

query_test2 = ("SELECT bi.PulpName, "
             "bi.BatchID, "
             "bi.SampleTime "            
             "FROM batchinfo AS bi "
             "WHERE bi.SampleTime > '{}'").format(str(sqlpullTo))

print(query_test)
cursor.execute(query_test)

# Query results
results = cursor.fetchall()

pe = pd.DataFrame(results, columns = cursor.column_names)
    
# print(cursor.column_names)
# print(cursor.rowcount)
# print(cursor.__dict__)

conn = sqlite3.connect("test3.db")
cc = conn.cursor()

#######################################################################
#   should end up in pulpeye.py
#

samples = dict()    # create empty samples dictionary
sampleList = list() # create empty list... to hold samples
c = 0               # initialize counter of samples (rows)  {remove in final}

# Query results into rows of sample data...  then load into dictionary of samples
for row in results:
    sample = dict()

    for i in range(len(row)):
        # print("     {}: {}".format(cursor.column_names[i].lower(), row[i]))
        sample[cursor.column_names[i].lower()] = row[i]

    sampleList.append(sample)

    cc.execute("INSERT INTO pulpeye VALUES (?,?,?,?,?,?,?)", row)
########################################################################

    # print(sample)                    # for testing...  {remove in final}
    # print("row:{} ".format(c), row)  # for testing...  {remove in final}
    c = c + 1                        # for testing...  {remove in final}

#########################################################################


# print(sampleList)
cursor.close()
pedb.close()

conn.commit()

conn.close()










