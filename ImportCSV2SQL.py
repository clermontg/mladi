
import os
import pymysql
conn = pymysql.connect(host='auview.ccm.pitt.edu',
                             user='cler',
                             password='',
                             database='mladi', port=3306, local_infile=1)
cur=conn.cursor()

qdemo ='''load data local infile '/ix1/mladi/work/cler/data/_demo.csv' into table mladi.EMR_demo \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 LINES  \
(Rownumber ,study_id, FIN_study_id, RACE, @Age, Sex, Facility, Unit, @regdate, @dischdate, Ethnicity, ENCNTR_type, disch_disp) \
set \
AGE = cast(@Age as unsigned), \
REG_DATE = str_to_date(left(@regdate,19), '%Y-%m-%d %H:%i:%s'), \
DISCH_DATE = str_to_date(left(@dischdate,19), '%Y-%m-%d %H:%i:%s'), \
RegUTCoffset = CAST(substring(@regdate,25,3) AS SIGNED), \
DischUTCoffset = CAST(substring(@dischdate,25,3) AS SIGNED) '''

qloc = '''load data local infile '/ix1/mladi/work/cler/data/_loc.csv' into table mladi.EMR_loc \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 LINES  \
(Rownumber ,study_id, FIN_study_id, @beg_date, @end_date, FACILITY, UNIT) \
set \
BEG_DATE = str_to_date(@beg_date, '%Y-%m-%d %H:%i:%s'), \
END_DATE = str_to_date(@end_date, '%Y-%m-%d %H:%i:%s') , \
BegUTCoffset = CAST(substring(@beg_date,25,3) AS SIGNED), \
EndUTCoffset = CAST(substring(@end_date,25,3) AS SIGNED) '''

qce ='''load data local infile '/ix1/mladi/work/cler/data/_ce.csv' into table mladi.EMR_ce \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 lines \
(Rownumber ,@dat, study_id, FIN_study_id, event_name, result_val, result_unit, result_stat, event_tag) SET \
chartdate = str_to_date(LEFT(@dat,23), '%Y-%m-%d %H:%i:%s') ,\
UTCoffset = CAST(substring(@dat,25,3) AS SIGNED) '''

qlab = '''load data local infile '/ix1/mladi/work/cler/data/_lab.csv' into table mladi.EMR_lab \
fields terminated by ','  OPTIONALLY ENCLOSED BY '\"' ignore 1 LINES \
(RowNumber, study_id, FIN_study_id, @edate, ORDERED_AS, EVENT_DISP, RESULT_VAL, RESULT_STAT, RESULT_UNIT, EVENT_TAG, NORMALCY_HIGH, \
@Vdate, NORMALCY, NORMALCY_LOW)  \
SET \
EVENT_DATE = str_to_date(@edate, '%Y-%m-%d %H:%i:%s'), \
VALID_DATE = str_to_date(@Vdate, '%Y-%m-%d %H:%i:%s'), eUTCoffset = CAST(substring(@edate,25,3) AS SIGNED), \
vUTCoffset = CAST(substring(@Vdate,25,3) AS SIGNED) '''

qio = '''load data local infile '/ix1/mladi/work/cler/data/_io.csv' into table mladi.EMR_io \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 lines \
(RowNumber,Study_id,FIN_Study_Id,@dat,IO_NAME,IO_DETAIL,@VOLUME,UNIT) set \
EVENT_date = str_to_date(@dat, '%Y-%m-%d %H:%i:%s'), \
VOLUME = cast(@VOLUME AS DECIMAL(9,1)), \
UTCoffset = CAST(substring(@dat,25,3) AS SIGNED) '''

qmed = '''load data local infile '/ix1/mladi/work/cler/data/_med.csv' into table mladi.EMR_meds \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 lines \
(RowNumber,Study_id,FIN_Study_Id,ORDERED_AS,CATALOG_DISP,@dat,RESULT_VAL,RESULT_STAT,EVENT_TAG,ROUTE,DOSE,DOSE_UNIT,VOLUME_DOSE_UNIT,  \
FREE_DOSE,VOLUME_DOSE) SET \
CHART_DATE= str_to_date(@dat, '%Y-%m-%d %H:%i:%s'),  \
UTCoffset = CAST(substring(@dat,25,3) AS SIGNED) '''

qicd = '''load data local infile '/ix1/mladi/work/cler/data/_icd.csv' into table mladi.EMR_icd \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 lines \
(RowNumber,@dat,Study_id,FIN_Study_Id,DX_IND,TYPE,CODE_TYPE,SEQ,CONFIRM_STAT,DISP,LIFE_CYCLE,SOURCE,CODE) SET \
CHART_DATE = str_to_date(@dat, '%Y-%m-%d %H:%i:%s') , \
UTCoffset = CAST(substring(@dat,25,3) AS SIGNED) '''

qpatient = '''load data local infile '/ix1/mladi/work/cler/data/_patient.csv' into table mladi.EMR_patient \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(Study_Id,FIN_Study_Id,@dat,BedLabel,Alias,Height,HeightUnit,Weight,WeightUnit,PressureUnit,PacedMode,ResuscitationStatus,ClinicalUnit,Gender,AdmitState) SET \
EVENT_TIME = str_to_date(concat(left(@dat,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
UTCoffset = cast(SUBSTRING(@dat,25,3) AS SIGNED) '''

