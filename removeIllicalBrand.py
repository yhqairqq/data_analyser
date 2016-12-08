#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
from bson.objectid import ObjectId

# 创建连接
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
# conn = pymongo.MongoClient('10.15.86.90',30000)
conn = pymongo.MongoClient('127.0.0.1', 33333)
# 连接数据库
db = conn.crawl
collection = db.MainShop5
page = 0
page_size = 10000
i = 1.0
last_row_id = ''
content = collection.find(
    projection={
        '_id': 1,
        'dataOrigin': 1,
        'shopId': 1
    }).sort('_id', pymongo.ASCENDING).limit(page_size)
count = collection.find(
    projection={
        '_id': 1
    }).sort('_id', pymongo.ASCENDING).count()

print 'totalSize:', count

if count == 0:
    exit(1)

while True:
    row = 0
    for json in content:
        row = row + 1
        if row == page_size - 1:
            last_row_id = json[u'_id']
        i = i + 1
        if i % 1000 == 0:
            print json
        if i % 10000 == 0:
            print "完成>>>>%.2f" % (i / count * 100), "%"
        try:
            shopId = json[u'shopId']
            dataOrigin = json[u'dataOrigin']
            curcor = collection.find({'dataOrigin':dataOrigin,'shopId':shopId})

            arr_id=[]
            for c in curcor:
                arr_id.append(c[u'_id'])
            if len(arr_id) >=2:
                ii=1
                while ii<len(arr_id):
                    if i%1000==0:
                      print '删除_id',arr_id[ii],'shopId',shopId,'dataOrigin',dataOrigin
                    result = collection.delete_one({u'_id': arr_id[ii]})
                    ii=ii+1
                count = collection.find(
                        projection={
                            '_id': 1
                        }).sort('_id', pymongo.ASCENDING).count()
        except Exception, e:
            print e,arr_id

    print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = collection.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)},
                # 任意元素匹配所有条件
            },
            projection={
                '_id': 1,
                'dataOrigin': 1,
                'shopId': 1
            }).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        exit(1);
