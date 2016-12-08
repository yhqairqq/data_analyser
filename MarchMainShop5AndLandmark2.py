#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId
import math

landmark_dic = {}
def loadLandMark(db):
    curcor = db.Landmark.find({})
    for json in curcor:
        landmark_dic[json[u'_id']]=json[u'centerCoordinates']

    print '地标加载成功,记录为',len(landmark_dic),'条'


def getGDDistance(p1,p2):

    lon1 = math.pi/180*p1[0]  #经
    lon2 = math.pi/180*p2[0]  #纬
    lat1 = math.pi/180*p1[1]
    lat2 = math.pi/180*p2[1]
    #地球半径
    R = 6371
    d = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*R
    return  d
# 创建连接
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('10.15.86.90', 30000)
# 连接数据库
db = conn.crawl

loadLandMark(db)
page = 0
page_size = 10000
i = 1.0
last_row_id = ''
content = db.MainShop5.find(
).sort('_id', pymongo.ASCENDING).limit(page_size)
count = db.MainShop5.find(
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
        # if i%1000==0:
        #     print json
        if i % 10000 == 0:
            print "完成>>>>%.2f" % (i / count * 100), "%"
        try:

            landArr = json[u'landArr']
            if isinstance(landArr,list):
                newlandArr=''
                if len(landArr)>0:
                    newlandArr= str(landArr[0])
                result = db.MainShop5.update_one({'_id':json[u'_id']},{'$set':{'landArr':newlandArr}})
            if result.matched_count>0 and i%1000==0:
                print '更新成功>>>',json[u'_id']

        except Exception, e:
            print e, "Exception"
    if last_row_id!='':
       print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = db.MainShop5.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)}
                # 任意元素匹配所有条件
            }
        ).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        exit(1);
