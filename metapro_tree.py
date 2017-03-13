#!/usr/bin/python
# -*- coding:UTF-8 -*-

import re,os,time,sys,commands,time
from optparse import OptionParser

p = OptionParser()
p.add_option('-f',dest='files',help="files containing amino acid sequences",type="str")
p.add_option('-m',dest='outfmt',help="outputfile format",type="int")
p.add_option('-e',dest='evalue',help="blastp's evalue,defult 10,cannot be string likes 1E-5!",type="str")
(opts,args) = p.parse_args()

if not (opts.files):sys.exit()
opts.outfmt=opts.outfmt if opts.outfmt else 0
opts.evalue=opts.evalue if opts.evalue else 10

#创建临时文件夹
pass if (os.path.exists(os.path.join(os.getcwd(),'tmpdir'))) else os.mkdir(os.path.join(os.getcwd(),'tmpdir'))
os.chdir(os.path.join(os.getcwd(),'tmpdir'))
fileIn=re.split(r'\,',opts.files)
for fileNum in range(0,len(fileIn)):
	os.system('cp "../"+fileIn[fileNum] .')
	file=open(fileIn[fileNum],'r')
	peptidesall=open('peptidesall.txt','a')
	peptidesall.write(file.read())
	file.close
	peptidesall.close
	
#simplify
os.system('sort -u peptidesall.txt > peptides.txt')

peptides=open('peptides.txt','r')
peptides_fasta=open('peptides_fasta.txt','w')
#line 是氨基酸序列 #lines是当前行数
lines=0
for line in peptides.readlines():
	lines+=1
	peptides_fasta.write('>'+line+lines)
	peptides_fasta.write(line)
peptides.close
peptides_fasta.close
#get lines
#lines=re.search(r'(\d+)? \w',commands.getoutput('wc -l peptides.txt')).group(1)

#split to 10 items by lines
line=2*(lines/10+1)
os.system("split -l line peptides_fasta.txt -d -a 1 'peptides_fasta'+line.")
os.system("ls |grep 'peptides_fasta'+line. >fastafile_name.txt")
fastafile_name=open('fastafile_name.txt','r')
for fasta_name in fastafile_name.read():
	fasta_name=fasta_name.strip('\n')
	sh=open(fasta_name+opts.evalue+'.sh','w')
	sh.write('''
#from aas to blastp for MEGAN6C and ktImportTaxonomy and mgpipev1
#PBS -l nodes=1:ppn=5
#PBS -l mem=10G
#PBS -q sg
cd \$PBS_O_WORKDIR
blastp -query fasta_name -outfmt opts.outfmt -evalue opts.evalue -matrix PAM30 -out fasta_name_opts.evalue_out -num_threads 8 -db nr -word_size 2 -window_size 15 -show_gis
cat fasta_name_opts.evalue.out>>all.out.txt";
''')
sh.close
os.system("qsub fasta_name+opts.evalue+'.sh'")

b=0
for (1;i<lines;1):
	time.sleep 10
	BLAST=open('all.out.txt','r')
	for line in BLAST.readlines():
		if re.search(r'Query='):i+=1
		if re.search(r'Value'):b+=10

for fileNum in range(0,len(fileIn)):
	os.system('cp "../"+fileIn[fileNum] .')
	file=open(fileIn[fileNum],'r')
	















