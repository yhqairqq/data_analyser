#!/usr/bin/env python
#coding:utf-8
# Author:   --<qingfengkuyu>
# Purpose: MongoDB的使用
# Created: 2014/4/14
#32位的版本最多只能存储2.5GB的数据（NoSQLFan：最大文件尺寸为2G，生产环境推荐64位）

import pymongo
import datetime
import random
import os
import fnmatch
import  json
#创建连接
#conn = pymongo.Connection('mysql1.cuone.com',27017)
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@localhost:27017/')
#conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#连接数据库
#db = conn.coupon
#collection = db.MainShop4
#i=1.0
#totalSize = collection.count()
fi = open('/Users/YHQ/baiduyun/qilin/tradeArea.log','r')
tradefo = open('/Users/YHQ/baiduyun/qilin/tradeArea1.log','w')
#totalSize = fi.tell();
#content = collection.find()
current = 0.0;
row=0
containerTradeArea=[]
for line in fi:
    current=current+ len(line)
    jsonObj = json.loads(line)
    containerTradeArea.append(jsonObj[u'tradingArea'])
    row=row+1
   # i=i+1
    if len(containerTradeArea)%100==0:
            containerTradeArea = list(set(containerTradeArea))
print '正在写入...'
tradefo.writelines(containerTradeArea)