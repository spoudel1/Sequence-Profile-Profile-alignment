#this is a play around script 
#input:
#output:

import sys
import os
import subprocess

outputfile=open(sys.argv[2],'w')
copying=False
outputfile.write('Source'+'\t'+'Target'+'\t'+'Probability'+'\t'+'E-value'+'\t'+'Score'+'\t'+'Aligned_cols'+'\t'+'Identities'+'\t'+'Similarity'+'\t'+'Sum_probability'+'\n')
_store=[]
def dupcheck(nameq,names):
    present=0
    for x in _store:
        x_split=x.split('#')
        if x_split[0]==nameq and x_split[1]==names or x_split[0]==names and x_split[1]==nameq:
            present=1
            break
    return present

with open(sys.argv[1],'r') as inputfile:
	for line in inputfile:
		line_strip=line.strip()
		if 'Command' in line_strip:
			line_split=line_strip.split(' ')
			query_temp=line_split[9]
			sub_temp=line_split[11]
			if '/' in query_temp:
				query_split=query_temp.split('/')
			#	query=query_split[2][:query_split[2].index('.')] # for sphere
				query=query_split[4][:query_split[4].index('.')] #for neighbour
			else:
				query=query_temp
			if '/' in sub_temp:
				sub_split=sub_temp.split('/')
			#	sub=sub_split[2][:sub_split[2].index('.')] # for sphere
				sub=sub_split[4][:sub_split[4].index('.')] # for neighbour
			else:
				sub=sub_temp
                        if not query == sub:
                            if dupcheck(query,sub)==0:
                                outputfile.write(query+'\t'+sub)
                                copying=True
                                _store.append(query+'#'+sub)
		elif copying:
			if 'Probab' in line_strip:
				line_split1=line_strip.split(' ')
				outputfile.write('\t'+line_split1[0][line_split1[0].index('=')+1:]+'\t'+line_split1[2][line_split1[2].index('=')+1:]+'\t'+line_split1[4][line_split1[4].index('=')+1:]+'\t'+line_split1[6][line_split1[6].index('=')+1:]+'\t'+line_split1[8][line_split1[8].index('=')+1:]+'\t'+line_split1[10][line_split1[10].index('=')+1:]+'\t'+line_split1[12][line_split1[12].index('=')+1:]+'\n')
				copying=False

