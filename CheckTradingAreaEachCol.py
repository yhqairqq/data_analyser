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

counter_dic = {"provinceCode_e": 0, "provinceCode_l": 0, "cityCode_e": 0, "cityCode_l": 0, 'countyCode_e': 0,
               'countyCode_l': 0,
               'province_e': 0, 'province_l': 0, 'city_e': 0, 'city_l': 0, 'county_e': 0, 'county_l': 0,
               'tradingAreaName_e': 0, 'tradingAreaName_l': 0,'centerCoordinates_e': 0, 'centerCoordinates_l': 0}


def count_col_empty_or_len(json, counter_dic,db):


    if len(json[u'provinceCode']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'provinceCode':json[u'provinceCode'],'tag':'provinceCode','len':0})
        counter_dic['provinceCode_e'] = counter_dic['provinceCode_e'] + 1

    else:
        if len(json[u'provinceCode']) != 6:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'provinceCode':json[u'provinceCode'],'tag':'provinceCode','len':1})
            counter_dic['provinceCode_l'] = counter_dic['provinceCode_l'] + 1



    if len(json[u'cityCode']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'cityCode':json[u'cityCode'],'tag':'cityCode','len':0})
        counter_dic['cityCode_e'] = counter_dic['cityCode_e'] + 1

    else:
        if len(json[u'cityCode']) != 6:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'cityCode':json[u'cityCode'],'tag':'cityCode','len':1})
            counter_dic['cityCode_l'] = counter_dic['cityCode_l'] + 1


    if len(json[u'countyCode']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'countyCode':json[u'countyCode'],'tag':'countyCode','len':0})
        counter_dic['countyCode_e'] = counter_dic['countyCode_e'] + 1

    else:
        if len(json[u'countyCode']) != 6:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'countyCode':json[u'countyCode'],'tag':'countyCode','len':0})
            counter_dic['countyCode_l'] = counter_dic['countyCode_l'] + 1



    if len(json[u'province']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'province':json[u'province'],'tag':'province','len':0})
        counter_dic['province_e'] = counter_dic['province_e'] + 1

    else:
        if len(json[u'province']) >20:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'province':json[u'province'],'tag':'province','len':1})
            counter_dic['province_l'] = counter_dic['province_l'] + 1


    if len(json[u'city']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':0})
        counter_dic['city_e'] = counter_dic['city_e'] + 1

    else:
        if len(json[u'city']) >20:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':1})
            counter_dic['city_l'] = counter_dic['city_l'] + 1



    if len(json[u'county']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'county':json[u'county'],'tag':'county','len':0})
        counter_dic['county_e'] = counter_dic['county_e'] + 1

    else:
        if len(json[u'county']) >20:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'county':json[u'county'],'tag':'county','len':1})
            counter_dic['county_l'] = counter_dic['county_l'] + 1


    if len(json[u'tradingAreaName']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'tradingAreaName':json[u'tradingAreaName'],'tag':'tradingAreaName','len':0})
        counter_dic['tradingAreaName_e'] = counter_dic['tradingAreaName_e'] + 1
    else:
        if len(json[u'tradingAreaName']) >20:
            db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'tradingAreaName':json[u'tradingAreaName'],'tag':'tradingAreaName','len':0})
            counter_dic['tradingAreaName_l'] = counter_dic['tradingAreaName_l'] + 1

    if len(json[u'centerCoordinates']) == 0:
        db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'centerCoordinates':json[u'centerCoordinates'],'tag':'centerCoordinates','len':0})
        counter_dic['centerCoordinates_e'] = counter_dic['centerCoordinates_e'] + 1
    else:
        for coor in json[u'centerCoordinates']:
            if coor == 0:
                db.WithErrorTradingArea.insert_one({'_id2':json[u'_id'],'centerCoordinates':json[u'centerCoordinates'],'tag':'centerCoordinates','len':0})
                counter_dic['centerCoordinates_l'] = counter_dic['centerCoordinates_l'] + 1
                break


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
        json[u'address']) < 1 or len(json[u'address']) > 256 or len(
        json[u'description']) > 2000 or json[u'coordinates'] == [0, 0] or len(
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
collection = db.TradingArea
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
            count_col_empty_or_len(json, counter_dic,db)
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
