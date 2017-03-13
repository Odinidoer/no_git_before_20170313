#!/usr/bin/env python
#coding:utf-8
#author:jun.yan@majorbio.com
#last_modified:20170113

from scipy.stats import linregress
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
stats = importr('stats')
import argparse,os

parser=argparse.ArgumentParser(description="from exp.txt calc pearson,p_value and FDR")
parser.add_argument("-f","-file",dest="file",type=str,required=True,help="please input file,normally 'exp.txt'")
parser.add_argument("--pearsonfilter",dest="pearsonfilter",type=float,default=0.99,help="pearson's filter: >0.99 or <-0.99 ; 0.99 as default")
parser.add_argument("--pvaluefilter",dest="pvaluefilter",type=float,default=0.01,help="p_value's filter: <0.01 ;always used to filter FDR; 0.01 as default")
parser.add_argument("-o","--out",dest = "out",type = str,default = "fin",help = "output pearson file: '*.txt'; 'fin' as default")
args=parser.parse_args()


#获得accession的列数信息和对应的组间的值
acc_has=[]
ac_value={}
with open("%s" %args.file,'r') as has:
	has.readline()
	for line in has.readlines():
		line=line.strip('\n')
		items=line.split('\t')
		accession=items[0]
		acc_has.append(accession)
		values=[float(x) for x in items[1:len(items)]]
		ac_value[accession]=values

#计算并筛选pearson以及相应的p_value		
fil1=open("fin_no_fdr.txt",'w')	
fil1.write("acc1\tacc2\tpearson_value\tp_value\n")
for i in range(0,len(acc_has)):
	for j in range(0,len(acc_has)):
		if i<j:
			result=linregress(ac_value[acc_has[i]],ac_value[acc_has[j]])
			pearson=result[2]
			pvalue=result[3]
			if (pearson>args.pearsonfilter or pearson<-(args.pearsonfilter)) and pvalue<args.pvaluefilter:				
				fil1.write("%s\t%s\t%s\t%s\n" %(acc_has[i],acc_has[j],pearson,pvalue))
fil1.close()	

#由pearson的p_value计算FDR，运用rpy2
FDR=[]
with open("fin_no_fdr.txt",'r') as FD:
	FD.readline()
	for line in FD.readlines():
		line=line.strip('\n')
		p_value=line.split('\t')[3]
		FDR.append(p_value)		
p_adjust = stats.p_adjust(FloatVector(FDR), method = 'BH')

fil2=open("%s.txt" %args.out,'w')	
fil2.write("acc1\tacc2\tpearson_value\tp_value\tFDR\n")
with open("fin_no_fdr.txt",'r')	as no_dfr:
	i=0
	no_dfr.readline()
	for line in no_dfr.readlines():
		line=line.strip('\n')
		pvalue=p_adjust[i]
		if pvalue<args.pvaluefilter:
			fil2.write("%s\t%s\n" %(line,pvalue))		
		i=1+1
fil2.close()

os.remove("fin_no_fdr.txt")