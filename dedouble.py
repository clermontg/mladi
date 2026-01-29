#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 18:07:00 2024

@author: cler
"""
import os
import csv
from datetime import datetime, timedelta
import pytz

def find_csv_files(source_folder):
    matching_files = []

    for root, dirs, files in os.walk(source_folder):
        # Check if the folder name starts with a capital letter A-Z
        for file in files:
            # Check if the file ends with 'num.csv' or 'wav.csv'
            if file.endswith('_cleaned.csv'):
                tfile = file.split('.')[0][:-8]+'.csv'
#                if file.endswith('value.csv') or file.endswith('sample.csv') or file.endswith('alert.csv'):
                full_path = os.path.join(root, file)
                tfull_path = os.path.join(root, tfile)
                os.rename(full_path, tfull_path)
                matching_files.append(tfull_path)

    return matching_files

def read_csv_to_set(file_path):
    line_set = set()

    try:
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Convert row (a list of columns) to a single string
                row_string = ','.join(row)
                line_set.add(row_string)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return line_set


def write_to_csv(csv_files, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for csv_file in csv_files:
            writer.writerow([csv_file])
        
def clean_csv(input_filename, output_filename, indices ):
    epoch = datetime(2000, 1, 1, 12, 00,00, 000000, tzinfo=pytz.utc)
    i = 0
    try:
        with open(input_filename, 'r', newline='', encoding='utf-8') as csvfile, \
             open(output_filename, 'w', newline='') as outfile:
    
            reader = csv.reader(csvfile, quotechar='"', escapechar = '\\')
            writer = csv.writer(outfile)
            header = next(reader)
            writer.writerow(header)
            snindex = indices[0]
            tsindex = indices[1]
    
            for line in reader:
                i += 1
    
                try:
                    sn = int(line[snindex]) 
                    zone = int(line[tsindex][24:27])
                except:
                    print(i)
                    print(line[14], line[2])
                    print(line)
                dt = datetime.strptime(line[tsindex][:23], "%Y-%m-%d %H:%M:%S.%f")
                dt_utc = (dt- timedelta(hours=zone)).replace(tzinfo=pytz.utc)
                milliseconds_since_epoch = int((dt_utc - epoch).total_seconds() * 1000)
                timediff = (sn - milliseconds_since_epoch)/3600000
                if abs(timediff) < 1.5 :
                    writer.writerow(line)
    except:
        print(input_filename,' likely does not exist')
                
def get_indices(filename):
#    types = ['alert']
    types = ['numericvalue','wavesample','alert','enumerationvalue','enumvalue']
    lookup_indices = [[4,3],[8,1],[0,0],[6,3],[6,3]]
    for index, string in enumerate(types):
        if string in filename:
            return lookup_indices[index]
            break
    return ([0,0])

source_folder_path = '/ix1/mladi/Pitt'  # Replace with the path to your source folder
tgtdir = '/ix1/mladi/work/cler/staging/'
files_to_fix_path = '/ix1/mladi/work/cler/files_to_fix_04_2025.csv'  # Replace with the desired output CSV file path
logfile = '/ix1/mladi/work/cler/log_of_fixed_files_04_2025.csv'


# Build the set to fix as all files minux already fixed files

allfiletofix_path = '/ix1/mladi/work/cler/files_to_fix_04_2025.csv'  # Replace this with the path to your CSV file
# allfiletofix_path = '/ix1/mladi/work/cler/badfiles_to_fix.csv'
allfilestofixset = read_csv_to_set(allfiletofix_path)
# $allfilestofixset = set(find_csv_files(source_folder_path))
fixedfiles_path = '/ix1/mladi/work/cler/fixed_badfiles.csv'  # Replace this with the path to your CSV file
fixedfilesset = read_csv_to_set(fixedfiles_path)
broken_files = sorted(list(allfilestofixset - fixedfilesset))


with open(logfile, 'a', newline='', encoding='utf-8') as logs:
    writer2 = csv.writer(logs)
    writer2.writerow(['File', 'Presize', 'Postsize'])
    for broken_file in broken_files:
        indices = get_indices(broken_file)
        if indices[0] == 0:
            continue
#        output_file = tgtdir + broken_file.split('/')[-1][:-4]+'_cleaned.csv'
        output_file = tgtdir + broken_file.split('/')[-1]
        try:
            clean_csv(broken_file, output_file, indices)
            presize = int(os.path.getsize(broken_file))
            postsize = int(os.path.getsize(output_file))
            if (postsize<presize) & (postsize>0):
                writer2.writerow([broken_file,presize,postsize,'fixed'])
                print(broken_file, ' fixed')
            else:
                writer2.writerow([broken_file,presize,postsize,'not broken'])
                os.remove(output_file)
                print(broken_file,' was not broken, staging file removed')
            logs.flush()
        except:
            print(broken_file,' likely does not exist')



