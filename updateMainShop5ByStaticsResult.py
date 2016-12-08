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


def updateCategory(db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = db.WithErrorMainShop5.find(
        filter={
            'tag':'subCategory'
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.WithErrorMainShop5.find(
         filter={
            'tag':'subCategory'
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

                one=db.MainShop5.find(
                    filter={
                        '_id':json[u'_id2']
                    }
                )
                for curcor in one:
                    date_time = datetime.datetime.utcnow()
                    #处理大小分类
                    category = curcor[u'category']
                    subCategory = curcor[u'subCategory']

                    if len(category)==0 or len(category[0])>60 or len(category[0])<1:
                        category=[u'其他']
                    if len(subCategory)==0 or len(subCategory[0])>60 or len(subCategory[0])<1:
                        subCategory=[u'其他']
                    #假如处理的方法
                    result =  db.MainShop5.update({'_id':json[u'_id2']},{'$set':{'category':category,'subCategory':subCategory,"updateAt":date_time}})
                    if result[u'nModified']==1 and i%1000==0 :
                          print '更新成功>>>>>>',curcor
            except Exception, e:
                print e, "Exception"

        print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = db.WithErrorMainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'tag':'subCategory'
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);

def updateEmptyBrand(db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
        filter={
            'brand':''
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
         filter={
           'brand':''
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

                # print i
                # 假如处理的方法
                result = db.MainShop6.update_one({'_id':json[u'_id']},{'$set':json},True)
                if result.upserted_id!=None :
                    result1 = db.MainShop5.delete_one({'_id':json[u'_id']})
                    if result1.deleted_count==1 and i%1000==0:
                        print '删除-->',json[u'_id']
                    if i%1000==0:
                      print '插入>>>>>>',json[u'_id']

            except Exception, e:
                print e, "Exception"

        if last_row_id!='':
          print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'brand':''
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);

def updateEmptyAddress(db):
    page_size = 100
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
        filter={
            'address':''
        }
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
         filter={
           'address':''
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
                if i%100==0:
                   print i
                # 假如处理的方法
                result = db.MainShop6.update_one({'_id':json[u'_id']},{'$set':json},True)
                if result.upserted_id!=None :
                    result1 = db.MainShop5.delete_one({'_id':json[u'_id']})
                    if result1.deleted_count==1 and i%1000==0:
                        print '删除-->',json[u'_id']
                    if i%1000==0:
                      print '插入>>>>>>',json[u'_id']

            except Exception, e:
                print e, "Exception"

        if last_row_id!='':
          print "last_row_id>>>>>" + str(last_row_id)

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)},
                    'address':''
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);

def updateIlligalBrand(db):
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
            if i % 10000 == 0:
                print "完成>>>>%.2f" % (i / count * 100), "%"
            try:
                brandname = json[u'brand']
                if check_contain_english(brandname) ==False and check_contain_chinese(brandname)==False and check_contain_digital(brandname)==False:
                    brandname =  remove_ch(brandname)
                    if len(brandname)==0:
                        result = db.MainShop6.update_one({'_id':json[u'_id']},{'$set':json},True)
                        if result.upserted_id!=None :
                            result1 = db.MainShop5.delete_one({'_id':json[u'_id']})
                            if result1.deleted_count==1 and i%1000==0:
                                print '删除-->',json[u'_id']
                            if i%1000==0:
                                print '插入>>>>>>',json[u'_id']

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
if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33333)
    conn = pymongo.MongoClient('10.15.86.90', 30000)
    # 连接数据库
    db = conn.crawl
    updateIlligalBrand(db)