#!/usr/bin/env python
#coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import datetime
import traceback
import  re


#字符串处理  替换单引号 一些无效的数据


fi = open('/Users/YHQ/baiduyun/exportInvalidRecord2.txt','rb')
fo = open('/Users/YHQ/baiduyun/exportInvalidRecordConvert2.txt','wb')

for line in fi:
    if len(line)<10:
        continue

    linecopy = line
    linecopy = re.sub(r'u\'',"\"",linecopy)
    linecopy = re.sub(r'\'',"\"",linecopy)
    linecopy = re.sub(r'\"createAt\"[^)]*\)\,','',linecopy)
    linecopy = re.sub(r'\"updateAt\"[^)]*\)\,','',linecopy)
    linecopy = re.sub(r'None','\"\"',linecopy)

    fo.writelines(linecopy)


fi.close()
fo.close()


