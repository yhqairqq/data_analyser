#!/usr/bin/env python
# coding:utf-8
#将品牌表中的子分类,改为其他
import pymongo
import datetime
from bson.objectid import ObjectId
from MapService import *
def updateOpenhours(db):
    page_size = 1000
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
        filter={
            'openingHours':[]
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
         filter={
           'openingHours':[]
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


                print ""

            except Exception, e:
                print e, "Exception",json[u'_id']

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'openingHours':[]
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);
if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33332)
    conn = pymongo.MongoClient('10.15.86.90', 30000)
    # 连接数据库
    db = conn.crawl
    updateOpenhours(db)

    # timeStr = u'90021:00'
    # print deepExtractTimeList(timeStr)
    # print  getOpenHour(timeStr)