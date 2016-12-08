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
conn = pymongo.MongoClient('10.15.86.90',30000)
# conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('mysql1.cuone.com',27017)
# 连接数据库
db = conn.crawl
c1 = db.MainShop5
c2 = db.brand
page = 0
page_size = 10000
i = 1.0
last_row_id = ''
brandId=0
#品牌名一致,分类不一致的记录数
totalRecord=0
content = c1.find(
    filter={
        '_id': {'$gt': ObjectId('57a029fc951f59b1cf85730a')}
    },
    projection={
        '_id': 1,
        'brand': 1,
        'category': 1,
        'subCategory': 1
    }).sort('_id', pymongo.ASCENDING).limit(page_size)
count = c1.find(
    filter={
        '_id': {'$gt': ObjectId('57a029fc951f59b1cf85730a')}
    },
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

        if i % 10000 == 0:
            print "完成>>>>%.2f" % (i / count * 100), "%"
        try:

            if len(json[u'brand']) != 0:
                brand = json[u'brand']
                brandId = brandId+1
                category = ''
                subCategory=''
                if json[u'category']!=None:
                    category=json[u'category'][0]
                if  json[u'subCategory']!=None:
                    subCategory=json[u'subCategory'][0]

                c2_count = 0
                c2_count = c2.find(
                    filter={
                        'name': brand,
                        'category':category,
                        'subCategory':subCategory
                    },
                    projection={
                         'name': 1,
                         'category':1,
                         'subCategory':1
                    }).sort('_id', pymongo.ASCENDING).count()

                if c2_count ==0:
                    date_time = datetime.datetime.utcnow()
                    result = c2.insert_one({'name':brand,'brandId':brandId,'category':category,'subCategory':subCategory,'createAt':date_time,'updateAt':date_time})
                    if result.inserted_id != None and i%1000 == 0:
                        print '插入成功',result.inserted_id
                    # c1_mainShop_count = c1.find(
                    #     filter={
                    #         'brand': brand,
                    #         'category':{'$ne':category},
                    #         'subCategory':{'$ne':subCategory}
                    #     },
                    #     projection={
                    #          'name': 1,
                    #          'category':1,
                    #          'subCategory':1
                    #     }).sort('_id', pymongo.ASCENDING).count()
                    # if c1_mainShop_count > 0:
                    #     totalRecord=totalRecord+c1_mainShop_count
        except Exception, e:
            print 'exception',e

    print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = c1.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)},
                # 'brand':u''
                # 任意元素匹配所有条件
            },
            projection={
                '_id': 1,
                'brand': 1,
                'category': 1,
                'subCategory': 1
            }).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        exit(1);
print 'totalRecord',totalRecord