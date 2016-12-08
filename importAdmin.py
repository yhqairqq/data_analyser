#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId


def importAdminFromFile(db,fi):
    i=0.0
    total = 3512.0
    for line in fi:
        i=i+1
        values = line.split('##')
        db.admin.insert_one({'code':values[1],'name':values[2]})
        if i%100==0:
          print "完成>>>>%.2f" % (i / total * 100), "%"
    print "完成>>>>%.2f" % (i / total * 100), "%"
    fi.close()

if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33333)
    conn = pymongo.MongoClient('10.15.86.90', 30000)
    # 连接数据库

    fi=open('/Users/YHQ/baiduyun/admin.csv','rb')
    db = conn.crawl
    importAdminFromFile(db,fi)