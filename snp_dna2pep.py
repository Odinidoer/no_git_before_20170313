#!/usr/bin/python
#-*- coding:UTF-8 -*-

import re,os,time,sys,commands,time
from optparse import OptionParser
p=OptionParser()
#file1	***
#file2	/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/dna/Solanum_lycopersicum.SL2.50.dna.toplevel.fa
#file3	/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/pep/Solanum_lycopersicum.SL2.50.pep.all.fa
#file4	/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/cdna/Solanum_lycopersicum.SL2.50.cdna.all.fa
p.add_option('--file1',dest='file1',help="snp file being searching",type="str")
p.add_option('--file2',dest='file2',help="db file containing dna_seq	file2=/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/dna/Solanum_lycopersicum.SL2.50.dna.toplevel.fa",type="str")
p.add_option('--file3',dest='file3',help="db file containing pep_seq	file3=/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/pep/Solanum_lycopersicum.SL2.50.pep.all.fa",type="str")
p.add_option('--file4',dest='file4',help="db file containing cdna_seq	file4=/mnt/ilustre/users/jun.yan/database/pub/release-32/plants/fasta/solanum_lycopersicum/cdna/Solanum_lycopersicum.SL2.50.cdna.all.fa",type="str")
(opts,args) = p.parse_args()
			
def find_mut_info(line):
	info=re.split(r'\t',line)[8]
	re_find=re.compile(r'(\w+?\d+?\w+?\d+?\.\d+?)\:\1\.\d+?\:\w+?\:\c\.([A-Za-z]*?)(\d+?)([A-Za-z]*?)\:p\.([A-Za-z]*?)(\d+?)([A-Za-z]*?),')
	return re_find.findall(info)

def find_complexmut_info(line):
	info=re.split(r'\t',line)[8]
	#re_find=re.compile(r'(\w+?\d+?\w+?\d+?\.\w+?)\:\1\.\d+?\:\w+?\:\c\.([A-Za-z]*?)(\d+?)\_\d+(\w+)\:p\.(\d+)\_\d+(\w+)(\d*),')
	re_find=re.compile(r'(\w+?\d+?\w+?\d+?\.\w+?)\:\1\.\d+?\:\w+?\:c\.([a-zA-Z]*)(\d*)\_?\d*([a-zA-Z]*)\:p\.([a-zA-Z]*)(\d*)\_?\d*([a-zA-Z]*),')
	return re_find.findall(info)
	
def find_gene_name(line):
#find find_pep_name from line that contains genename
	items=re.split(r'\t',line)
	GENE=items[6]
	gene=re.findall(r'(Solyc\d+?[a-zA-z]\d+?\.\d)',GENE)[0]
	return gene 
	
def find_chrom_loc(line,pep_all_fa):
#find find_pep_name from line that contains genename
	items=re.split(r'\t',line)
	GENE=items[6]
	gene=re.findall(r'(Solyc\d+?[a-zA-z]\d+?\.\d)',GENE)[0]
	os.environ['snp_gene']=gene
	os.environ['pep_all_fa']=pep_all_fa
	pepinfo=commands.getoutput('grep $snp_gene $pep_all_fa')
	if re.search(r'%s' % gene,pepinfo):
		chrom_loc=re.findall(r'(chromosome\:\w+?\.\w+?\:\d+?\:)',pepinfo)[0]
		return chrom_loc

def find_seq_from_db(name,db):
#find find_pep_seq_ref from pep_all_fa
	os.environ['search_name']=name
	os.environ['seqrch_db']=db
	i=10
	while i<10001:
		os.environ['search_len']=str(i)
		os.environ['search_len_huanhang']=str(i+1)
		data=commands.getoutput('grep -A $search_len $search_name $seqrch_db')
		#print data
		if re.subn(r'>',r'>',data)[1] > 1 or i==10000:
			data=commands.getoutput('grep -A $search_len_huanhang $search_name $seqrch_db')
			return re.sub(r'\n',r'',re.split(r'>.*?\n',data)[1])
			breaks
		else:
			i*=10
		
