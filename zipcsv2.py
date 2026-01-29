import os
import sys
import zipfile

def zip_csv_files(folder_path):
    # Create a zip file named 'csv_files.zip' in the given folder
    zip_file_path = os.path.join(folder_path, "compressed_csv_files.zip")
    with zipfile.ZipFile(zip_file_path, 'w',zipfile.ZIP_DEFLATED) as zipf:
        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                # Add the file to the zip
                zipf.write(file_path, filename)
    return zip_file_path

def delete_csv_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)

if __name__ == "__main__":
    # Check if folder name is provided
    if len(sys.argv) < 2:
        print("Please provide the folder name.")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"'{folder_path}' is not a valid folder.")
        sys.exit(1)

    zip_csv_files(folder_path)
    delete_csv_files(folder_path)