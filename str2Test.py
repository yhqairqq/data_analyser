#!/usr/bin/env python
#coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import traceback

fi=open('/Users/YHQ/baiduyun/chenwei/0805/str2Test.txt','rb')

line =fi.readline();
stack=[]
while line!=None and line != '' and line!='\n':
    newline=''
    l=len(line)
    i=0

    while i<l:
        newline =newline+line[i]
        ch=line[i]
        if line[i]=='"' and len(stack)==0:
            stack.append("s")
            i=i+1
            continue
        if line[i]=='"' and len(stack)==1 and i< l-1 and (line[i+1]==',' or line[i+1]==':' or line[i+1]=='}'):
            stack.pop()
            i=i+1
            continue
        if line[i]=='"' and len(stack)==1 and i< l-1 and  line[i+1]!=',' and line[i+1]!=':':
            #向前找到逗号或者冒号的下标,在下标前插入缺损的",下标改成插入位置,在新行尾部加入缺损的"
            index1=newline.rindex(',')
            index2=newline.rindex(':')
            index=0
            if index1>index2:
                index=index1
            else:
                index=index2
            newline = newline[0:index]+'"'+newline[index:]
            i = i+1
            continue
        i=i+1
    print newline
    line=fi.readline()

fi.close()