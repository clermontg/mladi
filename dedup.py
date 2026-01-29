#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 12:03:23 2023

@author: cler
"""

import glob
import os
from collections import deque

def deduphead(filename):
    # Open the file in read mode and read lines    
    dups = False
    with open(filename, 'r') as file:
        lines = file.readlines()   
    # Find the index of the second occurrence of the header (assuming the header is the first line)
    header = lines[0]
    try:
        second_header = lines[1]
    except:
        second_header = None  # Header was not found a second time
    # If the header was found a second time, remove it
    if header == second_header:
        dups = True
    if second_header is not None and dups:
        del lines[1]
        print(filename+' header deduped')
    # Write the modified lines back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)
        
def remove_nearby_duplicates(filename, window_size=20):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    past_lines = deque(maxlen=window_size)
    duplicate_count = 0

    for line in lines:
        if line not in past_lines:
            new_lines.append(line)
        else:
            duplicate_count += 1
        past_lines.append(line)

    # Write the modified lines back to the file
    with open(filename, 'w') as file:
        file.writelines(new_lines)
    if duplicate_count > 0:
        print(str(duplicate_count),'duplicates removed in file ',filename)

    
tgtdir = "/ix1/mladi/read/"
cdir = "/ix1/mladi/work/cler/"
dirlist = [f.path for f in os.scandir(tgtdir) if f.is_dir()]
olddirlist =  cdir+'dumpeddirs_in3.csv'
tplist = ["_wave","_numeric","_enum"]


with open(olddirlist,"r+") as f:
    olddumps = [line.rstrip() for line in f]
 # creates the sets of directories that have not been copied to /ix1/mladi/read yet
    newdirlist = list(set(dirlist) - set(olddumps))
    for tdir in newdirlist:
        f.write(tdir+'\n')
    f.close()    


# run the folders,
for tdir in newdirlist:
    print(tdir)
    dumpdate = tdir.split('/')[4]
    if not dumpdate.lower().islower(): # Only those folders that look like dates 
        if not os.path.exists(tgtdir+dumpdate):
            os.mkdir(tgtdir+dumpdate) # Create the folder in read,
        os.chdir(tdir)  
        # build list of type-specific files and prefixes in this folder
        tpindex = 0
        for tp in tplist:
            print(tp)
            for file in glob.glob('*'+tp+'.csv'): # All the files of that type in this folder,
                deduphead(file)
                remove_nearby_duplicates(file)
   