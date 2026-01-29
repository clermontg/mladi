import os
import glob

def fixfile(f):
    with open(f,"r") as fin, open("/ix1/mladi/work/cler/output.csv","w") as fout:
        quote_count = 0
        is_quote_open = False
        lout = ''
        this_line = fin.readline().rstrip('\n')
        while this_line:
            quote_count = this_line.count('"')
            if quote_count % 2 == 0:
                if is_quote_open == False:
                    lout = lout + this_line
                    fout.write(lout + '\n')
                    lout = ''
                else: # even number of quote but one is opened -> one closed and a new one opened
                    lout = lout + this_line
            else:
                if is_quote_open: # this closes the quotes
                    is_quote_open = False
                    lout = lout + this_line
                    fout.write(lout + '\n')
                    lout = ''
                else:
                    is_quote_open = True # this opens the quotes
                    lout = lout + this_line
            this_line = fin.readline().rstrip('\n')
    os.system('cp '+"/ix1/mladi/work/cler/output.csv"+' '+f)
    os.system('rm /ix1/mladi/work/cler/output.csv')
    


srccsv = r"/ix1/mladi/read2/"
tgtdir = "/ix1/mladi/read/"
cdir = "/ix1/mladi/work/cler/"
dirlist = [f.path for f in os.scandir(srccsv) if f.is_dir()]
olddirlist =  cdir+'dumpeddirs_in2.csv'
tplist = ["_lab","_wave","_wavesample","_alert","_numeric","_numericvalue","_enum","_enumerationvalue",'_demo','_patient','_ce','_cs','_cs_ce','_icd','_io','_loc','_meds','_surg','_micro','_suscep','_dialysis_ce','_dl_details_recent']
tplist2 = ["_lab","_micro"]
tmfield=[4,2,4,3,2,4,2,4,9,3,2,6,4,2,4,4,6,4,5,11,4,5]

with open(olddirlist,"r+") as f:
    olddumps = [line.rstrip() for line in f]
 # creates the sets of directories that have not been copied to /ix1/mladi/read yet
    newdirlist = list(set(dirlist) - set(olddumps)) 
    for tdir in newdirlist:
        f.write(tdir+'\n')
    f.close()

collatefile=cdir+'collate.csv' # This will create/append annotation file with folder name, pat, fin, type, number, start and end date,
cfile = open(collatefile,'a')

# run the folders,
for tdir in newdirlist:
    print(tdir)
    dumpdate = tdir.split('/')[4]
    if not dumpdate.lower().islower(): # Only those folders that look like dates 
        if not os.path.exists(tgtdir+dumpdate):
            os.mkdir(tgtdir+dumpdate) # Create the folder in read,
        os.chdir(tdir)  
        # build list of type-specific files and prefixes in this folder
        tpindex = 0
        for tp in tplist:
            #if tp != '_dl_details_recent':
            #    continue
            print(tp)
            prefixlist =[]
            filelist = []
            tpindex += 1 
            for file in glob.glob('*'+tp+'-*')+glob.glob('*'+tp+'.csv'): # All the files of that type in this folder,
                filelist.append(file)  # we have now constructed a list of files, patients and fins, but only need the tp-specific files,
                fin = file.split('_')[1]
                pat = file.split('_')[0]
                prefix = pat+'_'+fin+tp
                nbr = file.split('.')[0][len(file.split('.')[0]) - 6:]
                if nbr[0] != '-':
                    nbr = '-00000'
                if prefix not in prefixlist:
                    prefixlist.append(prefix)
                lineno = 0
                starttime='0'
                endtime='0'
                with open(file,"r") as thiscsv: # get the second line and get out
                    for line in thiscsv:
                        lineno += 1
                        try:
                            if lineno == 2:   # the first line has field names
                                starttime = line.split(',')[tmfield[tpindex-1]-1]
                                break #if there is a single line, stick with 0 starttime
                        except Exception:
                            print(thiscsv)
                            continue
                with open(file,"rb") as thiscsv:
                    try:
                        thiscsv.seek(-2, os.SEEK_END)
                        while thiscsv.read(1)!= b'\n':
                            thiscsv.seek(-2,os.SEEK_CUR)
                        line = thiscsv.readline().decode()
                        endtime = line.split(',')[tmfield[tpindex-1]-1]   
                    except OSError:
                        thiscsv.seek(0) # if there is a single line stick with 0 endtime                  
                outputline = tdir+','+ pat+','+fin+','+tp+','+nbr+','+starttime+','+endtime
                cfile.write(outputline+'\n')
            for prefix in prefixlist: # we have run through all files of this type, let's collate then
                tgtfile = tgtdir+dumpdate+'/'+prefix+'.csv'
                if file in glob.glob('*'+tp+'.csv'):
                    syscomcat = 'cat '+prefix+'.csv'+' > '+ tgtfile
                else:
                    syscomcat = 'cat '+prefix+'-*'+' > '+tgtfile
                syscomheader = 'head -n 1 '+tgtfile + ' > ' +tgtdir+dumpdate+'/header.txt'
                syscomrest = "grep -v 'Study_Id' " + tgtfile + ' > '+tgtdir+dumpdate+'/rest.txt'
                syscomcollate = 'cat ' +tgtdir+dumpdate+'/header.txt ' + tgtdir+dumpdate+'/rest.txt > ' + tgtfile
                syscomrm = 'rm ' + tgtdir+dumpdate+'/*.txt'
                os.system(syscomcat)
                os.system(syscomheader)
                os.system(syscomrest)
                os.system(syscomcollate)
                for tp2 in tplist2:
                    if tp2 in tgtfile:
                        fixfile(tgtfile)
                os.system(syscomrm)      
cfile.close()                   
