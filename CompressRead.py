import os
import zipfile
from datetime import datetime
import time

def compress_and_delete_csv_files(root_dir):
    current_year = str(datetime.now().year)
    oldtime = time.time()
    for folder_name, subfolders, filenames in os.walk(root_dir):
        if not filenames or folder_name == root_dir or current_year in folder_name or len(folder_name)!=24 or "2022" in folder_name or "2020" in folder_name or "2019" in folder_name:
            continue
        print(folder_name, time.time()-oldtime)
        oldtime = time.time()
        # Create a new zip file for each subfolder with the subfolder's name
        compressed_file_name = os.path.basename(folder_name) + "_compressed_csv_files.zip"
        zip_filename = os.path.join(folder_name, compressed_file_name)

        # Store the file paths to be deleted after zipping
        files_to_delete = []

        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename in filenames:
                if filename.endswith(".csv"):
                    file_path = os.path.join(folder_name, filename)
                    zip_file.write(file_path, os.path.basename(file_path))
                    files_to_delete.append(file_path)

        # Delete the original CSV files after zipping
        for file_path in files_to_delete:
            os.remove(file_path)
        print("Folder "+folder_name+" zipped")

if __name__ == "__main__":
    root_dir = "/ix1/mladi/read"
    compress_and_delete_csv_files(root_dir)
