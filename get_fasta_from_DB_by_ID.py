#!/usr/bin/python
#-*- coding:UTF-8 -*-

#由基因号搜索数据库的到对应的fasta信息文件
import linecache,sys,os,string,re
File_exp=sys.argv[1]
File_fa=sys.argv[2]


f1=open(File_exp,"r")
f2=open(File_fa,"r")
f3=open("exp.fasta","w")

data2=f2.read()+'\n>'
for line1 in f1.readlines():
	line1=line1.strip('\n')
	fasta=re.findall(r'(%s).*?\n(.*?)>' %line1,data2,re.S)
#	print (fasta)
	try:
		f3.write('>'+fasta[0][0]+'\n'+fasta[0][1])
	except:
		pass
f1.close()
f2.close()
f3.close()
