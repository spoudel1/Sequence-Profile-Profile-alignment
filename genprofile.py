#this script will can call two progams hmmer and hhblits

import sys
import subprocess
import os

#this class will call hmmer packages
class hhblits(object):
    #this will conduct multiple sequence alignment
    def clustal(self, patho,tfile):
	print 'came clustalo'
        subprocess.call(["clustalo", "-i", tfile, "--infmt", "fa", "-o", patho+"clustal/"+tfile+"_clustalo", "--outfmt", "fa", "--threads", "5"])
    
    #this function will make profile of the multiple sequence alignment
    def hhmake(self,patho,tfile,num):
        if num==1:
	    self.clustal(patho,tfile)
            subprocess.call(["hhmake", "-i", patho+"clustal/"+tfile+"_clustalo", "-id", "100", "-M", "100", "-diff", "inf", "-add_cons", "-seq", "0", "-o", patho+"hhmake/"+tfile+"_clustalo.hmm"])
        else:
            subprocess.call(["hhmake", "-i", patho+"clustal/"+tfile+"_clustalo", "-id", "100", "-M", "100", "-diff", "inf", "-add_cons", "-seq", "0", "-o", patho+"hhmake/"+tfile+"_clustalo.hmm"])

#this class will call hhblits packages
class hmmer(object):
    #this function will make profile using hmmer method
    def profile(self,patho,tfile,num):
        if num==1:
            hhblits().clustal(patho,tfile)
            subprocess.call(["hmmbuild", "--amino", patho+"hmmbuild/"+tfile+".hmm", patho+"clustal/"+tfile+"_clustalo"])
        else:
            subprocess.call(["hmmbuild", "--amino", patho+"hmmbuild/"+tfile+".hmm", patho+"clustal/"+tfile+"_clustalo"])

