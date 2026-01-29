#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 13:50:08 2025

@author: cler
"""
#!/usr/bin/env python3
import os
import sys
import zipfile
import csv
from filelock import FileLock, Timeout

def ensure_log_exists(log_path, log_lock):
    """Create the CSV log with header if it doesn't exist, under file-lock."""
    with log_lock:
        if not os.path.exists(log_path):
            with open(log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['folder_path', 'pre_zip_bytes', 'zip_bytes', 'file_count'])

def load_processed(log_path, log_lock):
    """Read all already‐processed folders from the CSV, under file-lock."""
    processed = set()
    with log_lock:
        if os.path.exists(log_path):
            with open(log_path, newline='') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    if row:
                        processed.add(row[0])
    return processed

def append_log(log_path, log_lock, folder, pre_size, zip_size, file_count):
    """Append one record to the CSV, under file-lock."""
    with log_lock:
        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([folder, pre_size, zip_size, file_count])

def process_subfolder(folder_path, log_path, log_lock):
    """Zip + verify + delete CSVs in folder, then log the result."""
    # 1) collect CSVs
    csv_files = [
        fn for fn in os.listdir(folder_path)
        if fn.lower().endswith('.csv')
           and os.path.isfile(os.path.join(folder_path, fn))
    ]
    file_count = len(csv_files)
    if file_count == 0:
        return

    # 2) compute pre-zip size
    pre_size = sum(
        os.path.getsize(os.path.join(folder_path, fn))
        for fn in csv_files
    )

    # 3) create the ZIP
    zip_name = os.path.basename(folder_path.rstrip(os.sep)) + '.zip'
    zip_path = os.path.join(folder_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fn in csv_files:
            full = os.path.join(folder_path, fn)
            zf.write(full, arcname=fn)

    # 4) verify integrity
    with zipfile.ZipFile(zip_path, 'r') as zf:
        bad = zf.testzip()
        if bad is not None:
            print(f"ERROR: corrupt member '{bad}' in {zip_path}; skipping deletion.")
            return

    # 5) delete originals
    for fn in csv_files:
        os.remove(os.path.join(folder_path, fn))

    # 6) log to CSV
    zip_size = os.path.getsize(zip_path)
    append_log(log_path, log_lock, folder_path, pre_size, zip_size, file_count)
    print(f"[✔] {folder_path}: {file_count} files, {pre_size}→{zip_size} bytes")

def main(root_folder):
    root_folder = os.path.abspath(root_folder)
    log_path = os.path.join(root_folder, 'zip_processed.csv')
    log_lock = FileLock(log_path + '.lock')

    # ensure log exists
    ensure_log_exists(log_path, log_lock)

    for entry in os.listdir(root_folder):
        sub = os.path.join(root_folder, entry)
        if not os.path.isdir(sub):
            continue

        # per-folder lock to avoid two processes zipping the same dir
        folder_lock = FileLock(os.path.join(sub, '.zip.lock'), timeout=0)
        try:
            with folder_lock:
                processed = load_processed(log_path, log_lock)
                if sub in processed:
                    continue
                process_subfolder(sub, log_path, log_lock)
        except Timeout:
            # another instance is already handling this folder
            continue

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py /ix1/mladi/Pitt")
        sys.exit(1)
    base = sys.argv[1]
    if not os.path.isdir(base):
        print(f"Error: '{base}' is not a valid directory.")
        sys.exit(1)
    main(base)