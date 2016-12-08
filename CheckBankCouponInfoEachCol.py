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

counter_dic = {"bankCode_e": 0, "bankCode_l": 0, "validDateDesc_e": 0, "validDateDesc_l": 0, 'city_e': 0, 'city_l': 0,
               'title_e': 0, 'title_l': 0}

def count_col_empty_or_len(json, counter_dic,db):

    if len(json[u'bankCode'])==0:
        db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'bankCode':json[u'bankCode'],'tag':'bankCode','len':0})
        counter_dic['bankCode_e']=counter_dic['bankCode_e']+1
    else:
        for bankcode in json[u'bankCode']:
            if len(bankcode)!=8:
                db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'bankCode':json[u'bankCode'],'tag':'bankCode','len':1})
                counter_dic['bankCode_l']=counter_dic['bankCode_l']+1
                break;

    if len(json[u'validDateDesc'])==0:
        db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'validDateDesc':json[u'validDateDesc'],'tag':'validDateDesc','len':0})
        counter_dic['validDateDesc_e']=counter_dic['validDateDesc_e']+1
    else:
        if len(json[u'validDateDesc'])> 60:
            db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'validDateDesc':json[u'validDateDesc'],'tag':'validDateDesc','len':1})
            counter_dic['validDateDesc_l']=counter_dic['validDateDesc_l']+1

    if len(str(json[u'city']))==0 or json[u'city']==0:
        db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':0})
        counter_dic['city_e']=counter_dic['city_e']+1
    else:
        if len(str(json[u'city']))!=6:
            db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':1})
            counter_dic['city_l']=counter_dic['city_l']+1

    if len(json[u'title'])==0:
        db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'title':json[u'title'],'tag':'title','len':0})
        counter_dic['title_e']=counter_dic['title_e']+1
    else:
        if len(json[u'title'])> 800:
            db.WithErrorBankCouponInfo.insert_one({'_id2':json[u'_id'],'title':json[u'title'],'tag':'title','len':1})
            counter_dic['title_l']=counter_dic['title_l']+1


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


def mainshop5_check_standardized(json, check_standard_count):
    if len(json[u'brand']) == 1:
        if (check_contain_chinese(json[u'brand']) or check_contain_english(json[u'brand'])) and (
                    check_contain_chinese(json[u'shopName']) or check_contain_english(json[u'shopName'])) and (
                    check_contain_chinese(json[u'address']) or check_contain_english(json[u'address'])):
            return check_standard_count
        else:
            return check_standard_count + 1
    else:
        return check_standard_count


def mainshop5_check_len(json, check_len_count):
    if check_len_count % 10000 == 0:
        print 'city', len(str(json[u'city'])), 'brand', len(json[u'brand']), 'shopName', len(
            json[u'shopName']), 'address', len(json[u'address']), 'description', len(
            json[u'description']), 'coordinates', (json[u'coordinates']), 'tradingArea', len(
            json[u'tradingArea']), 'hours', len(json[u'hours'])
    if len(str(json[u'city'])) != 6 or len(
            json[u'brand']) < 1 or len(json[u'brand']) > 60 or len(
        json[u'shopName']) < 1 or len(json[u'shopName']) > 120 or len(
        json[u'address']) < 1 or len(json[u'address']) > 256 or  json[u'coordinates'] == [0, 0] or len(
        json[u'tradingArea']) < 1 or len(json[u'tradingArea']) > 60 or len(
        json[u'hours']) < 1 or len(json[u'hours']) > 100:
        return check_len_count + 1
    return check_len_count


def mainshop5_check_type(json, check_type_count):
    if type(json[u'createAt']) is datetime.datetime and type(json[u'updateAt']) is datetime.datetime:
        return check_type_count

    return check_type_count + 1


# 创建连接
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
# conn = pymongo.MongoClient('127.0.0.1', 33333)
conn = pymongo.MongoClient('10.15.86.90', 30000)
# 连接数据库
db = conn.crawl
collection = db.BankCouponInfo
invalidRecordCollection = db.InvalidRecordForMainShop5
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
            count_col_empty_or_len(json,counter_dic,db)
            if i % 10000 == 0:
                print counter_dic

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
        print counter_dic
        exit(1);
