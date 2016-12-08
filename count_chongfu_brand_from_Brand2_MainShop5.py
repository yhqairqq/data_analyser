#!/usr/bin/env python
# coding:utf-8
# 直接从mainShop中导出brand,插入到brand2中,字段为 brandname,categry subcategray
import pymongo
import datetime
import random
import traceback
import re
from bson.objectid import ObjectId


# 创建连接
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.86.90:30000/')
# conn = pymongo.MongoClient('10.15.86.90',30000)
conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('mysql1.cuone.com',27017)
# 连接数据库
db = conn.crawl
collection = db.MainShop5
c2 = db.brand2
page = 0
page_size = 10000
i = 1.0
last_row_id = ''

fo = open('chongfubrand.txt','wb')
content = c2.find(
    filter={
        '_id': {'$gt': ObjectId('57c45cd4ec8d83142dd0924f')}
    },
    projection={
        '_id': 1,
        'name': 1
    }).sort('_id', pymongo.ASCENDING).limit(page_size)
count = c2.find(
    filter={
        '_id': {'$gt': ObjectId('57c45cd4ec8d83142dd0924f')}
    },
    projection={
        '_id': 1
    }).sort('_id', pymongo.ASCENDING).count()

print 'totalSize:', count

totalRecord=0

if count == 0:
    exit(1)
brand_dic = {}
while True:
    row = 0
    for json in content:
        row = row + 1
        if row == page_size - 1:
            last_row_id = json[u'_id']
        i = i + 1

        if i % 10000 == 0:
            print "完成>>>>%.2f" % (i / count * 100), "%"
        try:
            name = json[u'name']
            match = {
                'brand': name
            }
            group = {
                '_id': '$brand',
                'count': {'$sum': 1}

            }
            ret = collection.aggregate(
                [
                    {'$match': match},
                    {'$group': group}
                ]
            )
            for rd in ret:
                _count = rd[u'count']
                if _count > 1:
                    totalRecord=totalRecord+_count
                    if i%1000==0:
                      print 'brand-->',rd[u'_id']
                    fo.writelines(rd[u'_id']+","+str(_count)+'\n')

        except Exception, e:
            print 'exception', e

    print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = c2.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)},
                # 'brand':u''
                # 任意元素匹配所有条件
            },
            projection={
                '_id': 1,
                'name': 1
            }).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        exit(1);
print 'totalRecord=',totalRecord
fo.close()