def replace(str_in,start,end,ref,alt):
#replace ref by alt in mutation palce 
	if start and end:
		start,end=int(start)-1,int(end)-1
		str_in=re.sub(r'\n',r'',str_in)
		strlist=list(str_in)
		len_in=len(ref)
		if ref=='-':len_in=0
		if ref=='0':ref='N'
		if len(strlist)>end:
			#print strlist[start],ref
			#if ref=='-' or re.search(r'%s'%ref,strlist[start]):
			if ref=='-' or re.search(strlist[start],ref):
				for i in range(0,len_in):
					del strlist[start+i]
				if alt=='-':
					pass
				else:
					strlist.insert(start,alt)
				return ''.join(strlist)
			else :
				strlist='error:cannot match to pep in mut position'
				return strlist
		else:
			strlist='error:pep is too short to mut'
			return strlist
				
def replicate(DNA_seq):
#DNA to DNA
	DNA_seq=re.sub(r'\n',r'',DNA_seq)
	DNA2DNA_trans={'A':'T','G':'C','C':'G','T':'A'}
	return ''.join([DNA2DNA_trans[DNA_seq[i]] for i in range(0,len(DNA_seq))])
	
def transcript(DNA_seq):
#DNA to RNA
	DNA_seq=re.sub(r'\n',r'',DNA_seq)
	DNA2RNA_trans={'A':'U','G':'C','C':'G','T':'A','U':'A'}
	return ''.join([DNA2RNA_trans[DNA_seq[i]] for i in range(0,len(DNA_seq))])

def translate(codon):
#RNA to pep_seq
	pep_seq=['']
	RNA2pep_trans={
'UUU':'F','UUC':'F','UUA':'L','UUG':'L',#F±Ω±˚∞±À·£¨L¡¡∞±À·
'CUU':'L','CUC':'L','CUA':'L','CUG':'L',#L¡¡∞±À·
'AUU':'I','AUC':'I','AUA':'I','AUG':'M',#I“Ï¡¡∞±À·£¨Mµ∞∞±À·
'GUU':'V','GUC':'V','GUA':'V','GUG':'V',#VÁ”∞±À·
'UCU':'S','UCC':'S','UCA':'S','UCG':'S',#SÀø∞±À·
'CCU':'P','CCC':'P','CCA':'P','CCG':'P',#P∏¨∞∑À·
'ACU':'T','ACC':'T','ACA':'T','ACG':'T',#TÀ’∞±À·
'GCU':'A','GCC':'A','GCA':'A','GCG':'A',#±˚∞±À·
'UAU':'Y','UAC':'Y','UAA':'O','UAG':'O',#Y¬Á∞±À·£¨0÷’÷π√‹¬Î◊”
'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',#H◊È∞±À·£¨Qπ»∞±ı£∞∑
'AAU':'N','AAC':'N','AAA':'K','AAG':'K',#NÃÏ∂¨ı£∞∑£¨K¿µ∞±À·
'GAU':'D','GAC':'D','GAA':'E','GAG':'E',#DÃÏ∂¨∞±À·£¨Eπ»∞±À·
'UGU':'C','UGC':'C','UGA':'0','UGG':'W',#C∞ÎÎ◊∞±À·£¨W…´∞±À·
'CGU':'R','CGC':'R','CGA':'R','CGG':'R',#Ræ´∞±À·
'AGU':'S','AGC':'S','AGA':'R','AGG':'R',#SÀø∞±À·,Ræ´∞±À·
'GGU':'G','GGC':'G','GGA':'G','GGG':'G',#G∏ ∞±À·
}
	return RNA2pep_trans[codon]
		
def getPep(DNA_seq):	
#translate dnaseq to pepseq and i am not sure how to make sure which one is correct
	RNA_seq=transcript(transcript(DNA_seq))
	codon=re.findall(r'\w{3}',RNA_seq)
	pep_seq=['']
	for i in range(0,len(codon)):
		if translate(codon[i])=='0':
			break	
		else:
			pep_seq.append(translate(codon[i]))
	return ''.join(pep_seq)
	
