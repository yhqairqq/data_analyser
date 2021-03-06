#!/usr/bin/env python
#coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import datetime
import traceback
allFileNum = 0
conn = pymongo.MongoClient('mysql1.cuone.com',27017)
#conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
#连接数据库
db = conn.coupon
collection = db.MainShop5
def getFileList(regex, path):
    global allFileNum
    '''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + '/' + f) and fnmatch.fnmatch(f,regex)):
            # 添加文件
            fileList.append(path + '/' + f)

    return fileList

def processFileList(fileList):

    total=22220000.0
    count=0
    in_start=0.0
    for f in fileList:
        fi = open(f,'rb')
        print 'start process:'+f

        line = fi.readline()

        index=0
        start = time.clock()
        while line != None and line != "":

          if line == "" or len(line) == 0 or len(line.split(":")) < 3 or len(line) < 10:
              line = fi.readline()
              continue

          count=count+1
          try:
              obj=json.loads(line,"utf-8")

              if index==0:
                  in_start=time.clock()

              date_time = datetime.datetime.utcnow()
              #假如处理的方法
              result =  collection.update({'shopId':obj[u'shopId']},{'$set':{'tradingArea':obj[u'tradingArea'],'brand':obj[u'brand'],'category':obj[u'category'],'subCategory':obj[u'subCategory'],"createAt":date_time,"updateAt":date_time}})

              index = index+1
              if index%100==0:
                  if result[u'nModified']==0  :
                      print '更新失败>>>>>>',obj[u'shopId']
                  else:
                      print '更新成功>>>>>>',obj[u'shopId']
              if index==1000:
                 print "1000条数据处理时间:%f"% (time.clock()-in_start)
                 index=0
              if count%10000==0:
                  print "完成>>>>%.2f" % (count/total*100),"%"
          except Exception ,e:
              print '异常处理完成>>>>'

          line = fi.readline()

        fi.close()
        end = time.clock()
        print "处理文件消耗: %f s" % (end - start)
    print 'finish  .  . . '

if __name__ == '__main__':
   fileList=getFileList('*.txt', '/Users/YHQ/baiduyun/chenwei/0815')
   processFileList(fileList)




