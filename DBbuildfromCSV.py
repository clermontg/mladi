
import os, glob
import pandas as pd
import csv

def tpfields(tp):
    typelist=['_demo','_patient','_ce','_cs','_cs_ce','_alert','_icd','_io','_lab','_loc','_med','_surg','_micro','_suscep','_dialysis_ce','_dl_details_recent']
    fields=[['RowNumber','Study_id','Fin_Study_id',"RACE","age","SEX","FACILITY","UNIT",'REG_DATE','DISCH_DATE',"ETHNICITY","ENCNTR_TYPE","DISCH_DISP"],
       ["Study_Id","FIN_Study_Id","TimeStamp","BedLabel","Alias","Category","Height","HeightUnit","Weight","WeightUnit","PressureUnit","PacedMode","ResuscitationStatus","AdmitState","ClinicalUnit","Gender"],
       ["Row_Number","Chart_date","study_id","FIN_Study_id","event_name","result_val","result_unit","result_stat","event_tag"],
       ["Row_Number","Study_Id","FIN_Study_Id","FORM_STAT","ORDER_NAME","ORDER_DATE","FORM_DATE"],
        ["Row_Number","study_id","FIN_study_id","EVENT_DATE","EVENT_NAME","EVENT_TAG","RESULT_VAL"],
       ["study_id","FIN_Study_Id","TimeStamp","AlertId","Source","Code","Label","Severity","Kind","IsSilenced","SubtypeId","AnnounceTime","OnsetTime","EndTime","SequenceNumber"],
       ["Row_Number","DATE","Study_id","FIN_Study_Id","DX_IND","TYPE","CODE_TYPE","SEQ","CONFIRM_STAT","DISP","LIFE_CYCLE","SOURCE","CODE"],
       ["Row_Number","Study_id","FIN_Study_Id","DATE","IO_NAME","IO_DETAIL","VOLUME","UNIT"],
       ["Row_Number","Study_id","FIN_Study_Id","EVENT_DATE","ORDERED_AS","EVENT_DISP","RESULT_VAL","RESULT_STAT","RESULT_UNIT","EVENT_TAG","NORMALCY_HIGH","VALID_DATE","NORMALCY","NORMALCY_LOW"],
       ["Row_Number","Study_id","FIN_Study_Id","BEG_DATE","END_DATE","FACILITY","UNIT"],
       ["Row_Number","Study_id","FIN_Study_Id","ORDERED_AS","CATALOG_DISP","CHART_DATE","RESULT_VAL","RESULT_STAT","EVENT_TAG","ROUTE","DOSE","DOSE_UNIT","VOLUME_DOSE_UNIT","FREE_DOSE","VOLUME_DOSE"],
       ["Row_Number","Study_Id","FIN_Study_Id","start_date","end_date","surg_dur_min","cancel_reason","cancel_date","active_ind","active_status","surg_area_name","sched_start_date"],
       ["Row_Number","Study_Id","FIN_Study_Id","micro_seq_nbr","valid_date","organism","source_type","performed_date","collect_date","result_stat","chart_date","Accession"],
        ["Row_Number","Study_Id","FIN_Study_Id","micro_seq_nbr","Accession","antibiotic","test_name","detail_susceptibility","result","result_text_value","result_date","suscep_stat","valid_date"],
        ["Row_Number","Study_Id","FIN_Study_Id","date","event_name","event_tag","result_val","result_unit","result_stat"],
        ["Row_Number","Study_Id","FIN_Study_Id","ORDER_NAME","ORDER_DATE","OE_FIELD_NAME","OE_FIELD_DISPLAY_VALUE"]
           ]
    x = typelist.index(tp)
    s = fields[x][:]
    return(s)

srccsv= r"/ix1/mladi/read"
tgtdir = "/ix1/mladi/work/cler/"
dirlist = [f.path for f in os.scandir(srccsv) if f.is_dir()]
olddirlist =  tgtdir+'dumpeddirs.csv'
typelist=    typelist=['_demo','_patient','_ce','_cs','_cs_ce','_alert','_icd','_io','_lab','_loc','_med','_surg','_micro','_suscep','_dialysis_ce','_dl_details_recent']
with open(olddirlist) as f:
    olddumps = [line.rstrip() for line in f]
 # creates the sets of directories that have not been dumped to database yet
newdirlist = list(set(dirlist) - set(olddumps))
print(newdirlist) 
f = open(olddirlist,'a') 
for tdir in newdirlist:
    f.write(tdir+'\n')
f.close()
for tp in typelist:  # going through the type
    print(tp)
    demofields = tpfields(tp)
    tpfile=tgtdir+tp+'.csv'
    tfile = open(tpfile,'w')
    tfile.write(",".join(demofields)+"\n") #open the target type and run through the dirs 
    for tdir in newdirlist:
        dumpdate = tdir.split('/')[4]
        if not dumpdate.lower().islower(): # Only those folders that look like dates
            os.chdir(tdir)        
            # build list of FINS in this folder
            filelist=[]
            fins = []
            pats = []
            for file in glob.glob("*.csv"):
                if tp in file:      # just select the specific tp files
                    filelist.append(file)  # we have now constructed a list of files, patients and fins, but only need the tp-specific files
                    fin = file.split('_')[1]
                    pat = file.split('_')[0]
                    if fin not in fins:
                        fins.append(fin)
                        pats.append(pat)
            for file in filelist:
                thiscsv = open(file,"r")
                lineno = 0
                lines = thiscsv.readlines()
                for line in lines:
                    lineno += 1
                    if lineno > 1:   # the first line has field names
                        tfile.write(line)
                thiscsv.close()
    tfile.close()
