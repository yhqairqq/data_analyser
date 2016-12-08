#!/usr/bin/env python
#coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
from bson.objectid import ObjectId

#创建连接
#conn = pymongo.Connection('mysql1.cuone.com',27017)
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#连接数据库
db = conn.coupon
collection = db.MainShop5
page=0
page_size=10000
i=1.0
last_row_id=''

count=collection.find(filter={
    'brand':''
}).sort('_id',pymongo.ASCENDING).count()


first = collection.find(
filter={
    'brand':''
},
projection={
    '_id':1
}).sort('_id',pymongo.ASCENDING).limit(1)


start_id=''
for one in first:
    start_id = one[u'_id']
    if start_id != '':
        break;


last_row_id = start_id
content = collection.find(
    filter={
            '_id':{'$gt':ObjectId(last_row_id)}
            # 任意元素匹配所有条件
            },
    projection={
        '_id':1
    }).sort('_id',pymongo.ASCENDING).limit(page_size)


print 'totalSize:',count

if count==0:
    exit(1)

fo = open('incomplatedRecord.txt','wb')

while True:
    row=0
    for json in content:
      row = row+1
      if row == page_size-1:
          last_row_id=json[u'_id']
      i=i+1
      if i%1000==0:
          print json
      if i%10000==0:
        print "完成>>>>%.2f" % (i/count*100),"%"
      try:
        date_time = datetime.datetime.utcnow()
        #collection.update({'_id':ObjectId(json[u'_id'])},{'$set':{"createAt":date_time,"updateAt":date_time}})
        #fo.writelines(json.dumps(json))
        print json
      except Exception,e:
          print last_row_id

    print "last_row_id>>>>>"+str(last_row_id)

    if last_row_id !='':
        content = collection.find(
            filter={
                    '_id':{'$gt':ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                }).sort('_id',pymongo.ASCENDING).limit(page_size)
        last_row_id=''
    else :
        print "完成>>>>%.2f" % (i/count*100),"%"
        exit(1);

fo.close()
