#!/usr/bin/env python
#coding:utf-8

import pymongo
import datetime
import random
import traceback
import re
from bson.objectid import ObjectId


def getBrand(line):
    #【（﹙\(].+[）\)﹚】
    line=re.sub(u'【[^】]*】', "", line)
    line=re.sub(u'（[^）]*）', "", line)
    line=re.sub(u'﹙[^﹚]*﹚', "", line)
    line=re.sub(u'\([^\)]*\)', "", line)
    #|(（[^）]*）)|
    return line

#创建连接
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.86.90:30000/')
conn = pymongo.MongoClient('10.15.86.90',30000)
#conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#连接数据库
db = conn.crawl
collection = db.MainShop5
page=0
page_size=10000
i=1.0
last_row_id=''
content = collection.find(
    # filter={
    #     'brand':u''
    # },
    projection={
        '_id':1,
        'brand':1,
        'shopName':1
    }).sort('_id',pymongo.ASCENDING).limit(page_size)
count=collection.find(
    # filter={
    #     'brand':u''
    # },
    projection={
        '_id':1
    }).sort('_id',pymongo.ASCENDING).count()

print 'totalSize:',count

if count==0:
  exit(1)

while True:
    row=0
    for json in content:
      row = row+1
      if row == page_size-1:
          last_row_id=json[u'_id']
      i=i+1

      if i%10000==0:
        print "完成>>>>%.2f" % (i/count*100),"%"
      try:

         if len(json[u'brand'])==0:
             brand = getBrand(json[u'shopName'])
             if i%1000==0:
                 print 'shopName-->',json[u'shopName'],"brand--->",brand
             date_time = datetime.datetime.utcnow()
             result=collection.update({'_id':ObjectId(json[u'_id'])},{'$set':{"brand":brand,"createAt":date_time,"updateAt":date_time}})
             if result[u'nModified']==1:
                      print '更新成功>>>>>>',json
      except Exception,e:
          print last_row_id

    print "last_row_id>>>>>"+str(last_row_id)

    if last_row_id !='':
        content = collection.find(
            filter={
                    '_id':{'$gt':ObjectId(last_row_id)},
                    # 'brand':u''
                    # 任意元素匹配所有条件
                },
            projection={
                '_id':1,
                'brand':1,
                'shopName':1
            }).sort('_id',pymongo.ASCENDING).limit(page_size)
        last_row_id=''
    else :
        print "完成>>>>%.2f" % (i/count*100),"%"
        exit(1);


