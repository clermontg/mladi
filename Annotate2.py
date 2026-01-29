#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:52:31 2024

@author: cler
"""
import os
import csv
import pandas as pd
import glob
import time
from datetime import datetime

def tpfields(tp):
    filetype=['_n','_w','_e']
    fields=[['Label','MaxSN', 'MinSN', 'Counts', 'Density', 'Duration', 'Patid', 'Finid', 'Value_mean','Value_median', 'Value_std', 'Value max', 'Value min'],
           ['Label,''MaxSN', 'MinSN', 'Counts', 'Density', 'Duration', 'Patid', 'Finid'],
            ['Label','MaxSN', 'MinSN', 'Counts', 'Density', 'Duration', 'Patid', 'Finid']
             ]
    x = filetype.index(tp)
    s = fields[x][:]
    return(s)
              
def in_tpfiles(tp):
    filetype=['_n','_w','_e']
    in_type = ['_numericvalue','_wavesample','_enumerationvalue']
    x = filetype.index(tp)
    s = in_type[x]
    return(s)

def ref(x):
    y = x.split('_')
    u = y[len(y)-1]
    subs = ['numeric','wave','enumeration']
    for s in subs:
        if s in u:
            y[len(y)-1] = s + '.csv'
    delim = "_"
    temp = list(map(str, y))
    return(delim.join(temp))
              
def indname(tp, y):
    filetype=['_n','_w','_e']
    x = filetype.index(tp)    
    foi = [['NumericId'],['WaveId', 'Wave_ID'],['EnumerationId', 'Enumeration_ID']]
    soi = foi[x]
    u=[]
    for s in soi:
        if s in y:
            u = s
    return(u)

def sn(x): # transforms a data into SequenceNumber
    # as = pd.Series(pd.datetime(x[:19], format='%Y-%m-%d %H:%M:%S')) 
    dt = pd.to_datetime(x.str[:19], format='%Y-%m-%d %H:%M:%S', utc=None)
    base = pd.to_datetime('2000-01-01 00:00:00', format='%Y-%m-%d %H:%M:%S', utc=None)
    y = (dt - base).dt.total_seconds()
    x = y * 1000 +pd.to_numeric(x.str[20:23]) + pd.to_numeric(x.str[24:27])*3600000
    return(x)

def contains_seven_consecutive_caps(s):
    # Use regular expression to search for a substring of seven consecutive uppercase letters
    import re
    return 1 if re.search(r'[A-Z]{7,}', s) else 0

srccsv = r"/ix1/mladi/Pitt"
tgtdir = "/ix1/mladi/work/cler/"
newdirlist = [f.path for f in os.scandir(srccsv) if f.is_dir()]
outtypelist = ['_n', '_w', '_e']
infiletype = ['_numeric', '_wave', '_enumeration', '_enum']
delim = ','

for dir in newdirlist:
    if contains_seven_consecutive_caps(dir) == 0: # Only do new subjectid's
        continue
    os.chdir(dir)
    for file in glob.glob("*" + infiletype + ".csv"):
        for otp in outtypelist:
            demofields = tpfields(otp)
            outfile = tgtdir + otp + '.csv'
            # Since file opening, writing, and closing happen inside the loop, ensure they are properly managed.
            with open(outfile, 'a') as tfile:
                # tfile.write(delim.join(demofields) + "\n")
                pass  # Assuming your actual code for writing to tfile here
            
            oldfilelist = tgtdir + 'old' + otp + '.csv'
            newfilelist = tgtdir + 'new' + otp + '.csv'
            ftype = in_tpfiles(otp)

            with open(oldfilelist) as f:
                oldfiles = [line.rstrip() for line in f]
            filelist = [file for file in glob.glob("*" + ftype + ".csv") if file not in oldfiles]

            print('There are ', str(len(filelist)), ' ', otp, ' files to process')

            for file in filelist:
                print(file)
                with open(newfilelist, 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter='\n')
                    writer.writerow([file])  # Update file list

                # File processing logic here...

            # After processing each file for this output type, update file lists accordingly
            os.system(f'cat {newfilelist} >> {oldfilelist}')
            os.system(f'> {newfilelist}')