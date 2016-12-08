#!/usr/bin/env python
# coding:utf-8

import pymongo
import datetime
import random
import traceback
from bson.objectid import ObjectId


def conn(address, port):
    # 创建连接
    # conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
    conn = pymongo.MongoClient(address, port)
    # 连接数据库
    db = conn.crawl
    # collection = db[collection]
    return db


if __name__ == '__main__':
    # '10.15.86.90', 30000
    db = conn('127.0.0.1', 33333)
    MainShop5 = db.MainShop5
    WithErrorMainShop5 = db.WithErrorMainShop5

    content = MainShop5.find(
        ).sort('_id', pymongo.ASCENDING).limit(10)


    for curcor in content:
        WithErrorMainShop5.update_one({'_id':curcor[u'_id']},{'$set':curcor},True)
        print curcor
#
#     match = {
#         'name': 'yhq'
#     }
#
#     # groupby = 'userid'
#
#     group = {
#         '_id': '$name',
#         'count': {'$sum': 1}
#
#     }
#
#     ret = coll.aggregate(
#         [
#             {'$match': match},
#             {'$group': group}
#         ]
#     )
#
# # arr_id = []
# for i in ret:
#     print i[u'count']

# if len(arr_id) >=2:
#     print arr_id[1]
#     result = coll.delete_one({u'_id': arr_id[1]})
#     print result.deleted_count

# c.update_many({'name':'yhq'},{"$set":{'createAt':datetime.datetime.utcnow()}})
# c.update_many({'name':'yhq'},{"$addToSet":{'tag':{'$each':['美食','餐饮','娱乐','旅游']}}})
# i=0
# while True:
#    if i == 10:
#        break
#    result =  c.insert_one({'age':i,'name':'yhq'})
#    print result
#    i=i+1
    d = datetime.datetime.utcnow()
    x=1
    print type(d)
