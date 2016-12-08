#!/usr/bin/env python
# coding:utf-8
import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId

def countMarchDianpingAndMainShop(db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
        filter={
            'coordinates':[0,0]
        },
        projection={
             '_id':1,
            'shopId':1
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
         filter={
             'coordinates':[0,0]
        }
    ).sort('_id', pymongo.ASCENDING).count()
    print 'totalSize:', count
    if count == 0:
        exit(1)
    match_count=0
    while True:
        row = 0
        for json in content:
            row = row + 1
            if row == page_size - 1:
                last_row_id = json[u'_id']
            i = i + 1
            if i % 10000 == 0:
                print 'march_count--->',match_count,"完成>>>>%.2f" % (i / count * 100), "%"
            try:

                shopId = json[u'shopId']
                one=db.dianping_origindata.find(
                    filter={
                        'shop_id':shopId
                    }
                )
                for curcor in one:
                    match_count = match_count + 1
                    # cityname = re.sub(u'\"','',curcor[u'city'])
                    # if cityname.find(u'县')>=0 or cityname.find(u'市')>=0 or cityname.find(u'区')>=0:
                    #     cityname = cityname[0:len(cityname)-1]
                    # area = re.sub(u'\"','',curcor[u'area'])
                    # code=''
                    # codes = db.admin.find({'name':{'$regex':'.*'+cityname+'.*'}})
                    # for c in codes:
                    #     code = c[u'code']
                    #     break
                    # if code == None or code=='':
                    #     codes = db.admin.find({'name':{'$regex':'.*'+area+'.*'}})
                    #     for c in codes:
                    #         code = c[u'code']
                    #         break
                    # if code == None or code=='':
                    #     if i%100==0:
                    #         print '未能查询code-->','city-->',cityname,'area--->',area
                    #     continue
                    # result = db.MainShop5.update_many({'shopId':shopId},{'$set':{'city':int(code),'city1':int(code)}})
                    # if result.matched_count>0:
                    #     if i%1000==0:
                    #         print 'shopId-->',shopId
                    #     break
                if i%1000:
                    print match_count
            except Exception, e:
                print e,"Exception"

        if last_row_id!='':
            print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'coordinates':[0,0]
                    # 任意元素匹配所有条件
                },
                projection={
                     '_id':1,
                    'shopId':1
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print 'march_count-->',match_count
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);
if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33333)
    conn = pymongo.MongoClient('10.15.86.90', 30000)
    # 连接数据库
    db = conn.crawl
    countMarchDianpingAndMainShop(db)