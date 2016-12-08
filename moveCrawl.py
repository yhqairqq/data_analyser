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

def moveMainShop(orgin_db,dst_db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = orgin_db.MainShop5.find(
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = orgin_db.MainShop5.find(
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
                result = dst_db.MainShop.update_one({'_id':json[u'_id']},{'$set':json},True)
                if result.upserted_id!=None :
                    if i%1000==0:
                      print '插入>>>>>>',json[u'_id']

            except Exception, e:
                print e, "Exception"

        if last_row_id!='':
          print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = orgin_db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);
def moveBrand(orgin_db,dst_db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = orgin_db.brand.find(
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = orgin_db.brand.find(
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
                result = dst_db.brand.update_one({'_id':json[u'_id']},{'$set':json},True)
                if result.upserted_id!=None :
                    if i%1000==0:
                      print '插入>>>>>>',json[u'_id']

            except Exception, e:
                print e, "Exception"

        if last_row_id!='':
          print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = orgin_db.brand.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);
if __name__ == '__main__':
    # conn1 = pymongo.MongoClient('127.0.0.1', 33333)
    # conn2 = pymongo.MongoClient('127.0.0.1', 33332)
    conn1 = pymongo.MongoClient('10.15.86.90', 30000)
    conn2 = pymongo.MongoClient('10.15.159.169', 30000)
    # 连接数据库
    orgin_db = conn1.crawl
    dst_db=conn2.crawl_hz
    moveMainShop(orgin_db,dst_db)
    moveBrand(orgin_db,dst_db)