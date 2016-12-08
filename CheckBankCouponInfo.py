#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId

check_standard_count = 0
check_len_count = 0
check_type_count = 0


def check_contain_chinese(check_str):
    try:
        ch = unicode(check_str)
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        return False
    except Exception, e:
        print 'check_contain_chinese in', e


def check_contain_english(uchar):
    try:
        uchar = unicode(uchar)
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False
    except Exception, e:
        print 'check_contain_english in', e


def bank_check_standardized(json, check_standard_count):
    if len(json[u'brand']) == 1:
        if (check_contain_chinese(json[u'brand']) or check_contain_english(json[u'brand'])) and (
                    check_contain_chinese(json[u'shopName']) or check_contain_english(json[u'shopName'])) and (
                    check_contain_chinese(json[u'address']) or check_contain_english(json[u'address'])):
            return check_standard_count
        else:
            return check_standard_count + 1
    else:
        return check_standard_count


def bank_check_len(json, check_len_count):

    if check_len_count%10000==0:
         print 'bankCode',len(json[u'bankCode']),'cardTypeList',len(json[u'cardTypeList']),'categoryList',len(json[u'categoryList']),'validDateDesc',len(json[u'validDateDesc']),'city',len(json[u'city']), 'title',(json[u'title']), 'tradingArea',len(json[u'tradingArea']), 'hours',len(json[u'hours'])
    if len(str(json[u'city'])) != 6 or len(
            json[u'brand']) < 1 or len(json[u'brand']) > 60 or len(
        json[u'shopName']) < 1 or len(json[u'shopName']) > 120 or len(
        json[u'address']) < 1 or len(json[u'address']) > 256 or json[u'coordinates'] == [0, 0] or len(
        json[u'tradingArea']) < 1 or len(json[u'tradingArea']) > 60 or len(
        json[u'hours']) < 1 or len(json[u'hours']) > 100:
        return check_len_count + 1
    return check_len_count


def bank_check_type(json, check_type_count):
    if type(json[u'createAt']) is datetime.datetime and type(json[u'updateAt']) is datetime.datetime:
        return check_type_count

    return check_type_count + 1


# 创建连接
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('10.15.86.90', 30000)
# 连接数据库
db = conn.crawl
collection = db.BankCouponInfo
page = 0
page_size = 10000
i = 1.0
last_row_id = ''
content = collection.find(
).sort('_id', pymongo.ASCENDING).limit(page_size)
count = collection.find(
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
            check_type_count = bank_check_type(json, check_type_count)
            check_len_count = bank_check_len(json, check_len_count)
            check_standard_count = bank_check_standardized(json, check_standard_count)
            if check_len_count%10000==0:
                print 'totalRecord=', count, ',check_type_count=', check_type_count, ',check_len_count=', check_len_count, ',check_standard_count', check_standard_count

        except Exception, e:
            print e, "Exception"

    print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = collection.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)}
                # 任意元素匹配所有条件
            }
        ).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        print 'totalRecord=', count, ',check_type_count=', check_type_count, ',check_len_count=', check_len_count, ',check_standard_count', check_standard_count
        exit(1);
