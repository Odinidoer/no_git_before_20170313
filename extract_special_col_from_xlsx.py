#!/usr/bin/env python
#coding:utf-8
#author:jun.yan@majorbio.com
#last_modified:20170228

import argparse
import os
import pandas as pd
import re

parser = argparse.ArgumentParser(description="get col from xlsx")
parser.add_argument("-i", dest="i", type=str, required=True, help="please input file name : *.xlsx")
parser.add_argument("-s", dest="s", type=str, help="please input col names")
parser.add_argument("-o", dest="o", type=str, required=True, help="please output file name!")
args = parser.parse_args()

df = pd.read_excel("%s" %(args.i))
if args.s:
	mark = args.s.split(',')	
	with open('%s' %args.o,'w') as cols:
		cols.write('\t'.join(mark)+'\n')
		for i in range(df.shape[0]):
			ss=[]
			for col in mark:
				ss.append((str(pd.DataFrame(df,columns=['%s' %col])[i:i+1].iloc[0,0])))
			cols.write('\t'.join(ss)+'\n')
else:
	df.to_csv('%s' %args.o, sep="\t", index=False)