def get_enz_pep_split(pep,loc):	
	loc=int(loc)
	if len(pep)<7:
		enz='pep is too short to trypsin digeste'
	elif re.subn(r'K',r'K',pep)[1]+re.subn(r'R',r'R',pep)[1]<=2 or len(pep)<17:
		enz=pep
	else:
		enz_re=re.findall(r'[A-JL-QS-Z]*?[KR]',pep)
		pep='K'+pep
		#rint (re.findall(r'[KR]([A-JL-QS-Z]*?)$',pep)[0])
		lyc_list,start,end=[''],[''],['']
		start[0]=0
		end[0]=start[0]+len(enz_re[0])-1
		lyc_list.append(start[0])
		lyc_list.append(enz_re[0])
		lyc_list.append(end[0])
		for x in range(1,len(enz_re)):
			start.append(end[x-1]+1)
			end.append(start[x]+len(enz_re[x])-1)
			lyc_list.append(start[x])
			lyc_list.append(enz_re[x])
			lyc_list.append(end[x])
		lyc_list.append(len(pep)-len((re.search(r'[KR]([A-JL-QS-Z]*?)$',pep).group())))
		lyc_list.append((re.findall(r'[KR]([A-JL-QS-Z]*?)$',pep)[0]))
		lyc_list.append(len(pep))
		for x in range(0,len(enz_re)+1):
			if lyc_list[3*x+1]<=loc and loc<=lyc_list[3*x+3]:
				mark=x
				if mark<2:
					enz=lyc_list[2]+lyc_list[5]+lyc_list[8]
				elif mark<=len(enz_re)-2:
					enz=lyc_list[3*(mark-1)+2]+lyc_list[3*(mark)+2]+lyc_list[3*(mark+1)+2]
				else:
					enz=lyc_list[3*(len(enz_re)-2)+2]+lyc_list[3*(len(enz_re)-1)+2]+lyc_list[3*len(enz_re)+2]
				break	
	return enz

