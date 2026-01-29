#!/usr/bin/env python3
import os
import sys
import shutil
import csv
from zipfile import ZipFile
from collections import defaultdict

def move_csv_files_with_prefix(src_dir, dest_dir):
    # 1) Unzip any .zip archives in place
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(".zip"):
            zip_path = os.path.join(src_dir, filename)
            with ZipFile(zip_path, mode="r") as archive:
                archive.extractall(src_dir)
            print(f"Extracted {zip_path}")

    # 2) Group all .csv files by their first 15 characters
    prefix_dict = defaultdict(list)
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(".csv") and len(filename) >= 15:
            prefix = filename[:15]
            prefix_dict[prefix].append(filename)

    # 3) Move each group into its own subdirectory under dest_dir
    for prefix, files in prefix_dict.items():
        prefix_dir = os.path.join(dest_dir, prefix)
        os.makedirs(prefix_dir, exist_ok=True)

        for filename in files:
            src_path  = os.path.join(src_dir,  filename)
            dst_path  = os.path.join(prefix_dir, filename)

            try:
                shutil.move(src_path, dst_path)
            except Exception as e:
                print(f"ERROR moving {src_path} ? {dst_path}: {e}")
                continue

            # Verify: src no longer exists, dst does exist
            if os.path.exists(dst_path) and not os.path.exists(src_path):
                print(f"Moved: {src_path} -> {dst_path}")
            else:
                print(f"ERROR: verification failed for {src_path}")

    # 4) Final check: are there any .csv left behind?
    remaining = [f for f in os.listdir(src_dir) if f.lower().endswith(".csv")]
    if remaining:
        print(f"WARNING: {len(remaining)} CSV(s) remain in {src_dir}: {remaining}")

def main(dest_dir):
    # Validate destination directory
    if not os.path.isdir(dest_dir):
        print(f"Error: '{dest_dir}' is not a valid directory.")
        sys.exit(1)

    # Read source directories from CSV
    with open('/ix1/mladi/work/cler/sourcedirs.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row: 
                continue
            src_dir = row[0]
            if os.path.isdir(src_dir):
                print(f"\nProcessing source: {src_dir}")
                move_csv_files_with_prefix(src_dir, dest_dir)
            else:
                print(f"Skipping invalid directory: {src_dir}")

if __name__ == "__main__":
    # Optional dest_dir override via command-line
    destination = '/ix1/mladi/Pitt2/'
    if len(sys.argv) == 2:
        destination = sys.argv[1]
    main(destination)
