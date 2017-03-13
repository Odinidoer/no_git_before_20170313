#!/usr/bin/python

import re

data=open('1_1.txt','w')
with open('1.txt')as data1:
	for line in readlines():
		line=line.strip('\n')
		if re.search(r'(GN=.*?) ',line):
			data.write(line+'\t'+re.search(r'(GN=.*?) ',line).group(1)+'\n')
		else:
			data.write(line+'\t'+'GN'+'\n')
data.close()
