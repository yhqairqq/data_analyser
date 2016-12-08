#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
import json
import re
from bson.objectid import ObjectId


def check_contain_chinese(check_str):
    try:
        for ch in check_str:
            ch = unicode(ch)
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    except Exception, e:
        print 'check_contain_chinese in', e


def check_contain_english(uchar_str):
    try:
        for uchar in uchar_str:
            uchar = unicode(uchar)
            if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
        return False
    except Exception, e:
        print 'check_contain_english in', e

def check_contain_digital(uchar_str):
    try:
        for uchar in uchar_str:
            uchar = unicode(uchar)
            if uchar >= u'\u0030' and uchar <= u'\u0039':
                return True
        return False
    except Exception, e:
        print 'check_contain_digital in', e

def check_str(str):
    for ch in str:
        if check_contain_english(ch) or check_contain_chinese(ch):
            return True
    return False


def remove_ch(str):
    str =  re.sub(u' ','',str)
    str =  re.sub(u'…','',str)
    str =  re.sub(u'.','',str)
    str =  re.sub(u'。','',str)
    str =  re.sub(u',','',str)
    str =  re.sub(u'…','',str)
    str =  re.sub(u'＞','',str)
    str =  re.sub(u'@','',str)
    str =  re.sub(u'/','',str)
    str =  re.sub(u'-','',str)
    str =  re.sub(u'_','',str)
    str =  re.sub(u'#','',str)
    str =  re.sub(u'﹉','',str)
    str =  re.sub(u';','',str)
    str =  re.sub(u'、','',str)
    str =  re.sub(u'】','',str)
    str =  re.sub(u'%','',str)
    str =  re.sub(u'\+','',str)
    str =  re.sub(u'`','',str)
    str =  re.sub(u'、','',str)
    str =  re.sub(u'\?','',str)
    str =  re.sub(u'|','',str)
    str =  re.sub(u'！','',str)
    str =  re.sub(u'，','',str)
    str =  re.sub(u'～','',str)
    str =  re.sub(u'—','',str)
    str =  re.sub(u'。','',str)
    str =  re.sub(u'’','',str)
    str =  re.sub(u'‘','',str)
    str =  re.sub(u'\*','',str)
    str =  re.sub(u'（','',str)
    str =  re.sub(u'&','',str)
    str =  re.sub(u'》','',str)
    str =  re.sub(u'《','',str)
    return  str

# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.86.90:30000/')
conn = pymongo.MongoClient('10.15.86.90',30000)
# conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('mysql1.cuone.com',27017)
# 连接数据库
db = conn.crawl
page = 0
page_size = 10000
i = 1.0
last_row_id = ''
content = db.brand.find(
    filter={
        '_id': {'$gt': ObjectId('57c7b201ec8d8353e85e3a0b')}
    }).sort('_id', pymongo.ASCENDING).limit(page_size)
count = db.brand.find(
    filter={
        '_id': {'$gt': ObjectId('57c7b201ec8d8353e85e3a0b')}
    },
    projection={
        '_id': 1
    }).sort('_id', pymongo.ASCENDING).count()

print 'totalSize:', count

if count == 0:
    exit(1)
brand_dic = {}
arr=[]
fo = open('illigal_brandname.txt','wr')
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
            brandname=json[u'name']
            if check_contain_english(brandname) ==False and check_contain_chinese(brandname)==False and check_contain_digital(brandname)==False:
                brandname =  remove_ch(brandname)
                if len(brandname)==0:
                    result = db.brand2.update_one({'_id':json[u'_id']},{'$set':json},True)
                    if result.matched_count>0 :
                          print '更新成功>>>>>>',json[u'_id']
                    result1 = db.WithErrorMainShop5.delete_one({'_id2':json[u'_id']})
                    if result1.deleted_count>0 :
                         print '删除成功>>>>>>',json[u'_id']
        except Exception, e:
            print 'exception', e

    print "last_row_id>>>>>" + str(last_row_id)

    if last_row_id != '':
        content = db.brand.find(
            filter={
                '_id': {'$gt': ObjectId(last_row_id)},
                # 'brand':u''
                # 任意元素匹配所有条件
            },
           ).sort('_id', pymongo.ASCENDING).limit(page_size)
        last_row_id = ''
    else:
        print "完成>>>>%.2f" % (i / count * 100), "%"
        exit(1);
fo.close()