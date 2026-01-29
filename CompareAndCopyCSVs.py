import os
import shutil
import sys

def get_csv_files(directory):
    """Returns a dictionary of CSV files with their paths and modification times in the given directory."""
    csv_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                modification_time = os.path.getmtime(full_path)
                csv_files[full_path] = modification_time
    return csv_files

def compare_and_copy(src_a, src_b, deleted_dirs_file):
    """Compares CSV files between two directories and copies them accordingly, preserving subdirectory structure."""
    a_files = get_csv_files(src_a)
    b_files = get_csv_files(src_b)
    print(len(a_files)/22, len(b_files)/22)
    deleted_dirs = set()

    for b_path, b_mod_time in b_files.items():
        # Construct the relative path in src_b and the corresponding path in src_a
        relative_path = os.path.relpath(b_path, src_b)
        a_path = os.path.join(src_a, relative_path)

        # Ensure the directory exists in src_a
        os.makedirs(os.path.dirname(a_path), exist_ok=True)

        # Copy from B to A if the file doesn't exist in A or if it's newer in B
        if a_path not in a_files or b_mod_time > a_files.get(a_path, 0):
            shutil.copy2(b_path, a_path)
            # File copied, can be deleted from src B
        os.remove(b_path)
            # Add the directory to the list of deleted directories
        deleted_dirs.add(os.path.dirname(b_path))

    # Write the list of deleted subdirectories to the specified file
    with open(deleted_dirs_file, 'a') as file:
        for dir in sorted(deleted_dirs):
            file.write(f"{dir}\n")

if __name__ == "__main__":
    # Check if folder name is provided
    if len(sys.argv) < 2:
        print("Please provide the folder name.")
        sys.exit(1)
    
    subfolder = sys.argv[1]
    src_a = '/ix1/mladi/read/'+ subfolder
    src_b = '/ix1/mladi/read2/' + subfolder
    deleted_dirs_file = '/ix1/mladi/work/cler/consolidated.csv'

# Compare and copy files, preserving subdirectory structure and logging deleted directories
    compare_and_copy(src_a, src_b, deleted_dirs_file)
    print(src_b)

# Note: This script requires the necessary permissions to read, write, and delete files in these directories.
# Also, it assumes that the directory structure of /src/B is to be replicated in /src/A.
# The list of deleted subdirectories from /src/B will be written to 'consolidated.csv'.