def mutation_deal(file1,file2,file3,file4):	
	fi=open(file1,'r')
	if os.path.isfile(os.path.join(os.getcwd(),'pep'+file1)):os.remove(os.path.join(os.getcwd(),'pep'+file1))
	fo=open('pep'+file1,'a')
	for line in fi.readlines():
		line=line.strip('\n')
		#print line
		cdna_seq=new_cdna_seq=pep_seq=new_pep_seq=lyc_enzyme_pep=''
		if re.search(r'CHROM',line):
			cdna_seq='cDNA seq'
			new_cdna_seq='new cDNA seq'
			pep_seq='Peptide seq'
			new_pep_seq='New peptide seq'
			lyc_enzyme_pep='KR to split seq for lyc'
			fo.write(line+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
			fo.flush()
		else:	
			items=re.split(r'\t',line)
			type=items[7].strip('\t')
			if type=='nonsynonymous SNV':#pep			
				gene_name=find_gene_name(line)
				cdna_seq=find_seq_from_db(gene_name,file4)
				pep_seq=find_seq_from_db(gene_name,file3)
				mut_info=find_mut_info(line)
				new_pep_seq=replace(pep_seq,mut_info[0][5],mut_info[0][5],mut_info[0][4],mut_info[0][6])
				if not re.search(r'error',new_pep_seq):lyc_enzyme_pep=get_enz_pep_split(new_pep_seq,mut_info[0][5])
				fo.write(line+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
				fo.flush()
			if type=='stopgain SNV':
				mut_info=find_mut_info(line)
				if re.search(r'_',items[8]):
					mut_info=find_complexmut_info(line)
				if mut_info:
					gene_name=find_gene_name(line)
					cdna_seq=find_seq_from_db(gene_name,file4)
					pep_seq=find_seq_from_db(gene_name,file3)
					if re.search(r'wholegene',line):
							pass
					else:
						new_pep_seq=replace(pep_seq,mut_info[0][5],mut_info[0][5],mut_info[0][4],mut_info[0][6])
						new_pep_seq=''.join([new_pep_seq[x] for x in range(0,int(mut_info[0][5]))])
						if not re.search(r'error',new_pep_seq):lyc_enzyme_pep=get_enz_pep_split(new_pep_seq,mut_info[0][5])
				else:
					cdna_seq='re is broken'		
				fo.write(line+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
				fo.flush()
			if type=='stoploss SNV':#dna
				mut_info=find_mut_info(line)								
				gene_name=find_gene_name(line)
				cdna_seq=find_seq_from_db(gene_name,file4)
				new_cdna_seq=replace(cdna_seq,mut_info[0][2],mut_info[0][2],items[3],items[4])
				pep_seq=find_seq_from_db(gene_name,file3)
				fo.write(line+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
				fo.flush()
			if re.search(r'frameshift',type):#dna				
				if re.search(r'wholegene',line): 
					pass
				else:
					mut_info=find_mut_info(line)
					if re.search(r'_',items[8]):
						mut_info=find_complexmut_info(line)
					if mut_info:
						gene_name=find_gene_name(line)
						cdna_seq=find_seq_from_db(gene_name,file4)					
						if re.search(r'frameshift deletion',type):
							#print cdna_seq[int(mut_info[0][2])-1],items[3],replicate(items[3])
							if not re.search(cdna_seq[int(mut_info[0][2])-1],items[3]):items[3]=replicate(items[3])							
						new_cdna_seq=replace(cdna_seq,mut_info[0][2],mut_info[0][2],items[3],items[4])						
						pep_seq=find_seq_from_db(gene_name,file3)	
					else:
						cdna_seq='re is broken'
				fo.write(line+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
				fo.flush()	
		#print 'mutation_deal done'
	fo.close	
	fi.close	

def makeORF_hammscan(file1,file4):
	fi1=open('pep'+file1,'r')
	if os.path.isfile(os.path.join(os.getcwd(),file1+'.fa')):os.remove(os.path.join(os.getcwd(),file1+'.fa'))
	fo1=open(file1+'.fa','a')
	for line in fi1.readlines():
		line=line.strip('\n')
		if re.search(r'frameshift|stoploss SNV',line):
			items=re.split(r'\t',line)
			if re.search(r'wholegene',line): 
				pass
			info='>'+items[6]+'\n'+items[10]+'\n'
			if not re.search(r'error|re is broken',info):
				fo1.write(info)
				fo1.flush()
	fo1.close()
	fi1.close()
	os.environ['ALLFASTA']=file1+'.fa'
	os.system('/mnt/ilustre/app/rna/assemble_mrna/trinityrnaseq_r20140413/trinity-plugins/TransDecoder_r20131110/TransDecoder -t $ALLFASTA --cd_hit_est /mnt/ilustre/users/kai.luo/software/cdhit-master/cd-hit-est --search_pfam /mnt/ilustre/users/ting.kuang/software/pfamscan/pfam_database/Pfam-A.hmm -T 3000 -m 100 --CPU 10 >/dev/null 2>&1')
	#get the file already
	
def makeORF(file1,file4):
	cdsdb=str(file1)+'.fa.transdecoder.cds'
	f_orf=open(cdsdb,'r').read()
	pepdb=str(file1)+'.fa.transdecoder.pep'
	f_orf_pep=open(pepdb,'r').read()
	fi2=open('pep'+file1,'r')
	if os.path.isfile(os.path.join(os.getcwd(),'orf'+file1)):os.remove(os.path.join(os.getcwd(),'orf'+file1))
	fo2=open('orf'+file1,'w')
	title_mut='CHROM	START	END	REF	ALT	ANNO	GENE(in or nearby)	MUT_type	MUT_info'
	cdna_seq='cDNA seq'
	new_cdna_seq='new cDNA seq'
	pep_seq='Peptide seq'
	new_pep_seq='New peptide seq'
	lyc_enzyme_pep='KR to split seq for lyc'
	fo2.write(title_mut+'\t'+cdna_seq+'\t'+new_cdna_seq+'\t'+pep_seq+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')
	fo2.flush()
	
	for line in fi2.readlines():
		line=line.strip('\n')
		#print line
		items=re.split(r'\t',line)
		cdna_seq=new_cdna_seq=new_cdna_seq=new_pep_seq=lyc_enzyme_pep=''
		mut_info=find_mut_info(line)
		if re.search(r'_',items[8]):
			mut_info=find_complexmut_info(line)
		if re.search(r'MUT_type'):
			pass
		if re.search(r'frameshift|stoploss SNV',line):
			if re.search(r'wholegene|error|re is broken',line): 
				fo2.write(line+'\n')
				fo2.flush()
			else:	
				gene_name=find_gene_name(line)
				new_cdna=re.findall(r'>(%s.*?ORF).*?:(\d+)-(\d+).*?\n(.*?)>' % gene_name,f_orf,re.S)
				if len(new_cdna)>0 and new_cdna[0][1]<mut_info[0][2] and mut_info[0][2]<new_cdna[0][2]:
					new_cdna_seq=re.sub(r'\n',r'',new_cdna[0][3])
					new_cdna_name=new_cdna[0][0]
					new_pep_seq=re.findall(r'%s.+?\n(.*?)>' % new_cdna_name,f_orf_pep,re.S)[2]
					new_pep_seq=re.sub(r'\n',r'',new_pep_seq)
				lyc_enzyme_pep='this is from ORF'
				fo2.write(items[0]+'\t'+items[1]+'\t'+items[2]+'\t'+items[3]+'\t'+items[4]+'\t'+items[5]+'\t'+items[6]+'\t'+items[7]+'\t'+items[8]+'\t'+items[9]+'\t'+new_cdna_seq+'\t'+items[11]+'\t'+new_pep_seq+'\t'+lyc_enzyme_pep+'\n')	
				fo2.flush()
		else:
			fo2.write(line+'\n')
			fo2.flush()
		#print 'ORF done'	
	fi2.close()
	fo2.close()
	
if __name__=='__main__':			
	mutation_deal(opts.file1,opts.file2,opts.file3,opts.file4)	
	#print 'snp_sna2pep mutation_deal done'
	makeORF_hammscan(opts.file1,opts.file4)
	makeORF(opts.file1,opts.file4)
	#print 'snp_sna2pep makeORF done'

if __name__=='_1_main__':
	line='10	3007015	3007015	C	A	exonic	Solyc10g008980.2	nonsynonymous SNV	Solyc10g008980.2:Solyc10g008980.2.1:exon12:c.C1233A:p.N411K,'
	print line
	mut_info=find_complexmut_info(line)
	print mut_info
	transcripts=find_gene_name(line)
	print transcripts
	items=re.split(r'\t',line)
	type=items[7].strip('\t')
	gene_name=find_gene_name(line)
	cdna_seq=find_seq_from_db(gene_name,opts.file4)
	print cdna_seq
	new_cdna_seq=replace(cdna_seq,mut_info[0][2],mut_info[0][2],items[3],items[4])
	print new_cdna_seq
	pep_seq=find_seq_from_db(gene_name,opts.file3)
	print pep_seq
	mut_info=find_mut_info(line)
	new_cdna_seq=''
	new_pep_seq=replace(pep_seq,mut_info[0][5],mut_info[0][5],mut_info[0][4],mut_info[0][6])
	#new_pep_seq=''.join([new_pep_seq[x] for x in range(0,int(mut_info[0][5]))])
	print new_pep_seq
	lyc_enzyme_pep=get_enz_pep_split(new_pep_seq,mut_info[0][5])
	print lyc_enzyme_pep