#!/usr/bin/env python
#coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId

#创建连接
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
conn = pymongo.MongoClient('10.15.86.90',30000)
fo = open('exportNoStantardBrandRecord.txt','wr')
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
        'brand':1
    }).sort('_id',pymongo.ASCENDING).limit(page_size)
count=collection.find(
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
      # if i%1000==0:
      #     print json
      if i%10000==0:
        print "完成>>>>%.2f" % (i/count*100),"%"
      try:

          brand = json[u'brand']
          json1 = json

          if brand == None:
              fo.writelines(json)
              print json1
              continue


          #前置处理：去掉所有空白符以及%，*，/，@这4个特殊字符
          #判断逻辑：长度大于等于1，小于等于60，且长度为1时不能是英文字母
          brand = re.sub(r'[*]*[＊]*[％]*[／]*[@]*[%]*[/]*[ ]*',"",brand)

          l =len(brand)

          if  l > 60 or l<1 or (l==1 and ((brand[0]>='a' and brand[0]<='z') or (brand[0]>='A' and brand[0]<='Z'))):
              fo.writelines(json)
              print json1
          # if len(brand) == 1 and ((brand[0]>='a' and brand[0]<='z') or (brand[0]>='A' and brand[0]<='Z')):
          #     date_time = datetime.datetime.utcnow()
          #     result = collection.update({'_id':ObjectId(json[u'_id'])},{'$set':{'brand':brand,"createAt":date_time,"updateAt":date_time}})
          #     if result[u'nModified']==1:
          #         print json[u'brand'],">>>>>>",brand

      except Exception,e:
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
                'brand':1
            }).sort('_id',pymongo.ASCENDING).limit(page_size)
        last_row_id=''
    else :
        print "完成>>>>%.2f" % (i/count*100),"%"
        exit(1);


fo.close()