qalerts = '''load data local infile '/ix1/mladi/work/cler/data/_alert.csv' into table mladi.DWC_alert \
fields terminated by ',' optionally enclosed BY '\"' ignore 1 lines \
( \
study_id, FIN_Study_Id, @TIMESTAMP, AlertId, SOURCE, CODE, Label, Severity, Kind, IsSilenced, SubtypeId, @AnnounceTime, @OnsetTime, @EndTime, SequenceNumber) \
SET \
UTCoffset = CAST(substring(@TIMESTAMP,25,3) AS SIGNED), \
TIMESTAMP    = str_to_date(CONCAT(LEFT(@TIMESTAMP,23),\"000\"), '%Y-%m-%d %H:%i:%s.%f'), \
AnnounceTime = str_to_date(CONCAT(LEFT(@AnnounceTime,23),\"000\"), '%Y-%m-%d %H:%i:%s.%f'), \
OnsetTime    = str_to_date(CONCAT(LEFT(@Onsettime,23),\"000\"), '%Y-%m-%d %H:%i:%s.%f'), \
EndTime = str_to_date(CONCAT(LEFT(@EndTime,23),\"000\"), '%Y-%m-%d %H:%i:%s.%f') '''

qmicro = '''load data local infile '/ix1/mladi/work/cler/data/_micro.csv' into table mladi.EMR_micro \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,Study_Id,FIN_Study_Id,micro_seq_nbr,@valid_date,organism,source_type,@performed_date,@collect_date,result_stat,@chart_date,Accession) SET \
valid_date = str_to_date(concat(left(@valid_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
performed_date = str_to_date(concat(left(@performed_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
collect_date = str_to_date(concat(left(@collect_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
chart_date = str_to_date(concat(left(@chart_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
vUTCoffset = cast(SUBSTRING(@valid_date,25,3) AS SIGNED), \
pUTCoffset = cast(SUBSTRING(@performed_date,25,3) AS SIGNED), \
cUTCoffset = cast(SUBSTRING(@collect_date,25,3) AS SIGNED),\
UTCoffset = cast(SUBSTRING(@chart_date,25,3) AS SIGNED) '''

qsurg = '''load data local infile '/ix1/mladi/work/cler/data/_surg.csv' into table mladi.EMR_surg \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,Study_Id,FIN_Study_Id,@start_date,@end_date,surg_dur,cancel_reason,@cancel_date,active_ind,active_status,surg_area_name,@sched_start_date) \
SET \
start_date = str_to_date(concat(left(@start_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
end_date = str_to_date(concat(left(@end_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
cancel_date = str_to_date(concat(left(@cancel_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
sched_start_date = str_to_date(concat(left(@sched_start_date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
sUTCoffset = cast(SUBSTRING(@start_date,25,3) AS SIGNED), \
eUTCoffset = cast(SUBSTRING(@end_date,25,3) AS SIGNED), \
cUTCoffset = cast(SUBSTRING(@cancel_date,25,3) AS SIGNED),\
sdUTCoffset = cast(SUBSTRING(@sched_start_date,25,3) AS SIGNED) '''

qdlce = '''load data local infile '/ix1/mladi/work/cler/data/_dialysis_ce.csv' into table mladi.EMR_dl_ce \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,Study_Id,FIN_Study_Id,@date,event_name,event_tag,result_val,result_unit,result_stat) \
SET \
chartdate = str_to_date(concat(left(@date,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
UTCoffset = cast(SUBSTRING(@date,25,3) AS SIGNED) '''

qdldt = '''load data local infile '/ix1/mladi/work/cler/data/_dl_details_recent.csv' into table mladi.EMR_dl_dt \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,Study_Id,FIN_Study_Id,ORDER_NAME,@ORDER_DATE,OE_FIELD_NAME,OE_FIELD_DISPLAY) \
SET \
order_date = str_to_date(concat(left(@ORDER_DATE,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
UTCoffset = cast(SUBSTRING(@ORDER_DATE,25,3) AS SIGNED) '''

qsuscept = '''load data local infile '/ix1/mladi/work/cler/data/_suscep.csv' into table mladi.EMR_suscept \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,Study_Id,FIN_Study_Id,micro_seq_nbr,Accession,antibiotic,test_name,detail_suscept,result,result_text,@result_date,suscept_stat,@valid_date) \
SET \
result_date = str_to_date(concat(left(@result_DATE,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
valid_date = str_to_date(concat(left(@valid_DATE,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
rUTCoffset = cast(SUBSTRING(@result_DATE,25,3) AS SIGNED), \
vUTCoffset = cast(SUBSTRING(@valid_DATE,25,3) AS SIGNED) '''

qcsce = '''load data local infile '/ix1/mladi/work/cler/data/_cs_ce.csv' into table mladi.EMR_cs_ce \
fields terminated by ',' optionally enclosed by '\"' ignore 1 lines \
(RowNumber,study_id,FIN_study_id,@EVENT_DATE,EVENT_NAME,EVENT_TAG,RESULT_VAL) \
SET \
event_date = str_to_date(concat(left(@EVENT_DATE,23),'000'), '%Y-%m-%d %H:%i:%s.%f'), \
UTCoffset = cast(SUBSTRING(@EVENT_DATE,25,3) AS SIGNED) '''

# cur.execute(qcsce)
cur.execute(qsuscept)
cur.execute(qdldt)
cur.execute(qdlce)
cur.execute(qsurg)
# cur.execute(qdemo)
# cur.execute(qloc)
# cur.execute(qce)
# cur.execute(qlab)
# cur.execute(qio)
# cur.execute(qmed)
# cur.execute(qicd)
# cur.execute(qpatient)
# cur.execute(qalerts)
# cur.execute(qmicro)

conn.commit()
cur.close()
conn.close()
print('Done')

