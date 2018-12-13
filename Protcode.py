#this script will get hhalign file

import sys
import genprofile
import os
import time

start=time.time()

keyfile=open(sys.argv[1]).readlines()
fastafile=open(sys.argv[2]).readlines()

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
        for x in _store:
            if x == name:
                dpresent=1
                break
    return dpresent
count=0
tcount=0
for line in keyfile:
    line_strip=line.strip()
    line_split=line_strip.split('\t')
    if dupcheck(line_split[1].strip(),1)==0:
        _store.append(line_split[1].strip())
        print line_split[1],tcount
        if count==0:
            print 'came0',tcount,'tcount'
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
            patho="../Result/hhblits/"
            pathm="../Result/hmmer/"
            print 'came2',tcount
            if tcount==2:
                print 'came3',tcount
                #if only calling hmmer package without multiple sequence analysis
#                genprofile.hhblits().hhmake(patho,infile,1)
                genprofile.hmmer().profile(pathm,infile,1)
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
os.remove(infile)

