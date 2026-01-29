#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:40:50 2024

@author: cler
"""
import pymysql

import csv

def db_connect():

# Connect to the database
    conn = pymysql.connect(host='auview.ccm.pitt.edu',
                             user='cler',
                             password='',
                             database='mladi', port=3306, local_infile=1)
    return conn


def writetocsv(tablerows, thisfolder):
    filename = '/ix1/mladi/read/01312024/'+thisfolder+'_ce.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Row_Number,Study_Id,FIN_Study_Id,DATE,UTCOffset,event_name,result_val,result_unit,result_stat,event_tag'])
        for tablerow in tablerows:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(tablerow)
    return()


conn = db_connect()
cursor = conn.cursor()
tablename = 'mladi24.EMR_ce'
emptycefiles = 'empty_files_report.csv'
i = 0
with open(emptycefiles,'r') as emptycefile:
    rows = csv.reader(emptycefile)
    for row in rows:
        thisfolder = row[0].split('/')[4]
        thisencounter = thisfolder[8:]
        query = 'SELECT * FROM ' + tablename + ' where FIN_study_id = ' +thisencounter
        cursor.execute(query)
        tablerows = cursor.fetchall()
        writetocsv(tablerows, thisfolder)
        i += 1
        if i%50 == 0:
            print(i)

cursor.close()
conn.close()