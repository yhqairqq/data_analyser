#coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import traceback
from bson.objectid import ObjectId

#conn = pymongo.MongoClient('mysql1.cuone.com',27017)
conn = pymongo.MongoClient('mongodb://root:unionpay201607@localhost:27017/')
#连接数据库
db = conn.coupon
collection = db.MainShop5
fi = open("/Users/YHQ/baiduyun/remove.txt",'rb')
line = fi.readline()
fi.close()
ids = line.split(",")
total_size = len(ids)
i=0.0
for id in ids:
   i=i+1
   id=id.replace('[','')
   id=id.replace(']','')
   id=id.replace('"','')
   id=id.replace(' ','')
   try:
       result = collection.delete_one(
       filter={
           '_id':ObjectId(id)
       })
       if result.deleted_count==0:
           print "id 不存在:",id
       if i%1000==0:
           print '完成: %.2f ' % (i/total_size*100),"%"
   except Exception,e:
        print e
