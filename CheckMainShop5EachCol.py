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

counter_dic = {"category_e": 0, "category_l": 0, "subCategory_e": 0, "subCategory_l": 0, 'city_e': 0, 'city_l': 0,
               'brand_e': 0, 'brand_l': 0, 'shopName_e': 0, 'shopName_l': 0, 'address_e': 0, 'address_l': 0,
               'description_e': 0, 'description_l': 0, 'coordinates_e': 0, 'coordinates_l': 0, 'tradingArea_e': 0,
               'tradingArea_l': 0, 'hours_e': 0, 'hours_l': 0}
def count_col_empty_or_len(json, counter_dic,db):

    # print 'city',len(str(json[u'city']))
    # if len(json[u'category'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'category':json[u'category'],'tag':'category','len':0})
    #     counter_dic['category_e']=counter_dic['category_e']+1
    #
    # else:
    #     if len(json[u'category'][0])>60 or len(json[u'category'][0])<1:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'category':json[u'category'],'tag':'category','len':1})
    #         counter_dic['category_l']=counter_dic['category_l']+1
    #
    #
    # if len(json[u'subCategory'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'subCategory':json[u'subCategory'],'tag':'subCategory','len':0})
    #     counter_dic['subCategory_e']=counter_dic['subCategory_e']+1
    #
    # else:
    #     if len(json[u'subCategory'][0])>60 or len(json[u'subCategory'][0])<1:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'subCategory':json[u'subCategory'],'tag':'subCategory','len':1})
    #         counter_dic['subCategory_l']=counter_dic['subCategory_l']+1
    #
    #
    # if len(str(json[u'city']))==0 or json[u'city']==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':0})
    #     counter_dic['city_e']=counter_dic['city_e']+1
    #
    # else:
    #     if len(str(json[u'city']))!=6:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'city':json[u'city'],'tag':'city','len':1})
    #         counter_dic['city_l']=counter_dic['city_l']+1


    if len(json[u'brand'])==0:
        db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'brand':json[u'brand'],'tag':'brand','len':0})
        counter_dic['brand_e']=counter_dic['brand_e']+1

    else:
        if len(json[u'brand'])> 60:
            db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'brand':json[u'brand'],'tag':'brand','len':1})
            counter_dic['brand_l']=counter_dic['brand_l']+1


    # if len(json[u'shopName'])==0:
    #     counter_dic['shopName_e']=counter_dic['shopName_e']+1
    #
    # else:
    #     if len(json[u'shopName'])> 120:
    #         counter_dic['shopName_l']=counter_dic['shopName_l']+1


    # if len(json[u'address'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'address':json[u'address'],'tag':'address','len':0})
    #     counter_dic['address_e']=counter_dic['address_e']+1
    #
    # else:
    #     if len(json[u'address'])> 256:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'address':json[u'address'],'tag':'address','len':1})
    #         counter_dic['address_l']=counter_dic['address_l']+1
    #
    #
    # if len(json[u'description'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'description':json[u'description'],'tag':'description','len':0})
    #     counter_dic['description_e']=counter_dic['description_e']+1
    # else:
    #     if len(json[u'description'])> 2000:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'description':json[u'description'],'tag':'description','len':1})
    #         counter_dic['description_l']=counter_dic['description_l']+1
    #
    #
    # if len(json[u'coordinates'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'coordinates':json[u'coordinates'],'tag':'coordinates','len':0})
    #     counter_dic['coordinates_e']=counter_dic['coordinates_e']+1
    #
    # else:
    #     if json[u'coordinates']==[0,0]:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'coordinates':json[u'coordinates'],'tag':'coordinates','len':0})
    #         counter_dic['coordinates_e']=counter_dic['coordinates_e']+1
    #
    #
    # if len(json[u'tradingArea'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'tradingArea':json[u'tradingArea'],'tag':'tradingArea','len':0})
    #     counter_dic['tradingArea_e']=counter_dic['tradingArea_e']+1
    #
    # else:
    #     if len(json[u'tradingArea'])> 60:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'tradingArea':json[u'tradingArea'],'tag':'tradingArea','len':1})
    #         counter_dic['tradingArea_l']=counter_dic['tradingArea_l']+1
    #
    #
    # if len(json[u'hours'])==0:
    #     db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'hours':json[u'hours'],'tag':'hours','len':0})
    #     counter_dic['hours_e']=counter_dic['hours_e']+1
    #
    # else:
    #     if len(json[u'hours'])> 100:
    #         db.WithErrorMainShop5.insert_one({'_id2':json[u'_id'],'hours':json[u'hours'],'tag':'hours','len':1})
    #         counter_dic['hours_l']=counter_dic['hours_l']+1


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
collection = db.MainShop5
WithErrorMainShop5 = db.WithErrorMainShop5
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
