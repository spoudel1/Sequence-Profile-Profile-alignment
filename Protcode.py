#this script will get hhalign file

import sys
import genprofile
import os
import time
#import removeredundantseq

start=time.time()

if len(sys.argv)==5:
    keyfile=open(sys.argv[1]).readlines()
    fastafile=open(sys.argv[2]).readlines()
    filterfile=open(sys.argv[3]).readlines()
    paths=sys.argv[4]
elif len(sys.argv)==4:
    keyfile=open(sys.argv[1]).readlines()
    fastafile=open(sys.argv[2]).readlines()
    paths=sys.argv[4]
else:
    print 'please check the number of inputfiles, you need to provide atleast two files and not more than 3 files'
#fastafile_t=open(sys.argv[2]+'_dupremo','w')
#removeredundantseq.removered(fastafile_org,fastafile_t)
#fastafile=open(fastafile_t).readlines()
def findseq(pdbid,filename):
    present=0
    copying=False
    for word in fastafile:
        word_strip=word.strip()
        if word_strip.startswith('>'):
            if copying==True:
                break
            copying=False
            if pdbid in word_strip:
                filename.write('\n'+word_strip+'\n') 
                present=1
                copying=True
        elif copying:
            filename.write(word_strip)
    return present
_store=[]
def dupcheck(name,num):
    dpresent=0
    if num==1:
        for tline in filterfile:
            tline_split=tline.split('\t')
            if name == tline_split[0].strip():
                dpresent=1
                break
    if num==2:
        for x in _store:
            if x == name:
                dpresent=1
                break
    return dpresent
count=0
tcount=0

for line in keyfile:
    line_strip=line.strip()
    line_split=line_strip.split("\t")
    if dupcheck(line_split[1].strip(),1)==1:
        if dupcheck(line_split[1].strip(),2)==0:
            _store.append(line_split[1].strip())
            if count==0:
                if not os.path.isfile("tempfile"):
                      infile="G_"+line_split[1]
                      tempfile=open(infile,"w")
                if findseq(line_split[0].strip(),tempfile)==0:
                      print 'not found',line_split[0]
                else:
                     tcount=1
                count=1
            elif count==1:
                tempfile.close()
                patho="../Result/profile/"
#                patho="../Referencefile/profile/"
                # pathm="../Result/hmmer/"
                if tcount==2:
                    #if only calling hmmer package without multiple sequence analysis
                    genprofile.hhblits().hhmake(patho,infile,1,paths)
                    genprofile.hmmer().profile(patho,infile,2,paths)
                os.remove(infile)
                infile="G_"+line_split[1]
                tempfile=open(infile,"w")
                tcount=0
                if findseq(line_split[0].strip(),tempfile)==0:
                     print "not found",line_split[0]
                else:
                     tcount=1
        else:
            if findseq(line_split[0].strip(),tempfile)==0:
                print 'not found',line_split[0]
            else:
                if tcount==0:
                    tcount=1
                elif tcount==1:
                    tcount=2
if tcount==2:
    tempfile.close()
    patho="../Result/profile/"
    genprofile.hhblits().hhmake(patho,infile,1,paths)
    genprofile.hmmer().profile(patho,infile,2,paths)
os.remove(infile)

patho="../Result/profile/"
infile=open(sys.argv[1]).readlines()
genprofile.hhblits().hmmalign(patho,infile,2,paths)

#genprofile.hhblits().hhaligntotab("../Result/profile/Hmm_noade","../Result/profile/Hmm_noade_totab.csv")
genprofile.hhblits().hhaligntotab("../Result/profile/Hmm")
#genprofile.hhblits().hhaligntotab("../Result/hmmalign_struc","../Result/hmmalign_struc_totab.csv")
print 'total time taken',start-time.time()
