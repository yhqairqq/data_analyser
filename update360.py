#!/usr/bin/env python
#coding:utf-8
# Author:   --<qingfengkuyu>
# Purpose: MongoDB的使用
# Created: 2014/4/14
#32位的版本最多只能存储2.5GB的数据（NoSQLFan：最大文件尺寸为2G，生产环境推荐64位）

import pymongo
import datetime
import random

#创建连接
#conn = pymongo.Connection('mysql1.cuone.com',27017)
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@localhost:27017/')
conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#连接数据库
db = conn.coupon
collection = db.MainShop5
content = collection.find(
    filter={
            "coordinates": {"$all": [360,360]},
            'addressInfo.coordinates': {"$all": [360,360]}
            # 任意元素匹配所有条件
        },
    projection={
        '_id':1,
        'coordinates':1,
        'addressInfo.coordinates':1
    }
)


for cucor in content:
    print cucor
    collection.update({'_id':cucor[u'_id']},{'$set':{'coordinates':[0.0,0.0],'addressInfo.coordinates':[0.0,0.0]}})

