#!/usr/bin/env python
#coding: utf-8
#Program:
#    This program show "to get required file between two different files according same column"!
#History:
#2016/12/10     hui.wan     v1

import argparse, re

#参数设置
parser = argparse.ArgumentParser(description = 'this is used to get required file between two different files according same column.' + "\n" + "-"*30 + "\n" + 'Example:' + "\n" + 'python file1tofile2.py  -i1 out.list -i2 testMetabolism.list -l1 1 -l2 1 -o testout.list -ol1 1,2 -ol2 1' + '\n' + '-'*30)

parser.add_argument("-i1", "--inputfile1", type = str, help = 'input file1', required = True)
parser.add_argument("-i2", "--inputfile2",type = str, help = "input file2", required = True)
parser.add_argument("-o", "--outputfile", type = str, help = "output file", required = True)
parser.add_argument("-l1","--colnumber1", type = int, help = "matched colnumber in file1", default = 1, required = False)
parser.add_argument("-l2","--colnumber2", type = int, help = "matched colnumber in file2", default = 1, required = False)
parser.add_argument("-ol1","--outcolnumber1", type = str, help = "output colnumber in file1, use ',' and '-' to split colnumbers", required=False, default = '0')
parser.add_argument("-ol2","--outcolnumber2", type = str, help = "output colnumber in file2, use ',' and '-' to split colnumbers", required=False, default = '0')

#参数变量设置
args = vars(parser.parse_args())
i1 = args["inputfile1"]
i2 = args['inputfile2']
o = args['outputfile']
l1 = args['colnumber1']
l2 = args['colnumber2']
ol1 = args['outcolnumber1']
ol2 = args['outcolnumber2']

#全局变量申明
d = {i1:"i1",i2:"i2"}
#ol1 = [int(x) for x in ol1.split(',')]
#ol2 = [int(x) for x in ol2.split(',')]
d1 = {}
d2 = {}
od1 = ""
od2 = ""


#函数定义，判断输出列的列数
def getolnumber(oln):
    olTemp = re.findall(r'\d+\-?\d*',oln)   #为了取出1-10此类输入 olTemp=['1-10','12','14-16']
    ol = []
    for i in olTemp:
        if '-' in i:
            s = i.split('-')
            ol = ol + [x for x in range(int(s[0]),int(s[1])+1)]
        else:
            ol.append(int(i))
    return ol
    

#函数定义，提取列
def getColList(col,i):
    with open(i,'r') as f:
        frd = [line.rstrip('\n') for line in f.readlines()] #将文件每行内容作为元素存入列表中
	#删除空行
        try:
            frd.remove('')
        except:
            pass
            
    header = frd[0].split('\t') #取表头存入列表，用来判断文件列数
    
    #判断输入列数是否正确
    try:
        col = int(col)  #判断输入的是否为列数
        if col <= len(header):
            globals()["_".join(["col",str(col),d[i]])]=[x.split('\t')[col-1] for x in frd]
        else:
            print "\nError! %s is out of index in %s, please input right colnumber.\n" %(col, i)
            exit
    except:
        if col in header:   #输入的为列名
            coln = header.index(col)   
            globals()["_".join(["col", str(coln), d[i]])]=[x.split('\t')[coln] for x in frd]
        else:
            print "\nInput Error, this is no %s column in %s, please input right colname.\n" %(col,i)
            exit

#函数，输出列判断
#def add_od(i,y):
#    if d[i] == "i1":
#        d1[y]=globals()[y]
#    else:
#        d2[y]=globals()[y]
        
#函数，提取输出列，由于getColList函数参数只能输入数字，而本次需要输入列表，故建立getOutCol
def getOutCol(ol,i):
    if ol == [0]:
        globals()["_".join(["col",str(0),d[i]])]=[]
        #add_od(i,"_".join(["col",str(0),d[i]]))
    else:
        for j in ol:
            getColList(j,i)
            #add_od(i,"_".join(["col",str(j),d[i]]))     #将输出列变量及其内容存入字典，方便遍历每个列变量，从而取得对应的列内容  
            ##无需这样做了，将ol列表与对应变量组成字典，用ol列表遍历，就可以解决排序乱序问题

#运行函数，提取需要的列
def get_num_from_colV(x):
    return int(x.split('_')[1])

#运行函数，提取需要的列
ol1 = getolnumber(ol1)
ol2 = getolnumber(ol2)
getColList(l1,i1)
getOutCol(ol1,i1)
getColList(l2,i2)
getOutCol(ol2,i2)

for i in ol1:
    d1[i]=globals()['_'.join(['col',str(i),'i1'])]
for i in ol2:
    d2[i]=globals()['_'.join(['col',str(i),'i2'])]


#匹配列，并将输出列写入文件
col_i1 = globals()["_".join(["col",str(l1),'i1'])]
col_i2 = globals()["_".join(["col",str(l2),'i2'])]
with open(o,'w') as of:
    for i in range(len(col_i1)):
        for j in range(len(col_i2)):
            if col_i1[i] == col_i2[j]:
                #判断是否为空值，且进行字典排序
                if d1.values() != [[]]:
                    sd1 = [d1[x1] for x1 in ol1]
                    od1="\t".join([x[i] for x in sd1])
                if d2.values() != [[]]:
                    sd2 = [d2[x1] for x1 in ol2]
                    od2="\t".join([y[j] for y in sd2])
                    
                #判断是否为空值，且进行字典排序#############此法排序不好，不应该用这种字典###########
                #if d1.values() != [[]]:
                #    sd1=[d1[x] for x in sorted(d1.keys(),key = get_num_from_colV)]     #对字典key排序取value，将字典排序后存入元组，以免输出乱序
                #    od1="\t".join([x[i] for x in sd1])
                #if d2.values() != [[]]:
                #    sd2=[d2[x] for x in sorted(d2.keys(),key = get_num_from_colV)]
                #    od2="\t".join([y[j] for y in sd2])

                #空值判断不输出
                if d1.values() != [[]] and d2.values() != [[]]:
                    of.write("\t".join([od1,od2])+"\n")
                    
                if d1.values() == [[]] and d2.values() != [[]]:
                    of.write(od2+"\n")
                if d1.values() != [[]] and d2.values() == [[]]:
                    of.write(od1+"\n")
