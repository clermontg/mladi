#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 21:25:47 2024

@author: cler
"""
import csv
import os
import shutil

def move_files(csv_file, src_folder, target_rootdir):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            origin_file = src_folder + row[0]
            if not os.path.isfile(origin_file):
                print(f"File does not exist: {origin_file}")
                continue

            # Get the first characters of the file path
            subfolder_name = row[0][:15]
            target_subfolder = os.path.join(target_rootdir, subfolder_name)
            target_oldfolder = os.path.join(target_rootdir,'old_csvs')

            # Ensure the target subfolder exists
            os.makedirs(target_subfolder, exist_ok=True)

            # Move the file
            target_file = os.path.join(target_subfolder, os.path.basename(origin_file))
            target_oldfile = os.path.join(target_oldfolder, os.path.basename(origin_file))
            try:
                old_target_file = target_oldfile[:-4] + '_old.csv'
                os.rename(target_file, old_target_file)
                shutil.move(origin_file, target_file)
                print(f"Renamed existing file to {old_target_file} and moved {origin_file} to {target_file}")
            except Exception as e:
                print(f"Failed to move {origin_file} to {target_file}: {e}")

if __name__ == "__main__":
    # Define the path to your CSV file and target root directory
    csv_file = '/ix1/mladi/work/cler/staging/ready_to_transfer_0809.csv'
    target_rootdir = '/ix1/mladi/Pitt'
    src_folder =  '/ix1/mladi/work/cler/staging/'
    
    move_files(csv_file, src_folder, target_rootdir)
    print('done')