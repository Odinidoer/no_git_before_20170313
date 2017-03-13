#!/usr/bin/python

import re,sys
xml_file=sys.argv[1]

NCBI=open(xml_file,'r').read()

all_uniprot=re.findall(r'Query= (.*?)\n.*?Value\n\n(.*?)\.*?\d*?  ',NCBI,re.S)

with open('for_uniprot.xls','w') as uni:
	for i in range(0,len(all_uniprot)):
		uni.write(all_uniprot[i][0]+'\t'+all_uniprot[i][1]+'\n')
