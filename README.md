# mladi
Collection of scripts to process data files

At baseline every encounter has 22 files since 2020. it used to be 16. The additional files include micro, suscep, surg, dl_details, and dl_recent. I am missing one.

The CC2.py file fixes the multiline comma fields, checks whether there are 22 files per encounter and removes duplicates in /read2 files, then copies them to /read.

The dedup.py script processes already existing files in /read to remove duplicates in headers and lines

The CompressRead.py script runs through a rootdir e.g. /read) and runs through all folders, compressing all csv files in a folder in a single .zip. This is to save space. There is a consition which can specify the scope of folders (e.g. all folders with '2022' in their names.

The DBbuildfromcsv.py runs through folders in read and prepares data, in csv format, for import to database schema. Thus all patients' data from a type of EHR or alert file are grouped, resulting in 16 files deposited in the ix1/mladi//work/cler/data folder.

The ImportCSV2SQL.py script connects to a database and actually upload the output of the previous script (15 of 16 files) to a MySQL schema. For now, this is the mladi23 schema.
