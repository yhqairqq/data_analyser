#!/usr/bin/env python
#coding:utf-8


f='/Users/YHQ/baiduyun/chenwei/0818/testfile'
outf='/Users/YHQ/baiduyun/chenwei/0818/testfilejs'
fi = open(f,'rb')
fo = open(outf,'wb')
line = fi.readline()

c='brand'

i=0

while line!=None and line!="":
    line =line.replace("\n","")
    outline = "db."+c+".insert("+line+")\n"
    fo.writelines(outline)
    line=''
    line=fi.readline()
    i=i+1
    if i%10000==0:
        print '完成',i

print '完成',i
fi.close()
fo.close()
