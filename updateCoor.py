#!/usr/bin/env python
#coding:utf-8

import pymongo
import datetime
import random
import traceback
from bson.objectid import ObjectId

#创建连接
#conn = pymongo.Connection('mysql1.cuone.com',27017)
conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
#conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#连接数据库
db = conn.crawl
collection = db.MainShop5
page=0
page_size=10000
i=1.0
last_row_id=''
content = collection.find(
    projection={
        '_id':1,
        'coordinates':1,
        'addressInfo.coordinates':1
    }).sort('_id',pymongo.ASCENDING).limit(page_size)
count=collection.find(
    # filter={
    #         "coordinates.0": {'$ne': 90},
    #         "coordinates.1": {'$ne': 360},
    #         # 任意元素匹配所有条件
    #     },
    projection={
        '_id':1,
        'coordinates':1,
        'addressInfo.coordinates':1
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
      if i%1000==0:
          print json
      if i%10000==0:
        print "完成>>>>%.2f" % (i/count*100),"%"


      latitude=json[u'coordinates'][0]
      longitude=json[u'coordinates'][1]
      if latitude !=0 and longitude!=0:

          if latitude==360 or latitude<0:
              latitude=0.0
              longitude=0.0

          if longitude>=latitude:
              coor = [longitude,latitude]
              try:
                collection.update({'_id':ObjectId(json[u'_id'])},{'$set':{'coordinates':coor,'addressInfo.coordinates':coor}})
              except Exception,e:
                  print '异常'
                  print last_row_id

    print "last_row_id>>>>>"+str(last_row_id)

    if last_row_id !='':
        content = collection.find(
            filter={
                    '_id':{'$gt':ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                },
            projection={
                '_id':1,
                'coordinates':1,
                'addressInfo.coordinates':1
            }).sort('_id',pymongo.ASCENDING).limit(page_size)
        last_row_id=''
    else :
        print "完成>>>>%.2f" % (i/count*100),"%"
        exit(1);

