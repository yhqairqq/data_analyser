#!/usr/bin/env python
# coding:utf-8
#根据city 将数据从主表中删除,迁移到副表中
import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId

def export(db):
    page_size = 100
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
        filter={
            'city':310000
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
         filter={
            'city':310000
        }
    ).sort('_id', pymongo.ASCENDING).count()

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
                # 假如处理的方法
                result = db.MainShop_DataOrign_Shanghai.update_one({'_id':json[u'_id']},{'$set':json},True)
                if result.upserted_id!=None :
                    if i%1000==0:
                      print '插入>>>>>>',json[u'_id']

            except Exception, e:
                print e, "Exception",json

        if last_row_id!='':
          print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'city':310000
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);
if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33332)
    conn = pymongo.MongoClient('10.15.159.169', 30000)
    # 连接数据库
    db = conn.crawl_hz
    export(db)