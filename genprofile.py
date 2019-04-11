#this script will can call two progams hmmer and hhblits

import sys
import subprocess
import os

_store=[]
#this class will call hmmer packages
class hhblits(object):
    #this will conduct multiple sequence alignment
    def clustal(self, patho,tfile,paths):
        subprocess.call(["clustalo", "-i", tfile, "--infmt", "fa", "-o", patho+"clustal/"+paths+"/"+tfile+"_clustalo", "--outfmt", "fa", "--threads", "5"])
    
    #this function will make profile of the multiple sequence alignment
    def hhmake(self,patho,tfile,num,paths):
        if num==1:
	    self.clustal(patho,tfile,paths)
            subprocess.call(["hhmake", "-i", patho+"clustal/"+paths+"/"+tfile+"_clustalo", "-id", "100", "-M", "100", "-diff", "inf", "-add_cons", "-seq", "0", "-o", patho+"hhblits/hhmake/"+paths+"/"+tfile+"_clustalo.hmm"])
        else:
            subprocess.call(["hhmake", "-i", patho+"clustal/"+paths+"/"+tfile+"_clustalo", "-id", "100", "-M", "100", "-diff", "inf", "-add_cons", "-seq", "0", "-o", patho+"hhblits/hhmake/"+paths+"/"+tfile+"_clustalo.hmm"])

    def dupcheck(self,name):
	present=0
	for x in _store:
 	   if x==name:
		present=1
		break
	return present
    #this function will compare two profiles 
    def hmmalign(self,patho,tfile,num,paths):
	if num==1:
	    self.hhmake(patho,tfile,1,paths)
	    for root, dirs, files in os.walk(patho+"hhblits/hhmake/"+paths):
		for gfile in files:
		    for afile in files:
			if not gfile == afile:
				if self.dupcheck(gfile+'#'+afile)==0:
					_store.append(gfile+'#'+afile)
					subprocess.call(["hhalign", "-i", patho+"hhblits/hhmake/"+paths+"/"+gfile, "-t", patho+"hhblits/hhmake/"+paths+"/"+afile, "-id", "100", "-diff", "inf", "-glob", "-o", patho+"hhblits/test1", "-M", "100", "-hide_cons"])
	else:
    	    for root, dirs, files in os.walk(patho+"hhblits/hhmake/"+paths):
		for gfile in files:
		    for afile in files:
			if not afile == gfile:
				if self.dupcheck(gfile+'#'+afile)==0:
					_store.append(gfile+'#'+afile)
					subprocess.call(["hhalign", "-i", patho+"hhblits/hhmake/"+paths+"/"+gfile, "-t", patho+"hhblits/hhmake/"+paths+"/"+afile, "-id", "100", "-diff", "inf", "-glob", "-o", patho+"hhblits/test1", "-M", "100", "-hide_cons"])
    #this function will convert hmmalign file to a tabulated file
    def hhaligntotab(self,tfile):
	 tofile=tfile+'_totab.csv'
         outputfile=open(tofile,'w')
         copying=False
         outputfile.write('Query'+'\t'+'Subject'+'\t'+'Probability'+'\t'+'E-value'+'\t'+'Score'+'\t'+'Aligned_cols'+'\t'+'Identities'+'\t'+'Similarity'+'\t'+'Sum_probability'+'\n')
         with open(tfile,'r') as inputfile:
             for line in inputfile:
                 line_strip=line.strip()
                 if 'Command' in line_strip:
                     line_split=line_strip.split(' ')
                     query_temp=line_split[9]
		     sub_temp=line_split[11]
		     if '/' in query_temp:
		 	query_split=query_temp.split('/')
		 	query=query_split[6][:query_split[6].index('.')] #for neighbour
		     else:
		 	query=query_temp
		     if '/' in sub_temp:
		 	sub_split=sub_temp.split('/')
		 	sub=sub_split[6][:sub_split[6].index('.')] # for neighbour
		     else:
		 	sub=sub_temp
		     outputfile.write(query+'\t'+sub)
		     copying=True
		 elif copying:
			if 'Probab' in line_strip:
				line_split1=line_strip.split(' ')
				outputfile.write('\t'+line_split1[0][line_split1[0].index('=')+1:]+'\t'+line_split1[2][line_split1[2].index('=')+1:]+'\t'+line_split1[4][line_split1[4].index('=')+1:]+'\t'+line_split1[6][line_split1[6].index('=')+1:]+'\t'+line_split1[8][line_split1[8].index('=')+1:]+'\t'+line_split1[10][line_split1[10].index('=')+1:]+'\t'+line_split1[12][line_split1[12].index('=')+1:]+'\n')
				copying=False
		

#this class will call hhblits packages
class hmmer(object):
    #this function will make profile using hmmer method
    def profile(self,patho,tfile,num,paths):
        if num==1:
            hhblits().clustal(patho,tfile,paths)
            subprocess.call(["hmmbuild", "--amino", patho+"hmmer/hmmbuild/"+paths+"/"+tfile+".hmm", patho+"clustal/"+paths+"/"+tfile+"_clustalo"])
	elif num==2:
	    subprocess.call(["hmmbuild", "--amino", patho+"hmmer/hmmbuild/"+paths+"/"+tfile+".hmm", patho+"clustal/"+paths+"/"+tfile+"_clustalo"])	
        else:
            subprocess.call(["hmmbuild", "--amino", patho+"hmmer/hmmbuild/"+paths+"/"+tfile+".hmm", patho+"clustal/"+paths+"/"+tfile+"_clustalo"])
